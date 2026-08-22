## Context

The hero owns initialized GAS attributes and input bindings. CommonUI is configured but no production UI asset exists.

## Goals / Non-Goals

**Goals:** native abilities for the four prototype actions, input activation and a minimal runtime debug HUD.

**Non-Goals:** final UI art, cooldown design, animation tasks, network replication or new plugins.

## Decisions

- C++ abilities own action validation; existing character functions become implementation helpers.
- Input activates granted ability specs using stable input tags.
- The HUD is a code-created lightweight widget with no art dependency and reads only public GAS/tag state.

## Risks / Trade-offs

- [Temporary HUD outlives usefulness] → isolate it under a Prototype category and remove after production UI acceptance.
- [Ability activation adds indirection] → keep one synchronous ability per current action and retain smoke coverage.

## Migration Plan

1. Add abilities and input activation.
2. Add debug HUD and smoke checks.
3. Build and verify; replace presentation later without changing ability contracts.
