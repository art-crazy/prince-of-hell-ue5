## Context

See `proposal.md`. The project already enables Gameplay Ability System modules, but the hero, target dummy and hand/soul states still use isolated placeholder fields and functions.

## Goals / Non-Goals

**Goals:** add a minimal native ability-system component, an attribute set for the four vertical-slice resources, effect-based placeholder damage and deterministic verification without adding art assets.

**Non-Goals:** final ability UX, cooldown UI, network replication, a full Lyra framework, animation-driven effects, final enemy classes or content-authored ability Blueprints.

## Decisions

- The character owns its ability-system component and initializes a single default attribute set in C++. This keeps runtime rules inspectable and lets future Blueprints configure presentation without owning core state.
- Health is owned by combatants through a common interface/component boundary; placeholder melee applies a reusable instant damage gameplay effect. This replaces direct target-field mutation and avoids a hero-specific damage path.
- `State.HandDetached` and `State.SoulTransferring` remain stable public tags. Ability activation checks resources and tags before changing state, with no cost on an unavailable soul transfer.
- Attributes clamp current values to `[0, Max]`; this provides a deterministic baseline before data assets or UI tuning exist.
- The smoke test asserts initialized values, successful damage and safe failure behavior. This is the acceptance mechanism until designer-authored abilities exist.

Alternatives considered: copying Lyra's complete ability framework would add unnecessary dependency surface; keeping direct mutable health would make the future enemy and cue paths diverge.

## Risks / Trade-offs

- [C++ defaults require later balancing migration] → expose values as Blueprint defaults and defer data assets until the first content pass.
- [GAS setup can obscure simple prototype behavior] → keep exactly one damage effect and three callable signature actions, each covered by smoke.
- [Final mesh changes presentation timing] → the ability system contains no mesh or socket reference.

## Migration Plan

1. Add the native component, attributes, tags and instant damage effect.
2. Route placeholder combat and hand/soul checks through the shared state.
3. Build and run the full local verification from a clean clone.
4. Roll back by removing the new GAS classes and restoring the current placeholder paths; no binary migration is required.
