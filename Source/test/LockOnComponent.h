#pragma once

#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "LockOnComponent.generated.h"

class UInputAction;
class UInputMappingContext;
class AController;

/**
 * Native Enhanced Input binding for target lock-on.
 * Exists in C++ because Blueprint-authored EnhancedInputAction event nodes created
 * through the MCP automation bridge never fire their Triggered pin at runtime
 * (see Docs/AI/McpAutomationBridgeNotes.md) - BindAction here is not affected.
 */
UCLASS(ClassGroup = (Custom), meta = (BlueprintSpawnableComponent))
class TEST_API ULockOnComponent : public UActorComponent
{
	GENERATED_BODY()

public:
	ULockOnComponent();

	UPROPERTY(EditDefaultsOnly, Category = "LockOn|Input")
	TObjectPtr<UInputAction> LockOnAction;

	UPROPERTY(EditDefaultsOnly, Category = "LockOn")
	float SearchRadius = 1500.f;

	UPROPERTY(EditDefaultsOnly, Category = "LockOn")
	float SearchHalfAngleDegrees = 50.f;

	UPROPERTY(EditDefaultsOnly, Category = "LockOn")
	FName TargetableTag = "Lockable";

	UPROPERTY(EditDefaultsOnly, Category = "LockOn")
	float TurnInterpSpeed = 10.f;

	UPROPERTY(ReplicatedUsing = OnRep_LockedTarget, BlueprintReadOnly, Category = "LockOn")
	TObjectPtr<AActor> LockedTarget;

protected:
	virtual void BeginPlay() override;
	virtual void TickComponent(float DeltaTime, ELevelTick TickType, FActorComponentTickFunction* ThisTickFunction) override;
	virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

public:
	UPROPERTY(BlueprintReadOnly, Category = "LockOn|Debug")
	bool bInputBound = false;

	UPROPERTY(BlueprintReadOnly, Category = "LockOn|Debug")
	int32 TriggerCount = 0;

	UPROPERTY(BlueprintReadOnly, Category = "LockOn|Debug")
	int32 OverlapCount = 0;

private:
	void TryBindInput();
	void OnLockOnTriggered();
	AActor* FindBestTarget();
	void SetLockedTarget(AActor* NewTarget);

	UFUNCTION(Server, Reliable)
	void Server_SetLockedTarget(AActor* NewTarget);

	UFUNCTION()
	void OnRep_LockedTarget();

	UFUNCTION()
	void OnTargetEndPlay(AActor* EndedActor, EEndPlayReason::Type EndPlayReason);
};
