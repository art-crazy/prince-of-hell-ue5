#pragma once

#include "Kismet/BlueprintFunctionLibrary.h"

#include "PrinceAnimationGraphLibrary.generated.h"

/** Editor-only, repeatable conversion of the copied UE locomotion graph. */
UCLASS()
class PRINCEANIMATIONRUNTIME_API UPrinceAnimationGraphLibrary final : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    /** Rebinds the isolated graph to clips retargeted for the AccuRIG skeleton. */
    UFUNCTION(BlueprintCallable, Category = "Prince|Animation|Editor")
    static bool RebindAccuRigUE58Graph();
};
