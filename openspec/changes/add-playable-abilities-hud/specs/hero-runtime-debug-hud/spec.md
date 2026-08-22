## Purpose

Make the vertical-slice hero state observable in play without relying on logs or final UI art.

## ADDED Requirements

### Requirement: Runtime hero state is visible
The project SHALL show the hero's core resources and key action state in the prototype arena.

#### Scenario: Arena starts
- **WHEN** the player enters the prototype arena
- **THEN** the HUD displays valid Health, Stamina, Soul, HandIntegrity and lock/hand state
