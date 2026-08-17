"""Build a Manny-compatible Prince mesh without modifying any UE asset.

The script keeps the Tripo geometry/material slots, replaces its arbitrary
41-bone armature with the UE 5.8 Manny deform hierarchy and remaps vertex
weights to the closest Manny bones.  It intentionally produces a *candidate*
FBX in Saved/ReskinPipeline; importing it into UE is a separate, validated
step.  All decisions are written to a JSON report beside the FBX.

Run:
  blender --background --python ReskinPrinceToManny.py -- <tripo.fbx> <manny-layout.json> <out.fbx>
"""

import bpy
import json
import os
import sys
from collections import defaultdict
from mathutils import Matrix, Quaternion, Vector


def log(message):
    print("POH_RESKIN " + message)


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected arguments after --")
    return sys.argv[sys.argv.index("--") + 1:]


# Tripo's layout is intentionally mapped to Manny's deform bones only.  Twist
# weights are merged into the closest main bone; this is safer than binding an
# alien twist hierarchy to an incompatible source animation skeleton.
WEIGHT_MAP = {
    "Root": "root", "Hip": "pelvis", "Pelvis": "pelvis",
    "Waist": "spine_01", "Spine01": "spine_02", "Spine02": "spine_03",
    "NeckTwist01": "neck_01", "NeckTwist02": "neck_02", "Head": "head",
    "L_Clavicle": "clavicle_l", "L_Upperarm": "upperarm_l",
    "L_Forearm": "lowerarm_l", "L_Hand": "hand_l",
    "R_Clavicle": "clavicle_r", "R_Upperarm": "upperarm_r",
    "R_Forearm": "lowerarm_r", "R_Hand": "hand_r",
    "L_Thigh": "thigh_l", "L_Calf": "calf_l", "L_Foot": "foot_l",
    "L_ToeBase": "ball_l", "R_Thigh": "thigh_r", "R_Calf": "calf_r",
    "R_Foot": "foot_r", "R_ToeBase": "ball_r",
    "L_UpperarmTwist01": "upperarm_l", "L_UpperarmTwist02": "upperarm_l",
    "L_ForearmTwist01": "lowerarm_l", "L_ForearmTwist02": "lowerarm_l",
    "R_UpperarmTwist01": "upperarm_r", "R_UpperarmTwist02": "upperarm_r",
    "R_ForearmTwist01": "lowerarm_r", "R_ForearmTwist02": "lowerarm_r",
    "L_ThighTwist01": "thigh_l", "L_ThighTwist02": "thigh_l",
    "L_CalfTwist01": "calf_l", "L_CalfTwist02": "calf_l",
    "R_ThighTwist01": "thigh_r", "R_ThighTwist02": "thigh_r",
    "R_CalfTwist01": "calf_r", "R_CalfTwist02": "calf_r",
}


def ue_transform_matrix(data):
    """Turn the UE local transform JSON into a matrix for rest-pose layout."""
    t = Vector(data["translation"])
    q = Quaternion(data["rotation"])
    s = Vector(data["scale"])
    return Matrix.LocRotScale(t, q, s)


def load_reachable_layout(layout_path):
    with open(layout_path, encoding="utf-8") as source:
        raw = json.load(source)["bones"]
    by_name = {bone["name"]: bone for bone in raw}
    reachable = {"root"}
    changed = True
    while changed:
        changed = False
        for bone in raw:
            if bone["name"] not in reachable and bone.get("parent") in reachable:
                reachable.add(bone["name"])
                changed = True
    bones = [bone for bone in raw if bone["name"] in reachable]
    if "root" not in {bone["name"] for bone in bones}:
        raise RuntimeError("Manny layout does not include root")
    return bones


def global_rest_matrices(bones):
    local = {bone["name"]: ue_transform_matrix(bone["local"]) for bone in bones}
    parents = {
        bone["name"]: None if bone.get("parent") in (None, "None", "") else bone["parent"]
        for bone in bones
    }
    global_matrices = {}

    def resolve(name):
        if name in global_matrices:
            return global_matrices[name]
        parent = parents[name]
        matrix = local[name] if not parent else resolve(parent) @ local[name]
        global_matrices[name] = matrix
        return matrix

    for name in local:
        resolve(name)
    return global_matrices


