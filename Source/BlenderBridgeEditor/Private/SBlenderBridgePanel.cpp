// Copyright (c) 2026 Marko Stankovic. MIT License.

#include "SBlenderBridgePanel.h"

#include "IPythonScriptPlugin.h"
#include "PythonScriptTypes.h"
#include "Widgets/SBoxPanel.h"
#include "Widgets/Layout/SBorder.h"
#include "Widgets/Text/STextBlock.h"
#include "Widgets/Input/SButton.h"
#include "Widgets/Input/SMultiLineEditableTextBox.h"
#include "Styling/AppStyle.h"

#define LOCTEXT_NAMESPACE "SBlenderBridgePanel"

void SBlenderBridgePanel::Construct(const FArguments& InArgs)
{
	ChildSlot
	[
		SNew(SVerticalBox)

		+ SVerticalBox::Slot().AutoHeight().Padding(8)
		[
			SNew(STextBlock)
			.Text(LOCTEXT("Title", "Blender to UE5 Asset Bridge"))
			.Font(FAppStyle::Get().GetFontStyle("HeadingMedium"))
		]

		+ SVerticalBox::Slot().AutoHeight().Padding(8, 0)
		[
			SNew(SHorizontalBox)
			+ SHorizontalBox::Slot().AutoWidth().Padding(2)
			[
				SNew(SButton)
				.Text(LOCTEXT("Scan", "Scan Exports"))
				.ToolTipText(LOCTEXT("ScanTip", "List the .glb/.fbx assets waiting in the bridge drop-zone"))
				.OnClicked(this, &SBlenderBridgePanel::OnScanClicked)
			]
			+ SHorizontalBox::Slot().AutoWidth().Padding(2)
			[
				SNew(SButton)
				.Text(LOCTEXT("Import", "Import"))
				.ToolTipText(LOCTEXT("ImportTip", "Import all assets from the drop-zone into /Game, with naming + normal handling"))
				.OnClicked(this, &SBlenderBridgePanel::OnImportClicked)
			]
			+ SHorizontalBox::Slot().AutoWidth().Padding(2)
			[
				SNew(SButton)
				.Text(LOCTEXT("Validate", "Validate"))
				.ToolTipText(LOCTEXT("ValidateTip", "Run the pre-flight report: scale, tri budget, missing maps"))
				.OnClicked(this, &SBlenderBridgePanel::OnValidateClicked)
			]
		]

		+ SVerticalBox::Slot().FillHeight(1).Padding(8)
		[
			SNew(SBorder)
			.BorderImage(FAppStyle::Get().GetBrush("ToolPanel.GroupBorder"))
			[
				SNew(SMultiLineEditableTextBox)
				.IsReadOnly(true)
				.Text_Lambda([this]() { return LogText; })
			]
		]
	];

	AppendLog(TEXT("BlenderBridge ready. Scan the export drop-zone to begin."));
	AppendLog(TEXT("(Detailed results print to the Output Log.)"));
}

void SBlenderBridgePanel::RunPython(const FString& PythonCommand)
{
	IPythonScriptPlugin* Python = IPythonScriptPlugin::Get();
	if (Python && Python->IsPythonAvailable())
	{
		FPythonCommandEx Cmd;
		Cmd.Command = PythonCommand;
		Cmd.ExecutionMode = EPythonCommandExecutionMode::ExecuteStatement;
		const bool bOk = Python->ExecPythonCommandEx(Cmd);
		AppendLog(FString::Printf(TEXT("%s %s"), bOk ? TEXT("[ok]") : TEXT("[FAILED]"), *PythonCommand));
	}
	else
	{
		AppendLog(TEXT("ERROR: Python is unavailable. Enable the Python Editor Script Plugin and restart."));
	}
}

FReply SBlenderBridgePanel::OnScanClicked()
{
	RunPython(TEXT("import blender_bridge; blender_bridge.scan()"));
	return FReply::Handled();
}

FReply SBlenderBridgePanel::OnImportClicked()
{
	RunPython(TEXT("import blender_bridge; blender_bridge.run_import()"));
	return FReply::Handled();
}

FReply SBlenderBridgePanel::OnValidateClicked()
{
	RunPython(TEXT("import blender_bridge; blender_bridge.validate()"));
	return FReply::Handled();
}

void SBlenderBridgePanel::AppendLog(const FString& Line)
{
	LogText = FText::FromString(LogText.ToString() + Line + LINE_TERMINATOR);
}

#undef LOCTEXT_NAMESPACE
