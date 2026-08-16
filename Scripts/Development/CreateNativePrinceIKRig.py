"""Create the IK Rig for the skeleton actually used by the playable Prince mesh.

This is intentionally separate from the abandoned TripoRig retarget setup.
"""

import unreal


RIG_FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/Rigging"
RIG_NAME = "IK_POHPrince_Native"
RIG_PATH = f"{RIG_FOLDER}/{RIG_NAME}"
MESH_PATH = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/SK_POHPrince_NativeTripo"

CHAINS = (
    ("Spine", "Waist", "Spine02"),
    ("Neck", "NeckTwist01", "NeckTwist02"),
    ("Head", "Head", "Head"),
    ("LeftLeg", "L_Thigh", "L_Foot"),
    ("LeftFoot", "L_ToeBase", "L_ToeBase"),
    ("RightLeg", "R_Thigh", "R_Foot"),
    ("RightFoot", "R_ToeBase", "R_ToeBase"),
    ("LeftClavicle", "L_Clavicle", "L_Clavicle"),
    ("LeftArm", "L_Upperarm", "L_Hand"),
    ("RightClavicle", "R_Clavicle", "R_Clavicle"),
    ("RightArm", "R_Upperarm", "R_Hand"),
)

mesh = unreal.load_asset(MESH_PATH)
if not mesh:
    raise RuntimeError(f"Missing playable Prince mesh: {MESH_PATH}")

rig = unreal.load_asset(RIG_PATH)
if not rig:
    rig = unreal.IKRigDefinitionFactory.create_new_ik_rig_asset(RIG_FOLDER, RIG_NAME)
if not rig:
    raise RuntimeError("Unable to create Prince native IK Rig")

controller = unreal.IKRigController.get_controller(rig)
if not controller.set_skeletal_mesh(mesh):
    raise RuntimeError("Unable to bind native Prince mesh to IK Rig")
if not controller.set_retarget_root("Root"):
    raise RuntimeError("Unable to set native Prince retarget root")

existing = {str(chain.chain_name) for chain in controller.get_retarget_chains()}
for name, start_bone, end_bone in CHAINS:
    if name not in existing:
        result = controller.add_retarget_chain(name, start_bone, end_bone, "")
        if str(result) != name:
            raise RuntimeError(f"Unable to create chain {name}; got {result}")

if not unreal.EditorAssetLibrary.save_asset(RIG_PATH, only_if_is_dirty=False):
    raise RuntimeError("Unable to save native Prince IK Rig")

unreal.log_warning(f"POH_NATIVE_IKRIG_READY {RIG_PATH}")
