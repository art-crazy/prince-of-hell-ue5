"""Apply the validated native Tripo Prince mesh and idle clip to UE's pawn."""

import unreal


TEMPLATE_CHARACTER = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
PRINCE_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"
PRINCE_ANIMATION = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripoidle"
TARGET_VISUAL_HEIGHT_CM = 175.0
# Imported bounds can include dangling cloth below the soles.  A tiny overlap is
# preferable to visible hovering and remains safely inside the floor collision.
VISUAL_SOLE_OVERLAP_CM = 3.0


def calculate_mesh_placement(mesh_asset, capsule):
    """Fit any Tripo re-export to the template capsule without magic offsets."""
    bounds = mesh_asset.get_bounds()
    minimum_z = bounds.origin.z - bounds.box_extent.z
    maximum_z = bounds.origin.z + bounds.box_extent.z
    source_height = maximum_z - minimum_z
    if source_height <= 0.0:
        raise RuntimeError("Native Tripo mesh has invalid vertical bounds")

    scale = TARGET_VISUAL_HEIGHT_CM / source_height
    capsule_half_height = capsule.get_editor_property("capsule_half_height")
    # Character origin is capsule centre; move the mesh so its scaled minimum
    # touches the capsule bottom, i.e. the walkable floor.
    location_z = -capsule_half_height - minimum_z * scale - VISUAL_SOLE_OVERLAP_CM
    return location_z, scale


character = unreal.load_asset(TEMPLATE_CHARACTER)
mesh_asset = unreal.load_asset(PRINCE_MESH)
animation = unreal.load_asset(PRINCE_ANIMATION)
if not character or not mesh_asset or not animation:
    raise RuntimeError("Template character, Prince mesh, or test animation is unavailable")

cdo = unreal.get_default_object(character.generated_class())
mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
capsule = cdo.get_component_by_class(unreal.CapsuleComponent)
if not mesh or not capsule:
    raise RuntimeError("Third Person template character has no mesh or capsule component")

location_z, uniform_scale = calculate_mesh_placement(mesh_asset, capsule)
mesh.set_editor_property("skeletal_mesh_asset", mesh_asset)
mesh.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, location_z))
# UE Python's positional Rotator arguments are roll, pitch, yaw.  Use keywords:
# the former positional call assigned -90 degrees to pitch and laid Prince down.
mesh.set_editor_property(
    "relative_rotation",
    unreal.Rotator(pitch=0.0, yaw=-90.0, roll=0.0),
)
mesh.set_editor_property("relative_scale3d", unreal.Vector(uniform_scale, uniform_scale, uniform_scale))
mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_SINGLE_NODE)
mesh.set_editor_property(
    "animation_data",
    unreal.SingleAnimationPlayData(
        anim_to_play=animation,
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

unreal.log_warning(
    f"POH: Prince applied with mesh Z={location_z:.2f}, scale={uniform_scale:.4f}"
)
