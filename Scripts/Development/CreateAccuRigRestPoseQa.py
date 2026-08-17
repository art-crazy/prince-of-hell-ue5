"""Create a minimal, well-lit AccuRIG character QA map.

This deliberately uses the native AccuRIG reference pose, not an imported
animation or an AnimBP.  It is the visual baseline before every retargeting
change: if this map is wrong, the problem is mesh/placement; if it is right,
the next single clip is the only variable under test.
"""

import unreal


SOURCE_MAP = "/Game/ThirdPerson/Lvl_ThirdPerson"
SOURCE_GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"
SOURCE_CHARACTER = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation"
MAP = FOLDER + "/Lvl_POH_AccuRig_RestPose_QA"
GAME_MODE = FOLDER + "/GM_POH_AccuRigRestPose"
CHARACTER = FOLDER + "/BP_POH_AccuRigRestPose"
MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"

TARGET_VISUAL_HEIGHT_CM = 175.0
VISUAL_SOLE_OVERLAP_CM = 3.0


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


def duplicate_if_needed(source, target):
    asset = unreal.load_asset(target)
    if asset:
        return asset
    asset = unreal.EditorAssetLibrary.duplicate_asset(source, target)
    if not asset:
        raise RuntimeError("Could not create: " + target)
    return asset


mesh_asset = require(MESH)
source_game_mode = require(SOURCE_GAME_MODE)
character = duplicate_if_needed(SOURCE_CHARACTER, CHARACTER)
game_mode = duplicate_if_needed(SOURCE_GAME_MODE, GAME_MODE)

character_cdo = unreal.get_default_object(character.generated_class())
mesh_component = character_cdo.get_component_by_class(unreal.SkeletalMeshComponent)
capsule = character_cdo.get_component_by_class(unreal.CapsuleComponent)
if not mesh_component or not capsule:
    raise RuntimeError("Template pawn has no mesh or capsule")

bounds = mesh_asset.get_bounds()
minimum_z = bounds.origin.z - bounds.box_extent.z
maximum_z = bounds.origin.z + bounds.box_extent.z
source_height = maximum_z - minimum_z
if source_height <= 0.0:
    raise RuntimeError("AccuRIG mesh has invalid bounds")
scale = TARGET_VISUAL_HEIGHT_CM / source_height
location_z = -capsule.get_editor_property("capsule_half_height") - minimum_z * scale - VISUAL_SOLE_OVERLAP_CM

mesh_component.set_editor_property("skeletal_mesh_asset", mesh_asset)
mesh_component.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, location_z))
# The stock UE Third Person Character faces its gameplay-forward direction at
# -90 degrees yaw.  Keep this template contract for every replacement mesh;
# otherwise locomotion is visually rotated while movement remains correct.
mesh_component.set_editor_property("relative_rotation", unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0))
mesh_component.set_editor_property("relative_scale3d", unreal.Vector(scale, scale, scale))
mesh_component.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mesh_component.set_editor_property("animation_data", unreal.SingleAnimationPlayData(
    anim_to_play=None, saved_looping=False, saved_playing=False, saved_position=0.0, saved_play_rate=1.0
))
mesh_component.set_editor_property("anim_class", None)
mesh_component.set_editor_property("hidden_in_game", False)
mesh_component.set_editor_property("owner_no_see", False)
mesh_component.set_editor_property("cast_hidden_shadow", True)

movement = character_cdo.get_editor_property("character_movement")
movement.set_editor_property("max_walk_speed", 500.0)
movement.set_editor_property("max_walk_speed_crouched", 140.0)

source_gm_cdo = unreal.get_default_object(source_game_mode.generated_class())
game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
game_mode_cdo.set_editor_property("default_pawn_class", character.generated_class())
game_mode_cdo.set_editor_property("player_controller_class", source_gm_cdo.get_editor_property("player_controller_class"))

unreal.BlueprintEditorLibrary.compile_blueprint(character)
unreal.BlueprintEditorLibrary.compile_blueprint(game_mode)
for asset in (character, game_mode):
    if not unreal.EditorAssetLibrary.save_asset(asset.get_path_name(), only_if_is_dirty=False):
        raise RuntimeError("Could not save: " + asset.get_path_name())

if not unreal.EditorAssetLibrary.does_asset_exist(MAP):
    duplicate_if_needed(SOURCE_MAP, MAP)
if not unreal.EditorLoadingAndSavingUtils.load_map(MAP):
    raise RuntimeError("Could not load QA map")
world = unreal.EditorLevelLibrary.get_editor_world()
world.get_world_settings().set_editor_property("default_game_mode", game_mode.generated_class())
if not unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True):
    raise RuntimeError("Could not save QA map")

unreal.log_warning("POH_RESTPOSE_QA_READY map={} mesh_z={:.3f} scale={:.6f}".format(MAP, location_z, scale))
