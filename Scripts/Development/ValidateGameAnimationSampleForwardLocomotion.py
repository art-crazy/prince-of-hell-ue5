"""Technical validation for the three Game Animation Sample forward cells."""

import unreal


BLEND_SPACE = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_BS_Idle_Walk_Run"
EXPECTED = {
    0.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Stand_Idle_Loop.GAS_M_Neutral_Stand_Idle_Loop",
    300.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Walk_Loop_F.GAS_M_Neutral_Walk_Loop_F",
    600.0: "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core/GAS_M_Neutral_Run_Loop_F.GAS_M_Neutral_Run_Loop_F",
}


blend = unreal.load_asset(BLEND_SPACE)
target_skeleton = unreal.load_asset(
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig").get_editor_property("skeleton")
found = {}
for sample in blend.get_editor_property("sample_data"):
    position = sample.get_editor_property("sample_value")
    if abs(position.x) <= 0.01 and position.y in EXPECTED:
        animation = sample.get_editor_property("animation")
        found[position.y] = animation.get_path_name()
        if animation.get_editor_property("skeleton") != target_skeleton:
            raise RuntimeError("Forward cell uses wrong skeleton at speed {}".format(position.y))

if found != EXPECTED:
    raise RuntimeError("Unexpected forward locomotion cells: {}".format(found))
unreal.log_warning("POH_GAS_FORWARD_LOCOMOTION_VALIDATE_OK cells={}".format(len(found)))
