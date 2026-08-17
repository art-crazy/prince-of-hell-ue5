"""Configure UE IKRig and export one Manny idle QA clip for the new warrior."""

import unreal


FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/UE5Retargetable"
MESH_PATH = FOLDER + "/SK_POHPrince_UE5Retargetable"
RIG_PATH = FOLDER + "/Rigging/IK_POHPrince_UE5Retargetable"
RETARGETER_PATH = FOLDER + "/Rigging/RTG_Manny_To_POH_UE5Retargetable"
SOURCE_RIG = "/Game/_Sandbox/Rigging/IK_Mannequin_Template"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
SOURCE_ANIMATION = "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle"
OUTPUT_FOLDER = FOLDER + "/RetargetedUE58_IK_QA"

CHAINS = (
    ("Spine", "spine_01", "spine_03"),
    ("Neck", "neck_01", "neck_01"),
    ("Head", "head", "head"),
    ("LeftLeg", "thigh_l", "foot_l"),
    ("LeftFoot", "ball_l", "ball_l"),
    ("RightLeg", "thigh_r", "foot_r"),
    ("RightFoot", "ball_r", "ball_r"),
    ("LeftClavicle", "clavicle_l", "clavicle_l"),
    ("LeftArm", "upperarm_l", "hand_l"),
    ("RightClavicle", "clavicle_r", "clavicle_r"),
    ("RightArm", "upperarm_r", "hand_r"),
)


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


mesh = require(MESH_PATH)
source_rig = require(SOURCE_RIG)
source_mesh = require(SOURCE_MESH)
rig = unreal.load_asset(RIG_PATH)
if not rig:
    rig = unreal.IKRigDefinitionFactory.create_new_ik_rig_asset(FOLDER + "/Rigging", "IK_POHPrince_UE5Retargetable")
if not rig:
    raise RuntimeError("Could not create warrior IKRig")

rig_controller = unreal.IKRigController.get_controller(rig)
if not rig_controller.set_skeletal_mesh(mesh):
    raise RuntimeError("Could not assign warrior mesh to IKRig")
if not rig_controller.set_retarget_root("pelvis"):
    raise RuntimeError("Could not set warrior retarget root")
existing = {str(chain.chain_name) for chain in rig_controller.get_retarget_chains()}
for name, first, last in CHAINS:
    if name not in existing:
        if str(rig_controller.add_retarget_chain(name, first, last, "")) != name:
            raise RuntimeError("Could not create IKRig chain: " + name)
unreal.EditorAssetLibrary.save_asset(RIG_PATH, only_if_is_dirty=False)

retargeter = unreal.load_asset(RETARGETER_PATH)
if not retargeter:
    retargeter = unreal.EditorAssetLibrary.duplicate_asset(
        "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative",
        RETARGETER_PATH,
    )
if not retargeter:
    raise RuntimeError("Could not create warrior IK Retargeter")

controller = unreal.IKRetargeterController.get_controller(retargeter)
side = unreal.RetargetSourceOrTarget
controller.remove_all_ops()
controller.set_ik_rig(side.SOURCE, source_rig)
controller.set_ik_rig(side.TARGET, rig)
controller.add_default_ops()
controller.assign_ik_rig_to_all_ops(side.SOURCE, source_rig)
controller.assign_ik_rig_to_all_ops(side.TARGET, rig)
for chain, _, _ in CHAINS:
    if not controller.set_source_chain(chain, chain):
        raise RuntimeError("Could not map retarget chain: " + chain)

# Both source and target are conventional UE-style humanoid rigs. Keep the
# imported warrior rest pose untouched; IKRig applies proportional FK/IK safely.
target_bones = mesh.get_editor_property("skeleton").get_reference_pose().get_bone_names()
controller.reset_retarget_pose("Default Pose", target_bones, side.TARGET)
if not unreal.EditorAssetLibrary.save_asset(RETARGETER_PATH, only_if_is_dirty=False):
    raise RuntimeError("Could not save warrior IK Retargeter")

source_data = unreal.AssetRegistryHelpers.get_asset_registry().get_asset_by_object_path(
    unreal.Name(SOURCE_ANIMATION + ".MM_Idle")
)
inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = OUTPUT_FOLDER
inputs.prefix = "UE58_IKQA_"
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = False
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != 1:
    raise RuntimeError("Expected one warrior idle QA asset")
output = unreal.load_asset(str(outputs[0].package_name))
if not output or output.get_editor_property("skeleton") != mesh.get_editor_property("skeleton"):
    raise RuntimeError("Warrior QA animation targets the wrong skeleton")
unreal.EditorAssetLibrary.save_asset(str(outputs[0].package_name), only_if_is_dirty=False)
unreal.log_warning("POH_UE5_WARRIOR_IKQA_READY {}".format(outputs[0].package_name))
