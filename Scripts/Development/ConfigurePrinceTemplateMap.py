"""Set the Third Person template map's explicit GameMode override to Prince."""

import unreal


MAP_PATH = "/Game/ThirdPerson/Lvl_ThirdPerson"
GAME_MODE_PATH = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"

game_mode = unreal.load_asset(GAME_MODE_PATH)
if not game_mode:
    raise RuntimeError("Missing Prince template game mode")

if not unreal.EditorLoadingAndSavingUtils.load_map(MAP_PATH):
    raise RuntimeError("Could not load template map")

world = unreal.EditorLevelLibrary.get_editor_world()
if not world:
    raise RuntimeError("No editor world after loading template map")

world_settings = world.get_world_settings()
world_settings.set_editor_property("default_game_mode", game_mode.generated_class())

if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True):
    raise RuntimeError("Could not save template map GameMode override")

unreal.log_warning("POH: template map now explicitly uses Prince game mode")
