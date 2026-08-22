"""Create a clean Manny-to-native-Prince retargeter from the current UE 5.8 rig.

The old retargeter targets an obsolete imported skeleton and is deliberately not
modified.  This asset has the same core chain names on both sides, so mappings
are explicit and reproducible.
"""

import unreal


SOURCE_RETARGETER = "/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH"
TARGET_RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative"
SOURCE_RIG = "/Game/_Sandbox/Rigging/IK_Mannequin_Template"
TARGET_RIG = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/IK_POHPrince_Native"

source_rig = unreal.load_asset(SOURCE_RIG)
target_rig = unreal.load_asset(TARGET_RIG)
if not source_rig or not target_rig:
    raise RuntimeError("Source or native target IK Rig is unavailable")

retargeter = unreal.load_asset(TARGET_RETARGETER)
if not retargeter:
    retargeter = unreal.EditorAssetLibrary.duplicate_asset(SOURCE_RETARGETER, TARGET_RETARGETER)
if not retargeter:
    raise RuntimeError("Unable to create native Prince retargeter")

controller = unreal.IKRetargeterController.get_controller(retargeter)
source_or_target = unreal.RetargetSourceOrTarget

# This asset can be regenerated repeatedly.  add_default_ops() appends a new
# stack, so clearing first is essential: duplicated FK/IK/root passes corrupt
# the exported pose and can collapse the character outside the camera.
controller.remove_all_ops()
controller.set_ik_rig(source_or_target.SOURCE, source_rig)
controller.set_ik_rig(source_or_target.TARGET, target_rig)
controller.add_default_ops()
controller.assign_ik_rig_to_all_ops(source_or_target.SOURCE, source_rig)
controller.assign_ik_rig_to_all_ops(source_or_target.TARGET, target_rig)

for name in (
    "Spine", "Neck", "Head", "LeftLeg", "LeftFoot", "RightLeg", "RightFoot",
    "LeftClavicle", "LeftArm", "RightClavicle", "RightArm",
):
    if not controller.set_source_chain(name, name):
        raise RuntimeError(f"Unable to map retarget chain: {name}")

# Chain-to-chain alignment is deterministic and works across the intentionally
# different body proportions of Manny and the Prince mesh.
# The duplicated seed retargeter has an unrelated target pose.  Reset it before
# alignment; otherwise auto-align compounds offsets belonging to the retired
# TripoRig mesh.
target_bones = target_rig.get_editor_property("preview_skeletal_mesh").get_editor_property("skeleton").get_reference_pose().get_bone_names()
controller.reset_retarget_pose("Default Pose", target_bones, source_or_target.TARGET)
controller.auto_align_all_bones(
    source_or_target.TARGET,
    unreal.RetargetAutoAlignMethod.CHAIN_TO_CHAIN,
)

if not unreal.EditorAssetLibrary.save_asset(TARGET_RETARGETER, only_if_is_dirty=False):
    raise RuntimeError("Unable to save native Prince retargeter")

unreal.log_warning(f"POH_NATIVE_RETARGETER_READY {TARGET_RETARGETER}")
