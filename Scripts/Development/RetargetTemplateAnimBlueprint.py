"""Retarget the UE Third Person template's locomotion Anim Blueprint to Prince."""

import unreal


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing required asset: {}".format(path))
    return asset


source_blueprint = load("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed")
source_mesh = load("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
target_mesh = load("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
retargeter = load("/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
source_data = registry.get_asset_by_object_path(source_blueprint.get_path_name())
if not source_data.is_valid():
    raise RuntimeError("Could not resolve source animation blueprint")

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = [source_data]
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.prefix = "POH_"
inputs.target_path = "/Game/_Sandbox/Animation/RetargetedTemplateAligned"
inputs.include_referenced_assets = True
inputs.overwrite_existing_files = True

results = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if not results:
    raise RuntimeError("Animation Blueprint retarget produced no assets")

if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(False, True):
    raise RuntimeError("Could not save retargeted animation assets")

unreal.log_warning("POH: retargeted template Anim Blueprint and {} assets".format(len(results)))
