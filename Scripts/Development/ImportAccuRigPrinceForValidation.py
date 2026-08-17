"""Import the audited locally converted AccuRIG Prince into an isolated UE path.

Run with UnrealEditor-Cmd only while the interactive editor is closed.  This
script deliberately does not alter the playable NativeTripo character or its
Animation Blueprint.
"""

import unreal


SOURCE = r"C:\Users\artcr\Documents\Unreal Projects\test\Saved\AccuRig\Export\POH_Prince_AccuRig_Final.fbx"
DESTINATION = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig"
NAME = "SK_POHPrince_AccuRig"


task = unreal.AssetImportTask()
task.filename = SOURCE
task.destination_path = DESTINATION
task.destination_name = NAME
task.automated = True
task.replace_existing = False
task.save = True

options = unreal.FbxImportUI()
options.automated_import_should_detect_type = False
options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
options.import_mesh = True
options.import_as_skeletal = True
options.import_animations = False
options.import_materials = True
options.import_textures = True
task.options = options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
mesh = unreal.load_asset(DESTINATION + "/" + NAME)
if not mesh:
    raise RuntimeError("AccuRIG Prince import failed")

skeleton = mesh.get_editor_property("skeleton")
bone_names = [str(name) for name in skeleton.get_reference_pose().get_bone_names()]
for required in ("pelvis", "hand_l", "hand_r", "foot_l", "foot_r"):
    if required not in bone_names:
        raise RuntimeError("Imported AccuRIG skeleton is missing required bone: " + required)

unreal.EditorAssetLibrary.save_asset(mesh.get_path_name())
unreal.log_warning("POH_ACCURIG_IMPORT_READY mesh={} bones={}".format(mesh.get_path_name(), len(bone_names)))
