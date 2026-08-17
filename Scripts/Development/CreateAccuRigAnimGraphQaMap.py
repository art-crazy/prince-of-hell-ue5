"""Create an isolated playable map for the AccuRIG UE5.8 AnimBP.

The established third-person map and the historical single-node pawn are left
unchanged. This map is the only place where the new AnimBP becomes playable.
"""

import unreal


SOURCE_GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"
SOURCE_MAP = "/Game/ThirdPerson/Lvl_ThirdPerson"
FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation"
GAME_MODE = FOLDER + "/GM_POH_AccuRigAnimGraph"
MAP = FOLDER + "/Lvl_POH_AccuRigAnimGraph_QA"
CHARACTER = FOLDER + "/BP_POH_AccuRigCharacter"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


source_game_mode = require(SOURCE_GAME_MODE)
character = require(CHARACTER)
game_mode = unreal.load_asset(GAME_MODE)
if not game_mode:
    game_mode = unreal.EditorAssetLibrary.duplicate_asset(SOURCE_GAME_MODE, GAME_MODE)
if not game_mode:
    raise RuntimeError("Could not create isolated Prince game mode")

game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
source_cdo = unreal.get_default_object(source_game_mode.generated_class())
game_mode_cdo.set_editor_property("default_pawn_class", character.generated_class())
game_mode_cdo.set_editor_property("player_controller_class", source_cdo.get_editor_property("player_controller_class"))
unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
if not unreal.EditorAssetLibrary.save_asset(GAME_MODE, only_if_is_dirty=False):
    raise RuntimeError("Could not save isolated Prince game mode")

if not unreal.EditorAssetLibrary.does_asset_exist(MAP):
    if not unreal.EditorAssetLibrary.duplicate_asset(SOURCE_MAP, MAP):
        raise RuntimeError("Could not duplicate isolated AnimBP QA map")

if not unreal.EditorLoadingAndSavingUtils.load_map(MAP):
    raise RuntimeError("Could not load isolated AnimBP QA map")
world = unreal.EditorLevelLibrary.get_editor_world()
if not world:
    raise RuntimeError("No editor world after loading isolated map")
world.get_world_settings().set_editor_property("default_game_mode", game_mode.generated_class())

if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True):
    raise RuntimeError("Could not save isolated AnimBP QA map")

unreal.log_warning("POH_ANIMGRAPH_QA_READY map={} gamemode={} pawn={}".format(MAP, GAME_MODE, CHARACTER))
