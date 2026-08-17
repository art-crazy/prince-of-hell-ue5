"""Log the imported AccuRIG candidate's usable humanoid topology.

This script is diagnostic-only: it makes no runtime or asset changes.  Its
output is the contract used by the candidate IK Rig creation script.
"""

import unreal


MESH_PATH = "/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/SK_POHPrince_AccuRig"


mesh = unreal.load_asset(MESH_PATH)
if not mesh:
    raise RuntimeError("Missing AccuRIG candidate mesh: " + MESH_PATH)

skeleton = mesh.get_editor_property("skeleton")
reference_pose = skeleton.get_reference_pose()
bone_names = [str(name) for name in reference_pose.get_bone_names()]
unreal.log_warning("POH_ACCURIG_AUDIT bones={} mesh={}".format(len(bone_names), MESH_PATH))
unreal.log_warning("POH_ACCURIG_AUDIT_NAMES {}".format(",".join(bone_names)))

for name in (
    "root", "pelvis", "spine_01", "spine_02", "spine_03", "neck_01", "head",
    "clavicle_l", "upperarm_l", "lowerarm_l", "hand_l",
    "clavicle_r", "upperarm_r", "lowerarm_r", "hand_r",
    "thigh_l", "calf_l", "foot_l", "ball_l",
    "thigh_r", "calf_r", "foot_r", "ball_r",
):
    unreal.log_warning("POH_ACCURIG_AUDIT_BONE name={} present={}".format(name, name in bone_names))
