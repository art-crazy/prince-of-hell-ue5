import unreal

ASSET_TOOLS = unreal.AssetToolsHelpers.get_asset_tools()


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: {}".format(path))
    return asset


def create_if_missing(name, package_path, asset_class, factory):
    path = "{}/{}".format(package_path, name)
    asset = unreal.load_asset(path)
    if asset:
        return asset
    return ASSET_TOOLS.create_asset(name, package_path, asset_class, factory)


manny_mesh = load("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
hero_mesh = load("/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig")
hero_rig = load("/Game/_Sandbox/Characters/PrinceOfHell/Rigging/IK_POHPrince")

rig_factory = unreal.IKRigDefinitionFactory()
manny_rig = create_if_missing(
    "IK_Mannequin_Template",
    "/Game/_Sandbox/Rigging",
    unreal.IKRigDefinition,
    rig_factory,
)
manny_controller = unreal.IKRigController.get_controller(manny_rig)
if not manny_controller.get_skeletal_mesh():
    if not manny_controller.set_skeletal_mesh(manny_mesh):
        raise RuntimeError("Could not assign Manny mesh to IK rig")
    if not manny_controller.apply_auto_generated_retarget_definition():
        raise RuntimeError("Could not characterize Manny IK rig")

hero_controller = unreal.IKRigController.get_controller(hero_rig)
if not hero_controller.get_skeletal_mesh():
    if not hero_controller.set_skeletal_mesh(hero_mesh):
        raise RuntimeError("Could not assign Prince mesh to IK rig")

if len(hero_controller.get_retarget_chains()) == 0:
    if not hero_controller.apply_auto_generated_retarget_definition():
        raise RuntimeError("Prince skeleton needs manual IK-chain characterization")

retargeter_factory = unreal.IKRetargetFactory()
retargeter = create_if_missing(
    "RTG_Mannequin_To_POH",
    "/Game/_Sandbox/Rigging",
    unreal.IKRetargeter,
    retargeter_factory,
)
retarget_controller = unreal.IKRetargeterController.get_controller(retargeter)
retarget_controller.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, manny_rig)
retarget_controller.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, hero_rig)
retarget_controller.add_default_ops()
retarget_controller.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)

for path in [
    "/Game/_Sandbox/Rigging/IK_Mannequin_Template",
    "/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH",
]:
    if not unreal.EditorAssetLibrary.save_asset(path, only_if_is_dirty=False):
        raise RuntimeError("Could not save {}".format(path))

unreal.log_warning("POH: Manny-to-Prince retargeter ready")
