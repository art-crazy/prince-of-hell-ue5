## Purpose

Provide a playable and measurable third-person vertical-slice loop before the final skeletal hero is available.

## ADDED Requirements

### Requirement: Placeholder player loop is playable
The project SHALL launch the prototype arena with a controllable placeholder player that can move, orient the camera, dodge, lock a nearby target and perform one melee action.

#### Scenario: Arena starts
- **WHEN** the prototype map is launched
- **THEN** the player receives the exploration/combat input context and can control the placeholder pawn

#### Scenario: No target is available
- **WHEN** the player activates lock-on with no eligible target
- **THEN** the action leaves movement and camera control usable

### Requirement: Placeholder content remains replaceable
The project SHALL keep final hero presentation independent of placeholder gameplay logic.

#### Scenario: Approved hero is imported
- **WHEN** the approved skeletal mesh replaces the placeholder
- **THEN** the player loop retains its input, ability contracts and smoke coverage