def build_manny_armature(bones):
    """Create a deform-only armature with the exact reachable Manny hierarchy."""
    matrices = global_rest_matrices(bones)
    children = defaultdict(list)
    for bone in bones:
        if bone.get("parent"):
            children[bone["parent"]].append(bone["name"])

    # Blender's FBX exporter serializes an armature object as a scene node.
    # UE specially collapses the conventional "Armature" node, while a custom
    # name becomes an illegal extra bone when importing against SK_Mannequin.
    arm_data = bpy.data.armatures.new("__POH_TEMP_ARMATURE_DATA__")
    arm_obj = bpy.data.objects.new("__POH_TEMP_ARMATURE_OBJECT__", arm_data)
    bpy.context.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    arm_obj.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    edit_bones = {}
    for spec in bones:
        name = spec["name"]
        matrix = matrices[name]
        head = matrix.translation
        child_names = children.get(name, [])
        if child_names:
            tail = matrices[child_names[0]].translation
        else:
            direction = (matrix.to_3x3() @ Vector((1.0, 0.0, 0.0))).normalized()
            tail = head + direction * 3.0
        if (tail - head).length < 0.01:
            tail = head + Vector((3.0, 0.0, 0.0))
        edit_bone = arm_data.edit_bones.new(name)
        edit_bone.head = head
        edit_bone.tail = tail
        edit_bone.use_deform = True
        edit_bones[name] = edit_bone
    for spec in bones:
        parent = spec.get("parent")
        if parent not in (None, "None", ""):
            edit_bones[spec["name"]].parent = edit_bones[parent]
            edit_bones[spec["name"]].use_connect = False
    bpy.ops.object.mode_set(mode="OBJECT")
    return arm_obj


def import_tripo_mesh(source_fbx):
    bpy.ops.import_scene.fbx(filepath=source_fbx, use_anim=False)
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    if not meshes or not armatures:
        raise RuntimeError("Tripo FBX must contain a mesh and armature")
    return meshes, armatures


def remap_weights(meshes, new_armature):
    report = {"meshes": [], "unmapped_source_groups": []}
    target_names = {bone.name for bone in new_armature.data.bones}
    for mesh in meshes:
        source_groups = list(mesh.vertex_groups)
        source_by_index = {group.index: group.name for group in source_groups}
        target_groups = {name: mesh.vertex_groups.new(name=name) for name in target_names}
        transferred = 0
        unmapped = set()
        for vertex in mesh.data.vertices:
            merged = defaultdict(float)
            for assignment in vertex.groups:
                source = source_by_index[assignment.group]
                target = WEIGHT_MAP.get(source)
                if target and target in target_groups:
                    merged[target] += assignment.weight
                else:
                    unmapped.add(source)
            total = sum(merged.values())
            if total:
                for target, weight in merged.items():
                    target_groups[target].add([vertex.index], weight / total, "REPLACE")
                    transferred += 1
        for group in source_groups:
            mesh.vertex_groups.remove(group)
        modifier = mesh.modifiers.get("Armature") or mesh.modifiers.new("Armature", "ARMATURE")
        modifier.object = new_armature
        report["meshes"].append({"name": mesh.name, "vertices": len(mesh.data.vertices), "assigned_weights": transferred})
        report["unmapped_source_groups"].extend(sorted(unmapped))
    report["unmapped_source_groups"] = sorted(set(report["unmapped_source_groups"]))
    return report


def main():
    source_fbx, layout_path, output_fbx = args_after_separator()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    meshes, source_armatures = import_tripo_mesh(source_fbx)
    log("SOURCE meshes={} armatures={} vertices={}".format(len(meshes), len(source_armatures), sum(len(mesh.data.vertices) for mesh in meshes)))
    layout = load_reachable_layout(layout_path)
    manny = build_manny_armature(layout)
    report = remap_weights(meshes, manny)
    for source_armature in source_armatures:
        bpy.data.objects.remove(source_armature, do_unlink=True)
    manny.name = "Armature"
    manny.data.name = "Armature"
    bpy.ops.object.select_all(action="DESELECT")
    manny.select_set(True)
    for mesh in meshes:
        mesh.select_set(True)
    bpy.context.view_layer.objects.active = manny
    os.makedirs(os.path.dirname(output_fbx), exist_ok=True)
    bpy.ops.export_scene.fbx(
        filepath=output_fbx, use_selection=True, object_types={"ARMATURE", "MESH"},
        add_leaf_bones=False, bake_anim=False, use_mesh_modifiers=True,
        apply_unit_scale=True, apply_scale_options="FBX_SCALE_ALL",
        axis_forward="-Z", axis_up="Y", armature_nodetype="NULL",
        use_armature_deform_only=True,
    )
    report.update({"source_fbx": source_fbx, "layout": layout_path, "output_fbx": output_fbx, "manny_reachable_bones": len(layout), "armature_object": manny.name})
    report_path = os.path.splitext(output_fbx)[0] + ".report.json"
    with open(report_path, "w", encoding="utf-8") as target:
        json.dump(report, target, indent=2)
    log("SUCCESS output={} bones={} report={}".format(output_fbx, len(layout), report_path))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("POH_RESKIN FAILURE {}".format(error))
        raise SystemExit(2)
