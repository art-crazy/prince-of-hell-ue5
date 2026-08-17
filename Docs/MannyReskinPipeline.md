# UE Manny reskin pipeline

## Blender MCP

Interactive Blender work uses the `dcc-mcp-blender` extension (v0.2.1), which starts a local MCP server when Blender launches. An agent may need to reconnect after Blender starts before its tools become available.

The repeatable reskin pipeline deliberately runs Blender with `--factory-startup`: asset builds must not start interactive MCP add-ons or depend on UI state. This keeps FBX export deterministic.

## Goal

Replace the arbitrary Tripo skeleton with the UE 5.8 Manny deform hierarchy,
so the Prince can use UE animations directly. This eliminates the fragile
retargeting path that made the mesh disappear.

## Safety rules

- The existing `NativeTripo` mesh remains the playable fallback.
- The pipeline outputs only to `Saved/ReskinPipeline`; it does not overwrite a
  `.uasset`, map, Blueprint or the runtime subsystem.
- Import is permitted only after the candidate passes the structural validator.
- The FBX armature object must be exactly `Armature`; any custom armature node
  is rejected because UE interprets it as a missing skeleton bone.
- The first UE import must go to `/Game/_Sandbox/Characters/PrinceOfHell/MannyCandidate`.
  It must reference `/Game/Characters/Mannequins/Meshes/SK_Mannequin`.

## Run

From PowerShell:

```powershell
& 'C:\Users\artcr\Documents\Unreal Projects\test\Scripts\Reskin\BuildPrinceMannyCandidate.ps1'
```

The script writes its output to:

- `Saved/ReskinPipeline/POH_Prince_MannyCandidate.fbx`
- `Saved/ReskinPipeline/POH_Prince_MannyCandidate.report.json`
- `Saved/Logs/PrinceMannyReskin.log`

## Validation gates

1. Blender validator: exactly one armature, every reachable Manny deform bone,
   and core Manny vertex-weight groups.
2. UE import validation: import as a new skeletal mesh using `SK_Mannequin`.
   Reject on a generated duplicate skeleton. A current UE 5.8 Interchange
   warning about bind-pose merging is tracked as a blocker until visual QA.
3. Direct-asset check: assign `/Game/Characters/Mannequins/Anims/Unarmed/MM_Idle`
   to the candidate mesh in a preview window. The mesh must remain visible.
4. Runtime check: update the character only after idle, walking, running,
   jump, fall and landing all pass manual QA.

## UE isolated import

Run these only after the Blender gate passes. The first script imports only to
the sandbox candidate path and fails if UE creates another skeleton:

```powershell
$project = 'C:/Users/artcr/Documents/Unreal Projects/test/test.uproject'
$editor = 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
& $editor $project -run=pythonscript -script='C:/Users/artcr/Documents/Unreal Projects/test/Scripts/Reskin/ImportPrinceMannyCandidate.py' -unattended -nullrhi
& $editor $project -run=pythonscript -script='C:/Users/artcr/Documents/Unreal Projects/test/Scripts/Reskin/ValidatePrinceMannyCandidate.py' -unattended -nullrhi
```

Close Unreal Editor before executing a commandlet: `.uasset`, maps, config and
all editor/commandlet tasks are single-writer resources.

If UE logs a bone-tree merge error, the candidate is rejected even when its
asset points to `SK_Mannequin`. Run `ExportMannyForReskin.py` first and rebuild
from `Manny_ExactUE58.fbx`; this exact-FBX route is the release path.

## Expected visual caveat

The first pass transfers Tripo weights onto Manny's closest deform bones;
Tripo twist weights are merged into their parent limbs. It is a correctness-first candidate: it
should be visible and animate. Any local deformation artifacts are refined in
Blender only after the direct Manny animation gate passes.

## Isolated in-game verification

The runtime default remains the stable Tripo model. For an A/B verification of
the isolated candidate, open the UE Output Log console before starting PIE and
enter:

```
poh.UseMannyCandidate 1
```

Then start PIE and verify idle, walking, sprinting, jumping, falling and
landing. Logs use the `POH_RUNTIME_ANIMATION_*` prefix. Restart the editor (or
set the variable back to `0` before the next PIE world) to return to stable
Tripo. Do not promote this candidate until visual QA passes and the UE import
warning is eliminated.
