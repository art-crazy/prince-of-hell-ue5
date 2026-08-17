"""Create isolated AccuRIG Character + Animation Blueprint foundation.

No active map, game mode or working character is changed.  This removes the
old Single Node dependency from the new production path before states and Foot
IK are added.
"""

import unreal


FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation"
SOURCE_CHARACTER = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
TARGET_CHARACTER = FOLDER + "/BP_POH_AccuRigCharacter"
TARGET_ANIMBP = FOLDER + "/ABP_POH_AccuRig_UE58"
TARGET_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


mesh_asset = require(TARGET_MESH)
character_bp = unreal.load_asset(TARGET_CHARACTER)
if not character_bp:
    character_bp = unreal.EditorAssetLibrary.duplicate_asset(SOURCE_CHARACTER, TARGET_CHARACTER)
if not character_bp:
    raise RuntimeError("Unable to create Prince Character Blueprint")

anim_bp = require(TARGET_ANIMBP)
if anim_bp.get_editor_property("target_skeleton") != mesh_asset.get_editor_property("skeleton"):
    raise RuntimeError("Production AnimBP is not bound to the AccuRIG skeleton")

cdo = unreal.get_default_object(character_bp.generated_class())
mesh = cdo.get_editor_property("mesh")
mesh.set_skeletal_mesh(mesh_asset)
mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
mesh.set_editor_property("anim_class", anim_bp.generated_class())

movement = cdo.get_editor_property("character_movement")
movement.set_editor_property("max_walk_speed", 260.0)
movement.set_editor_property("max_walk_speed_crouched", 140.0)

unreal.BlueprintEditorLibrary.compile_blueprint(anim_bp)
unreal.BlueprintEditorLibrary.compile_blueprint(character_bp)
for asset in (anim_bp, character_bp):
    if not unreal.EditorAssetLibrary.save_asset(asset.get_path_name(), only_if_is_dirty=False):
        raise RuntimeError("Unable to save: " + asset.get_path_name())

unreal.log_warning("POH_ANIMBP_FOUNDATION_READY character={} animbp={} skeleton={}".format(
    character_bp.get_path_name(), anim_bp.get_path_name(), mesh_asset.get_editor_property("skeleton").get_path_name()
))
