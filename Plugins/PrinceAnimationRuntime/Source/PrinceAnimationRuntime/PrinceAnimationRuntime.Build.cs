using UnrealBuildTool;

public class PrinceAnimationRuntime : ModuleRules
{
    public PrinceAnimationRuntime(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine" });
        PrivateDependencyModuleNames.Add("InputCore");
        if (Target.bBuildEditor)
        {
            PrivateDependencyModuleNames.AddRange(new[] { "UnrealEd", "AnimGraph", "BlueprintGraph", "KismetCompiler" });
        }
    }
}
