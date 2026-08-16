# Animation pipeline

## Current safe path

The playable mesh is `SK_POHPrince_NativeTripo`; its skeleton is the only valid
target for gameplay animation. Do not use assets below `TripoRig` or
`RetargetedTemplateAligned`: they target an obsolete skeleton and their
Animation Blueprint has Control Rig hierarchy errors.

`IK_POHPrince_Native` and `RTG_Manny_To_POHNative` retarget UE 5.8 Manny core
locomotion to the playable skeleton. The generated clips are stored in
`NativeTripo/RetargetedManny` and are validated by
`Scripts/Development/ValidateNativePrinceRetargeting.py`.

They are currently **quarantined from runtime**: their package/skeleton links
validate, but visual QA found the mesh disappearing when those clips play.
Native Tripo clips remain the playable fallback until the retarget pose/root
motion is corrected in the Retargeter editor.

## State policy

- Idle and locomotion may loop.
- Jump is a short transition.
- Fall must use a looping airborne clip until landing.
- Land is a short transition, never a loop.
- Tripo dive and fall exports are authored full actions. They must not be wired
  into the ordinary jump/fall state machine. Dive belongs to a later sprint
  ability with matching movement timing.

The final runtime implementation must be an Animation Blueprint state machine
or compatible UE gameplay-animation graph. The temporary world subsystem is a
safe fallback only and must be disabled only after visual verification of the
new graph.
