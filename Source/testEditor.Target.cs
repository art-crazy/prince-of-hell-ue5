using UnrealBuildTool;
using System.Collections.Generic;

public class testEditorTarget : TargetRules
{
	public testEditorTarget(TargetInfo Target) : base(Target)
	{
		Type = TargetType.Editor;
		DefaultBuildSettings = BuildSettingsVersion.Latest;
		IncludeOrderVersion = EngineIncludeOrderVersion.Latest;

		ExtraModuleNames.Add("test");
	}
}
