"""Read-only Blender audit for incoming humanoid FBX skin weights.

Run with Blender in background, passing an FBX path after ``--``. A candidate
is rejected when a body mesh is primarily weighted to its scene root or has
only a handful of deform groups: it cannot be repaired by UE IK Retargeter.
"""

import bpy
import sys


argv = sys.argv
source = argv[argv.index("--") + 1] if "--" in argv else None
if not source:
    raise RuntimeError("Usage: blender --background --python AuditFbxSkinWeights.py -- <file.fbx>")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=source)

for mesh in (obj for obj in bpy.context.scene.objects if obj.type == "MESH"):
    counts = {group.name: 0 for group in mesh.vertex_groups}
    unweighted = 0
    for vertex in mesh.data.vertices:
        if not vertex.groups:
            unweighted += 1
        for assignment in vertex.groups:
            counts[mesh.vertex_groups[assignment.group].name] += 1
    vertex_count = len(mesh.data.vertices)
    root_share = counts.get("root", 0) / max(1, vertex_count)
    print("POH_SKIN_AUDIT mesh={} vertices={} groups={} unweighted={} root_share={:.3f}".format(
        mesh.name, vertex_count, len(counts), unweighted, root_share
    ))
    for name, count in sorted(counts.items()):
        print("POH_SKIN_AUDIT group={} vertices={}".format(name, count))
    if len(counts) < 12 or root_share > 0.90:
        raise RuntimeError("REJECTED: insufficient distributed humanoid skin weights")
