"""Retarget UE5.8's complete Unarmed locomotion graph into the AccuRIG sandbox.

This retains UE's authored state machine and referenced motion set.  It never
modifies the project Third Person pawn or the playable NativeTripo assets.
"""

import unreal


RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging/RTG_Manny_To_POHAccuRig"
SOURCE_BLUEPRINT = "/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


source_blueprint = require(SOURCE_BLUEPRINT)
retargeter = require(RETARGETER)
source_mesh = require(SOURCE_MESH)
target_mesh = require(TARGET_MESH)
registry = unreal.AssetRegistryHelpers.get_asset_registry()
source_data = registry.get_asset_by_object_path(unreal.Name(source_blueprint.get_path_name()))
if not source_data.is_valid():
    raise RuntimeError("Unable to resolve UE unarmed Animation Blueprint")

# Batch retargeting cannot reliably overwrite a referenced Blend Space in
# place; it creates a suffixed asset while leaving stale dependencies behind.
# This folder is an isolated, generated candidate only, so recreate it as one
# atomic asset set. Nothing in production may reference this path.
if unreal.EditorAssetLibrary.does_directory_exist(TARGET_FOLDER):
    if not unreal.EditorAssetLibrary.delete_directory(TARGET_FOLDER):
        raise RuntimeError("Unable to clear generated AccuRIG motion set")

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = "UE58_"
inputs.include_referenced_assets = True
inputs.overwrite_existing_files = True
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if not outputs:
    raise RuntimeError("UE Unarmed Animation Blueprint retarget produced no assets")

for output in outputs:
    path = str(output.package_name)
    if not unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False):
        raise RuntimeError("Unable to save retargeted asset: " + path)
    unreal.log_warning("POH_ACCURIG_ABP_READY {}".format(path))
