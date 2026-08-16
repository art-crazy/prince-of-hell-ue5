"""Verify the complete playable Prince template hand-off without opening the editor."""

import unreal


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: {}".format(path))
    return asset


character = load("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
game_mode = load("/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode")
expected_mesh = load("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
expected_anim = load("/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_ABP_Unarmed")

character_cdo = unreal.get_default_object(character.generated_class())
mesh = character_cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh:
    raise RuntimeError("Prince character has no skeletal mesh component")
if mesh.get_editor_property("skeletal_mesh_asset") != expected_mesh:
    raise RuntimeError("Prince mesh is not assigned to the playable character")
if mesh.get_editor_property("anim_class") != expected_anim.generated_class():
    raise RuntimeError("Retargeted locomotion Anim Blueprint is not assigned")

game_mode_cdo = unreal.get_default_object(game_mode.generated_class())
if game_mode_cdo.get_editor_property("default_pawn_class") != character.generated_class():
    raise RuntimeError("The UE third-person game mode does not use its Prince-updated template pawn")

if not unreal.EditorLoadingAndSavingUtils.load_map("/Game/ThirdPerson/Lvl_ThirdPerson"):
    raise RuntimeError("Could not load template map for validation")
map_game_mode = unreal.EditorLevelLibrary.get_editor_world().get_world_settings().get_editor_property("default_game_mode")
if map_game_mode != game_mode.generated_class():
    raise RuntimeError("Template map override does not use the UE third-person game mode")

unreal.log_warning("POH PLAYABLE TEMPLATE VALIDATION PASSED")
