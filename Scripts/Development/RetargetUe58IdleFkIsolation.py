"""Create an isolated FK-only UE IKRig retarget test.

Used to identify whether a malformed pose comes from the IK/root passes rather
than from the native Tripo mesh. It never changes the production retargeter or
runtime assets.
"""

import unreal


SEED_RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative"
RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative_FKQA"
SOURCE_RIG = "/Game/_Sandbox/Rigging/IK_Mannequin_Template"
TARGET_RIG = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/IK_POHPrince_Native"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"
SOURCE_ANIMATION = "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedUE58_IK_FKQA"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


retargeter = unreal.load_asset(RETARGETER)
if not retargeter:
    retargeter = unreal.EditorAssetLibrary.duplicate_asset(SEED_RETARGETER, RETARGETER)
if not retargeter:
    raise RuntimeError("Could not create isolated FK retargeter")

source_rig = require(SOURCE_RIG)
target_rig = require(TARGET_RIG)
source_mesh = require(SOURCE_MESH)
target_mesh = require(TARGET_MESH)
controller = unreal.IKRetargeterController.get_controller(retargeter)
side = unreal.RetargetSourceOrTarget

controller.remove_all_ops()
controller.set_ik_rig(side.SOURCE, source_rig)
controller.set_ik_rig(side.TARGET, target_rig)
controller.add_default_ops()
controller.assign_ik_rig_to_all_ops(side.SOURCE, source_rig)
controller.assign_ik_rig_to_all_ops(side.TARGET, target_rig)

for chain in (
    "Spine", "Neck", "Head", "LeftLeg", "LeftFoot", "RightLeg", "RightFoot",
    "LeftClavicle", "LeftArm", "RightClavicle", "RightArm",
):
    if not controller.set_source_chain(chain, chain):
        raise RuntimeError("Missing chain mapping: " + chain)

# Preserve the target's imported rest pose exactly. No auto-align is applied in
# this diagnostic clip. Only FK chain retargeting is allowed to animate it.
target_bones = target_mesh.get_editor_property("skeleton").get_reference_pose().get_bone_names()
controller.reset_retarget_pose("Default Pose", target_bones, side.TARGET)
for index in range(controller.get_num_retarget_ops()):
    controller.set_retarget_op_enabled(index, controller.get_op_name(index) == "FK Chains")

if not unreal.EditorAssetLibrary.save_asset(RETARGETER, only_if_is_dirty=False):
    raise RuntimeError("Could not save isolated FK retargeter")

source_data = unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(
    unreal.Name(SOURCE_ANIMATION + ".MM_Idle")
)
inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = "FKQA_"
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = False
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != 1:
    raise RuntimeError("Expected one FK QA output")
unreal.EditorAssetLibrary.save_asset(str(outputs[0].package_name), only_if_is_dirty=False)
unreal.log_warning("POH_FKQA_IDLE_READY {}".format(outputs[0].package_name))
