"""Log available UE 5.8 Manny animation paths for deterministic validation."""

import unreal


ROOT = "/Game/Characters/Mannequins/Anims"
assets = unreal.EditorAssetLibrary.list_assets(ROOT, recursive=True, include_folder=False)
for path in sorted(assets):
    asset = unreal.load_asset(path)
    if isinstance(asset, unreal.AnimSequence):
        unreal.log_warning("POH_MANNY_ANIM {}".format(path))
unreal.log_warning("POH_MANNY_ANIM_LIST PASS count={}".format(len(assets)))
