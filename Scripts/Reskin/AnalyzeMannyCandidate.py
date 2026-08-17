"""Read-only geometry and bind-pose diagnostic for the Manny candidate FBX.

This is intentionally independent from Unreal and animation clips.  It finds
bad topology, unweighted vertices, unexpected armature nodes and transforms
before an FBX reaches UE's Interchange importer.

Run:
  blender --factory-startup --background --python AnalyzeMannyCandidate.py -- <candidate.fbx> <report.json>
"""

import bpy
import json
import math
import os
import sys


def args_after_separator():
    if "--" not in sys.argv:
        raise RuntimeError("Expected arguments after --")
    return sys.argv[sys.argv.index("--") + 1:]


def matrix_rows(matrix):
    return [[round(value, 7) for value in row] for row in matrix]


def mesh_report(mesh):
    vertices = mesh.data.vertices
    groups = {group.index: group.name for group in mesh.vertex_groups}
    unweighted = []
    invalid_weight_sums = []
    for vertex in vertices:
        total = sum(assignment.weight for assignment in vertex.groups)
        if total <= 1e-6:
            unweighted.append(vertex.index)
        elif abs(total - 1.0) > 1e-4:
            invalid_weight_sums.append({"vertex": vertex.index, "sum": round(total, 6)})

    degenerate = 0
    for polygon in mesh.data.polygons:
        if polygon.area <= 1e-10:
            degenerate += 1

    modifier = next((item for item in mesh.modifiers if item.type == "ARMATURE"), None)
    return {
        "name": mesh.name,
        "vertices": len(vertices),
        "polygons": len(mesh.data.polygons),
        "degenerate_polygons": degenerate,
        "unweighted_vertex_count": len(unweighted),
        "unweighted_vertex_examples": unweighted[:20],
        "non_normalized_weight_count": len(invalid_weight_sums),
        "non_normalized_weight_examples": invalid_weight_sums[:20],
        "vertex_groups": sorted(groups.values()),
        "armature_modifier_target": modifier.object.name if modifier and modifier.object else None,
        "object_matrix": matrix_rows(mesh.matrix_world),
        "bounds": {
            "min": [round(min(vertex.co[index] for vertex in vertices), 5) for index in range(3)],
            "max": [round(max(vertex.co[index] for vertex in vertices), 5) for index in range(3)],
        },
    }


def main():
    candidate, output = args_after_separator()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=candidate, use_anim=False)
    armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if len(armatures) != 1 or not meshes:
        raise RuntimeError("Expected exactly one armature and at least one mesh")

    armature = armatures[0]
    bones = armature.data.bones
    zero_length = [bone.name for bone in bones if bone.length <= 1e-6]
    zero_determinant = [bone.name for bone in bones if abs(bone.matrix_local.to_3x3().determinant()) <= 1e-8]
    report = {
        "candidate": os.path.abspath(candidate),
        "armature": {
            "object_name": armature.name,
            "data_name": armature.data.name,
            "bone_count": len(bones),
            "root_bones": sorted(bone.name for bone in bones if bone.parent is None),
            "zero_length_bones": zero_length,
            "zero_determinant_bones": zero_determinant,
            "object_matrix": matrix_rows(armature.matrix_world),
        },
        "meshes": [mesh_report(mesh) for mesh in meshes],
    }
    report["passes_static_gate"] = (
        armature.name == "Armature"
        and not zero_length
        and not zero_determinant
        and all(item["unweighted_vertex_count"] == 0 for item in report["meshes"])
        and all(item["degenerate_polygons"] == 0 for item in report["meshes"])
        and all(item["armature_modifier_target"] == armature.name for item in report["meshes"])
    )
    os.makedirs(os.path.dirname(output), exist_ok=True)
    with open(output, "w", encoding="utf-8") as target:
        json.dump(report, target, indent=2)
    print("POH_MANNY_GEOMETRY_ANALYSIS {} report={}".format(
        "PASS" if report["passes_static_gate"] else "FAIL", output))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("POH_MANNY_GEOMETRY_ANALYSIS FAILURE {}".format(error))
        raise
