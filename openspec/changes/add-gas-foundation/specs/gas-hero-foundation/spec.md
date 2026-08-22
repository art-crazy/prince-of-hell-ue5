## Purpose

Provide a reusable, observable hero resource foundation for the vertical slice before final mesh, animation and UI assets are available.

## ADDED Requirements

### Requirement: Hero resources are initialized and observable
The playable hero SHALL expose Health, Stamina, Soul and HandIntegrity as initialized runtime resources with a concise debug output path.

#### Scenario: Arena starts
- **WHEN** the prototype arena gives control to the hero
- **THEN** all four resources have valid current and maximum values and their state can be inspected in runtime logs

#### Scenario: Resource change is bounded
- **WHEN** a gameplay action changes a resource beyond its permitted range
- **THEN** the resulting current value remains within zero and its configured maximum
