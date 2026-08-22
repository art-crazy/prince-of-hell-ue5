# Animation plan

## Prototype set

| Group | Required clips |
| --- | --- |
| Locomotion | idle, walk, jog/run, start, stop, jump, fall, land |
| Survival | light hit, heavy hit, stagger, knockdown, death |
| Combat | three-hit melee chain, charged attack, dodge, block/recovery |
| Signature hand | detach, launch, airborne loop, impact, recall, reattach |
| Presentation | inspect, taunt, interaction |

## Implementation

Use UE5 IK Rig and IK Retargeter to map source humanoid animations to the Prince. Build locomotion in an Animation Blueprint. Use Animation Montages with gameplay notifies for combat and hand actions.

The projectile hand uses a dedicated skeletal mesh component. Its baseline state is a deliberately detached telekinetic hover beside the left forearm, with a low-cost ember/ash tether. At the detach notify it expands from that hover into simulated/projectile motion; at recall it follows a spline or homing path and returns to the forearm socket.

Locomotion needs a small authored hover layer: stable gap, soft counter-motion and no collision jitter. The hand may briefly "look busy"—for example, turn palm-up at a chest or collectible—only in non-combat idle variants; readability and combat timing always win over the joke.

AI-generated clips are acceptable for blockout. Final combat needs review for readable anticipation, impact frames, recovery, root motion and foot contact.

## Quality baseline and fidelity spike

The shipping baseline is an Animation Blueprint with locomotion state/Blend Space, IK Rig/Retargeter, Montages and Motion Warping. It remains playable during all experiments.

Current sandbox baseline explicitly switches the derived idle/walk/run clips
from character speed through `DA_POHPrinceVisualProfile`. The project setting
selects the profile, while a Blueprint may override it; mesh, import offset and
sandbox animation assets can therefore be promoted or replaced without changing
gameplay code. The prebuilt `BS_POH_Locomotion` remains a validated editor asset,
but is not the runtime authority because the single-node player could retain an
idle pose on this imported skeleton. This is a temporary layer; the next
animation milestone promotes the same contract to `ABP_POHPrince` before adding
combat montages.

The current Tripo profile uses `Z=-96` and a `Yaw=-90°` correction. This aligns
the mesh's authored forward axis with UE Character forward while preserving an
upright pose. Orientation corrections belong in the visual profile, never in
pawn movement code; automated retarget QA rejects profile pitch/roll and an
unexpected yaw, and the result is visually verified in PIE whenever the import
changes.

Enable **Control Rig** and **FullBodyIK** for authored corrective layers: foot grounding, aiming/reaching, weapon contact and the detached-hand forearm socket. The correction layer must be inspectable with rig/socket debug and must not require edits to the immutable source mesh. The intentional left-hand gap is accepted only when the hover layer owns it; a gap on another limb or an unstable transform is a retarget/weighting defect.

**Pose Search / Motion Matching is not a default dependency.** It enters `spike/motion-matching` only after a licensed, coherent root-motion locomotion set exists. The spike compares the same input sequence against the baseline and records:

- responsiveness: start, stop, turn and dodge transitions are at least as readable;
- fidelity: no more visible foot slide or pose pops than the baseline;
- performance: target-PC Unreal Insights frame-time and memory are no worse than baseline within the agreed tolerance;
- fallback: disabling the spike restores the existing Animation Blueprint without broken references.

Game Animation Sample is a separate reference project, not a content dependency. Any source clip is registered in `Docs/AssetManifest.json` before leaving `Content/_Sandbox/`.

The current acquisition and licence boundary are recorded in
[`GameAnimationSampleReference.md`](GameAnimationSampleReference.md). The
reference must be installed separately and opened once before it is used for
the animation-quality spike.
