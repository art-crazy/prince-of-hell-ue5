# Prince of Hell — Template Foundation

Active playable foundation: UE 5.8 Third Person template.

The original C++ prototype remains in `prince-of-hell-ue5 5.8`; this project keeps Epic's tested third-person camera, input, collision, and animation stack intact. The Prince of Hell skeletal mesh, materials, physics asset, IK rig, and existing retargeted locomotion clips live under `Content/_Sandbox`.

Next integration step: create a child of `BP_ThirdPersonCharacter`, retarget its locomotion to the Prince skeleton, then set that child as the default pawn. Do not replace the template camera system.

Parallel agent workflow: [Docs/AI/SUBAGENT_WORKFLOW.md](Docs/AI/SUBAGENT_WORKFLOW.md).

Editing Blueprints via the MCP automation bridge: read [Docs/AI/McpAutomationBridgeNotes.md](Docs/AI/McpAutomationBridgeNotes.md)
first — it lists which node types are reliable and which silently fail.

`openspec/` was imported from the separate C++ prototype repo and does not reflect
this Blueprint-only project's real state — see [openspec/STATUS.md](openspec/STATUS.md)
before trusting any checkbox there.
