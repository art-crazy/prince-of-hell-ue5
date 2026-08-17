"""Create a clean, unskinned FBX copy for AccuRIG.

Usage (from Blender):
  blender --background --python PrepareStaticMeshForAccuRig.py -- source.fbx output.fbx

The source file is never changed.  The output contains only visible mesh objects:
armatures, animation data, armature modifiers and invalid vertex weights are removed.
"""

from __future__ import annotations

import os
import sys

import bpy


def cli_args() -> tuple[str, str]:
    try:
        separator = sys.argv.index("--")
        source, destination = sys.argv[separator + 1 : separator + 3]
    except (ValueError, IndexError):
        raise RuntimeError("Expected: -- <source.fbx> <output.fbx>")
    return os.path.abspath(source), os.path.abspath(destination)


def main() -> None:
    source, destination = cli_args()
    if not os.path.isfile(source):
        raise RuntimeError(f"Source FBX was not found: {source}")

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=source, use_anim=False)

    # Some Tripo FBX exports carry a tiny default ``Cube`` helper alongside the
    # character. It is not character geometry and makes AccuRIG's auto-bind
    # fail, so exclude only that unambiguous helper. Keep every real mesh part.
    meshes = [
        item
        for item in bpy.context.scene.objects
        if item.type == "MESH"
        and not (
            item.name.casefold() == "cube"
            and len(item.data.vertices) == 8
            and len(item.data.polygons) == 6
        )
    ]
    if not meshes:
        raise RuntimeError("The source FBX contains no mesh objects")

    for mesh in meshes:
        mesh.parent = None
        for modifier in list(mesh.modifiers):
            mesh.modifiers.remove(modifier)
        mesh.vertex_groups.clear()
        mesh.animation_data_clear()

    for item in list(bpy.context.scene.objects):
        if item not in meshes:
            bpy.data.objects.remove(item, do_unlink=True)

    bpy.ops.object.select_all(action="DESELECT")
    for mesh in meshes:
        mesh.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    if destination.casefold().endswith(".obj"):
        bpy.ops.wm.obj_export(
            filepath=destination,
            export_selected_objects=True,
            export_materials=True,
            export_uv=True,
            export_normals=True,
            export_triangulated_mesh=True,
            path_mode="AUTO",
        )
    else:
        bpy.ops.export_scene.fbx(
            filepath=destination,
            use_selection=True,
            object_types={"MESH"},
            bake_anim=False,
            add_leaf_bones=False,
            path_mode="AUTO",
            embed_textures=False,
        )

    print(f"ACCURIG_STATIC_FBX={destination}")
    print(f"MESH_COUNT={len(meshes)}")
    print("VERTEX_GROUPS_REMOVED=YES")


if __name__ == "__main__":
    main()
