## Purpose

Ensure any developer or agent can verify the project from a clean checkout before the team invests in continuous-integration infrastructure.

## ADDED Requirements

### Requirement: Local verification has one documented entry point
The project SHALL provide one documented local command or script that checks the text configuration, required asset metadata and available automated tests without relying on an editor cache.

#### Scenario: Clean checkout is verified
- **WHEN** a contributor obtains a clean checkout with required LFS content
- **THEN** they can run the documented verification entry point and receive a pass, fail or explicit prerequisite error

### Requirement: CI adoption is gated by unattended local verification
The project SHALL not introduce a self-hosted CI runner until the local verification entry point completes unattended on the development machine.

#### Scenario: Verification requires manual interaction
- **WHEN** the local verification flow waits for an editor dialog or other user action
- **THEN** CI setup remains deferred and the manual dependency is recorded

### Requirement: Build artifacts and caches remain separated
The project SHALL retain build logs and review artifacts outside versioned source paths while keeping only reproducible configuration, scripts and selected source assets in Git.

#### Scenario: Build produces generated data
- **WHEN** a local build or test creates cache, trace or packaged output
- **THEN** the generated output is excluded from Git unless explicitly selected as a release artifact

