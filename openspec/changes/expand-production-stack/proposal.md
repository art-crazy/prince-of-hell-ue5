## Why

The project already has a sound UE5 gameplay stack, but its production loop needs stronger safeguards before agents and imported AI art begin to create expensive rework. Small teams and successful prototypes usually win by reusing proven engine samples, automating asset/functional checks, and treating animation and performance as measurable systems rather than late polish.

## What Changes

- Define an **animation quality foundation**: use UE's Game Animation Sample as a read-only reference; add Control Rig and Full Body IK for authored corrections; evaluate Pose Search/Motion Matching only as a bounded spike after a sufficient root-motion library exists.
- Define a **production validation and observability foundation**: UE Data Validation, Automation/Functional smoke tests, screenshot comparison, Unreal Insights/Memory Insights, RenderDoc and a reproducible GPU-crash capture procedure.
- Add a minimal **build and release lane**: local deterministic build/validation script first; GitHub Actions with a self-hosted Windows runner only after the project can compile unattended. Do not add a hosted build service or distributed compilation infrastructure yet.
- Set the **modularity boundary**: use C++ components, interfaces, data assets and Gameplay Tags now. Study Lyra as a reference, but do not copy it or turn the vertical slice into Game Feature plugins until a second independently shippable experience needs it.
- Define external DCC choices: Blender remains mandatory; a future commercial Houdini licence is for procedural environment/VFX tools; Substance 3D Painter is the first paid art-tool candidate after the hero mesh passes QA. Cascadeur, video mocap and animation libraries are evaluated per animation spike, not purchased by default.
- Add versioned SaveGame data for the vertical-slice choice and soul/vessel state when those mechanics are implemented.

## Capabilities

### New Capabilities

- `animation-quality-pipeline`: A reproducible path from source clips to a responsive, retargeted, debuggable player locomotion and hand-action setup.
- `production-validation`: Automated asset, functional, visual and performance checks with actionable local artifacts.
- `build-readiness`: A reproducible local verification lane and a documented threshold for introducing self-hosted CI.

### Modified Capabilities

- None.

## Impact

Affected areas are `Docs/TechStack.md`, `Docs/Animation/AnimationPlan.md`, the future UE project configuration, editor automation scripts, CI configuration, and the asset manifest. New engine plugins are limited to Control Rig, FullBodyIK, Data Validation and Automation/Functional Testing; Pose Search is spike-only. No third-party runtime plugin, paid service, generated asset or binary content is added by this planning change. Each imported sample asset must be separately checked against its Fab/UE licence and recorded in the manifest. Rollback is straightforward: disable added engine plugins and retain the existing Animation Blueprint plus Montages/Motion Warping baseline.
