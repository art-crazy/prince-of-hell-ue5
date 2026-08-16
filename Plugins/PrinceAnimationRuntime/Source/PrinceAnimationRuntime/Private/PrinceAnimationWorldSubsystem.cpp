#include "PrinceAnimationWorldSubsystem.h"

#include "Animation/AnimationAsset.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"

namespace PrinceAnimationPaths
{
    constexpr TCHAR Mesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig.SK_POHPrince_TripoRig");
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_Idle.A_POH_Idle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_WalkF.A_POH_WalkF");
    constexpr float StartWalkingSpeed = 10.0f;
    constexpr float StopWalkingSpeed = 4.0f;
}

void UPrinceAnimationWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    PrinceMesh = LoadObject<USkeletalMesh>(nullptr, PrinceAnimationPaths::Mesh);
    IdleAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Idle);
    WalkAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Walk);

    if (UWorld* World = GetWorld())
    {
        ActorSpawnedHandle = World->AddOnActorSpawnedHandler(FOnActorSpawned::FDelegate::CreateUObject(this, &UPrinceAnimationWorldSubsystem::RegisterPrince));
        for (TActorIterator<ACharacter> It(World); It; ++It)
        {
            RegisterPrince(*It);
        }
    }
}

void UPrinceAnimationWorldSubsystem::Deinitialize()
{
    if (UWorld* World = GetWorld(); ActorSpawnedHandle.IsValid())
    {
        World->RemoveOnActorSpawnedHandler(ActorSpawnedHandle);
    }

    PrinceCharacters.Empty();
    ActiveAnimations.Empty();
    Super::Deinitialize();
}

void UPrinceAnimationWorldSubsystem::Tick(float)
{
    UWorld* World = GetWorld();
    if (!World || !PrinceMesh || !IdleAnimation || !WalkAnimation)
    {
        return;
    }

    for (auto It = ActiveAnimations.CreateIterator(); It; ++It)
    {
        if (!It.Key().IsValid())
        {
            It.RemoveCurrent();
        }
    }

    for (auto It = PrinceCharacters.CreateIterator(); It; ++It)
    {
        ACharacter* Character = It->Get();
        if (!Character)
        {
            It.RemoveCurrent();
            continue;
        }

        if (USkeletalMeshComponent* Mesh = Character->GetMesh())
        {
            UpdatePrince(*Mesh, Character->GetVelocity().SizeSquared2D());
        }
    }
}

void UPrinceAnimationWorldSubsystem::RegisterPrince(AActor* Actor)
{
    ACharacter* Character = Cast<ACharacter>(Actor);
    if (!Character)
    {
        return;
    }

    USkeletalMeshComponent* Mesh = Character->GetMesh();
    if (Mesh && Mesh->GetSkeletalMeshAsset() == PrinceMesh)
    {
        PrinceCharacters.Add(Character);
    }
}

void UPrinceAnimationWorldSubsystem::UpdatePrince(USkeletalMeshComponent& Mesh, const float HorizontalSpeedSquared)
{
    TObjectPtr<UAnimationAsset>& Active = ActiveAnimations.FindOrAdd(&Mesh);
    const bool bWasWalking = Active == WalkAnimation;
    const float Threshold = bWasWalking ? PrinceAnimationPaths::StopWalkingSpeed : PrinceAnimationPaths::StartWalkingSpeed;
    UAnimationAsset* Desired = HorizontalSpeedSquared >= FMath::Square(Threshold) ? WalkAnimation : IdleAnimation;
    if (Active == Desired)
    {
        return;
    }

    Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
    Mesh.PlayAnimation(Desired, true);
    Active = Desired;
}

TStatId UPrinceAnimationWorldSubsystem::GetStatId() const
{
    RETURN_QUICK_DECLARE_CYCLE_STAT(UPrinceAnimationWorldSubsystem, STATGROUP_Tickables);
}

bool UPrinceAnimationWorldSubsystem::IsTickable() const
{
    return bEnableRuntimeLocomotion && PrinceMesh && IdleAnimation && WalkAnimation;
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
