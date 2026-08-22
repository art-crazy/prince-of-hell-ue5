## Context

See `proposal.md`. The project has a compiled UE5.8 C++ shell, a deterministic map smoke test and no approved hero mesh or animation library.

## Goals / Non-Goals

**Goals:** a controller-safe Manny placeholder, reusable C++ gameplay contracts, data-driven inputs/tags and a graybox test arena.

**Non-Goals:** final combat tuning, production animation assets, Motion Matching, final VFX/UI, or promotion of any placeholder mesh.

## Decisions

- Use the engine Manny only as a presentation placeholder; C++ owns state and action rules, while future Blueprint assets configure values and presentation.
- Add abilities in the vertical-slice order: locomotion/camera → target/dodge/melee → hand state → soul state. This isolates failures and preserves a playable baseline.
- Use Gameplay Tags for `State.HandDetached`, `State.SoulTransferring`, `Ability.Hand.Detach`, `Ability.Hand.Recall` and `Ability.Soul.Transfer`; do not couple state to a skeletal-mesh socket.
- Make the first arena interaction and target dummy lightweight actors. GAS integration follows once its base component/attribute setup can be smoke-tested; avoid a large Lyra-style framework.

## Risks / Trade-offs

- [Manny animations mask final rig issues] → treat retarget/rig QA as a later explicit gate.
- [Placeholder code becomes art-specific] → require interfaces/tags rather than mesh references.
- [Systems grow before the loop is fun] → keep exactly one attack, one dummy and one interaction until a playtest.

## Migration Plan

1. Build and smoke-test the placeholder loop.
2. Import approved hero into sandbox and test retargeting.
3. Replace only mesh/animation bindings after validation; retain C++ contracts and tests.
4. Roll back by selecting Manny bindings if the imported hero fails QA.
