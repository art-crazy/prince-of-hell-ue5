"""Build the isolated production AnimBP from UE's authored graph.

The C++ helper replaces only animation references with their AccuRIG IK
Retargeter outputs. No playable map, pawn or legacy test asset is modified.
"""

import unreal


if not unreal.PrinceAnimationGraphLibrary.rebind_accu_rig_ue58_graph():
    raise RuntimeError("AccuRIG UE58 AnimGraph rebind failed; see POH_ANIMGRAPH_BUILD logs")

unreal.log_warning("POH_ANIMGRAPH_BUILD_PYTHON_VALIDATED")
