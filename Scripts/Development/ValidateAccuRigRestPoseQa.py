"""Validate the minimal reference-pose QA map without visual inspection."""

import unreal


MAP = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/Lvl_POH_AccuRig_RestPose_QA"
GAME_MODE = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/GM_POH_AccuRigRestPose"
CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigRestPose"
MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


game_mode = require(GAME_MODE)
character = require(CHARACTER)
expected_mesh = require(MESH)
require(MAP)
game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
character_cdo = unreal.get_default_object(character.generated_class())
mesh = character_cdo.get_component_by_class(unreal.SkeletalMeshComponent)

if game_mode_cdo.get_editor_property("default_pawn_class") != character.generated_class():
    raise RuntimeError("QA game mode does not use the rest-pose character")
if mesh.get_editor_property("skeletal_mesh_asset") != expected_mesh:
    raise RuntimeError("QA character uses the wrong mesh")
if mesh.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_SINGLE_NODE:
    raise RuntimeError("QA character must not use an AnimBP")
if mesh.get_editor_property("animation_data").anim_to_play:
    raise RuntimeError("QA character must use the native AccuRIG rest pose")
if mesh.get_editor_property("anim_class"):
    raise RuntimeError("QA character must not have an AnimBP class")

unreal.log_warning("POH_RESTPOSE_QA_VALIDATE_OK map={} pawn={}".format(MAP, CHARACTER))
