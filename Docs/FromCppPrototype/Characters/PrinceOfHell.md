# Prince of Hell — character contract

## Gameplay identity

The player controls an undead prince whose soul manifests as hellfire in the eye sockets. His left hand is a detachable combat tool: it can fly, strike, pull objects, return to the body, and leave a fire trail.

The left hand is deliberately **not connected to the forearm by bone**. It normally hovers a few centimetres from the stump, held by disciplined telekinesis rather than anatomy. This is a character feature, not a rigging defect: the Prince is so proud of his magic that he treats an absent hand as an inconvenience only when it drifts off to inspect loot before he does.

## Visual direction

- Adult humanoid skeleton; readable skull, jaw, separated ribs and vertebrae.
- Asymmetrical blackened plate armour, charcoal/deep-blue torn cloth, weathered leather.
- Embers are emissive VFX, not permanently baked into the base-colour texture.
- The body is visually dark but the silhouette must read on a dark UE5 level.
- The detached-hand gap must read as intentional: a subtle ember/ash tether or faint telekinetic distortion bridges the left forearm and hovering hand without resembling a broken mesh seam.

## UE5 LOD0 acceptance target

| Requirement | Target |
| --- | --- |
| Pose for rigging | A-pose or T-pose, symmetrical and neutral |
| Topology | Triangles, manifold where possible; the authored left detached hand is the sole intentional floating fragment |
| Triangle budget | 60,000–90,000 (target: 80,000) |
| Materials | 1–3 PBR material slots |
| Textures | 4K master; downscale to 2K for LODs when required |
| UVs | Non-overlapping UV0 for base colour/normal/ORM; UV1 for lightmap only if required |
| Rig | Humanoid hierarchy with root, pelvis, spine, head, arms, legs, hands and feet |
| Scale | UE centimetres; character height documented on import |

## Modular telekinetic hand

The detachable left hand is an independent skeletal mesh or mesh section with a stable socket at the left forearm. It must support four states: **hovering** (the default, visibly separated), attached for close-up/cinematic fallback, projectile, and recalled. Fire, ash tether and trails are Niagara systems attached to sockets, not geometry.

The default hover offset is a small, stable art-directed gap; it must not jitter during locomotion or look like a retargeting/skinning failure. Combat can exaggerate the orbit, but the hand always preserves a readable silhouette and a clear return path to `Socket_HandDetach`.

Runtime contract: absence of `State.HandLaunched` means the intended default
**Hovering** state. `State.HandLaunched` is present only while the hand is
travelling or performing an ability; recall clears it and returns to Hovering.
`IsHandDetached()` remains a compatibility wrapper for the original prototype
API; all new code and UI use `IsHandLaunched()`.
