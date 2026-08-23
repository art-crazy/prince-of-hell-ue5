using UnrealBuildTool;
using System.Collections.Generic;

public class testTarget : TargetRules
{
	public testTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Game;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;

		ExtraModuleNames.Add("test");
	}
}
