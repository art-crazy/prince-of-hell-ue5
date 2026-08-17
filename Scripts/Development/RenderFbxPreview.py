"""Render a neutral front preview of an FBX for source-selection QA.

Usage: blender --background --python RenderFbxPreview.py -- source.fbx preview.png
"""

from __future__ import annotations

import os
import sys

import bpy
from mathutils import Vector


def args() -> tuple[str, str]:
    marker = sys.argv.index("--")
    return os.path.abspath(sys.argv[marker + 1]), os.path.abspath(sys.argv[marker + 2])


def aim_at(camera: bpy.types.Object, point: Vector) -> None:
    camera.rotation_euler = (point - camera.location).to_track_quat("-Z", "Y").to_euler()


def main() -> None:
    source, destination = args()
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=source, use_anim=False)

    points = [
        obj.matrix_world @ Vector(corner)
        for obj in bpy.context.scene.objects
        if obj.type == "MESH"
        for corner in obj.bound_box
    ]
    if not points:
        raise RuntimeError("No mesh objects found")
    lower = Vector((min(p[i] for p in points) for i in range(3)))
    upper = Vector((max(p[i] for p in points) for i in range(3)))
    center = (lower + upper) * 0.5
    span = upper - lower

    bpy.ops.object.camera_add(location=(center.x, lower.y - max(span.x, span.z) * 2.0, center.z))
    camera = bpy.context.object
    aim_at(camera, center)
    bpy.context.scene.camera = camera
    camera.data.type = "ORTHO"
    camera.data.ortho_scale = max(span.x, span.z) * 1.2

    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "MATERIAL"
    scene.display.shading.show_shadows = True
    scene.render.resolution_x = 800
    scene.render.resolution_y = 800
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = destination
    os.makedirs(os.path.dirname(destination), exist_ok=True)
    bpy.ops.render.render(write_still=True)
    print(f"PREVIEW={destination}")


if __name__ == "__main__":
    main()
