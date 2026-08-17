"""Validate that the imported candidate can reference direct UE Manny clips."""

import unreal


MESH_PATH = "/Game/_Sandbox/Characters/PrinceOfHell/MannyCandidate/SK_POHPrince_MannyCandidate"
MANNY_SKELETON = "/Game/Characters/Mannequins/Meshes/SK_Mannequin"
DIRECT_CLIPS = (
    "/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle",
    "/Game/Characters/Mannequins/Anims/Unarmed/Walk/MF_Unarmed_Walk_Fwd",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jog/MF_Unarmed_Jog_Fwd",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Jump",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Fall_Loop",
    "/Game/Characters/Mannequins/Anims/Unarmed/Jump/MM_Land",
)

mesh = unreal.load_asset(MESH_PATH)
skeleton = unreal.load_asset(MANNY_SKELETON)
if not mesh or not skeleton:
    raise RuntimeError("Candidate mesh or Manny skeleton is unavailable")
if mesh.get_editor_property("skeleton") != skeleton:
    raise RuntimeError("Candidate is not on the UE Manny skeleton")
for clip_path in DIRECT_CLIPS:
    clip = unreal.load_asset(clip_path)
    if not clip:
        raise RuntimeError("Missing UE animation: " + clip_path)
    if clip.get_editor_property("skeleton") != skeleton:
        raise RuntimeError("UE animation has unexpected skeleton: " + clip_path)
    unreal.log_warning("POH_MANNY_DIRECT_CLIP {}".format(clip_path))
unreal.log_warning("POH_MANNY_IMPORT_VALIDATE PASS mesh={} clips={}".format(MESH_PATH, len(DIRECT_CLIPS)))
