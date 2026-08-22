## Why

The prototype loop currently keeps health, hand state and combat outcomes in isolated placeholder logic. A small Gameplay Ability System foundation is needed now so damage, stamina and the signature hand/soul actions share authoritative, observable state before final character art arrives.

## What Changes

- Add a hero `AbilitySystemComponent` and an attribute set for Health, Stamina, Soul and HandIntegrity.
- Route the existing placeholder melee damage through a reusable gameplay-effect path.
- Define minimal C++ ability contracts for hand detach, hand recall and soul transfer; unavailable transfer remains safe.
- Expose a compact runtime debug readout/log and extend the deterministic smoke test for attribute changes and failure-safe ability activation.
- Do not add binary assets, new plugins or a production animation dependency.

## Capabilities

### New Capabilities

- `gas-hero-foundation`: A single-player hero exposes initialized GAS attributes and safe ability activation contracts for the vertical slice.
- `gas-combat-resolution`: Placeholder combat applies and validates damage through GAS rather than directly mutating an actor field.
- `gas-ability-state-contracts`: Existing hand and soul placeholder actions retain their outcomes while becoming GAS-backed.

### Modified Capabilities

- None.

## Impact

Changes C++ runtime classes, gameplay tags, deterministic smoke coverage and the ability contract specification. The existing `GameplayAbilities`, `GameplayTags` and `GameplayTasks` modules are already enabled; no new asset, service, license or LFS payload is introduced. Rollback removes the new component/attribute classes and preserves the current placeholder loop.
