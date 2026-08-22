# OpenSpec workflow

OpenSpec is the shared change contract for Codex and Claude. It is mandatory for gameplay mechanics, architecture, asset-pipeline changes, new plugins, performance work and any change that alters a player-facing contract. It is deliberately optional for a typo, a formatting fix or a small isolated documentation correction.

## Daily flow

1. Explore only when the solution is unclear.
2. Propose one bounded change before implementation.
3. Review its player outcome, acceptance criteria, non-goals, asset/license impact and rollback path.
4. Implement from its tasks, validate on a test map or with an automated check, and commit the change with the implementation.
5. Archive only after the persistent specs reflect what shipped.

## Agent entry points

| Agent | Start a proposal | Other flow |
| --- | --- | --- |
| Codex | `$openspec-propose "add-hand-recall"` | `$openspec-apply-change`, `$openspec-archive-change` |
| Claude Code | `/opsx:propose add-hand-recall` | `/opsx:apply`, `/opsx:archive` |

Use an English kebab-case name that describes the outcome, not an implementation detail. Examples: `add-hand-recall`, `prototype-soul-transfer`, `import-prince-mesh`.

## Project-specific rule

An OpenSpec change cannot replace the existing production documents. `Docs/ProductionPlan.md`, `Docs/TechStack.md`, `Docs/Conventions.md` and `Docs/AssetManifest.json` remain the durable record and are updated when a completed change affects them.
