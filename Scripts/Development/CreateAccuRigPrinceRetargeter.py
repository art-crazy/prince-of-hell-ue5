"""Create a sandbox-only UE Manny -> AccuRIG Prince IK Retargeter.

No animation is exported and no runtime asset is changed here.  The retargeter
is intentionally a prerequisite for a later single-idle validation.
"""

import unreal


SEED_RETARGETER = "/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH"
SOURCE_RIG = "/Game/_Sandbox/Rigging/IK_Mannequin_Template"
TARGET_RIG = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging/IK_POHPrince_AccuRig"
TARGET_RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging/RTG_Manny_To_POHAccuRig"

source_rig = unreal.load_asset(SOURCE_RIG)
target_rig = unreal.load_asset(TARGET_RIG)
seed = unreal.load_asset(SEED_RETARGETER)
if not source_rig or not target_rig or not seed:
    raise RuntimeError("Missing source IK Rig, candidate IK Rig, or seed retargeter")

retargeter = unreal.load_asset(TARGET_RETARGETER)
if not retargeter:
    retargeter = unreal.EditorAssetLibrary.duplicate_asset(SEED_RETARGETER, TARGET_RETARGETER)
if not retargeter:
    raise RuntimeError("Unable to create AccuRIG Prince retargeter")

controller = unreal.IKRetargeterController.get_controller(retargeter)
side = unreal.RetargetSourceOrTarget
controller.remove_all_ops()
controller.set_ik_rig(side.SOURCE, source_rig)
controller.set_ik_rig(side.TARGET, target_rig)
controller.add_default_ops()
controller.assign_ik_rig_to_all_ops(side.SOURCE, source_rig)
controller.assign_ik_rig_to_all_ops(side.TARGET, target_rig)

for name in (
    "Spine", "Neck", "Head", "LeftLeg", "LeftFoot", "RightLeg", "RightFoot",
    "LeftClavicle", "LeftArm", "RightClavicle", "RightArm",
):
    if not controller.set_source_chain(name, name):
        raise RuntimeError("Unable to map retarget chain: " + name)

# The duplicated seed must not carry reference-pose offsets from the abandoned
# Tripo rig.  Start the candidate with AccuRIG's own valid rest pose instead.
candidate_mesh = target_rig.get_editor_property("preview_skeletal_mesh")
target_bones = candidate_mesh.get_editor_property("skeleton").get_reference_pose().get_bone_names()
controller.reset_retarget_pose("Default Pose", target_bones, side.TARGET)
controller.auto_align_all_bones(side.TARGET, unreal.RetargetAutoAlignMethod.CHAIN_TO_CHAIN)

if not unreal.EditorAssetLibrary.save_asset(TARGET_RETARGETER, only_if_is_dirty=False):
    raise RuntimeError("Unable to save AccuRIG Prince retargeter")

unreal.log_warning("POH_ACCURIG_RETARGETER_READY {}".format(TARGET_RETARGETER))
