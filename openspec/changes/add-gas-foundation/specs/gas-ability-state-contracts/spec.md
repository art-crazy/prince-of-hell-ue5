## Purpose

Keep the detachable-hand and soul-transfer mechanics safe while moving their runtime state onto the shared ability foundation.

## ADDED Requirements

### Requirement: Signature ability state is shared and safe
The project SHALL expose hand detach, hand recall and soul transfer through the shared ability foundation while preserving their existing stable gameplay tags and safe unavailable behavior.

#### Scenario: Hand state changes
- **WHEN** the hero detaches or recalls the hand
- **THEN** the shared runtime state and corresponding gameplay tag agree on the resulting condition

#### Scenario: No soul vessel exists
- **WHEN** the hero attempts soul transfer without a valid vessel
- **THEN** the action fails without consuming resources, disabling input or corrupting hand state
