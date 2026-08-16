"""Read-only compatibility check for the individual Prince locomotion clips."""

import unreal

PRINCE_SKELETON = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"
ANIMATIONS = (
    "/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_Idle",
    "/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_WalkF",
    "/Game/_Sandbox/Animation/PrinceOfHell/Retargeted/A_POH_RunF",
    "/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_MM_Jump",
    "/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_MM_Fall_Loop",
    "/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_MM_Land",
)

mesh = unreal.load_asset(PRINCE_SKELETON)
if not mesh:
    raise RuntimeError("Prince skeletal mesh is unavailable")

expected_skeleton = mesh.get_editor_property("skeleton")
for path in ANIMATIONS:
    animation = unreal.load_asset(path)
    if not animation:
        raise RuntimeError("Missing animation: {}".format(path))
    if animation.get_editor_property("skeleton") != expected_skeleton:
        raise RuntimeError("Animation targets a different skeleton: {}".format(path))
    unreal.log("PRINCE LOCOMOTION ASSET OK: {}".format(path))

unreal.log("PRINCE LOCOMOTION ASSET AUDIT PASSED")
