# Agent instructions

Read [Docs/AI/SUBAGENT_WORKFLOW.md](Docs/AI/SUBAGENT_WORKFLOW.md) before delegating work.

- The active foundation is the UE 5.8 Third Person template; retain its camera, input and collision pipeline.
- Treat `.uasset`, `.umap`, `Config/`, `*.uproject`, and Unreal Editor/commandlets as single-writer resources.
- Keep changes inside the assigned file ownership boundary; report a conflict instead of editing another agent's area.
- Validate every change and return only changed paths, validation, and blockers.
