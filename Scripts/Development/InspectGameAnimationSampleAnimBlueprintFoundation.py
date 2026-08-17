"""Read-only check of the migrated Game Animation Sample AnimBP foundation."""

import unreal


for path in (
    "/Game/Blueprints/RetargetedCharacters/ABP_GenericRetarget",
    "/Game/Blueprints/RetargetedCharacters/BP_Manny",
):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing migrated foundation asset: " + path)
    unreal.log_warning("POH_GAS_FOUNDATION asset={} class={}".format(path, asset.get_class().get_name()))
    if asset.get_class().get_name() == "AnimBlueprint":
        skeleton = asset.get_editor_property("target_skeleton")
        unreal.log_warning("POH_GAS_FOUNDATION skeleton={}".format(skeleton.get_path_name() if skeleton else "None (generic retarget graph)"))
    else:
        cdo = unreal.get_default_object(asset.generated_class())
        components = cdo.get_components_by_class(unreal.SkeletalMeshComponent)
        for mesh in components:
            unreal.log_warning("POH_GAS_FOUNDATION component={} mesh={} animation_mode={} anim_class={}".format(
                mesh.get_name(), mesh.get_skeletal_mesh_asset().get_path_name() if mesh.get_skeletal_mesh_asset() else "None",
                mesh.get_editor_property("animation_mode"), mesh.get_editor_property("anim_class")
            ))
