"""Build a Prince candidate bound to the armature exported from UE Manny."""
import bpy
import importlib.util
import json
import os
import sys
from mathutils import Vector


def args():
    return sys.argv[sys.argv.index("--") + 1:]


def bounds(objects):
    points = [obj.matrix_world @ Vector(corner) for obj in objects for corner in obj.bound_box]
    return min(point.z for point in points), max(point.z for point in points)


source_fbx, manny_fbx, output_fbx = args()
module_path = os.path.join(os.path.dirname(__file__), "ReskinPrinceToManny.py")
spec = importlib.util.spec_from_file_location("poh_reskin", module_path)
reskin = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reskin)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=source_fbx, use_anim=False)
source_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
source_armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
if len(source_armatures) != 1 or not source_meshes:
    raise RuntimeError("Expected one Tripo armature and at least one mesh")
source_min_z, source_max_z = bounds(source_meshes)

# Detach first: the original armature must never reach the exported FBX.
for mesh in source_meshes:
    world = mesh.matrix_world.copy()
    mesh.parent = None
    mesh.matrix_world = world
for armature in source_armatures:
    bpy.data.objects.remove(armature, do_unlink=True)

bpy.ops.import_scene.fbx(filepath=manny_fbx, use_anim=False)
target_armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
target_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH" and obj not in source_meshes]
if len(target_armatures) != 1 or not target_meshes:
    raise RuntimeError("Exact Manny FBX must contain one armature and a mesh")
target_armature = target_armatures[0]
target_min_z, target_max_z = bounds(target_meshes)
source_height = source_max_z - source_min_z
target_height = target_max_z - target_min_z
if source_height <= 1e-6 or target_height <= 1e-6:
    raise RuntimeError("Invalid source or Manny mesh bounds")

# UE's FBX exporter omits several root links; restore only the authoritative
# parent links from the Skeleton layout while preserving every exported bone
# axis and roll.
layout_path = r"C:\Users\artcr\Documents\Unreal Projects\test\Saved\ReskinPipeline\MannySkeletonLayout.json"
parents = {item["name"]: item.get("parent") for item in json.load(open(layout_path, encoding="utf-8"))["bones"]}
bpy.context.view_layer.objects.active = target_armature
target_armature.select_set(True)
bpy.ops.object.mode_set(mode="EDIT")
for name, parent_name in parents.items():
    bone = target_armature.data.edit_bones.get(name)
    parent = target_armature.data.edit_bones.get(parent_name) if parent_name not in (None, "None", "") else None
    if bone and parent and bone.parent != parent:
        bone.parent = parent
        bone.use_connect = False
bpy.ops.object.mode_set(mode="OBJECT")

# Match the visible source character to Manny's real-world scale before skinning.
scale = target_height / source_height
for mesh in source_meshes:
    for vertex in mesh.data.vertices:
        vertex.co.z = (vertex.co.z - source_min_z) * scale + target_min_z
        vertex.co.x *= scale
        vertex.co.y *= scale
for mesh in target_meshes:
    bpy.data.objects.remove(mesh, do_unlink=True)

report = reskin.remap_weights(source_meshes, target_armature)
target_armature.name = "Armature"
target_armature.data.name = "Armature"
bpy.ops.object.select_all(action="DESELECT")
target_armature.select_set(True)
for mesh in source_meshes:
    mesh.select_set(True)
bpy.context.view_layer.objects.active = target_armature
os.makedirs(os.path.dirname(output_fbx), exist_ok=True)
bpy.ops.export_scene.fbx(
    filepath=output_fbx, use_selection=True, object_types={"ARMATURE", "MESH"},
    add_leaf_bones=False, bake_anim=False, use_mesh_modifiers=True,
    apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL",
    axis_forward="-Z", axis_up="Y", armature_nodetype="NULL", use_armature_deform_only=False,
)
print("POH_EXACT_MANNY_RESKIN SUCCESS output={} bones={} scale={:.6f} weights={}".format(
    output_fbx, len(target_armature.data.bones), scale, sum(item["assigned_weights"] for item in report["meshes"])))
