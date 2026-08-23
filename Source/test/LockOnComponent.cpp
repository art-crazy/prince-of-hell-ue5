#include "LockOnComponent.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "InputAction.h"
#include "GameFramework/Pawn.h"
#include "GameFramework/Controller.h"
#include "GameFramework/PlayerController.h"
#include "Kismet/KismetSystemLibrary.h"
#include "Kismet/KismetMathLibrary.h"
#include "Net/UnrealNetwork.h"

ULockOnComponent::ULockOnComponent()
{
	PrimaryComponentTick.bCanEverTick = true;
	SetIsReplicatedByDefault(true);
}

void ULockOnComponent::BeginPlay()
{
	Super::BeginPlay();
	TryBindInput();
}

void ULockOnComponent::TryBindInput()
{
	if (bInputBound)
	{
		return;
	}

	const APawn* OwnerPawn = Cast<APawn>(GetOwner());
	if (!OwnerPawn || !OwnerPawn->IsLocallyControlled())
	{
		return;
	}

	APlayerController* PC = Cast<APlayerController>(OwnerPawn->GetController());
	if (!PC || !PC->InputComponent)
	{
		return;
	}

	if (UEnhancedInputComponent* EIC = Cast<UEnhancedInputComponent>(PC->InputComponent))
	{
		if (LockOnAction)
		{
			EIC->BindAction(LockOnAction, ETriggerEvent::Triggered, this, &ULockOnComponent::OnLockOnTriggered);
			bInputBound = true;
		}
	}
}

void ULockOnComponent::OnLockOnTriggered()
{
	++TriggerCount;

	if (LockedTarget)
	{
		SetLockedTarget(nullptr);
		return;
	}

	SetLockedTarget(FindBestTarget());
}

AActor* ULockOnComponent::FindBestTarget()
{
	AActor* Owner = GetOwner();
	const APawn* OwnerPawn = Cast<APawn>(Owner);
	if (!Owner || !OwnerPawn)
	{
		return nullptr;
	}

	const APlayerController* PC = Cast<APlayerController>(OwnerPawn->GetController());
	if (!PC || !PC->PlayerCameraManager)
	{
		return nullptr;
	}

	const FVector ViewLoc = PC->PlayerCameraManager->GetCameraLocation();
	const FVector ViewForward = PC->PlayerCameraManager->GetCameraRotation().Vector();

	TArray<AActor*> Overlaps;
	TArray<TEnumAsByte<EObjectTypeQuery>> ObjectTypes;
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_Pawn));
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldDynamic));
	ObjectTypes.Add(UEngineTypes::ConvertToObjectType(ECC_WorldStatic));
	TArray<AActor*> ToIgnore;
	ToIgnore.Add(Owner);

	UKismetSystemLibrary::SphereOverlapActors(Owner, ViewLoc, SearchRadius, ObjectTypes, nullptr, ToIgnore, Overlaps);
	OverlapCount = Overlaps.Num();

	const float CosHalfAngle = FMath::Cos(FMath::DegreesToRadians(SearchHalfAngleDegrees));

	AActor* Best = nullptr;
	float BestDot = CosHalfAngle;

	for (AActor* Candidate : Overlaps)
	{
		if (!IsValid(Candidate) || Candidate->IsHidden() || !Candidate->ActorHasTag(TargetableTag))
		{
			continue;
		}

		const FVector ToCandidate = (Candidate->GetActorLocation() - ViewLoc).GetSafeNormal();
		const float Dot = FVector::DotProduct(ViewForward, ToCandidate);
		if (Dot > BestDot && HasLineOfSight(ViewLoc, Candidate))
		{
			BestDot = Dot;
			Best = Candidate;
		}
	}

	return Best;
}

bool ULockOnComponent::HasLineOfSight(const FVector& ViewLoc, const AActor* Candidate) const
{
	FHitResult Hit;
	FCollisionQueryParams Params;
	Params.AddIgnoredActor(GetOwner());
	Params.AddIgnoredActor(Candidate);
	const bool bBlocked = GetWorld()->LineTraceSingleByChannel(Hit, ViewLoc, Candidate->GetActorLocation(), ECC_Visibility, Params);
	return !bBlocked;
}

void ULockOnComponent::SetLockedTarget(AActor* NewTarget)
{
	if (GetOwner()->HasAuthority())
	{
		if (LockedTarget != NewTarget)
		{
			if (LockedTarget)
			{
				LockedTarget->OnEndPlay.RemoveDynamic(this, &ULockOnComponent::OnTargetEndPlay);
			}
			LockedTarget = NewTarget;
			if (LockedTarget)
			{
				LockedTarget->OnEndPlay.AddDynamic(this, &ULockOnComponent::OnTargetEndPlay);
			}
			OnRep_LockedTarget();
		}
	}
	else
	{
		Server_SetLockedTarget(NewTarget);
	}
}

void ULockOnComponent::Server_SetLockedTarget_Implementation(AActor* NewTarget)
{
	if (NewTarget)
	{
		if (!IsValid(NewTarget) || !NewTarget->ActorHasTag(TargetableTag))
		{
			return;
		}

		const AActor* Owner = GetOwner();
		const bool bWithinRange = FVector::DistSquared(Owner->GetActorLocation(), NewTarget->GetActorLocation()) <= FMath::Square(SearchRadius * 1.5f);
		if (!bWithinRange)
		{
			return;
		}
	}

	SetLockedTarget(NewTarget);
}

void ULockOnComponent::OnRep_LockedTarget()
{
}

void ULockOnComponent::OnTargetEndPlay(AActor* EndedActor, EEndPlayReason::Type EndPlayReason)
{
	if (GetOwner()->HasAuthority())
	{
		SetLockedTarget(nullptr);
	}
}

void ULockOnComponent::TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction)
{
	Super::TickComponent(DeltaTime, TickType, ThisTickFunction);

	if (!bInputBound)
	{
		TryBindInput();
	}

	if (!LockedTarget)
	{
		return;
	}

	APawn* OwnerPawn = Cast<APawn>(GetOwner());
	if (!OwnerPawn || !OwnerPawn->IsLocallyControlled())
	{
		return;
	}

	AController* Controller = OwnerPawn->GetController();
	if (!Controller)
	{
		return;
	}

	const FVector From = OwnerPawn->GetPawnViewLocation();
	const FVector To = LockedTarget->GetActorLocation();
	const FRotator LookAt = UKismetMathLibrary::FindLookAtRotation(From, To);
	const FRotator NewRotation = FMath::RInterpTo(Controller->GetControlRotation(), LookAt, DeltaTime, TurnInterpSpeed);
	Controller->SetControlRotation(NewRotation);
}

void ULockOnComponent::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
	Super::GetLifetimeReplicatedProps(OutLifetimeProps);
	DOREPLIFETIME(ULockOnComponent, LockedTarget);
}
