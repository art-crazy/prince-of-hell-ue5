"""Split Prince's disconnected telekinetic hand before AccuRIG.

Usage:
  blender --background --python SplitTelekineticHandForAccuRig.py -- source.fbx body.fbx hand.fbx

The largest connected mesh island becomes the AccuRIG body. The second-largest
island is exported as the detached hand asset. Tiny floating artifacts are
discarded. This keeps a non-anatomical limb out of AccuRIG's auto-bind while
preserving it for UE procedural animation.
"""

from __future__ import annotations

import os
import sys

import bmesh
import bpy


def cli_args() -> tuple[str, str, str]:
    marker = sys.argv.index("--")
    source, body, hand = sys.argv[marker + 1 : marker + 4]
    return tuple(os.path.abspath(value) for value in (source, body, hand))


def connected_components(mesh: bpy.types.Mesh) -> list[set[int]]:
    work = bmesh.new()
    work.from_mesh(mesh)
    visited: set[int] = set()
    components: list[set[int]] = []
    for vertex in work.verts:
        if vertex.index in visited:
            continue
        pending = [vertex]
        component: set[int] = set()
        visited.add(vertex.index)
        while pending:
            current = pending.pop()
            component.add(current.index)
            for edge in current.link_edges:
                neighbor = edge.other_vert(current)
                if neighbor.index not in visited:
                    visited.add(neighbor.index)
                    pending.append(neighbor)
        components.append(component)
    work.free()
    return sorted(components, key=len, reverse=True)


def create_part(source: bpy.types.Object, keep_indices: set[int], name: str) -> bpy.types.Object:
    work = bmesh.new()
    work.from_mesh(source.data)
    discard = [vertex for vertex in work.verts if vertex.index not in keep_indices]
    bmesh.ops.delete(work, geom=discard, context="VERTS")
    data = bpy.data.meshes.new(f"{name}_Mesh")
    work.to_mesh(data)
    work.free()
    for material in source.data.materials:
        data.materials.append(material)
    result = bpy.data.objects.new(name, data)
    bpy.context.scene.collection.objects.link(result)
    result.matrix_world = source.matrix_world.copy()
    return result


def export_part(obj: bpy.types.Object, destination: str) -> None:
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    bpy.ops.export_scene.fbx(
        filepath=destination,
        use_selection=True,
        object_types={"MESH"},
        bake_anim=False,
        add_leaf_bones=False,
        path_mode="AUTO",
        embed_textures=False,
    )


def main() -> None:
    source_path, body_path, hand_path = cli_args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=source_path, use_anim=False)
    source = max(
        (item for item in bpy.context.scene.objects if item.type == "MESH"),
        key=lambda item: len(item.data.vertices),
    )
    components = connected_components(source.data)
    if len(components) < 2 or len(components[1]) < 100:
        raise RuntimeError("A distinct telekinetic-hand mesh island was not found")

    body = create_part(source, components[0], "POH_Warrior_BodyForAccuRig")
    hand = create_part(source, components[1], "POH_TelekineticLeftHand")
    for item in list(bpy.context.scene.objects):
        if item not in {body, hand}:
            bpy.data.objects.remove(item, do_unlink=True)
    export_part(body, body_path)
    export_part(hand, hand_path)
    print(f"BODY_FBX={body_path} vertices={len(components[0])}")
    print(f"HAND_FBX={hand_path} vertices={len(components[1])}")


if __name__ == "__main__":
    main()
