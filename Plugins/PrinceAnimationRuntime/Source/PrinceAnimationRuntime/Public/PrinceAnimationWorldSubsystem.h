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
    bool bWasAirborne = false;
    bool bUseDive = false;
};

/**
 * Uses Tripo-native clips exported on the same skeleton as the playable mesh.
 * This avoids the deformation caused by cross-skeleton retargeting.
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
    TObjectPtr<UAnimationAsset> DiveAnimation;

    UPROPERTY(Transient)
    TObjectPtr<UAnimationAsset> FallAnimation;

    /** Allows isolated clip QA without modifying runtime source code. */
    UPROPERTY(Config, EditAnywhere, Category="Prince|Animation")
    bool bEnableRuntimeLocomotion = true;
    FDelegateHandle ActorSpawnedHandle;
    TSet<TWeakObjectPtr<ACharacter>> PrinceCharacters;
    TMap<TWeakObjectPtr<USkeletalMeshComponent>, FPrinceAnimationState> AnimationStates;
};
