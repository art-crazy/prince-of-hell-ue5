"""Import the user-supplied UE5-retargetable warrior as an isolated asset.

Never replaces the playable Tripo import: this mesh must pass UE retarget QA
before it is allowed into the game runtime.
"""

import unreal


SOURCE_FBX = r"C:\Users\artcr\Documents\Codex\2026-08-17\new-chat\outputs\SK_Warrior_UE5_Retargetable.fbx"
DESTINATION = "/Game/_Sandbox/Characters/PrinceOfHell/UE5Retargetable"
NAME = "SK_POHPrince_UE5Retargetable"

task = unreal.AssetImportTask()
task.filename = SOURCE_FBX
task.destination_path = DESTINATION
task.destination_name = NAME
task.automated = True
task.replace_existing = False
task.save = True

options = unreal.FbxImportUI()
options.import_mesh = True
options.import_as_skeletal = True
options.import_animations = False
options.import_materials = True
options.import_textures = True
task.options = options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
if not task.imported_object_paths:
    raise RuntimeError("UE5-retargetable warrior import produced no assets")

mesh = unreal.load_asset(DESTINATION + "/" + NAME)
if not mesh:
    raise RuntimeError("Imported skeletal mesh not found")
if not mesh.get_editor_property("skeleton"):
    raise RuntimeError("Imported mesh has no skeleton")
for object_path in task.imported_object_paths:
    unreal.EditorAssetLibrary.save_asset(object_path, only_if_is_dirty=False)

unreal.log_warning("POH_UE5_WARRIOR_IMPORTED {}".format(task.imported_object_paths))
