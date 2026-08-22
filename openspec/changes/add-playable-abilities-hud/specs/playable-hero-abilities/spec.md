## Purpose

Provide robust, ability-owned actions for the playable hero while the final character presentation remains unavailable.

## ADDED Requirements

### Requirement: Hero actions activate safely
The project SHALL activate melee, dodge, hand state and soul-transfer actions through the hero ability system.

#### Scenario: Input action succeeds
- **WHEN** the player invokes an eligible hero action
- **THEN** the action completes through its ability path and updates the shared runtime state

#### Scenario: Action is unavailable
- **WHEN** an action lacks a valid target or vessel
- **THEN** it fails without corrupting resources, tags or player input
