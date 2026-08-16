"""Make the validated template-derived Prince character the project's playable pawn."""

import unreal


SOURCE_GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"
TARGET_GAME_MODE = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonGameMode"
PRINCE_CHARACTER = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter"

source = unreal.load_asset(SOURCE_GAME_MODE)
character = unreal.load_asset(PRINCE_CHARACTER)
if not source or not character:
    raise RuntimeError("Template game mode or Prince character blueprint is unavailable")

game_mode = unreal.load_asset(TARGET_GAME_MODE)
if not game_mode:
    game_mode = unreal.EditorAssetLibrary.duplicate_asset(SOURCE_GAME_MODE, TARGET_GAME_MODE)
if not game_mode:
    raise RuntimeError("Could not create Prince template game mode")

game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
game_mode_cdo.set_editor_property("default_pawn_class", character.generated_class())

unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
if not unreal.EditorAssetLibrary.save_asset(TARGET_GAME_MODE, only_if_is_dirty=False):
    raise RuntimeError("Could not save Prince template game mode")

unreal.log_warning("POH: configured template game mode to spawn Prince")
