"""Import the validated native Tripo locomotion package in an isolated UE folder.

The package is deliberately not wired to gameplay here. Import and asset audit
must pass before it may replace the existing fallback animation source.
"""

import glob
import os

import unreal


source_root = os.path.join(unreal.Paths.project_saved_dir(), "TripoNativeLocomotion")
sources = glob.glob(os.path.join(source_root, "*.fbx"))
if len(sources) != 1:
    raise RuntimeError("Expected exactly one native locomotion FBX in {}".format(source_root))

destination = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo"
task = unreal.AssetImportTask()
task.filename = sources[0]
task.destination_path = destination
task.destination_name = "SK_POHPrince_NativeTripo"
task.automated = True
task.replace_existing = True
task.save = True

options = unreal.FbxImportUI()
options.import_mesh = True
options.import_as_skeletal = True
options.import_animations = True
options.import_materials = True
options.import_textures = True
task.options = options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
if not task.imported_object_paths:
    raise RuntimeError("Native locomotion import produced no assets")

for object_path in task.imported_object_paths:
    unreal.EditorAssetLibrary.save_asset(object_path, only_if_is_dirty=False)

unreal.log_warning("POH native locomotion import complete: {}".format(task.imported_object_paths))
