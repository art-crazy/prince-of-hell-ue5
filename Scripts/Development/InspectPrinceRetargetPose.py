"""Emit the reference-pose data needed to repair Prince's retarget base pose."""

import unreal


def load(path):
    asset = unreal.load_asset(path)
    if not asset:
        raise RuntimeError("Missing asset: {}".format(path))
    return asset


hero_rig = load("/Game/_Sandbox/Characters/PrinceOfHell/Rigging/IK_POHPrince")
manny_rig = load("/Game/_Sandbox/Rigging/IK_Mannequin_Template")


def describe(label, rig):
    controller = unreal.IKRigController.get_controller(rig)
    root = controller.get_retarget_root()
    lines = ["{} root={}".format(label, root)]
    for chain in controller.get_retarget_chains():
        lines.append("{} chain={}".format(label, chain))
    for bone in [root, "pelvis", "spine_01", "head", "foot_l", "foot_r"]:
        if bone:
            lines.append(
                "{} ref[{}]={}".format(
                    label, bone, controller.get_ref_pose_transform_of_bone(bone)
                )
            )
    return "\n".join(lines)


unreal.log_warning("POH RETARGET INSPECTION\n{}\n{}".format(
    describe("Manny", manny_rig), describe("Prince", hero_rig)
))
