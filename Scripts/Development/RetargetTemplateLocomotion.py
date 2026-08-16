"""Retarget the template locomotion blend space and its referenced clips to Prince."""

import unreal


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing required asset: {}".format(path))
    return asset


source_blend_space_path = "/Game/Characters/Mannequins/Anims/Unarmed/BS_Idle_Walk_Run"
source_blend_space = load(source_blend_space_path)
source_mesh = load("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
target_mesh = load("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
retargeter = load("/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
source_data = registry.get_asset_by_object_path(source_blend_space.get_path_name())
if not source_data.is_valid():
    raise RuntimeError("Could not resolve asset registry data for locomotion blend space")

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.prefix = "POH_"
inputs.target_path = "/Game/_Sandbox/Animation/RetargetedTemplate"
inputs.include_referenced_assets = True
inputs.overwrite_existing_files = True

results = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if not results:
    raise RuntimeError("Locomotion retarget produced no assets")

if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True):
    raise RuntimeError("Could not save retargeted locomotion assets")

unreal.log_warning("POH: retargeted {} template locomotion assets".format(len(results)))
