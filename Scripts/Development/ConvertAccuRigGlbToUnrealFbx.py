"""Convert AccuRIG's local rigged GLB cache to an Unreal-ready FBX.

Usage:
  blender --background --python ConvertAccuRigGlbToUnrealFbx.py -- input.glb output.fbx
"""

from __future__ import annotations

import os
import sys

import bpy


def cli_args() -> tuple[str, str]:
    marker = sys.argv.index("--")
    return os.path.abspath(sys.argv[marker + 1]), os.path.abspath(sys.argv[marker + 2])


def main() -> None:
    source, destination = cli_args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=source)

    armatures = [item for item in bpy.context.scene.objects if item.type == "ARMATURE"]
    meshes = [item for item in bpy.context.scene.objects if item.type == "MESH" and len(item.vertex_groups) > 0]
    if len(armatures) != 1 or len(meshes) != 1:
        raise RuntimeError("Expected one rigged character mesh and one armature from AccuRIG GLB")

    bpy.ops.object.select_all(action="DESELECT")
    armatures[0].select_set(True)
    meshes[0].select_set(True)
    bpy.context.view_layer.objects.active = armatures[0]

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    bpy.ops.export_scene.fbx(
        filepath=destination,
        use_selection=True,
        object_types={"ARMATURE", "MESH"},
        bake_anim=False,
        add_leaf_bones=False,
        use_armature_deform_only=True,
        path_mode="AUTO",
        embed_textures=False,
    )
    print(f"UE_FBX={destination}")
    print(f"BONES={len(armatures[0].data.bones)}")
    print(f"VERTEX_GROUPS={len(meshes[0].vertex_groups)}")


if __name__ == "__main__":
    main()
