"""Import the validated candidate against UE 5.8's existing Manny skeleton.

This script is intentionally isolated from runtime assets. It must only be
run after BuildPrinceMannyCandidate.ps1 succeeds.
"""

import unreal


SOURCE = r"C:\Users\artcr\Documents\Unreal Projects\test\Saved\ReskinPipeline\POH_Prince_MannyCandidate.fbx"
DESTINATION = "/Game/_Sandbox/Characters/PrinceOfHell/MannyCandidate"
NAME = "SK_POHPrince_MannyCandidate"
MANNY_SKELETON = "/Game/Characters/Mannequins/Meshes/SK_Mannequin"


def log(message):
    unreal.log_warning("POH_MANNY_IMPORT " + message)


if not unreal.Paths.file_exists(SOURCE):
    raise RuntimeError("Candidate FBX is missing: " + SOURCE)
skeleton = unreal.load_asset(MANNY_SKELETON)
if not skeleton:
    raise RuntimeError("UE Manny skeleton is missing: " + MANNY_SKELETON)

task = unreal.AssetImportTask()
task.filename = SOURCE
task.destination_path = DESTINATION
task.destination_name = NAME
task.automated = True
task.replace_existing = True
task.save = True

options = unreal.FbxImportUI()
options.automated_import_should_detect_type = False
options.mesh_type_to_import = unreal.FBXImportType.FBXIT_SKELETAL_MESH
options.import_mesh = True
options.import_as_skeletal = True
options.import_animations = False
options.skeleton = skeleton
task.options = options

unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
mesh = unreal.load_asset(DESTINATION + "/" + NAME)
if not mesh:
    raise RuntimeError("UE candidate import did not create a skeletal mesh")
if mesh.get_editor_property("skeleton") != skeleton:
    raise RuntimeError("Candidate was not bound to SK_Mannequin; rejecting generated skeleton")

bone_names = {str(name) for name in mesh.get_editor_property("skeleton").get_reference_pose().get_bone_names()}
required = {"root", "pelvis", "spine_01", "thigh_l", "hand_l", "foot_r"}
missing = required - bone_names
if missing:
    raise RuntimeError("Manny skeleton does not contain expected bones: " + ", ".join(sorted(missing)))

unreal.EditorAssetLibrary.save_asset(mesh.get_path_name())
log("STRUCTURAL_ONLY mesh={} skeleton={} bones={}".format(mesh.get_path_name(), skeleton.get_path_name(), len(bone_names)))
