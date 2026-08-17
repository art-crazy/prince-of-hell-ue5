"""Import the real-axis Manny candidate without touching the old candidate."""
import runpy

# The base importer is deliberately data-only, so reuse its structural checks
# with an isolated source and destination.
globals_dict = {
    "SOURCE": r"C:\Users\artcr\Documents\Unreal Projects\test\Saved\ReskinPipeline\POH_Prince_ExactMannyCandidate.fbx",
    "DESTINATION": "/Game/_Sandbox/Characters/PrinceOfHell/ExactMannyCandidate",
    "NAME": "SK_POHPrince_ExactMannyCandidate",
}
source = r"C:\Users\artcr\Documents\Unreal Projects\test\Scripts\Reskin\ImportPrinceMannyCandidate.py"
code = compile(open(source, encoding="utf-8").read(), source, "exec")
exec(code, globals_dict)
