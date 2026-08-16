import unreal

SOURCE_BLUEPRINT = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
TARGET_BLUEPRINT = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter"
HERO_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"
HERO_ANIM_BLUEPRINT = "/Game/_Sandbox/Animation/RetargetedTemplateAligned/POH_ABP_Unarmed"
HERO_MESH_LOCATION = unreal.Vector(0.0, 0.0, -96.0)
HERO_MESH_ROTATION = unreal.Rotator(pitch=0.0, yaw=-90.0, roll=0.0)
# Tripo's imported character is 100 cm tall, while the UE third-person
# capsule is 192 cm.  This scale keeps the feet on the capsule base and
# fills the same readable framing as the template mannequin.
HERO_MESH_SCALE = unreal.Vector(1.75, 1.75, 1.75)

source = unreal.load_asset(SOURCE_BLUEPRINT)
hero_mesh = unreal.load_asset(HERO_MESH)
hero_anim_blueprint = unreal.load_asset(HERO_ANIM_BLUEPRINT)
if not source or not hero_mesh or not hero_anim_blueprint:
    raise RuntimeError("Template character, Prince mesh, or retargeted animation blueprint is unavailable")

target = unreal.load_asset(TARGET_BLUEPRINT)
if not target:
    target = unreal.EditorAssetLibrary.duplicate_asset(SOURCE_BLUEPRINT, TARGET_BLUEPRINT)
if not target:
    raise RuntimeError("Could not create Prince third-person character blueprint")

generated_class = target.generated_class()
cdo = unreal.get_default_object(generated_class)
mesh_component = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh_component:
    raise RuntimeError("Template character has no skeletal mesh component")

mesh_component.set_editor_property("skeletal_mesh_asset", hero_mesh)
mesh_component.set_editor_property("relative_location", HERO_MESH_LOCATION)
mesh_component.set_editor_property("relative_rotation", HERO_MESH_ROTATION)
mesh_component.set_editor_property("relative_scale3d", HERO_MESH_SCALE)
mesh_component.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
mesh_component.set_editor_property("anim_class", hero_anim_blueprint.generated_class())

# Camera, controls and collision remain inherited from UE's Third Person template.
unreal.BlueprintEditorLibrary.compile_blueprint(target)
if not unreal.EditorAssetLibrary.save_asset(TARGET_BLUEPRINT, only_if_is_dirty=False):
    raise RuntimeError("Could not save Prince third-person character blueprint")

unreal.log_warning("POH: created template-derived Prince character blueprint")
