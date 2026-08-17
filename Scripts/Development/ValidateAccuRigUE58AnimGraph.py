"""Technical validation of the isolated AccuRIG UE5.8 AnimBP.

This validates skeleton binding and package dependencies only; visual animation
review remains a human step.
"""

import unreal


BLUEPRINT = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58"
EXPECTED_SKELETON = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig_Skeleton"
RETARGETED_ROOT = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/"
SOURCE_ROOT = "/Game/Characters/Mannequins/Anims/Unarmed/"

bp = unreal.load_asset(BLUEPRINT)
expected_skeleton = unreal.load_asset(EXPECTED_SKELETON)
if not bp or not expected_skeleton:
    raise RuntimeError("Missing AnimBP or AccuRIG skeleton")

if bp.get_editor_property("target_skeleton") != expected_skeleton:
    raise RuntimeError("AnimBP is not bound to the AccuRIG skeleton")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
options = unreal.AssetRegistryDependencyOptions(
    include_hard_package_references=True,
    include_soft_package_references=True,
    include_hard_management_references=False,
    include_soft_management_references=False,
    include_searchable_names=False,
)
dependencies = [str(item) for item in registry.get_dependencies(unreal.Name(BLUEPRINT), options)]
target_dependencies = [item for item in dependencies if RETARGETED_ROOT in item]
source_dependencies = [item for item in dependencies if SOURCE_ROOT in item]
if source_dependencies:
    raise RuntimeError("AnimBP still references Manny source animations: {}".format(source_dependencies))
if not target_dependencies:
    raise RuntimeError("AnimBP has no AccuRIG retargeted animation dependencies")

unreal.log_warning("POH_ANIMGRAPH_VALIDATE_OK target_refs={} total_refs={}".format(
    len(target_dependencies), len(dependencies)
))
