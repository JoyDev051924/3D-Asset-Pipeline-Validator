// Copyright (c) 2026 Marko Stankovic. MIT License.

#pragma once

#include "CoreMinimal.h"
#include "Widgets/SCompoundWidget.h"

/** The BlenderBridge import panel. Buttons drive the bundled `blender_bridge` Python package. */
class SBlenderBridgePanel : public SCompoundWidget
{
public:
	SLATE_BEGIN_ARGS(SBlenderBridgePanel) {}
	SLATE_END_ARGS()

	void Construct(const FArguments& InArgs);

private:
	FReply OnScanClicked();
	FReply OnImportClicked();
	FReply OnValidateClicked();

	/** Execute a one-line Python command via the Python Editor Script Plugin. */
	void RunPython(const FString& PythonCommand);
	void AppendLog(const FString& Line);

	FText LogText;
};
