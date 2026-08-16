"""Fail-fast asset validation for the Prince third-person integration."""

import unreal


def require_asset(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing required asset: {}".format(path))
    return asset


hero_mesh = require_asset("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
require_asset("/Game/_Sandbox/Characters/PrinceOfHell/Rigging/IK_POHPrince")
require_asset("/Game/_Sandbox/Rigging/IK_Mannequin_Template")
require_asset("/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH")
character_blueprint = require_asset("/Game/_Sandbox/Blueprints/BP_POHThirdPersonCharacter")

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

unreal.log_warning("POH VALIDATION PASSED: template character, Prince mesh and retarget assets are wired")
