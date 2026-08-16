"""Apply Prince's correctly-oriented reference pose to UE's Third Person pawn.

The first Game Animation Sample retarget pass is deliberately excluded: all of
its tested clips rotate the Tripo skeleton onto the ground.  The base mesh is
already Z-up, so an animation-free reference pose is the safe playable fallback
until a dedicated IK Retargeter profile is authored.
"""

import unreal


TEMPLATE_CHARACTER = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
PRINCE_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"


character = unreal.load_asset(TEMPLATE_CHARACTER)
mesh_asset = unreal.load_asset(PRINCE_MESH)
if not character or not mesh_asset:
    raise RuntimeError("Template character or Prince mesh is unavailable")

cdo = unreal.get_default_object(character.generated_class())
mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh:
    raise RuntimeError("Third Person template character has no skeletal mesh component")

# The imported model is 100 cm high; the template uses a 192 cm capsule.
mesh.set_editor_property("skeletal_mesh_asset", mesh_asset)
mesh.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, -96.0))
mesh.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))
mesh.set_editor_property("relative_scale3d", unreal.Vector(1.75, 1.75, 1.75))
# Do not assign any current POH retargeted clip here.  Their root bone rotates
# this skeleton onto the ground; with no clip Unreal displays the mesh's Z-up
# reference pose, which is the only verified correct orientation.
mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mesh.set_editor_property(
    "animation_data",
    unreal.SingleAnimationPlayData(
        anim_to_play=None,
        saved_looping=True,
        saved_playing=True,
        saved_position=0.0,
        saved_play_rate=1.0,
    ),
)
mesh.set_editor_property("anim_class", None)
mesh.set_editor_property("owner_no_see", False)
mesh.set_editor_property("hidden_in_game", False)

unreal.BlueprintEditorLibrary.compile_blueprint(character)
if not unreal.EditorAssetLibrary.save_asset(TEMPLATE_CHARACTER, only_if_is_dirty=False):
    raise RuntimeError("Could not save the updated Third Person template character")

unreal.log_warning("POH: Prince applied to UE 5.8 Third Person template character")
