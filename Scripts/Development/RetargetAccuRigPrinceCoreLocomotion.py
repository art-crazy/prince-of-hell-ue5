"""Retarget the approved UE5 locomotion core to the AccuRIG Prince sandbox.

Prerequisite: ``RetargetAccuRigPrinceIdleQa.py`` has passed a human visual
check.  This does not assign an Animation Blueprint or touch gameplay assets.
"""

import unreal


RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging/RTG_Manny_To_POHAccuRig"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_Core"
SOURCE_ANIMATIONS = (
    "/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Jump",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Fall_Loop",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Land",
)


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


retargeter = require(RETARGETER)
source_mesh = require(SOURCE_MESH)
target_mesh = require(TARGET_MESH)
registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = []
for path in SOURCE_ANIMATIONS:
    name = path.rsplit("/", 1)[-1]
    data = registry.get_asset_by_object_path(unreal.Name(path + "." + name))
    if not data.is_valid():
        raise RuntimeError("Missing Manny animation: " + path)
    assets.append(data)

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = assets
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = "UE58_"
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = True
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != len(assets):
    raise RuntimeError("Expected {} core clips, got {}".format(len(assets), len(outputs)))

target_skeleton = target_mesh.get_editor_property("skeleton")
for output in outputs:
    path = str(output.package_name)
    asset = unreal.load_asset(path)
    if not asset or asset.get_editor_property("skeleton") != target_skeleton:
        raise RuntimeError("Invalid retarget output: " + path)
    if not unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False):
        raise RuntimeError("Unable to save retargeted output: " + path)
    unreal.log_warning("POH_ACCURIG_CORE_READY {}".format(path))
