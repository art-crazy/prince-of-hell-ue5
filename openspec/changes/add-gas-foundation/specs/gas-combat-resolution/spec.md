## Purpose

Ensure the prototype combat loop uses one reusable, testable damage resolution path that can later serve ordinary enemies and elites.

## ADDED Requirements

### Requirement: Melee damage resolves through gameplay effects
The project SHALL resolve a successful placeholder melee hit through the shared gameplay-effect damage path rather than by directly mutating an actor's health field.

#### Scenario: Target is in melee range
- **WHEN** the hero attacks a valid locked target within melee range
- **THEN** the target's health decreases through the shared damage path and the result is observable in the gameplay smoke test

#### Scenario: Target is invalid
- **WHEN** the hero attacks without a valid target or with a target outside melee range
- **THEN** no damage effect is applied and player control remains usable
