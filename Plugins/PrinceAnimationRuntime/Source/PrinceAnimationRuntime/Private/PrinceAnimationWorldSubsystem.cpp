#include "PrinceAnimationWorldSubsystem.h"

#include "Animation/AnimationAsset.h"
#include "Components/SkeletalMeshComponent.h"
#include "Engine/SkeletalMesh.h"
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
    PrinceMesh = LoadObject<USkeletalMesh>(nullptr, PrinceAnimationPaths::Mesh);
    IdleAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Idle);
    WalkAnimation = LoadObject<UAnimationAsset>(nullptr, PrinceAnimationPaths::Walk);
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

    for (TActorIterator<ACharacter> It(World); It; ++It)
    {
        ACharacter& Character = **It;
        USkeletalMeshComponent* Mesh = Character.GetMesh();
        if (!Mesh || Mesh->GetSkeletalMeshAsset() != PrinceMesh)
        {
            continue;
        }

        UpdatePrince(*Mesh, Character.GetVelocity().SizeSquared2D());
    }
}

void UPrinceAnimationWorldSubsystem::UpdatePrince(USkeletalMeshComponent& Mesh, const float HorizontalSpeedSquared)
{
    UAnimationAsset* Desired = HorizontalSpeedSquared >= FMath::Square(PrinceAnimationPaths::WalkThreshold) ? WalkAnimation : IdleAnimation;
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

bool UPrinceAnimationWorldSubsystem::IsTickable() const
{
    return PrinceMesh && IdleAnimation && WalkAnimation;
}

bool UPrinceAnimationWorldSubsystem::DoesSupportWorldType(const EWorldType::Type WorldType) const
{
    return WorldType == EWorldType::Game || WorldType == EWorldType::PIE;
}
