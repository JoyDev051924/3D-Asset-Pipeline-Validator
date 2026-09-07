// Copyright (c) 2026 Marko Stankovic. MIT License.

using UnrealBuildTool;

public class BlenderBridgeEditor : ModuleRules
{
	public BlenderBridgeEditor(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[]
		{
			"Core",
		});

		PrivateDependencyModuleNames.AddRange(new string[]
		{
			"CoreUObject",
			"Engine",
			"InputCore",
			"Slate",
			"SlateCore",
			"UnrealEd",
			"ToolMenus",
			"Projects",
			"WorkspaceMenuStructure",
			"PythonScriptPlugin",
		});
	}
}
