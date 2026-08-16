"""Align Prince's target retarget pose to UE's Mannequin chains before export."""

import unreal


retargeter_path = "/Game/_Sandbox/Rigging/RTG_Mannequin_To_POH"
retargeter = unreal.load_asset(retargeter_path)
if not retargeter:
    raise RuntimeError("Missing retargeter: {}".format(retargeter_path))

controller = unreal.IKRetargeterController.get_controller(retargeter)
controller.auto_align_all_bones(unreal.RetargetSourceOrTarget.TARGET)

if not unreal.EditorAssetLibrary.save_asset(retargeter_path, only_if_is_dirty=False):
    raise RuntimeError("Could not save aligned retargeter")

unreal.log_warning("POH: aligned target retarget pose from mapped template chains")
