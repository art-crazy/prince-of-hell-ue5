#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"

#include "PrinceAnimationAssetTools.generated.h"

/** Editor-safe, deterministic changes to generated Prince animation assets. */
UCLASS()
class PRINCEANIMATIONRUNTIME_API UPrinceAnimationAssetTools final : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    /** Replaces only the forward idle/walk/run cells in the generated Prince
     *  Blend Space with the retargeted Game Animation Sample loops. */
    UFUNCTION(BlueprintCallable, Category="Prince|Animation", meta=(DevelopmentOnly))
    static bool ApplyGameAnimationSampleForwardLocomotion();
};
