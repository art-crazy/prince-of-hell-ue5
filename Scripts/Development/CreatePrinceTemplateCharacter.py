import unreal

SOURCE_BLUEPRINT = "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"
TARGET_BLUEPRINT = "/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter"
HERO_MESH = "/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig"

source = unreal.load_asset(SOURCE_BLUEPRINT)
hero_mesh = unreal.load_asset(HERO_MESH)
if not source or not hero_mesh:
    raise RuntimeError("Template character or Prince mesh is unavailable")

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

# Do not replace the template's input, camera, collision or animation state-machine here.
# The retargeted Animation Blueprint is the next atomic change.
unreal.BlueprintEditorLibrary.compile_blueprint(target)
if not unreal.EditorAssetLibrary.save_asset(TARGET_BLUEPRINT, only_if_is_dirty=False):
    raise RuntimeError("Could not save Prince third-person character blueprint")

unreal.log_warning("POH: created template-derived Prince character blueprint")
