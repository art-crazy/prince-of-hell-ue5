"""Retarget only UE 5.8's core locomotion/jump clips to the playable Prince.

The result is a clean source for a later state machine: no Control Rig, no
legacy TripoRig skeleton and no full-action Tripo clips forced into fall state.
"""

import unreal


RETARGETER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging/RTG_Manny_To_POHNative"
SOURCE_MESH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"
TARGET_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedManny"
SOURCE_ANIMATIONS = (
    "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Jump",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Fall_Loop",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Land",
)

retargeter = unreal.load_asset(RETARGETER)
source_mesh = unreal.load_asset(SOURCE_MESH)
target_mesh = unreal.load_asset(TARGET_MESH)
if not retargeter or not source_mesh or not target_mesh:
    raise RuntimeError("Native Prince retarget prerequisites are unavailable")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = []
for path in SOURCE_ANIMATIONS:
    asset_name = path.rsplit("/", 1)[-1]
    asset_data = registry.get_asset_by_object_path(unreal.Name(f"{path}.{asset_name}"))
    if not asset_data.is_valid():
        raise RuntimeError(f"Cannot find Manny animation: {path}")
    assets.append(asset_data)

inputs = unreal.IKRetargetBatchOperationInputs()
inputs.assets_to_retarget = assets
inputs.source_mesh = source_mesh
inputs.target_mesh = target_mesh
inputs.ik_retarget_asset = retargeter
inputs.target_path = TARGET_FOLDER
inputs.prefix = "POH_"
inputs.include_referenced_assets = False
inputs.overwrite_existing_files = True
outputs = unreal.IKRetargetBatchOperation.run_batch_retarget(inputs)
if len(outputs) != len(SOURCE_ANIMATIONS):
    raise RuntimeError(f"Retarget produced {len(outputs)} assets; expected {len(SOURCE_ANIMATIONS)}")

for output in outputs:
    if not unreal.EditorAssetLibrary.save_asset(str(output.package_name), only_if_is_dirty=False):
        raise RuntimeError(f"Unable to save retargeted animation: {output.package_name}")
    unreal.log_warning(f"POH_NATIVE_RETARGET_OUTPUT {output.package_name}")
