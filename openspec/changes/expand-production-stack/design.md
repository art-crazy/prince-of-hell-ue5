## Context

See `proposal.md` for motivation. The project is a small-team UE5.8 vertical slice with a custom skeletal hero generated as source art, a Git/LFS repository, and agents that need explicit, reviewable contracts. The existing baseline is C++ plus Blueprints, GAS, IK Rig/Retargeter, Montages and Motion Warping.

## Goals / Non-Goals

**Goals:**

- Raise animation quality without requiring a large paid motion-capture library.
- Catch content and gameplay regressions before manual playtests.
- Make performance evidence routine on the Intel Arc target PC.
- Preserve a simple, reproducible build path before adding service infrastructure.

**Non-Goals:**

- Rebuild the project from Lyra or adopt full Game Feature plugin architecture.
- Replace the working baseline with Motion Matching before a source library exists.
- Add a third-party runtime framework, cloud telemetry, multiplayer or a paid DCC subscription in this change.

## Decisions

### Animation is layered, not replaced

The baseline remains Animation Blueprint + Blend Spaces/State Machine, Montages, IK Retargeter and Motion Warping. Add Control Rig + FullBodyIK as editor/runtime corrective tools for feet, weapon/hand contact and bespoke sequences. Evaluate Pose Search/Motion Matching only in `spike/motion-matching` after at least a coherent root-motion locomotion set is imported and measured.

This follows the practical small-team pattern of shipping readable gameplay with a finite set of clips first, then increasing fidelity through data and authoring. UE's Game Animation Sample is copied neither wholesale nor into production; it is a separate, version-pinned reference project. Alternatives considered: a giant third-party animation framework adds merge and upgrade cost; hand-authored state transitions alone are simpler but scale poorly when the library grows.

### Reusable contracts over full Lyra adoption

Use C++ interfaces/components, Gameplay Tags, Data Assets and subsystem boundaries for the vertical slice. Borrow patterns from Lyra only where a bounded system needs them. Game Features and Modular Gameplay stay deferred until two independently enabled feature sets exist. This avoids the common indie failure mode of adopting a sample game's multiplayer and plugin architecture before the core loop is proven.

### Validation is local-first and engine-native

Use Python/editor validation for source and manifest rules, UE Data Validation for imported content, Automation/Functional Tests for mechanics, and screenshot comparison for visual regressions. A `Scripts/verify_project` entry point will orchestrate checks that do not need an open editor. Gauntlet remains a later packaging/session smoke-test layer after core tests work locally.

### Measure, then optimise

Create per-gate Unreal Insights and Memory Insights captures, use on-screen stat commands for rapid diagnosis, and use RenderDoc only for a specific rendering issue. GPU failures record the Intel driver version and UE logs; no registry/TDR changes are made as a workaround. Alternatives considered: external telemetry or permanent GPU debugging add cost/noise before a playable build exists.

Every production promotion also declares a local budget: expected CPU/GPU frame-time, memory impact, active-instance limit and a fallback. The vertical-slice target is stable 60 FPS in representative combat, not an editor-idle or empty-map average.

### CI and DCC spending are threshold decisions

GitHub Actions on a self-hosted Windows runner begins after local unattended verification works. Unreal Build Accelerator stays local/default; a remote cache is not justified by one workstation. Blender remains required. Commercial Houdini is considered only for reusable procedural environment or VFX tooling. Substance 3D Painter is the first paid art candidate after the hero's source mesh, UVs and material slots pass QA. Cascadeur or video mocap requires a time-boxed hand-action/locomotion comparison and a licence review.

### Save data remains narrow and versioned

When soul transfer and the first choice are implemented, one versioned SaveGame data asset records choice flags and vessel state. Gameplay Tags identify states; save data stores stable identifiers, not runtime object references.

## Risks / Trade-offs

- [Motion Matching consumes content production time and memory] → Require a fixed clip inventory, profiling capture and baseline fallback before adoption.
- [Automated UE tests become flaky] → Keep smoke tests short, deterministic and separate slow visual/performance captures from every-commit checks.
- [Generated character rig is unsuitable] → Treat Blender/rig QA and retarget test as a gate before buying animation tools or making final clips.
- [Self-hosted CI disrupts the workstation] → Run it only on demand initially and keep artifacts/cache outside Git.
- [Paid DCC tool adds recurring cost without quality gain] → Use a time-boxed paid-tool comparison against Blender plus engine-native tools.

## Migration Plan

1. Update durable stack and animation documents with the accepted decisions.
2. Add engine plugins and test configuration only after UE5.8 installation and a C++ project exist.
3. Create the local verification entry point; prove it on a clean checkout.
4. Run the animation and performance spikes on branches; accept or remove each based on the criteria in the tasks.
5. Roll back any rejected spike by disabling its plugin/configuration and retaining baseline assets and tests.
