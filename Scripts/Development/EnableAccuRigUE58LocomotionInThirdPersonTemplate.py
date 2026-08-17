"""Enable UE5.8's authored locomotion graph on the stock Third Person pawn.

The graph is a copied UE AnimBP whose sequence and blend-space references were
retargeted to the AccuRIG skeleton by ``RebindAccuRigUE58Graph``.  It owns idle,
walk/run, jump, fall and land states.  No legacy runtime animation system is
allowed to touch this pawn.
"""

import unreal


CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigRestPose"
ANIM_BP = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58"
MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: " + path)
    return asset


character = require(CHARACTER)
anim_bp = require(ANIM_BP)
mesh_asset = require(MESH)
if anim_bp.get_editor_property("target_skeleton") != mesh_asset.get_editor_property("skeleton"):
    raise RuntimeError("Locomotion AnimBP does not target the AccuRIG skeleton")

cdo = unreal.get_default_object(character.generated_class())
mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh:
    raise RuntimeError("Prince pawn has no SkeletalMeshComponent")

mesh.set_editor_property("skeletal_mesh_asset", mesh_asset)
mesh.set_editor_property("relative_rotation", unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0))
mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
mesh.set_editor_property("anim_class", anim_bp.generated_class())
# Clear old test playback data: only the authored state machine may supply pose.
mesh.set_editor_property("animation_data", unreal.SingleAnimationPlayData(
    anim_to_play=None, saved_looping=False, saved_playing=False, saved_position=0.0, saved_play_rate=1.0
))

# The legacy runtime subsystem is opt-in only.  Ensure this production pawn has
# no opt-in tag even if an old experimental asset was duplicated into it.
tags = list(cdo.get_editor_property("tags"))
cdo.set_editor_property("tags", [tag for tag in tags if str(tag) != "POHRuntimeSingleNode"])
if not any(str(tag) == "POHSprintControl" for tag in cdo.get_editor_property("tags")):
    cdo.set_editor_property("tags", list(cdo.get_editor_property("tags")) + [unreal.Name("POHSprintControl")])

movement = cdo.get_editor_property("character_movement")
# Match UE's third-person authored locomotion range.  The source Blend Space
# reaches its run samples above the old experimental 260 cm/s cap.
# W is a walk; Shift is handled by the movement-only runtime controller and
# raises it to the authored run range.  The AnimBP receives the real velocity.
movement.set_editor_property("max_walk_speed", 260.0)
movement.set_editor_property("max_walk_speed_crouched", 140.0)

unreal.BlueprintEditorLibrary.compile_blueprint(character)
if not unreal.EditorAssetLibrary.save_asset(character.get_path_name(), only_if_is_dirty=False):
    raise RuntimeError("Could not save: " + character.get_path_name())

unreal.log_warning("POH_UE58_LOCOMOTION_ENABLED pawn={} animbp={}".format(CHARACTER, ANIM_BP))
