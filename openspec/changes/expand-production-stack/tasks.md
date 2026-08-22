## 1. Durable decisions

- [x] 1.1 Update the technical stack and animation plan with the accepted baseline, deferred systems and spike acceptance criteria.
- [x] 1.2 Add an animation-source record template to the asset manifest and document sandbox-to-production promotion.
- [x] 1.3 Record the target-PC profiling protocol, including Intel driver version, frame-time budget and trace storage location.

## 2. UE project foundation

- [x] 2.1 Create the UE5.8 C++ project and enable Control Rig, FullBodyIK, Data Validation, Automation/Functional Testing and required existing gameplay plugins.
- [x] 2.2 Create a sandbox content area, a production asset validation rule set and a commandlet/editor entry point that reports failures.
- [x] 2.3 Create a minimal test map and deterministic smoke test that proves the project launches and the player pawn accepts input.

## 3. Animation quality spike

- [x] 3.1 Acquire the UE Game Animation Sample as a separate reference project and record its engine version and licence applicability without copying content to production.
- [ ] 3.2 Import a licensed prototype locomotion set into sandbox content, verify root motion and retarget it to the hero test skeleton.
- [ ] 3.3 Build a Control Rig plus FullBodyIK correction test for foot contact and the detached-hand socket; capture debug evidence.
- [ ] 3.4 Run `spike/motion-matching` with a fixed root-motion clip set, a Pose Search database and an Unreal Insights capture; accept it only if responsiveness, memory and frame-time criteria beat or match the baseline.
- [ ] 3.5 Remove or merge the motion-matching spike according to its recorded outcome while preserving a runnable baseline branch.

## 4. Verification and observability

- [x] 4.1 Add `Scripts/verify_project` to run repository checks, asset-manifest validation and available unattended UE tests from one documented entry point.
- [x] 4.2 Add Automation/Functional smoke coverage for hero spawn, input, hand detach/recall and soul-transfer state as each mechanic is implemented.
- [x] 4.3 Add screenshot-comparison and Unreal Insights/Memory Insights capture instructions; keep traces and review images out of Git unless selected as release evidence.
- [x] 4.4 Document RenderDoc and GPU-crash triage, including logs, device-removed detection and driver reproduction data; do not change Windows TDR values as a fix.

## 5. Build readiness and review

- [x] 5.1 Verify the complete local check from a clean checkout with Git LFS content and record prerequisites/failure modes.
- [ ] 5.2 Add an on-demand self-hosted Windows GitHub Actions workflow only after the local check completes unattended.
- [ ] 5.3 Run a vertical-slice gate capture and review the data before introducing remote UBA caching, paid DCC subscriptions, animation libraries or external telemetry.
