"""Validate the Tripo-native locomotion package before runtime integration."""

import unreal


ROOT = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo"


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing native locomotion asset: {}".format(path))
    return asset


mesh = load(ROOT + "/SK_POHPrince_NativeTripo")
skeleton = mesh.get_editor_property("skeleton")
if not skeleton:
    raise RuntimeError("Native mesh has no skeleton")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
assets = registry.get_assets_by_path(ROOT, recursive=True, include_only_on_disk_assets=True)
animations = [
    unreal.load_asset(asset.package_name)
    for asset in assets
    if asset.asset_class_path.asset_name == "AnimSequence"
]

expected_tokens = ("fall", "idle", "jump", "run", "walk")
names = [asset.get_name().lower() for asset in animations if asset]
for token in expected_tokens:
    if not any(token in name for name in names):
        raise RuntimeError("Missing native Tripo '{}' animation; found {}".format(token, names))

if len(animations) != len(expected_tokens):
    raise RuntimeError("Expected exactly {} native clips, found {}: {}".format(
        len(expected_tokens), len(animations), names
    ))

for animation in animations:
    if animation.get_editor_property("skeleton") != skeleton:
        raise RuntimeError("Animation '{}' targets a different skeleton".format(animation.get_name()))

unreal.log_warning(
    "POH NATIVE LOCOMOTION VALIDATION PASSED: mesh={}, animations={}".format(
        mesh.get_path_name(),
        sorted(names),
    )
)
