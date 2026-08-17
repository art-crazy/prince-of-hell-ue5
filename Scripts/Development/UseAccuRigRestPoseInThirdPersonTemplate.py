"""Use the stock UE Third Person map with an unmodified AccuRIG baseline.

No level is duplicated or assembled here.  The map keeps UE's authored
lighting, controller, camera, collision and player start; only its game mode's
default pawn is switched to the isolated Prince reference-pose character.
"""

import unreal


GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"
CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigRestPose"

game_mode = unreal.load_asset(GAME_MODE)
character = unreal.load_asset(CHARACTER)
if not game_mode or not character:
    raise RuntimeError("Stock game mode or AccuRIG baseline pawn is missing")

cdo = unreal.get_default_object(game_mode.generated_class())
cdo.set_editor_property("default_pawn_class", character.generated_class())
unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
if not unreal.EditorAssetLibrary.save_asset(GAME_MODE, only_if_is_dirty=False):
    raise RuntimeError("Could not save stock Third Person game mode")

unreal.log_warning("POH_STOCK_TEMPLATE_BASELINE_READY pawn={}".format(CHARACTER))
