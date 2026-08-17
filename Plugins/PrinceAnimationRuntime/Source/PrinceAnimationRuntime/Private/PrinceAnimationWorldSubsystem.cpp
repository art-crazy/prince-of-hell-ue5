#include "PrinceAnimationWorldSubsystem.h"

#include "Animation/AnimationAsset.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"
#include "GameFramework/CharacterMovementComponent.h"
#include "GameFramework/PlayerController.h"
#include "HAL/IConsoleManager.h"
#include "InputCoreTypes.h"

DEFINE_LOG_CATEGORY_STATIC(LogPrinceAnimation, Log, All);

static TAutoConsoleVariable<int32> CVarPrinceUseMannyCandidate(
    TEXT("poh.UseMannyCandidate"),
    0,
    TEXT("Use the isolated UE Manny-skeleton Prince candidate. 0 = stable Tripo fallback, 1 = direct UE 5.8 animation verification."),
    ECVF_Default);

namespace PrinceAnimationPaths
{
    constexpr TCHAR Mesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo.SK_POHPrince_NativeTripo");
    // This asset is only the stable reference pose while the character is being reskinned to Manny.
    // It must not be replaced with an incompatible Manny retargeted clip.
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripoidle.SK_POHPrince_NativeTripoidle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripowalk.SK_POHPrince_NativeTripowalk");
    constexpr TCHAR Run[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTriporun.SK_POHPrince_NativeTriporun");
    constexpr TCHAR Jump[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripojump.SK_POHPrince_NativeTripojump");
    constexpr TCHAR CandidateMesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/MannyCandidate/SK_POHPrince_MannyCandidate.SK_POHPrince_MannyCandidate");
    constexpr TCHAR CandidateIdle[] = TEXT("/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle.MM_Idle");
    constexpr TCHAR CandidateWalk[] = TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Fwd.MF_Unarmed_Walk_Fwd");
    constexpr TCHAR CandidateRun[] = TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd.MF_Unarmed_Jog_Fwd");
    constexpr TCHAR CandidateJump[] = TEXT("/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Jump.MM_Jump");
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
    const bool bUseMannyCandidate = CVarPrinceUseMannyCandidate.GetValueOnGameThread() != 0;
    bMannyCandidateMode = bUseMannyCandidate;
    PrinceMesh = LoadObject<USkeletalMesh>(nullptr, bUseMannyCandidate ? PrinceAnimationPaths::CandidateMesh : PrinceAnimationPaths::Mesh);
    IdleAnimation = LoadObject<UAnimationAsset>(nullptr, bUseMannyCandidate ? PrinceAnimationPaths::CandidateIdle : PrinceAnimationPaths::Idle);
    WalkAnimation = bUseMannyCandidate ? nullptr : LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Walk);
    RunAnimation = bUseMannyCandidate ? nullptr : LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Run);
    JumpAnimation = bUseMannyCandidate ? nullptr : LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Jump);
    UE_LOG(LogPrinceAnimation, Log, TEXT("POH_RUNTIME_ANIMATION_PATH mode=%s mesh=%s idle=%s locomotion=%s"),
        bUseMannyCandidate ? TEXT("MannyCandidate") : TEXT("NativeTripo"),
        *GetNameSafe(PrinceMesh), *GetNameSafe(IdleAnimation),
        bUseMannyCandidate ? TEXT("disabled-for-diagnosis") : TEXT("enabled"));

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
    if (!World || !PrinceMesh || !IdleAnimation || (!bMannyCandidateMode && (!WalkAnimation || !RunAnimation || !JumpAnimation)))
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
            if (!bMannyCandidateMode)
            {
                UpdatePlayerMovementSpeed(*Character);
            }
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
    const USkeletalMesh* StableMesh = LoadObject<USkeletalMesh>(nullptr, PrinceAnimationPaths::Mesh);
    if (Mesh && (Mesh->GetSkeletalMeshAsset() == PrinceMesh || Mesh->GetSkeletalMeshAsset() == StableMesh))
    {
        if (Mesh->GetSkeletalMeshAsset() != PrinceMesh)
        {
            Mesh->SetSkeletalMesh(PrinceMesh);
        }
        PrinceCharacters.Add(Character);
        UE_LOG(LogPrinceAnimation, Log, TEXT("POH_RUNTIME_ANIMATION_REGISTER character=%s mesh=%s"), *GetNameSafe(Character), *GetNameSafe(PrinceMesh));
    }
}

void UPrinceAnimationWorldSubsystem::UpdatePrince(ACharacter& Character, USkeletalMeshComponent& Mesh, const float HorizontalSpeedSquared)
{
    FPrinceAnimationState& State = AnimationStates.FindOrAdd(&Mesh);
    TObjectPtr<UAnimationAsset>& Active = State.ActiveAnimation;

    if (bMannyCandidateMode)
    {
        // Deliberately play exactly one compatible asset. If this fails, the
        // defect is in the imported mesh/bind pose rather than locomotion.
        if (Active != IdleAnimation)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            Mesh.PlayAnimation(IdleAnimation, true);
            Active = IdleAnimation;
        }
        return;
    }

    const UCharacterMovementComponent* Movement = Character.GetCharacterMovement();
    if (Movement && Movement->IsFalling())
    {
        State.bWasFalling = true;
        if (Active != JumpAnimation)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            Mesh.PlayAnimation(JumpAnimation, false);
            Active = JumpAnimation;
            State.bAppliedIdleReferencePose = false;
        }
        return;
    }

    if (State.bWasFalling)
    {
        State.bWasFalling = false;
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
            State.bAppliedIdleReferencePose = false;
        }
        return;
    }

    const bool bWasWalking = Active == WalkAnimation;
    const float Threshold = bWasWalking ? PrinceAnimationPaths::StopWalkingSpeed : PrinceAnimationPaths::StartWalkingSpeed;
    if (HorizontalSpeedSquared < FMath::Square(Threshold))
    {
        if (!State.bAppliedIdleReferencePose)
        {
            Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
            // A null single-node animation evaluates to no pose for this imported skeleton,
            // making the mesh disappear. Keep a compatible source pose until the Manny reskin lands.
            Mesh.PlayAnimation(IdleAnimation, true);
            Active = IdleAnimation;
            State.bAppliedIdleReferencePose = true;
        }
        return;
    }

    UAnimationAsset* Desired = WalkAnimation;
    if (Active == Desired)
    {
        return;
    }

    Mesh.SetAnimationMode(EAnimationMode::AnimationSingleNode);
    Mesh.PlayAnimation(Desired, true);
    Active = Desired;
    State.bAppliedIdleReferencePose = false;
}

TStatId UPrinceAnimationWorldSubsystem::GetStatId() const
{
    RETURN_QUICK_DECLARE_CYCLE_STAT(UPrinceAnimationWorldSubsystem, STATGROUP_Tickables);
}

bool UPrinceAnimationWorldSubsystem::IsTickable() const
{
    return bEnableRuntimeLocomotion && PrinceMesh && IdleAnimation &&
        (bMannyCandidateMode || (WalkAnimation && RunAnimation && JumpAnimation));
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
