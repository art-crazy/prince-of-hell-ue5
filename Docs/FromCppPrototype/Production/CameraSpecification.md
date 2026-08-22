# Combat camera

The prototype uses a stable native UE third-person camera rather than the
experimental Gameplay Camera System. Its framing is deliberately close to a
Souls-like combat view: the spring-arm pivot is at the upper torso, the camera
is slightly over the right shoulder, and the character occupies the lower third
of the screen. This leaves readable space for threats and the level ahead.

Current baseline (editable under **Project Settings → Prince of Hell Prototype → Camera**):

- arm length: 260 cm;
- pivot: 72 cm above the capsule origin;
- shoulder offset: 72 cm right;
- field of view: 70 degrees;
- collision probe: 12 cm; camera collision is always enabled;
- positional smoothing: 18 speed, clamped to 32 cm; rotation is direct so
  mouse input remains responsive.

The spawn view begins 10 degrees down, then belongs entirely to player input.

The Q lock-on owns control yaw while a valid target is locked. Free movement is
always evaluated from the rendered camera's horizontal forward/right vectors.
Any future camera system replacement must preserve those two contracts and pass
the movement sandbox smoke test.
