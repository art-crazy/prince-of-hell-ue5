"""Duplicate UE's authored locomotion graph for the isolated AccuRIG AnimBP.

The graph is created in a new production asset. It is not assigned to a
playable map by this script; reference replacement and QA are separate steps.
"""

import unreal


SOURCE = "/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed"
TARGET = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58"
TARGET_SKELETON = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig_Skeleton"

source = unreal.load_asset(SOURCE)
target_skeleton = unreal.load_asset(TARGET_SKELETON)
if not source or not target_skeleton:
    raise RuntimeError("Source blueprint or AccuRIG skeleton is unavailable")

anim_bp = unreal.load_asset(TARGET)
if not anim_bp:
    anim_bp = unreal.EditorAssetLibrary.duplicate_asset(SOURCE, TARGET)
if not anim_bp:
    raise RuntimeError("Could not duplicate authored UE locomotion graph")

anim_bp.set_editor_property("target_skeleton", target_skeleton)
unreal.BlueprintEditorLibrary.compile_blueprint(anim_bp)
if not unreal.EditorAssetLibrary.save_asset(TARGET, only_if_is_dirty=False):
    raise RuntimeError("Could not save AccuRIG UE58 AnimBP")

unreal.log_warning("POH_UE58_ANIMGRAPH_CREATED asset={} graphs={}".format(
    TARGET, [graph.get_name() for graph in unreal.BlueprintEditorLibrary.list_graphs(anim_bp)]
))
