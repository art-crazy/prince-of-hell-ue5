# Character pipeline

## Source of truth

`SourceArt/Characters/PrinceOfHell/` is for the original downloadable FBX/GLB and its texture bundle. Never overwrite it. Work on a copy in Blender.

## Import sequence

1. Verify the downloaded mesh using the asset manifest validator.
2. In Blender: apply transforms, inspect normals, UVs, materials and disconnected pieces.
3. Produce a UE-ready LOD0 under the triangle contract; retain the high-poly source only for baking/reference.
4. Create LOD1 (roughly 45–55% of LOD0) and LOD2 (roughly 20–30% of LOD0).
5. Confirm a humanoid skeleton, then import to UE5 as a Skeletal Mesh.
6. Create an IK Rig and an IK Retargeter against UE5 Manny.
7. Add a socket to the left forearm and test the detachable-hand Blueprint.

`Scripts/validate_asset_manifest.py` validates the actual recorded pipeline
state. It distinguishes a source ready to import, a sandbox asset that still
requires retargeting, and a production-approved asset; it must not report an
already imported source as merely ready for import.
For an imported asset it also verifies that both immutable FBX exports and the
recorded UE `.uasset` files exist locally and are not unfetched Git LFS
pointers.

## QA gates

- No un-applied non-uniform scale.
- No missing PBR texture maps or material slots.
- No visible foot sliding in idle/walk/run after retargeting.
- Hand projectile can detach, collide, recall and reattach without a transform pop.
- LOD transitions preserve the silhouette of skull, shoulders, rib cage and hand.

## Current Tripo source QA

The exported 2026-08-16 source is stored immutably under
`SourceArt/Characters/PrinceOfHell/Tripo/2026-08-16/` with its original ZIP,
FBX, and 4K PBR texture bundle in Git LFS. Blender 5.2 inspection found two
mesh objects, 76,100 triangles, 37,892 vertices, UV0 and two material slots.
The original source has **no armature**, so it remains a mesh/material reference.
Tripo Auto-Rig v2.5 subsequently produced a separate immutable derivative at
`SourceArt/Characters/PrinceOfHell/Tripo/2026-08-16/Rigged/`: Blender found one
humanoid armature with 41 bones while preserving the validated geometry and
materials. The derivative was imported on 2026-08-16 into
`/Game/_Sandbox/Characters/PrinceOfHell/SK_POHPrince_TripoRig` with a separate
UE Skeleton and imported PBR maps. Retarget and visual review are still
required before production promotion.

The reproducible UE sandbox QA script, `Scripts/validate_tripo_prince.py`,
passed on 2026-08-16: the mesh resolves to its UE Skeleton, has 41 bones and
one bound material slot. UE Data Validation also completed with zero errors
and zero warnings.

Official Unreal MCP inspection on 2026-08-16 confirmed the imported LOD0 has
48,351 render vertices, one section, one material slot and **one LOD only**.
This is acceptable for a sandbox animation target but is a hard promotion gate
for the hero: author LOD1 (roughly 45–55% of LOD0) and LOD2 (roughly 20–30%)
from the cleaned Blender source, then visually check skull, ribs, shoulders
and the telekinetic hand silhouette at each transition. Do not apply blind
automatic reduction to the current sandbox mesh: its visual quality is still
the reference against which the authored LODs must be compared.

The sandbox IK Rig is `/Game/_Sandbox/Characters/PrinceOfHell/Rigging/IK_POHPrince`.
It maps the Tripo skeleton's pelvis as the retarget root and `Root` as the
root-motion bone, with Spine, arm, leg, foot and neck chains. A licensed
locomotion source and its retargeter remain required before production
promotion; the Game Animation Sample is still reference-only.

`Socket_HandDetach` is attached to `L_Forearm` with an identity offset on the
sandbox mesh. Its final position is intentionally deferred until a retargeted
animation can be reviewed; this avoids baking an unverified visual offset into
the source character contract.

The UE-generated Physics Asset is bound to the sandbox mesh for collision and
ragdoll prototyping. It remains sandbox-only until its bodies and constraints
are visually reviewed against the retargeted hero.

## Reproducible visual QA

`Scripts/create_poh_visual_qa_map.py` creates the editor-only map
`/Game/_Sandbox/QA/L_POHCharacterVisualQA`. It holds the real Tripo rig in the
retargeted idle, a neutral floor and controlled movable key/fill/rim lighting.
The script is idempotent: rerunning it updates the existing lighting setup, so
the review scene never needs a baked-light build. This is
the first review surface for proportions, materials, hand hover readability,
skin weights and future LOD transitions; it is not a gameplay map or a source
of shipping lighting. It uses `APOHVisualQAGameMode`, which intentionally
suppresses the prototype dummy/brazier encounter and command-line gameplay
smoke. Recreate the map only through
the script, then review
idle, walk and run in the Skeletal Mesh/Animation editors before promotion.

## Movement sandbox

`Scripts/create_movement_sandbox_map.py` creates `/Game/Maps/L_MovementSandbox`:
a lit, code-owned obstacle course using only Engine BasicShapes. It inherits the
project's normal `APOHGameMode`, so PIE spawns the actual Prince of Hell pawn.
Use it for collision, scale, camera clearance, movement, dodge and future
vault/climb validation. It deliberately contains no copied Game Animation
Sample content; that project remains a reference rather than a runtime
dependency.

## License gate

Do not import the Tripo source as a commercial game asset until the export and asset licence are available on the account. Houdini Apprentice outputs are also non-commercial.

## Clean-clone verification

Before importing the approved hero, run `Scripts/verify_project.ps1` from a fresh Git clone. It must build the editor target and pass data validation, map smoke and gameplay smoke before any source or imported binary asset is promoted.

Verified on 2026-08-16 from `prince-of-hell-ue5-clean-verify` at commit `0db4bfe`: the unattended check passed build, Data Validation, prototype-map smoke and gameplay smoke. The explicitly recorded `awaiting_tripo_export` manifest state is valid for this gate only.

Prerequisites are UE 5.8.1, Visual Studio 2022 Build Tools with the Windows SDK, Python 3.11+ and Git LFS. `Scripts/verify_project.ps1 -SkipUnreal` is a manifest/configuration preflight only; it cannot establish build readiness. A missing engine, unavailable `git lfs`, a failing manifest, a non-zero editor build or a smoke test without its pass marker is a hard failure. Generated `Saved`, `Intermediate` and Derived Data Cache output remains local and must not be committed.
