"""Fail fast if generated Manny animations target the wrong Prince skeleton."""

import unreal


TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"
TARGET_RIG = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/IK_POHPrince_Native"
RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative"
ANIMATIONS = (
    "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Idle",
    "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MF_Unarmed_Jog_Fwd",
    "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Jump",
    "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Fall_Loop",
    "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny/POH_MM_Land",
)

mesh = unreal.load_asset(TARGET_MESH)
rig = unreal.load_asset(TARGET_RIG)
retargeter = unreal.load_asset(RETARGETER)
if not mesh or not rig or not retargeter:
    raise RuntimeError("Native Prince retargeting prerequisites are missing")

target_skeleton = mesh.get_editor_property("skeleton")
rig_controller = unreal.IKRigController.get_controller(rig)
if rig_controller.get_skeletal_mesh() != mesh:
    raise RuntimeError("Native Prince IK Rig references another mesh")

retarget_controller = unreal.IKRetargeterController.get_controller(retargeter)
if retarget_controller.get_ik_rig(unreal.RetargetSourceOrTarget.TARGET) != rig:
    raise RuntimeError("Native Prince retargeter points at another target IK Rig")

for path in ANIMATIONS:
    animation = unreal.load_asset(path)
    if not animation:
        raise RuntimeError(f"Missing retargeted animation: {path}")
    if animation.get_editor_property("skeleton") != target_skeleton:
        raise RuntimeError(f"Wrong skeleton on {path}")
    unreal.log_warning(f"POH_NATIVE_RETARGET_VALID {path}")
