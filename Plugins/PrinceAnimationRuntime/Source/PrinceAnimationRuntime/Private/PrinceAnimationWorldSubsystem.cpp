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
    constexpr TCHAR Mesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo.SK_POHPrince_NativeTripo");
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripoidle.SK_POHPrince_NativeTripoidle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripowalk.SK_POHPrince_NativeTripowalk");
    constexpr TCHAR Run[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTriporun.SK_POHPrince_NativeTriporun");
    constexpr TCHAR Jump[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripojump.SK_POHPrince_NativeTripojump");
    constexpr TCHAR Dive[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/A_POH_NativeTripo_Divedive.A_POH_NativeTripo_Divedive");
    constexpr TCHAR Fall[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripofall.SK_POHPrince_NativeTripofall");
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
    JumpAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Jump);
    DiveAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Dive);
    FallAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Fall);

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
    if (!World || !PrinceMesh || !IdleAnimation || !WalkAnimation || !RunAnimation || !JumpAnimation || !DiveAnimation || !FallAnimation)
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
    if (Movement && Movement->IsFalling())
    {
        // The movement component is the authority for airborne state. Using its
        // vertical velocity makes jumping and walking off an edge deterministic
        // without carrying transient state between frames.
        const bool bMovingAtTakeoff = HorizontalSpeedSquared >= FMath::Square(PrinceAnimationPaths::StartWalkingSpeed);
        UAnimationAsset* Desired = Character.GetVelocity().Z > KINDA_SMALL_NUMBER
            ? (bMovingAtTakeoff ? DiveAnimation : JumpAnimation)
            : FallAnimation;
        if (Active != Desired)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            Mesh.PlayAnimation(Desired, Desired == FallAnimation);
            Active = Desired;
        }
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
    return bEnableRuntimeLocomotion && PrinceMesh && IdleAnimation && WalkAnimation && RunAnimation && JumpAnimation && DiveAnimation && FallAnimation;
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
