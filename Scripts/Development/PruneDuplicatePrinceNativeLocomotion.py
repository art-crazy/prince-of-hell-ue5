"""Remove only verified duplicate clips produced by the multi-action FBX import."""

import unreal


ROOT = "/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo"
PREFIX = "SK_POHPrince_NativeTripo"
TOKENS = ("fall", "idle", "jump", "run", "walk")


for token in TOKENS:
    base_path = "{}/{}{}".format(ROOT, PREFIX, token)
    duplicate_path = base_path + "1"
    base = unreal.load_asset(base_path)
    duplicate = unreal.load_asset(duplicate_path)
    if not base or not duplicate:
        raise RuntimeError("Expected duplicate pair is missing: {}, {}".format(base_path, duplicate_path))
    if base.get_editor_property("skeleton") != duplicate.get_editor_property("skeleton"):
        raise RuntimeError("Duplicate '{}' has a different skeleton".format(duplicate.get_name()))
    if abs(base.get_play_length() - duplicate.get_play_length()) > 0.001:
        raise RuntimeError("Duplicate '{}' has a different duration".format(duplicate.get_name()))
    if not unreal.EditorAssetLibrary.delete_asset(duplicate_path):
        raise RuntimeError("Could not delete verified duplicate '{}'".format(duplicate_path))

unreal.log_warning("POH native locomotion duplicates pruned")
