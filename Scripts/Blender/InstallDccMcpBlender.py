"""Install and enable the official DCC MCP Blender extension for Blender 5.2."""

import bpy
import os


ARCHIVE = r"C:\Users\artcr\Documents\Unreal Projects\test\Tools\dcc_mcp_blender_addon_win64_v0.2.1.zip"
REPOSITORY = "user_default"
PACKAGE = "bl_ext.user_default.dcc_mcp_blender"


if not os.path.exists(ARCHIVE):
    raise RuntimeError("DCC MCP Blender archive is missing: " + ARCHIVE)

installed = any(addon.module == PACKAGE for addon in bpy.context.preferences.addons)
if not installed:
    result = bpy.ops.extensions.package_install_files(
        filepath=ARCHIVE,
        repo=REPOSITORY,
        enable_on_install=True,
        overwrite=True,
    )
    if "FINISHED" not in result:
        raise RuntimeError("Extension installation failed: " + str(result))

if not any(addon.module == PACKAGE for addon in bpy.context.preferences.addons):
    bpy.ops.preferences.addon_enable(module=PACKAGE)

bpy.ops.wm.save_userpref()
enabled = any(addon.module == PACKAGE for addon in bpy.context.preferences.addons)
if not enabled:
    raise RuntimeError("DCC MCP Blender was not enabled")
print("POH_DCC_MCP_BLENDER_INSTALL PASS package={} archive={}".format(PACKAGE, ARCHIVE))
