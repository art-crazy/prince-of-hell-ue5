"""Export exactly one UE 5.8 Manny idle to the AccuRIG Prince candidate.

The generated sequence remains sandbox-only.  A human visual check is required
before any locomotion sequence or runtime Blueprint is retargeted.
"""

import unreal


RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging/RTG_Manny_To_POHAccuRig"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"
SOURCE_ANIMATION = "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_IK_QA"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


retargeter = require(RETARGETER)
source_mesh = require(SOURCE_MESH)
target_mesh = require(TARGET_MESH)
registry = unreal.AssetRegistryHelpers.get_asset_registry()
source_data = registry.get_asset_by_object_path(unreal.Name(SOURCE_ANIMATION + ".MM_Idle"))
if not source_data.is_valid():
    raise RuntimeError("Manny idle source animation is unavailable")

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = "UE58_IKQA_"
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = True
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != 1:
    raise RuntimeError("Expected one AccuRIG idle QA asset, got {}".format(len(outputs)))

output_path = str(outputs[0].package_name)
output = unreal.load_asset(output_path)
if not output:
    raise RuntimeError("Retarget output failed to load: " + output_path)
if output.get_editor_property("skeleton") != target_mesh.get_editor_property("skeleton"):
    raise RuntimeError("Retargeted idle is bound to the wrong skeleton")
if not unreal.EditorAssetLibrary.save_asset(output_path, only_if_is_dirty=False):
    raise RuntimeError("Unable to save AccuRIG idle QA sequence")

unreal.log_warning("POH_ACCURIG_IDLE_QA_READY {}".format(output_path))
