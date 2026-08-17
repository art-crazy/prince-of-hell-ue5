"""Migrate a compact, reusable Game Animation Sample movement source set.

Run against GameAnimationSample.uproject.  The target is only a source library;
every clip is retargeted to the Prince's AccuRIG skeleton in the test project.
"""

import unreal


DESTINATION_CONTENT = r"C:\Users\artcr\Documents\Unreal Projects\test\Content"
ASSET_NAMES = {
    "M_Neutral_Crouch_Idle_Loop",
    "M_Neutral_Transition_Stand_to_Crouch",
    "M_Neutral_Transition_Crouch_to_Stand",
    "M_Neutral_Jump_F_Land_Roll_Lfoot",
    "M_Neutral_Jump_F_Land_Roll_Rfoot",
}

registry = unreal.AssetRegistryHelpers.get_asset_registry()
existing = []
for asset in registry.get_all_assets():
    if str(asset.asset_class_path.asset_name) != "AnimSequence":
        continue
    if str(asset.asset_name) in ASSET_NAMES:
        existing.append(str(asset.package_name))
missing = sorted(ASSET_NAMES - {path.rsplit("/", 1)[-1] for path in existing})
if missing:
    raise RuntimeError("Missing Game Animation Sample packages: {}".format(missing))

unreal.log_warning("POH_GAS_MIGRATE {} packages".format(len(existing)))
unreal.AssetToolsHelpers.get_asset_tools().migrate_packages(existing, DESTINATION_CONTENT)
unreal.log_warning("POH_GAS_MIGRATE_COMPLETE")
