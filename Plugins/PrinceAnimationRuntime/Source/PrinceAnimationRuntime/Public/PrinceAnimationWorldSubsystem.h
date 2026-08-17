#pragma once

#include "Subsystems/WorldSubsystem.h"
#include "Tickable.h"

#include "PrinceAnimationWorldSubsystem.generated.h"

class UAnimationAsset;
class AActor;
class ACharacter;
class USkeletalMesh;
class USkeletalMeshComponent;

/** Runtime state belongs to one mesh and is pruned when that mesh is destroyed. */
struct FPrinceAnimationState
{
    TObjectPtr<UAnimationAsset> ActiveAnimation;
    bool bWasFalling = false;
    bool bAppliedIdleReferencePose = false;
};

/**
 * Temporary runtime fallback while the production Animation Blueprint is built.
 * It uses either native clips or UE 5.8 clips retargeted to the playable
 * skeleton; it never plays legacy assets for another skeleton.
 */
UCLASS(Config=Game, DefaultConfig)
class PRINCEANIMATIONRUNTIME_API UPrinceAnimationWorldSubsystem final : public UTickableWorldSubsystem
{
    GENERATED_BODY()

public:
    virtual void Initialize(FSubsystemCollectionBase& Collection) override;
    virtual void Deinitialize() override;
    virtual void Tick(float DeltaTime) override;
    virtual TStatId GetStatId() const override;
    virtual bool IsTickable() const override;
    virtual bool DoesSupportWorldType(const EWorldType::Type WorldType) const override;

private:
    void RegisterPrince(AActor* Actor);
    void UpdatePrince(ACharacter& Character, USkeletalMeshComponent& Mesh, float HorizontalSpeedSquared);
    void UpdatePlayerMovementSpeed(ACharacter& Character) const;

    UPROPERTY(Transient)
    TObjectPtr<USkeletalMesh> PrinceMesh;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> IdleAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> WalkAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> RunAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> JumpAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> FallAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> LandAnimation;

    // The Manny candidate is intentionally restricted to a single idle clip
    // while its bind pose and skinning are diagnosed.
    bool bMannyCandidateMode = false;

    /** AccuRIG is the validated UE-compatible candidate; it may use the full
     *  retargeted UE 5.8 locomotion set without touching the fallback mesh. */
    bool bAccuRigCandidateMode = false;

    /** Allows isolated clip QA without modifying runtime source code. */
    UPROPERTY(Config, EditAnywhere, Category="Prince|Animation")
    bool bEnableRuntimeLocomotion = true;
    FDelegateHandle ActorSpawnedHandle;
    TSet<TWeakObjectPtr<ACharacter>> PrinceCharacters;
    TMap<TWeakObjectPtr<USkeletalMeshComponent>, FPrinceAnimationState> AnimationStates;
};
