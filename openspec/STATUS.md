# OpenSpec status vs. actual project state

`config.yaml` and every change under `changes/` were imported wholesale from the
separate C++ prototype repo (`prince-of-hell-ue5`, see the `f3a713e docs: import
design docs and openspec specs from main (C++ prototype)` commit). They describe a
`Source/`-based C++ project with a native GAS runtime.

**This project (`test.uproject`) has no `Source/` folder — it is Blueprint-only**
(see [`../README.md`](../README.md) and [`../AGENTS.md`](../AGENTS.md)). None of the
checked-off tasks below were implemented here; the `[x]` boxes reflect the other
repo's history, not this one.

| Change | Real status in this (Blueprint) project |
|---|---|
| `add-gas-foundation` | Not started. No native `AbilitySystemComponent`/attribute set exists here. |
| `add-playable-abilities-hud` | Not started. No native abilities or HUD exist here. |
| `core-loop-placeholder` | Partially reflected: input actions, lock-on target dummy and Gameplay Tag contracts described here do **not** exist as Blueprint content yet, except that the player pawn (`CHAR_BP_POH_MM_Final`) itself is set up. Task 1.2 (placeholder presentation binding) is genuinely unchecked/undone. |
| `expand-production-stack` | Foundation items (project/plugins/test map) are real and match this project. The animation-quality-spike and CI items (3.2–3.5, 5.2–5.3) are still open here. |

Until someone rewrites these as Blueprint-scoped changes (or the team commits to
building the C++ layer in this project), treat every checkbox in `changes/*/tasks.md`
as **unverified against `test.uproject`**, not as done work.
