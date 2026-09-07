// Copyright (c) 2026 Marko Stankovic. MIT License.

#include "BlenderBridgeEditorModule.h"
#include "SBlenderBridgePanel.h"

#include "ToolMenus.h"
#include "Framework/Docking/TabManager.h"
#include "Widgets/Docking/SDockTab.h"
#include "WorkspaceMenuStructure.h"
#include "WorkspaceMenuStructureModule.h"
#include "Styling/AppStyle.h"

#define LOCTEXT_NAMESPACE "FBlenderBridgeEditorModule"

static const FName BlenderBridgeTabName(TEXT("BlenderBridge"));

void FBlenderBridgeEditorModule::StartupModule()
{
	FGlobalTabmanager::Get()->RegisterNomadTabSpawner(
		BlenderBridgeTabName,
		FOnSpawnTab::CreateRaw(this, &FBlenderBridgeEditorModule::SpawnBridgeTab))
		.SetDisplayName(LOCTEXT("TabTitle", "BlenderBridge"))
		.SetTooltipText(LOCTEXT("TabTooltip", "Import and validate Blender assets"))
		.SetGroup(WorkspaceMenu::GetMenuStructure().GetToolsCategory())
		.SetIcon(FSlateIcon(FAppStyle::GetAppStyleSetName(), "LevelEditor.Tabs.ContentBrowser"));

	// Add a Tools-menu entry that invokes the tab.
	UToolMenus::RegisterStartupCallback(
		FSimpleMulticastDelegate::FDelegate::CreateRaw(this, &FBlenderBridgeEditorModule::RegisterMenus));
}

void FBlenderBridgeEditorModule::ShutdownModule()
{
	UToolMenus::UnRegisterStartupCallback(this);
	UToolMenus::UnregisterOwner(this);
	FGlobalTabmanager::Get()->UnregisterNomadTabSpawner(BlenderBridgeTabName);
}

void FBlenderBridgeEditorModule::RegisterMenus()
{
	FToolMenuOwnerScoped OwnerScoped(this);

	UToolMenu* Menu = UToolMenus::Get()->ExtendMenu(TEXT("LevelEditor.MainMenu.Tools"));
	FToolMenuSection& Section = Menu->FindOrAddSection(TEXT("Tools"));
	Section.AddMenuEntry(
		TEXT("OpenBlenderBridge"),
		LOCTEXT("OpenBridge", "BlenderBridge"),
		LOCTEXT("OpenBridgeTooltip", "Open the BlenderBridge asset importer"),
		FSlateIcon(FAppStyle::GetAppStyleSetName(), "LevelEditor.Tabs.ContentBrowser"),
		FUIAction(FExecuteAction::CreateLambda([]()
		{
			FGlobalTabmanager::Get()->TryInvokeTab(BlenderBridgeTabName);
		})));
}

TSharedRef<SDockTab> FBlenderBridgeEditorModule::SpawnBridgeTab(const FSpawnTabArgs& Args)
{
	return SNew(SDockTab)
		.TabRole(ETabRole::NomadTab)
		[
			SNew(SBlenderBridgePanel)
		];
}

#undef LOCTEXT_NAMESPACE

IMPLEMENT_MODULE(FBlenderBridgeEditorModule, BlenderBridgeEditor)
