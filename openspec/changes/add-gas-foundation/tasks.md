## 1. GAS runtime foundation

- [x] 1.1 Add native hero ability-system and attribute-set classes for Health, Stamina, Soul and HandIntegrity with bounded values.
- [x] 1.2 Initialize the hero's ability system, stable state tags and a concise resource debug path without presentation dependencies.

## 2. Shared combat and signature state

- [x] 2.1 Add a reusable instant damage gameplay effect and route placeholder melee resolution through it.
- [x] 2.2 Route hand detach/recall and the unavailable soul-transfer path through the shared ability state while preserving safe outcomes.

## 3. Verification and handoff

- [x] 3.1 Extend deterministic gameplay smoke coverage for initialized attributes, effect damage, bounded values and unavailable transfer.
- [x] 3.2 Build, run the full local verification and document the GAS foundation boundary for future Blueprint content.
