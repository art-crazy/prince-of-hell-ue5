# Target-PC profiling protocol

## Goal

Vertical-slice gates target stable **60 FPS**, which is a 16.67 ms frame-time budget. The target machine is recorded in every capture; current graphics driver baseline is **Intel Arc 32.0.101.8864**. Record the exact driver, UE version, Windows version, resolution, scalability preset and commit SHA again with each capture.

Performance is a feature acceptance criterion. A new gameplay system, animation set, Niagara effect, material or AI behavior MUST declare a measurable budget before production promotion: expected CPU/GPU frame-time impact, memory impact, active-instance limit and its fallback (LOD, culling, pooling, lower quality tier or removal). An attractive effect that causes reproducible hitches is not accepted as production-ready.

## Capture workflow

1. Use a packaged Development build or Standalone Game; close applications that compete for GPU memory.
2. Reproduce a named test-map route three times after shader warm-up. Record `stat unit`, `stat gpu`, `stat game` and the test route name.
3. Capture CPU/GPU timings with Unreal Insights. For memory investigations, run a separate capture with `-trace=default,memory` and inspect it in Memory Insights.
4. Store raw `.utrace`, `.ucache`, screenshots and RenderDoc captures under local `PerformanceCaptures/<date>-<commit>/`. This directory is ignored by Git; commit only a short Markdown/CSV gate report when evidence must be retained.
5. A gate passes only when the representative capture meets the budget and no single reproducible hitch/crash is hidden by an average.

## Review rule

Profile in a representative fight with the hand, enemy AI, VFX, UI and environment active. Empty-map screenshots, editor idle frame rate and average FPS alone do not prove performance. If the 60 FPS budget is missed, identify the dominant cost first, then reduce/optimise that cost; do not mask it by changing Windows TDR settings or disabling diagnostic tools.

## Visual comparison procedure

Screenshot comparison is a review gate, not an every-frame automated test yet.
For a candidate visual change:

1. Use the named prototype map and a documented camera transform, resolution,
   scalability preset, RHI and console-variable set.
2. Capture a `before` and `after` image after shaders have warmed up. Keep
   dynamic time of day, random seeds and transient debug overlays fixed or
   explicitly record why they differ.
3. Put both review images and any image-diff output in
   `PerformanceCaptures/<date>-<commit>/Visual/`; never add raw captures to
   Git. A selected release-evidence image may be committed only with a compact
   report explaining why it is representative.
4. Review silhouette readability, UI legibility, material response, VFX
   visibility and unwanted differences. Record pass/fail plus the capture path
   in the gate report.

## Insights capture commands

Use an explicit trace directory outside Git for a repeatable capture:

```text
UnrealEditor.exe PrinceOfHell.uproject -trace=default,frame,gpu,bookmark -tracefile="<absolute>\PerformanceCaptures\<date>-<commit>\Baseline.utrace"
UnrealEditor.exe PrinceOfHell.uproject -trace=default,memory -tracefile="<absolute>\PerformanceCaptures\<date>-<commit>\Memory.utrace"
```

Open the first trace in Unreal Insights for CPU/GPU/frame analysis and the
second in Memory Insights. Each report records the route, build commit, UE
version, driver, capture command, peak memory and the worst representative
frame; raw `.utrace` and `.ucache` files remain ignored.

## Rendering and GPU-crash triage

- For a visual rendering issue, capture one reproducible frame in RenderDoc and record map, camera position, RHI and driver version.
- For `DXGI_ERROR_DEVICE_REMOVED`, GPU timeout or OOM, preserve the recent `Saved/Logs` file, reproduction steps, UE version and driver version. Reproduce with `-gpucrashdebugging` only when needed; do not combine it with other debug switches.
- Do not alter Windows TDR registry values as a workaround. First isolate the pass, content, VRAM pressure, driver or external application involved.

## References

- [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)
- [Memory Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/memory-insights-in-unreal-engine)
- [Performance profiling](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine)
- [GPU crash debugging](https://dev.epicgames.com/documentation/unreal-engine/dealing-with-a-gpu-crash-when-using-unreal-engine)
