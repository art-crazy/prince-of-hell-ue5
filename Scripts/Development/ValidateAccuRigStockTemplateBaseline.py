"""Technical checks for the stock Third Person + AccuRIG baseline."""

import unreal


MAP = "/Game/ThirdPerson/Lvl_ThirdPerson"
GAME_MODE = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"
CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigRestPose"
MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing: " + path)
    return asset


game_mode = require(GAME_MODE)
character = require(CHARACTER)
mesh_asset = require(MESH)
require(MAP)
game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
character_cdo = unreal.get_default_object(character.generated_class())
mesh = character_cdo.get_component_by_class(unreal.SkeletalMeshComponent)

if game_mode_cdo.get_editor_property("default_pawn_class") != character.generated_class():
    raise RuntimeError("Stock game mode is not using the isolated AccuRIG pawn")
if mesh.get_editor_property("skeletal_mesh_asset") != mesh_asset:
    raise RuntimeError("Baseline pawn mesh changed")
if mesh.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_SINGLE_NODE:
    raise RuntimeError("Baseline pawn must not use an AnimBP")
if mesh.get_editor_property("animation_data").anim_to_play:
    raise RuntimeError("Baseline pawn must use native AccuRIG rest pose")

unreal.log_warning("POH_STOCK_TEMPLATE_BASELINE_VALIDATE_OK map={} pawn={}".format(MAP, CHARACTER))
