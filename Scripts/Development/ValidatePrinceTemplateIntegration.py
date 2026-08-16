"""Fail-fast asset validation for the Prince third-person integration."""

import math

import unreal


def require_asset(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing required asset: {}".format(path))
    return asset


hero_mesh = require_asset("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
hero_rig = require_asset("/Game/_Sandbox/Characters/PrinceOfHell/Rigging/IK_POHPrince")
manny_rig = require_asset("/Game/_Sandbox/Rigging/IK_Mannequin_Template")
retargeter = require_asset("/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH")
character_blueprint = require_asset("/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter")

for rig, expected_mesh, label in [
    (hero_rig, hero_mesh, "Prince"),
    (manny_rig, require_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"), "Manny"),
]:
    configured_mesh = unreal.IKRigController.get_controller(rig).get_skeletal_mesh()
    if configured_mesh != expected_mesh:
        raise RuntimeError("{} IK rig targets the wrong skeletal mesh".format(label))

retarget_controller = unreal.IKRetargeterController.get_controller(retargeter)
if retarget_controller.get_ik_rig(unreal.RetargetSourceOrTarget.SOURCE) != manny_rig:
    raise RuntimeError("Retargeter source is not the Manny IK rig")
if retarget_controller.get_ik_rig(unreal.RetargetSourceOrTarget.TARGET) != hero_rig:
    raise RuntimeError("Retargeter target is not the Prince IK rig")

generated_class = character_blueprint.generated_class()
if not generated_class:
    raise RuntimeError("Prince character blueprint has no generated class")

character_cdo = unreal.get_default_object(generated_class)
mesh_component = character_cdo.get_component_by_class(unreal.SkeletalMeshComponent)
if not mesh_component:
    raise RuntimeError("Prince character blueprint has no skeletal mesh component")

assigned_mesh = mesh_component.get_editor_property("skeletal_mesh_asset")
if assigned_mesh != hero_mesh:
    raise RuntimeError(
        "Prince character blueprint references '{}', expected '{}'".format(
            assigned_mesh.get_path_name() if assigned_mesh else "None",
            hero_mesh.get_path_name(),
        )
    )

mesh_location = mesh_component.get_editor_property("relative_location")
mesh_rotation = mesh_component.get_editor_property("relative_rotation")
if not math.isclose(mesh_location.z, -96.0, abs_tol=0.01) or not math.isclose(mesh_rotation.yaw, -90.0, abs_tol=0.01):
    raise RuntimeError(
        "Prince character blueprint has an invalid mesh placement: location={}, rotation={}"
        .format(mesh_location, mesh_rotation)
    )

unreal.log_warning("POH VALIDATION PASSED: template character, Prince mesh and retarget assets are wired")
