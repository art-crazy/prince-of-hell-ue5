## Purpose

Provide a repeatable, measurable path from licensed source animation to responsive player movement and signature hand actions without making an experimental animation system a hidden dependency.

## ADDED Requirements

### Requirement: Animation sources have an explicit provenance and readiness record
The project SHALL record the source, licence status, skeleton target, root-motion status and intended use of every animation library or imported clip before it is used outside a sandbox.

#### Scenario: Prototype clip is evaluated
- **WHEN** a new locomotion or combat clip is imported for evaluation
- **THEN** it remains in a sandbox with its source and intended prototype use recorded

#### Scenario: Source licence is unknown
- **WHEN** the source or licence status of a clip cannot be verified
- **THEN** the clip MUST NOT be promoted to production content

### Requirement: Player animation has a stable baseline and an isolated fidelity path
The project SHALL keep the Animation Blueprint, Montages, IK retargeting and Motion Warping path runnable while a higher-fidelity locomotion experiment is evaluated separately.

#### Scenario: Motion-matching spike is rejected
- **WHEN** the spike lacks a sufficient root-motion library or misses its performance target
- **THEN** the playable character continues to use the baseline animation path without broken input or combat actions

### Requirement: Signature hand actions are corrected and debugged before acceptance
The project SHALL provide a reviewable rig/IK correction path and visual debug for detach, launch, recall and reattach actions.

#### Scenario: Hand reattach is reviewed
- **WHEN** a hand reattach montage is played on the target skeletal mesh
- **THEN** the reviewer can inspect socket alignment and contact without altering the source mesh

