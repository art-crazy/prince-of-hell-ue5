# Animation pipeline

## Current safe path

The playable mesh is `SK_POHPrince_NativeTripo`; its skeleton is the only valid
target for gameplay animation. Do not use assets below `TripoRig` or
`RetargetedTemplateAligned`: they target an obsolete skeleton and their
Animation Blueprint has Control Rig hierarchy errors.

## UE5-retargetable warrior candidate

The user-supplied `SK_Warrior_UE5_Retargetable.fbx` is imported separately as
`SK_POHPrince_UE5Retargetable`. Its conventional humanoid bone names are
configured in `IK_POHPrince_UE5Retargetable`; the paired retargeter is
`RTG_Manny_To_POH_UE5Retargetable`. The first isolated UE 5.8 validation clip
is `UE58_IKQA_MM_Idle`. It is not connected to runtime until visual QA accepts
the mesh and its idle pose.

**2026-08-17: rejected for animation.** Blender audit found only five deform
groups; 37,880 of 37,884 vertices are weighted to `root`, while the two foot
groups each affect nearly the entire mesh. UE cannot correct broken skinning
with IKRig, so this candidate stays quarantined. Re-rig the static mesh through
AccuRIG (or equivalent) and validate the exported FBX first with
`Scripts/Development/AuditFbxSkinWeights.py`.

## AccuRIG rebuild (required before new UE animation work)

The clean AccuRIG input is generated, never edited in place:
`Saved/AccuRig/POH_Warrior_StaticForAccuRig_Clean.fbx`. Generate it again from a new
Tripo export with:

```text
Blender 5.2\blender.exe --background --python Scripts/Development/PrepareStaticMeshForAccuRig.py -- <source.fbx> Saved/AccuRig/POH_Warrior_StaticForAccuRig_Clean.fbx
```

The preparation script preserves the source FBX and materials but intentionally
strips its armature and all vertex weights. It rebuilds the export scene around
one mesh object, so no import helper or source-rig node can reach AccuRIG. For
this specific character, use the **complete original model** and leave
AccuRIG's automatically placed body and hand guides unchanged unless a guide
is visibly outside the anatomy. Field testing showed that manually placing a
guide on the disconnected wrist makes AccuRIG fail, while its default solve
produces a valid 100-bone, fully weighted rig. Test with an included motion
before export.

The disconnected telekinetic hand is an intentional Prince feature. Do not
separate it before the AccuRIG solve: the complete model is the reliable rigging
input. After a successful solve/import, separate the hand as an accessory in
the UE preparation stage. The hand component will be driven from a
left-forearm socket with a deterministic telekinetic offset, inertia and
rotation; it is never a physics-driven part of the humanoid skin.

When AccuRIG cloud export is unavailable but the local **Calibrate** preview
works, its successful rig is cached in `Saved/AccuRig/.../accurig_offset.iAvatar`
and `accurig.glb`. Convert the cached GLB locally with
`ConvertAccuRigGlbToUnrealFbx.py`, then run `AuditFbxSkinWeights.py`. The valid
Prince export has 48,894 vertices, 100 deform groups, and zero unweighted
vertices. Import it into a new isolated UE candidate. Only then create a
Manny-to-Prince IK Rig / IK Retargeter and QA one idle animation before any
locomotion is connected.

### Validated manual AccuRIG export

The preferred current source is the successful user export
`Saved/AccuRig/Export/POH_Prince_AccuRig_Final.fbx`, made with **Unreal (UE5
Skeleton)** and **Character Only**. It has 37,884 vertices, 54 non-empty skin
groups, and zero unweighted vertices. It is a clean, upright A-pose and must
be imported only through `ImportAccuRigPrinceForValidation.py` to the isolated
`/Game/_Sandbox/Characters/PrinceOfHell/AccuRig` path. It must not replace the
playable NativeTripo mesh until the reference pose and a single retargeted idle
clip have passed visual QA.

### Current AccuRIG candidate state

The candidate was imported successfully on 2026-08-17 as
`SK_POHPrince_AccuRig` (118 bones) with its materials. Its UE-compatible
humanoid hierarchy was audited (`root`, `pelvis`, spine, limbs, hands and feet
all present). The isolated assets are:

- `IK_POHPrince_AccuRig` — target IK Rig with explicit humanoid chains.
- `RTG_Manny_To_POHAccuRig` — Manny-to-Prince IK Retargeter using the native
  AccuRIG rest pose, not copied Blender rotations.
- `UE58_IKQA_MM_Idle` — exactly one retargeted UE 5.8 idle sequence.

