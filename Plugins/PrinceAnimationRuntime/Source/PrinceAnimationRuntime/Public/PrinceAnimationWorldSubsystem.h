#pragma once

#include "Subsystems/WorldSubsystem.h"
#include "Tickable.h"

#include "PrinceAnimationWorldSubsystem.generated.h"

class UAnimationAsset;
class AActor;
class ACharacter;
class USkeletalMesh;
class USkeletalMeshComponent;

/**
 * Uses only individually validated clips while the dedicated IK retargeter is
 * being rebuilt. This avoids the incompatible Control Rig in the bulk export.
 */
UCLASS()
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
    void UpdatePrince(USkeletalMeshComponent& Mesh, float HorizontalSpeedSquared);

    TObjectPtr<USkeletalMesh> PrinceMesh;
    TObjectPtr<UAnimationAsset> IdleAnimation;
    TObjectPtr<UAnimationAsset> WalkAnimation;
    FDelegateHandle ActorSpawnedHandle;
    TSet<TWeakObjectPtr<ACharacter>> PrinceCharacters;
    TMap<TWeakObjectPtr<USkeletalMeshComponent>, TObjectPtr<UAnimationAsset>> ActiveAnimations;
};
