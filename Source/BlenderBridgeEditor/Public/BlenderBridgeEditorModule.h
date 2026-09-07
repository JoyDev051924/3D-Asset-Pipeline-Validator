// Copyright (c) 2026 Marko Stankovic. MIT License.

#pragma once

#include "CoreMinimal.h"
#include "Modules/ModuleManager.h"

/**
 * Editor-only module for BlenderBridge.
 * Registers a dockable "BlenderBridge" tab (under Tools) that hosts the import panel.
 * All asset work is delegated to the bundled `blender_bridge` Python package
 * (Content/Python) via the Python Editor Script Plugin.
 */
class FBlenderBridgeEditorModule : public IModuleInterface
{
public:
	virtual void StartupModule() override;
	virtual void ShutdownModule() override;

private:
	void RegisterMenus();
	TSharedRef<class SDockTab> SpawnBridgeTab(const class FSpawnTabArgs& Args);
};
