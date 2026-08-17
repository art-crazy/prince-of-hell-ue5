# Blender MCP: animation brief for the Prince

## Decision

Do **not** replace the Prince's native Tripo skeleton with Manny. The mesh is
authored and weighted for its native skeleton; replacing it through FBX loses
bone bases and creates explosive deformations. UE 5.8 animation is instead
retargeted and baked onto the native skeleton in Blender, one clip at a time.

Blender MCP is an interactive DCC control layer, not an animation generator.
It is used to inspect the source armature, create constraints, bake a result,
and export a reviewable FBX. Every generated clip is imported into an isolated
UE sandbox and manually reviewed before it is used at runtime.

## Character-specific rules

- The Prince is a dark-armoured skeletal warrior: heavy, deliberate weight
  shifts; no cartoon bounce or rubbery spine.
- One arm is intentionally detached and held by telekinesis. It must never be
  welded visually to the shoulder during animation.
- That hand follows the shoulder with a small delayed arc, a subtle hover and
  a restrained finger curl. Its offset is a deliberate character cue, not an
  import error.
- Keep the silhouette readable: cloak, armour plates and separated hand must
  not intersect aggressively in the first three locomotion clips.
- Root motion stays disabled for ordinary locomotion. The UE CharacterMovement
  component owns translation; baked clips animate pose only.

## Clip order

1. Idle: the baseline visibility and bind-pose test.
2. Walk forward: confirms hips, legs, feet and facing.
3. Jog forward: confirms pelvis/spine rotation under speed.
4. Jump start and fall loop: only after locomotion passes.
5. Landing, dash, attacks, traversal and the floating-hand accent layer.

Do not work on two clips simultaneously. A failure must be attributable to a
single source clip, mapping, or bake step.

## Agent prompt: inspect and prepare

```text
Open the native Tripo Prince FBX in Blender. Do not alter geometry, materials,
the original armature, or existing vertex weights. Inspect the armature and
write a report listing every deform bone, parent, rest-pose orientation, bone
length, mesh binding modifier, and unused/non-deform nodes. Validate that all
vertices have normalized weights and identify the detached hand chain. Create
only a non-destructive retarget workspace: a separate collection for a UE
source animation and an empty constraints layer. Do not export or overwrite
any game asset. Report findings and wait for the selected UE source clip.
```

## Agent prompt: retarget one UE clip

```text
Retarget exactly one UE 5.8 source animation to the native Tripo Prince
armature. Preserve the Tripo mesh, materials, skeleton names, hierarchy and
weights. Use a separate source collection and constraints only; never replace
the Tripo armature with Manny. Map hips, spine, neck, head, clavicles, upper
arms, forearms, hands, thighs, calves, feet and toes by anatomical meaning.
Bake pose animation to a duplicate of the native armature at the source frame
rate, with root translation removed. The detached telekinetic hand must retain
its authored shoulder-relative offset, trail the shoulder slightly, and never
snap into the torso. Validate frames 0, midpoint and final frame for stretched
vertices, inverted limbs, foot penetration and cloak/armour intersections.
Export only the baked animation FBX to the requested sandbox path; do not
overwrite the playable character or UE assets. Return the mapping and QA
report.
```

## UE acceptance gate

Each animation must be imported against the native Tripo skeleton into
`/Game/_Sandbox/Characters/PrinceOfHell/NativeTripo/RetargetedUE58`. It passes
only when the mesh is visible in idle, has no vertex explosion, keeps feet and
hands anatomically plausible, and plays correctly in a UE preview before any
runtime reference changes.
