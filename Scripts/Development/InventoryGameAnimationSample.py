"""Read-only inventory of Game Animation Sample motion assets.

Run this script against GameAnimationSample.uproject.  It deliberately only
reports source clips: the Prince receives them later through the existing
AccuRIG IK Retargeter, never by direct Manny assignment.
"""

import unreal


TERMS = (
    "mantle", "vault", "climb", "travers", "roll", "dodge", "slide",
    "crouch", "sprint", "jump", "land", "fall", "idle", "walk", "jog",
)

registry = unreal.AssetRegistryHelpers.get_asset_registry()
for asset in registry.get_all_assets():
    if str(asset.asset_class_path.asset_name) != "AnimSequence":
        continue
    path = str(asset.package_name)
    lower = path.lower()
    if any(term in lower for term in TERMS):
        unreal.log_warning("POH_GAS_SOURCE {}".format(path))
