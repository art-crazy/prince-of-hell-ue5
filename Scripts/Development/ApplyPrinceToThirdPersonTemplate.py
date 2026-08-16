"""Replace only the visual/animation layer of UE 5.8's ready Third Person pawn."""

import unreal


TEMPLATE_CHARACTER = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
PRINCE_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"
PRINCE_ANIM = "/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_ABP_Unarmed"


character = unreal.load_asset(TEMPLATE_CHARACTER)
mesh_asset = unreal.load_asset(PRINCE_MESH)
anim_blueprint = unreal.load_asset(PRINCE_ANIM)
if not character or not mesh_asset or not anim_blueprint:
    raise RuntimeError("Template character, Prince mesh, or retargeted animation Blueprint is unavailable")

cdo = unreal.get_default_object(character.generated_class())
mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh:
    raise RuntimeError("Third Person template character has no skeletal mesh component")

# The imported model is 100 cm high; the template uses a 192 cm capsule.
mesh.set_editor_property("skeletal_mesh_asset", mesh_asset)
mesh.set_editor_property("relative_location", unreal.Vector(0.0, 0.0, -96.0))
mesh.set_editor_property("relative_rotation", unreal.Rotator(0.0, -90.0, 0.0))
mesh.set_editor_property("relative_scale3d", unreal.Vector(1.75, 1.75, 1.75))
mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
mesh.set_editor_property("anim_class", anim_blueprint.generated_class())
mesh.set_editor_property("owner_no_see", False)
mesh.set_editor_property("hidden_in_game", False)

unreal.BlueprintEditorLibrary.compile_blueprint(character)
if not unreal.EditorAssetLibrary.save_asset(TEMPLATE_CHARACTER, only_if_is_dirty=False):
    raise RuntimeError("Could not save the updated Third Person template character")

unreal.log_warning("POH: Prince applied to UE 5.8 Third Person template character")
