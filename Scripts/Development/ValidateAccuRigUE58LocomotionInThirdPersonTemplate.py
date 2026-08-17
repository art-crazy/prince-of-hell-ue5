"""Technical validation for UE5.8 locomotion in the stock Third Person map."""

import unreal


MAP = "/Game/ThirdPerson/Lvl_ThirdPerson"
CHARACTER = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/BP_POH_AccuRigRestPose"
ANIM_BP = "/Game/_Sandbox/Characters/PrinceOfHell/ProductionAnimation/ABP_POH_AccuRig_UE58"
MESH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"
EXPECTED = (
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MM_Idle",
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MF_Unarmed_Walk_Fwd",
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MF_Unarmed_Jog_Fwd",
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MM_Jump",
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MM_Fall_Loop",
    "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedUE58_ABP/UE58_MM_Land",
)


def require(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing: " + path)
    return asset


require(MAP)
character = require(CHARACTER)
anim_bp = require(ANIM_BP)
mesh_asset = require(MESH)
for path in EXPECTED:
    clip = require(path)
    if clip.get_editor_property("skeleton") != mesh_asset.get_editor_property("skeleton"):
        raise RuntimeError("Wrong target skeleton: " + path)

cdo = unreal.get_default_object(character.generated_class())
mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if mesh.get_editor_property("skeletal_mesh_asset") != mesh_asset:
    raise RuntimeError("Pawn mesh changed")
if mesh.get_editor_property("animation_mode") != unreal.AnimationMode.ANIMATION_BLUEPRINT:
    raise RuntimeError("Pawn is not in Animation Blueprint mode")
if mesh.get_editor_property("anim_class") != anim_bp.generated_class():
    raise RuntimeError("Pawn uses the wrong locomotion AnimBP")
rotation = mesh.get_editor_property("relative_rotation")
if abs(rotation.yaw + 90.0) > 0.01:
    raise RuntimeError("Pawn mesh is not aligned to UE Third Person forward")
movement = cdo.get_editor_property("character_movement")
if movement.get_editor_property("max_walk_speed") < 500.0:
    raise RuntimeError("Pawn speed cannot reach authored run samples")
if any(str(tag) == "POHRuntimeSingleNode" for tag in cdo.get_editor_property("tags")):
    raise RuntimeError("Legacy runtime animation override is enabled on production pawn")

unreal.log_warning("POH_UE58_LOCOMOTION_VALIDATE_OK pawn={} clips={}".format(CHARACTER, len(EXPECTED)))
