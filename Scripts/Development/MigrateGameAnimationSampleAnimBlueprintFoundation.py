"""Migrate the UE5.8 Game Animation Sample AnimBP foundation for adaptation.

Run against GameAnimationSample.uproject.  This imports the generic retarget
graph and the Manny reference character into an isolated library.  It never
changes the playable Prince pawn or any project defaults.
"""

import unreal


DESTINATION_CONTENT = r"C:\Users\artcr\Documents\Unreal Projects\test\Content"
PACKAGE_NAMES = (
    "/Game/Blueprints/RetargetedCharacters/ABP_GenericRetarget",
    "/Game/Blueprints/RetargetedCharacters/BP_Manny",
)

registry = unreal.AssetRegistryHelpers.get_asset_registry()
packages = []
for package_name in PACKAGE_NAMES:
    asset_name = package_name.rsplit("/", 1)[-1]
    data = registry.get_asset_by_object_path(unreal.Name(package_name + "." + asset_name))
    if not data.is_valid():
        raise RuntimeError("Missing Game Animation Sample foundation asset: " + package_name)
    packages.append(str(data.package_name))

unreal.log_warning("POH_GAS_ANIMBP_MIGRATE count={}".format(len(packages)))
unreal.AssetToolsHelpers.get_asset_tools().migrate_packages(packages, DESTINATION_CONTENT)
unreal.log_warning("POH_GAS_ANIMBP_MIGRATE_COMPLETE")
