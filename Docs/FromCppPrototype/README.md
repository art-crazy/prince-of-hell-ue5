# Imported from the `main` branch (native C++ prototype)

This folder mirrors the `Docs/` tree from the `main` branch of this same
repository (`origin/main`, commit `f42fa96`), which hosts an unrelated,
native C++/GAS prototype of Prince of Hell (its own `PrinceOfHell.uproject`,
`Source/PrinceOfHell/*`, no shared git history with `template-foundation`).

That project is not the one we are actively developing — `test.uproject`
(this repo, `template-foundation` branch) is a Blueprint project built on
Epic's Third Person template, with the Prince of Hell character retargeted
onto it. It has no C++ module.

These docs are kept for reference: general design intent (character
description, production plan, tech/animation conventions) still applies.
Implementation-specific docs — in particular `Production/CameraSpecification.md`
and `Production/GameplayCameraSystemSpike.md` — describe the C++ prototype's
own camera system (Spring Arm vs. an experimental GameplayCameraRig) and do
**not** describe how the Blueprint camera in this project works today.

The matching `openspec/` change proposals (GAS foundation, playable
abilities + HUD, core loop, production stack) live at the repo root and
describe the same C++ prototype's feature specs.
