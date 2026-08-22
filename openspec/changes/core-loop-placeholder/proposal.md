> **Mostly not implemented in this Blueprint-only project** — imported from the C++ prototype repo. See [`../../STATUS.md`](../../STATUS.md).

## Why

The Tripo hero cannot yet be exported, but the vertical slice must prove the combat fantasy now. A UE5 Manny-based implementation lets us validate responsiveness, ability contracts and performance before art integration, then replace only the presentation layer after character QA.

## What Changes

- Add a playable third-person placeholder loop: movement, camera, lock-on, dodge, one melee action and a target dummy.
- Establish C++ GAS-ready state and ability contracts for hand detach/recall and soul transfer without making art, animation libraries or experimental animation systems dependencies.
- Add a graybox arena interaction (brazier) and a debug HUD/log path for gameplay tags and core state.
- Keep all placeholder assets under `Content/_Sandbox/` or UE starter content; no generated or third-party character art is promoted.

## Capabilities

### New Capabilities

- `placeholder-core-loop`: A playable, measurable Manny-based third-person combat loop that remains functional before the final hero is imported.
- `hero-ability-contracts`: C++ gameplay-state interfaces and tags for detachable-hand and soul-transfer systems, with safe placeholder behavior.

### Modified Capabilities

- None.

## Impact

Adds C++ gameplay classes, Enhanced Input assets/configuration, sandbox Blueprints/maps and Automation smoke coverage. Uses already enabled engine-native systems only; no new UE plugin, external runtime dependency, paid service or imported asset is introduced. Placeholder content is deleted or replaced after the approved Prince of Hell mesh is imported; the C++ contracts, tests and performance budgets remain.
