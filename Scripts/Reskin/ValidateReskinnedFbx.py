"""Read-only structural validation for the Manny-reskinned candidate FBX."""

import bpy
import json
import os
import sys


def arg_values():
    return sys.argv[sys.argv.index("--") + 1:]


candidate, layout_path = arg_values()
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=candidate, use_anim=False)
with open(layout_path, encoding="utf-8") as source:
    raw_bones = json.load(source)["bones"]
    required = {"root"}
    changed = True
    while changed:
        changed = False
        for bone in raw_bones:
            if bone["name"] not in required and bone.get("parent") in required:
                required.add(bone["name"])
                changed = True
armatures = [obj for obj in bpy.context.scene.objects if obj.type == "ARMATURE"]
meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
if len(armatures) != 1 or not meshes:
    raise RuntimeError("Expected exactly one armature and at least one mesh")
armature = armatures[0]
if armature.name != "Armature":
    raise RuntimeError("UE-safe armature object must be named Armature, got: " + armature.name)
actual = {bone.name for bone in armature.data.bones}
missing = sorted(required - actual)
weighted = set()
for mesh in meshes:
    weighted.update(group.name for group in mesh.vertex_groups)
if missing:
    raise RuntimeError("Missing Manny bones: " + ", ".join(missing[:10]))
if not weighted.intersection({"root", "pelvis", "spine_01", "thigh_l", "upperarm_l"}):
    raise RuntimeError("Candidate has no core Manny vertex weights")
print("POH_RESKIN_VALIDATE PASS bones={} meshes={} weighted_groups={} file={}".format(len(actual), len(meshes), len(weighted), os.path.basename(candidate)))
