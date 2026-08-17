"""Technical validation for the isolated AccuRIG AnimBP QA map."""

import unreal


MAP = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/Lvl_POH_AccuRigAnimGraph_QA"
GAME_MODE = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/GM_POH_AccuRigAnimGraph"
CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigCharacter"
ANIMBP = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58"

for path in (MAP, GAME_MODE, CHARACTER, ANIMBP):
    if not unreal.load_asset(path):
        raise RuntimeError("Missing required QA asset: " + path)

game_mode = unreal.load_asset(GAME_MODE)
character = unreal.load_asset(CHARACTER)
anim_bp = unreal.load_asset(ANIMBP)
game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
character_cdo = unreal.get_default_object(character.generated_class())
mesh = character_cdo.get_editor_property("mesh")

if game_mode_cdo.get_editor_property("default_pawn_class") != character.generated_class():
    raise RuntimeError("QA game mode does not use the isolated AccuRIG character")
if mesh.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_BLUEPRINT:
    raise RuntimeError("QA character is not in Animation Blueprint mode")
if mesh.get_editor_property("anim_class") != anim_bp.generated_class():
    raise RuntimeError("QA character is not assigned the AccuRIG UE58 AnimBP")

unreal.log_warning("POH_ANIMGRAPH_QA_VALIDATE_OK map={} pawn={} animbp={}".format(MAP, CHARACTER, ANIMBP))
