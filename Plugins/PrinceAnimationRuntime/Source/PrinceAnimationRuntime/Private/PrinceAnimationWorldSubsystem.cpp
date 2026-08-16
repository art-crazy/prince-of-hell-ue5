#include "PrinceAnimationWorldSubsystem.h"

#include "Animation/AnimationAsset.h"
#include "Components/SkeletalMeshComponent.h"
#include "EngineUtils.h"
#include "GameFramework/Character.h"
#include "PrinceAnimationRuntimeModule.h"

namespace PrinceAnimationPaths
{
    constexpr TCHAR Mesh[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig.SK_POHPrince_TripoRig");
    constexpr TCHAR Idle[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_Idle.A_POH_Idle");
    constexpr TCHAR Walk[] = TEXT("/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_WalkF.A_POH_WalkF");
    constexpr float WalkThreshold = 5.0f;
}

void UPrinceAnimationWorldSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    IdleAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Idle);
    WalkAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Walk);
}

void UPrinceAnimationWorldSubsystem::Tick(float DeltaTime)
{
    UWorld* World = GetWorld();
    if (!World || !IdleAnimation || !WalkAnimation)
    {
        return;
    }

    for (TActorIterator<ACharacter> It(World); It; ++It)
    {
        ACharacter& Character = **It;
        USkeletalMeshComponent* Mesh = Character.GetMesh();
        if (!Mesh || !Mesh->GetSkeletalMeshAsset() || Mesh->GetSkeletalMeshAsset()->GetPathName() != PrinceAnimationPaths::Mesh)
        {
            continue;
        }

        UpdatePrince(*Mesh, Character.GetVelocity().Size2D());
    }
}

void UPrinceAnimationWorldSubsystem::UpdatePrince(USkeletalMeshComponent& Mesh, const float HorizontalSpeed)
{
    UAnimationAsset* Desired = HorizontalSpeed >= PrinceAnimationPaths::WalkThreshold ? WalkAnimation : IdleAnimation;
    TObjectPtr<UAnimationAsset>& Active = ActiveAnimations.FindOrAdd(&Mesh);
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
