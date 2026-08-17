"""Use Game Animation Sample's neutral full-body forward loops in Prince's Blend Space.

This changes only the forward samples (W / W+Shift).  Side and backward
samples remain on the existing retargeted UE set until their matching GAS
directions are migrated as one coherent follow-up.
"""

import unreal


BLEND_SPACE = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_BS_Idle_Walk_Run"
CLIPS = {
    0.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Stand_Idle_Loop",
    300.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Walk_Loop_F",
    600.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Run_Loop_F",
}


if not unreal.PrinceAnimationAssetTools.apply_game_animation_sample_forward_locomotion():
    raise RuntimeError("Unable to replace forward locomotion cells")
if not unreal.EditorAssetLibrary.save_asset(BLEND_SPACE, only_if_is_dirty=False):
    raise RuntimeError("Unable to save locomotion Blend Space")

unreal.log_warning("POH_GAS_FORWARD_LOCOMOTION_APPLIED samples=3")