This is a **visual-QA gate**, not a runtime swap. Open only
`UE58_IKQA_MM_Idle` on `SK_POHPrince_AccuRig` and verify the character is
upright, visible, grounded and intact. If it passes, generate walk/run/jump in
small batches with the same retargeter. If it fails, keep this evidence and
adjust the IK Retargeter pose/chains; do not modify the mesh in Blender or
reintroduce direct Manny assignment.

The idle passed visual QA. The candidate now also has UE 5.8 directional
walk/jog clips, its idle/walk/run blend space, jump, falling and landing in
`RetargetedUE58_ABP`. UE's batch tool preserved the authored motion set but
does not export an Animation Blueprint asset; `PrinceAnimationRuntime`
therefore has an opt-in profile (`poh.AnimationProfile=2`) which selects the
approved clips while a production graph is assembled. It derives scale and
ground contact from the imported mesh bounds, so it has no model-specific
height offset. Profile `0` remains the existing NativeTripo fallback; profile
`1` is retired direct-Manny diagnosis and must not be used. Profile `2` is the
default runtime profile.

The AccuRIG runtime placement uses a 4 cm visual lift after bounds fitting.
This compensates for the character's hanging cloth in the imported bounds;
never reintroduce a fixed raw mesh Z offset. Per-bone motion blur is disabled
for this candidate because it produces dark trails on the cloth/telekinetic
silhouette; it does not alter lighting or shadows.

The AccuRIG target pose must remain its imported rest pose. Do not use global
chain-to-chain auto-align for this rig: its neck/head rest orientation already
matches the mesh and auto-align produces an unnatural upward gaze.

### Game Animation Sample expansion set

The local UE 5.8 Game Animation Sample vault installation is the approved
source for higher-quality traversal and transition motion. Its source assets
are migrated into this project only as a library and then retargeted through
`IK_GAS_UEFN_Mannequin` and `RTG_GAS_UEFN_To_POHAccuRig`; direct skeleton or
animation assignment remains prohibited.

The first expansion batch is isolated in
`/Game/_Sandbox/Characters/PrinceOfHell/AccuRig/RetargetedGAS_Core`:

- `GAS_M_Neutral_Crouch_Idle_Loop` — crouched idle.
- `GAS_M_Neutral_Transition_Stand_to_Crouch` — enter crouch.
- `GAS_M_Neutral_Transition_Crouch_to_Stand` — leave crouch.
- `GAS_M_Neutral_Jump_F_Land_Roll_Lfoot` / `Rfoot` — forward landing roll
  variants.

The crouch idle is wired into the temporary runtime adapter: hold **Left Ctrl**
to crouch and release it to stand. The entry/exit clips remain isolated until
their root transform is matched to the capsule change; using them early lifts
the imported mesh off the ground. This temporary key fallback will be replaced
by the production Enhanced Input action and Animation Blueprint. The roll
clips remain isolated because their root-motion timing must be paired with a
traversal action, rather than played as an in-place cosmetic clip.

The runtime automatically compensates the visual mesh for the crouched capsule
height, preserving the soles on the ground. For a rare re-export whose bounds
need a cosmetic adjustment, use the UE console command
`poh.AccuRigCrouchVisualOffset <centimetres>` while playing (for example,
`poh.AccuRigCrouchVisualOffset 2`). Default `0` is the correct baseline;
positive raises the crouched mesh and negative lowers it.

The repeatable migration and retarget scripts are
`MigrateGameAnimationSampleCoreMoves.py` (run against the vault sample) and
`RetargetGameAnimationSampleCoreMoves.py` (run against `test.uproject`).

`IK_POHPrince_Native` and `RTG_Manny_To_POHNative` are the production
retargeting pair. Manny uses `pelvis` as retarget root; Prince uses `Hip`.
The target retarget pose always starts from the native Tripo rest pose and is
then aligned chain-to-chain. This preserves Tripo bone axes and scales root
motion for the character's proportions.

They are currently **quarantined from runtime**: their package/skeleton links
validate, but visual QA found the mesh disappearing when those clips play.
Native Tripo clips remain the playable fallback until visual QA approves the
isolated IK clip generated by
`Scripts/Development/RetargetUe58IdleViaIKRig.py`. Only then may approved UE
locomotion clips be generated and connected to runtime.

If that complete stack distorts or hides the mesh, use
`RetargetUe58IdleFkIsolation.py`. It creates a separate FK-only clip without
IK, pelvis-motion, root-motion or curve-remap passes. This identifies the
faulting retarget operation without changing production assets.

## Prohibited paths

- Do not replace the native Tripo skeleton with `SK_Mannequin`.
- Do not copy Manny local rotations in Blender; the two rigs have different
  local bone axes and that deforms the mesh.
- Blender MCP is for mesh/clip inspection and deliberate cosmetic work (the
  Prince's telekinetic detached hand), never as the primary UE retargeter.

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
