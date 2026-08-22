## Purpose

Define safe, observable contracts for the signature hand and soul mechanics before final art and animation are integrated.

## ADDED Requirements

### Requirement: Hero states are explicit
The project SHALL expose detachable-hand and soul-transfer state through stable gameplay tags and debug output.

#### Scenario: Hand state changes
- **WHEN** a placeholder hand detach or recall action completes
- **THEN** the corresponding state tag and debug state reflect the resulting condition

#### Scenario: Transfer is unavailable
- **WHEN** no valid vessel exists
- **THEN** soul transfer fails without disabling player control or corrupting state
