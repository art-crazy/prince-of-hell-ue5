"""Read-only Blender inspection of the downloaded Prince FBX source."""

import bpy
import sys


source_path = sys.argv[sys.argv.index("--") + 1]
bpy.ops.import_scene.fbx(filepath=source_path)

for obj in bpy.context.scene.objects:
    if obj.type in {"ARMATURE", "MESH"}:
        print(
            "POH_FBX {} {} location={} rotation={} scale={}".format(
                obj.type,
                obj.name,
                tuple(round(v, 6) for v in obj.location),
                tuple(round(v, 6) for v in obj.rotation_euler),
                tuple(round(v, 6) for v in obj.scale),
            )
        )
        if obj.type == "ARMATURE":
            for bone in list(obj.data.bones)[:12]:
                print(
                    "POH_FBX_BONE {} parent={} head={} tail={}".format(
                        bone.name,
                        bone.parent.name if bone.parent else "None",
                        tuple(round(v, 6) for v in bone.head_local),
                        tuple(round(v, 6) for v in bone.tail_local),
                    )
                )

for action in bpy.data.actions:
    print(
        "POH_FBX_ACTION {} frames={}-{}".format(
            action.name,
            int(action.frame_range.x),
            int(action.frame_range.y),
        )
    )
