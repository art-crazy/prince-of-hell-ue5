"""Create a clean, isolated IK Rig for the AccuRIG Prince candidate.

The chains intentionally use the UE5 humanoid naming emitted by AccuRIG.  This
is the only approved animation transfer route for this candidate: never assign
Manny animations directly to this skeleton.
"""

import unreal


FOLDER = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/Rigging"
NAME = "IK_POHPrince_AccuRig"
PATH = FOLDER + "/" + NAME
MESH_PATH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"

CHAINS = (
    ("Spine", "spine_01", "spine_05"),
    ("Neck", "neck_01", "neck_02"),
    ("Head", "head", "head"),
    ("LeftLeg", "thigh_l", "foot_l"),
    ("LeftFoot", "ball_l", "ball_l"),
    ("RightLeg", "thigh_r", "foot_r"),
    ("RightFoot", "ball_r", "ball_r"),
    ("LeftClavicle", "clavicle_l", "clavicle_l"),
    ("LeftArm", "upperarm_l", "hand_l"),
    ("RightClavicle", "clavicle_r", "clavicle_r"),
    ("RightArm", "upperarm_r", "hand_r"),
)


mesh = unreal.load_asset(MESH_PATH)
if not mesh:
    raise RuntimeError("Missing AccuRIG candidate mesh: " + MESH_PATH)

rig = unreal.load_asset(PATH)
if not rig:
    rig = unreal.IKRigDefinitionFactory.create_new_ik_rig_asset(FOLDER, NAME)
if not rig:
    raise RuntimeError("Unable to create AccuRIG Prince IK Rig")

controller = unreal.IKRigController.get_controller(rig)
if not controller.set_skeletal_mesh(mesh):
    raise RuntimeError("Unable to bind AccuRIG mesh to IK Rig")
if not controller.set_retarget_root("pelvis"):
    raise RuntimeError("Unable to set AccuRIG retarget root")

existing = {str(chain.chain_name) for chain in controller.get_retarget_chains()}
for name, start_bone, end_bone in CHAINS:
    if name not in existing:
        result = controller.add_retarget_chain(name, start_bone, end_bone, "")
        if str(result) != name:
            raise RuntimeError("Unable to create chain {}: {}".format(name, result))

if not unreal.EditorAssetLibrary.save_asset(PATH, only_if_is_dirty=False):
    raise RuntimeError("Unable to save AccuRIG Prince IK Rig")

unreal.log_warning("POH_ACCURIG_IKRIG_READY {} chains={}".format(PATH, len(CHAINS)))
