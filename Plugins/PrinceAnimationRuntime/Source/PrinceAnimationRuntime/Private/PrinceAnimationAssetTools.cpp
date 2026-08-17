#include "PrinceAnimationAssetTools.h"

#include "Animation/AnimSequence.h"
#include "Animation/BlendSpace.h"

namespace PrinceAnimationAssetPaths
{
    constexpr TCHAR BlendSpace[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_BS_Idle_Walk_Run.UE58_BS_Idle_Walk_Run");
    constexpr TCHAR OldIdle[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MM_Idle.UE58_MM_Idle");
    constexpr TCHAR OldWalk[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MF_Unarmed_Walk_Fwd.UE58_MF_Unarmed_Walk_Fwd");
    constexpr TCHAR OldRun[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MF_Unarmed_Jog_Fwd.UE58_MF_Unarmed_Jog_Fwd");
    constexpr TCHAR GasIdle[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Stand_Idle_Loop.GAS_M_Neutral_Stand_Idle_Loop");
    constexpr TCHAR GasWalk[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Walk_Loop_F.GAS_M_Neutral_Walk_Loop_F");
    constexpr TCHAR GasRun[] = TEXT("/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Run_Loop_F.GAS_M_Neutral_Run_Loop_F");
}

bool UPrinceAnimationAssetTools::ApplyGameAnimationSampleForwardLocomotion()
{
#if WITH_EDITOR
    UBlendSpace* BlendSpace = LoadObject<UBlendSpace>(nullptr, PrinceAnimationAssetPaths::BlendSpace);
    UAnimSequence* OldIdle = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::OldIdle);
    UAnimSequence* OldWalk = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::OldWalk);
    UAnimSequence* OldRun = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::OldRun);
    UAnimSequence* GasIdle = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::GasIdle);
    UAnimSequence* GasWalk = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::GasWalk);
    UAnimSequence* GasRun = LoadObject<UAnimSequence>(nullptr, PrinceAnimationAssetPaths::GasRun);
    if (!BlendSpace || !OldIdle || !OldWalk || !OldRun || !GasIdle || !GasWalk || !GasRun)
    {
        return false;
    }

    BlendSpace->Modify();
    TMap<UAnimationAsset*, UAnimationAsset*> Replacements;
    Replacements.Add(OldIdle, GasIdle);
    Replacements.Add(OldWalk, GasWalk);
    Replacements.Add(OldRun, GasRun);
    BlendSpace->ReplaceReferredAnimations(Replacements);
    BlendSpace->ValidateSampleData();
    BlendSpace->MarkPackageDirty();
    BlendSpace->PostEditChange();
    return true;
#else
    return false;
#endif
}
