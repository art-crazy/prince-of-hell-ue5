## Purpose

Make asset, gameplay, visual and performance regressions detectable by a small team and coding agents before they reach the main branch or a playable review build.

## ADDED Requirements

### Requirement: Production assets are validated before promotion
The project SHALL validate naming, source provenance, manifest completeness and required import properties before an asset moves from sandbox content to a production folder.

#### Scenario: Asset is incomplete
- **WHEN** an imported character asset lacks a required manifest field or violates a naming rule
- **THEN** validation reports the failing asset and blocks its production promotion

### Requirement: Core mechanics have repeatable smoke coverage
The project SHALL provide a fast smoke check for the playable test map and each completed core mechanic, with a result that can be read locally and by CI.

#### Scenario: Hand ability regresses
- **WHEN** a change prevents the player from completing detach and recall on the test map
- **THEN** the relevant smoke check fails with a reproducible log or test result

### Requirement: Performance evidence accompanies vertical-slice gates
The project SHALL retain a reproducible CPU/GPU frame-time and memory capture for each vertical-slice gate on the target PC configuration.

#### Scenario: Frame budget is exceeded
- **WHEN** a review capture exceeds the agreed frame-time budget
- **THEN** the gate report identifies the capture and marks the performance criterion as unmet

### Requirement: Rendering failures preserve actionable evidence
The project SHALL document a reproducible GPU-crash and rendering-artifact capture procedure appropriate to the active hardware and driver.

#### Scenario: GPU failure occurs
- **WHEN** a reproducible device-removed or rendering-artifact failure occurs
- **THEN** the report includes engine version, driver version, reproduction steps and the relevant log or frame capture

