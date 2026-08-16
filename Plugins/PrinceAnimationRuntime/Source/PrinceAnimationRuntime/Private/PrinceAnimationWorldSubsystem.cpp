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
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Idle.POH_MM_Idle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripowalk.SK_POHPrince_NativeTripowalk");
    constexpr TCHAR Run[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MF_Unarmed_Jog_Fwd.POH_MF_Unarmed_Jog_Fwd");
    constexpr TCHAR Jump[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Jump.POH_MM_Jump");
    constexpr TCHAR Fall[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Fall_Loop.POH_MM_Fall_Loop");
    constexpr TCHAR Land[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Land.POH_MM_Land");
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
    FallAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Fall);
    LandAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Land);

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

void UPrinceAnimationWorldSubsystem::Tick(float DeltaTime)
{
    UWorld* World = GetWorld();
    if (!World || !PrinceMesh || !IdleAnimation || !WalkAnimation || !RunAnimation || !JumpAnimation || !FallAnimation || !LandAnimation)
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
            UpdatePrince(*Character, *Mesh, Character->GetVelocity().SizeSquared2D(), DeltaTime);
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

void UPrinceAnimationWorldSubsystem::UpdatePrince(ACharacter& Character, USkeletalMeshComponent& Mesh, const float HorizontalSpeedSquared, const float DeltaTime)
{
    FPrinceAnimationState& State = AnimationStates.FindOrAdd(&Mesh);
    TObjectPtr<UAnimationAsset>& Active = State.ActiveAnimation;
    const UCharacterMovementComponent* Movement = Character.GetCharacterMovement();
    if (Movement && Movement->IsFalling())
    {
        State.bWasFalling = true;
        State.AirborneElapsedSeconds += DeltaTime;
        UAnimationAsset* Desired = State.AirborneElapsedSeconds < JumpAnimation->GetPlayLength()
            ? JumpAnimation.Get()
            : FallAnimation.Get();
        const bool bLoop = Desired == FallAnimation;
        if (Active != Desired)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            Mesh.PlayAnimation(Desired, bLoop);
            Active = Desired;
        }
        return;
    }

    if (State.bWasFalling)
    {
        State.bWasFalling = false;
        State.AirborneElapsedSeconds = 0.0f;
        State.LandingRemainingSeconds = LandAnimation->GetPlayLength();
        Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
        Mesh.PlayAnimation(LandAnimation, false);
        Active = LandAnimation;
        return;
    }

    if (State.LandingRemainingSeconds > 0.0f)
    {
        State.LandingRemainingSeconds = FMath::Max(0.0f, State.LandingRemainingSeconds - DeltaTime);
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
    return bEnableRuntimeLocomotion && PrinceMesh && IdleAnimation && WalkAnimation && RunAnimation && JumpAnimation && FallAnimation && LandAnimation;
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
