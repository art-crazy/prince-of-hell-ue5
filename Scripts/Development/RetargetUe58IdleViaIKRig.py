"""Produce one isolated UE 5.8 idle QA clip through UE's IK Retargeter.

This is the only supported path for Manny animation on the native Tripo mesh.
It deliberately does not touch runtime assets: visual QA must approve this one
clip before locomotion clips are generated.
"""

import unreal


SOURCE_RIG = "/Game/_Sandbox/Rigging/IK_Mannequin_Template"
TARGET_RIG = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/IK_POHPrince_Native"
RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"
SOURCE_ANIMATION = "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedUE58_IK"
PREFIX = "IKQA_"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing required asset: " + path)
    return asset


source_rig = require(SOURCE_RIG)
target_rig = require(TARGET_RIG)
retargeter = require(RETARGETER)
source_mesh = require(SOURCE_MESH)
target_mesh = require(TARGET_MESH)

source_controller = unreal.IKRigController.get_controller(source_rig)
target_controller = unreal.IKRigController.get_controller(target_rig)
if source_controller.get_retarget_root() != "pelvis":
    raise RuntimeError("Manny retarget root must be pelvis")
if target_controller.get_retarget_root() != "Hip":
    raise RuntimeError("Prince retarget root must be Hip")

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
        raise RuntimeError("Missing explicit chain mapping: " + chain)

# Reset only the target retarget pose to the original native-Tripo rest pose.
# Chain-to-chain alignment compensates proportional differences without writing
# Manny transforms into Tripo bone local spaces.
target_bones = target_mesh.get_editor_property("skeleton").get_reference_pose().get_bone_names()
controller.reset_retarget_pose("Default Pose", target_bones, side.TARGET)
controller.auto_align_all_bones(side.TARGET, unreal.RetargetAutoAlignMethod.CHAIN_TO_CHAIN)

if controller.get_num_retarget_ops() != 5:
    raise RuntimeError("Unexpected default IK retarget operation stack")
if not unreal.EditorAssetLibrary.save_asset(RETARGETER, only_if_is_dirty=False):
    raise RuntimeError("Could not save configured IK Retargeter")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
source_data = registry.get_asset_by_object_path(unreal.Name(SOURCE_ANIMATION + ".MM_Idle"))
if not source_data.is_valid():
    raise RuntimeError("Missing UE 5.8 idle source animation")

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = PREFIX
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = False
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != 1:
    raise RuntimeError("Expected exactly one QA animation")

output_data = outputs[0]
output = unreal.load_asset(str(output_data.package_name))
if not output:
    raise RuntimeError("Retargeted QA asset was not created")
if output.get_editor_property("skeleton") != target_mesh.get_editor_property("skeleton"):
    raise RuntimeError("Retargeted QA clip has wrong skeleton")
unreal.EditorAssetLibrary.save_asset(str(output_data.package_name), only_if_is_dirty=False)
unreal.log_warning("POH_IKQA_IDLE_READY {}".format(output_data.package_name))
