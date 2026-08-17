"""Export only UE's original Manny mesh; never export the Tripo mesh here.

The old mixed exporter could hit a skin-cache assertion while serializing the
Tripo mesh.  Manny alone is stable and gives Blender the exact UE hierarchy.
"""

import os
import unreal


MESH_PATH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
OUTPUT = r"C:\Users\artcr\Documents\Unreal Projects\test\Saved\ReskinPipeline\Manny_ExactUE58.fbx"

mesh = unreal.load_asset(MESH_PATH)
if not mesh:
    raise RuntimeError("Manny skeletal mesh is unavailable")
os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
task = unreal.AssetExportTask()
task.object = mesh
task.filename = OUTPUT
task.automated = True
task.replace_identical = True
task.prompt = False
task.exporter = unreal.SkeletalMeshExporterFBX()
if not unreal.Exporter.run_asset_export_task(task):
    raise RuntimeError("Manny FBX export failed")
if not os.path.exists(OUTPUT) or os.path.getsize(OUTPUT) < 1024:
    raise RuntimeError("Manny FBX export produced no usable file")
unreal.log_warning("POH_MANNY_EXACT_EXPORT PASS {} bytes={}".format(OUTPUT, os.path.getsize(OUTPUT)))
