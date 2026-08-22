# Gameplay Camera System — controlled spike

## Status

`GameplayCameras` is enabled for this UE 5.8 project. It is an Epic **Experimental** plugin, so it is isolated from the shipping camera path.

## Boundaries

- The current Spring Arm camera remains the default player camera.
- No gameplay, input, animation, or GAS code depends on the experimental plugin.
- The spike will live in `/Game/Camera/Experimental`; its assets can be deleted without affecting the vertical slice.
- Player movement reads the active player view, not `FollowCamera`; this preserves screen-relative input if an experimental rig becomes the view target.

## Evaluation target

Create a shoulder-third-person rig with: character lower-left framing, clear forward combat space, collision-safe obstruction handling, and a blend to a lock-on rig. Compare it in `L_MovementSandbox` against the current camera before adopting it.

## Adoption gate

Adopt only if the rig is visibly better, performs within the camera budget, survives a packaged build, and does not force an experimental dependency into the release path. Otherwise retain the current C++ camera and use the results as tuning reference.
