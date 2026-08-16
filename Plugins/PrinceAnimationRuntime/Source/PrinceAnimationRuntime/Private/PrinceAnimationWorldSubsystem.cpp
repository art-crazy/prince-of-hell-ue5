#include "PrinceAnimationWorldSubsystem.h"

#include "Animation/AnimationAsset.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "InputCoreTypes.h"

namespace PrinceAnimationPaths
{
    constexpr TCHAR Mesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig.SK_POHPrince_TripoRig");
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_Idle.A_POH_Idle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_WalkF.A_POH_WalkF");
    constexpr TCHAR Run[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_RunF.A_POH_RunF");
    constexpr float StartWalkingSpeed = 10.0f;
    constexpr float StopWalkingSpeed = 4.0f;
    constexpr float StartRunningSpeed = 400.0f;
    constexpr float StopRunningSpeed = 340.0f;
    constexpr float WalkSpeed = 260.0f;
    constexpr float SprintSpeed = 600.0f;
}

void UPrinceAnimationWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    PrinceMesh = LoadObject<USkeletalMesh>(nullptr, PrinceAnimationPaths::Mesh);
    IdleAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Idle);
    WalkAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Walk);
    RunAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Run);

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
    AnimationStates.Empty();
    Super::Deinitialize();
}

void UPrinceAnimationWorldSubsystem::Tick(float)
{
    UWorld* World = GetWorld();
    if (!World || !PrinceMesh || !IdleAnimation || !WalkAnimation || !RunAnimation)
    {
        return;
    }

    for (auto It = AnimationStates.CreateIterator(); It; ++It)
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
            UpdatePlayerMovementSpeed(*Character);
            UpdatePrince(*Character, *Mesh, Character->GetVelocity().SizeSquared2D());
        }
    }
}

void UPrinceAnimationWorldSubsystem::UpdatePlayerMovementSpeed(ACharacter& Character) const
{
    if (!Character.IsPlayerControlled())
    {
        return;
    }

    APlayerController* Controller = Cast<APlayerController>(Character.GetController());
    UCharacterMovementComponent* Movement = Character.GetCharacterMovement();
    if (!Controller || !Movement)
    {
        return;
    }

    Movement->MaxWalkSpeed = Controller->IsInputKeyDown(EKeys::LeftShift)
        ? PrinceAnimationPaths::SprintSpeed
        : PrinceAnimationPaths::WalkSpeed;
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

void UPrinceAnimationWorldSubsystem::UpdatePrince(ACharacter& Character, USkeletalMeshComponent& Mesh, const float HorizontalSpeedSquared)
{
    FPrinceAnimationState& State = AnimationStates.FindOrAdd(&Mesh);
    TObjectPtr<UAnimationAsset>& Active = State.ActiveAnimation;
    const UCharacterMovementComponent* Movement = Character.GetCharacterMovement();
    // The old bulk-retargeted airborne clips can deform this skeleton. Hold
    // the last known-safe locomotion pose in air until a proper IK retarget
    // profile is authored and visually approved.
    if (Movement && Movement->IsFalling())
    {
        return;
    }

    const bool bWasRunning = Active == RunAnimation;
    const float RunThreshold = bWasRunning ? PrinceAnimationPaths::StopRunningSpeed : PrinceAnimationPaths::StartRunningSpeed;
    if (HorizontalSpeedSquared >= FMath::Square(RunThreshold))
    {
        if (Active != RunAnimation)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            Mesh.PlayAnimation(RunAnimation, true);
            Active = RunAnimation;
        }
        return;
    }

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
    return bEnableRuntimeLocomotion && PrinceMesh && IdleAnimation && WalkAnimation && RunAnimation;
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
