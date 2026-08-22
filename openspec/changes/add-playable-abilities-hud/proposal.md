## Why

The GAS foundation is verified but player actions still enter through placeholder methods, and resources are visible only in logs. The vertical slice needs ability-owned action flow and an in-game debug readout before enemy AI adds more state.

## What Changes

- Add native Gameplay Abilities for melee, dodge, hand detach/recall and safe soul transfer.
- Route existing Enhanced Input actions into granted abilities without changing bindings.
- Add a lightweight CommonUI/UMG debug HUD for hero resources, state tags and lock target.
- Keep UI and abilities independent of final character assets; no third-party plugin or binary art is added.

## Capabilities

### New Capabilities

- `playable-hero-abilities`: Hero actions activate through the shared ability system and fail safely.
- `hero-runtime-debug-hud`: The arena exposes resources and key hero state in a lightweight runtime HUD.

### Modified Capabilities

- None.

## Impact

C++ runtime/UI classes, input routing and smoke coverage. Uses already enabled GAS and CommonUI modules. Rollback restores direct placeholder actions and removes the HUD classes.
