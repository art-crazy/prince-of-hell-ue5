"""Report the runtime-relevant visual transform of the Prince pawn."""

import unreal


CHARACTER_PATH = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter"
MESH_PATH = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"
GAME_MODE_PATH = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonGameMode"


def _log(label, value):
    unreal.log_warning("POH VISUAL {}: {}".format(label, value))


character = unreal.load_asset(CHARACTER_PATH)
hero_mesh = unreal.load_asset(MESH_PATH)
game_mode = unreal.load_asset(GAME_MODE_PATH)

if not character or not hero_mesh or not game_mode:
    raise RuntimeError("Prince character Blueprint, skeletal mesh, or game mode was not found")

cdo = unreal.get_default_object(character.generated_class())
game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
_log("game_mode_default_pawn", game_mode_cdo.get_editor_property("default_pawn_class"))
for game_mode_path in ("/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode", GAME_MODE_PATH):
    mode = unreal.load_asset(game_mode_path)
    mode_cdo = unreal.get_default_object(mode.generated_class())
    _log("mode {} pawn".format(game_mode_path), mode_cdo.get_editor_property("default_pawn_class"))
    _log("mode {} controller".format(game_mode_path), mode_cdo.get_editor_property("player_controller_class"))
mesh_component = cdo.get_component_by_class(unreal.SkeletalMeshComponent)

_log("mesh_asset", mesh_component.get_editor_property("skeletal_mesh_asset").get_path_name())
_log("relative_location", mesh_component.get_editor_property("relative_location"))
_log("relative_rotation", mesh_component.get_editor_property("relative_rotation"))
_log("relative_scale", mesh_component.get_editor_property("relative_scale3d"))
_log("visible", mesh_component.get_editor_property("visible"))
_log("hidden_in_game", mesh_component.get_editor_property("hidden_in_game"))
_log("owner_no_see", mesh_component.get_editor_property("owner_no_see"))
_log("only_owner_see", mesh_component.get_editor_property("only_owner_see"))
_log("bounds_scale", mesh_component.get_editor_property("bounds_scale"))
_log("animation_mode", mesh_component.get_editor_property("animation_mode"))
_log("anim_class", mesh_component.get_editor_property("anim_class"))

spring_arm = cdo.get_component_by_class(unreal.SpringArmComponent)
camera = cdo.get_component_by_class(unreal.CameraComponent)
if spring_arm:
    _log("spring_arm_length", spring_arm.get_editor_property("target_arm_length"))
    _log("spring_arm_relative_location", spring_arm.get_editor_property("relative_location"))
    _log("spring_arm_relative_rotation", spring_arm.get_editor_property("relative_rotation"))
    _log("spring_arm_use_control_rotation", spring_arm.get_editor_property("use_pawn_control_rotation"))
if camera:
    _log("camera_relative_location", camera.get_editor_property("relative_location"))
    _log("camera_relative_rotation", camera.get_editor_property("relative_rotation"))
    _log("camera_use_control_rotation", camera.get_editor_property("use_pawn_control_rotation"))

for blueprint_path in (
    "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter",
    "/Game/Variant_Combat/Blueprints/BP_CombatCharacter",
    CHARACTER_PATH,
):
    blueprint = unreal.load_asset(blueprint_path)
    blueprint_cdo = unreal.get_default_object(blueprint.generated_class())
    _log("class {}".format(blueprint_path), blueprint.generated_class().get_path_name())
    components = blueprint_cdo.get_components_by_class(unreal.ActorComponent)
    _log(
        "components {}".format(blueprint_path),
        ["{}:{}".format(component.get_name(), component.get_class().get_name()) for component in components],
    )

try:
    _log("mesh_bounds", hero_mesh.get_bounds())
except Exception as exc:
    _log("mesh_bounds_unavailable", exc)

unreal.log_warning("POH VISUAL INSPECTION COMPLETE")
