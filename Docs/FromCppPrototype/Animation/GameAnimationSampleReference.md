# Game Animation Sample — reference record

## Status

The project was saved to the Epic/Fab account library and installed locally on
2026-08-16 as a separate UE 5.8.1 reference project. The installed project is
outside this repository and no sample content has been copied into production
or sandbox content.

Planned reference location (not versioned):

```text
C:\Users\artcr\UnrealReferences\GameAnimationSample
```

Verified installed project file (not versioned):

```text
C:\Users\artcr\UnrealReferences\GameAnimationSample\GameAnimationSample.uproject
```

The Launcher reports the project as compatible with Unreal Engine 5.8. The
project file declares `EngineAssociation: 5.8`; its first UE 5.8.1 editor launch
was verified on 2026-08-16. The sample remains an external reference project.

## Observed listing metadata

| Field | Value |
| --- | --- |
| Publisher | Epic Games |
| Listing | [Fab: Game Animation Sample](https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016) |
| Compatible engine versions | UE 5.4–5.8 |
| Distribution | Complete project |
| Target platforms | Windows, macOS, Linux |
| Listing statement | UE-Only Content — use only with Unreal Engine-based products |
| AI-use flag | No |
| Intended role | Read-only learning/reference project; never a production content dependency |

The listing also links to the Fab Standard License. A minimal sandbox evaluation
was created on 2026-08-16: the UEFN mannequin mesh, its skeleton and
`M_Neutral_Idle_turn_left`, stand idle, forward walk and forward run were staged
as a minimal Asset Registry-verified selection, then retargeted to the POH Tripo
skeleton. The staging packages and temporary IK setup are removed after
conversion, leaving only the derived sandbox clips. The exact assets, licence
context and root-motion status are recorded in `Docs/AssetManifest.json`. No
sample content is treated as a production dependency until visual QA approves it.

The temporary sandbox source mesh is stripped of materials, post-process
animation, physics and LOD-settings references after import. It is used solely
for batch retargeting and is removed with the staging content, which prevents
unrelated sample dependencies from entering the project.

## Boundary

Do not copy the sample project wholesale, add it as a plugin, or reference its
assets across projects. Its architecture and animation patterns may inform our
own C++/Blueprint implementation. Any clip transfer is a separate sandbox
decision and must respect the listing's AI-use restriction: no sample content is
supplied to generative AI services.

## Installation acceptance check

The reference project was opened once through UE 5.8.1 on 2026-08-16. OpenSpec
task 3.1 is complete; importing a licensed clip into the sandbox is a separate
task and must not copy the sample wholesale.
