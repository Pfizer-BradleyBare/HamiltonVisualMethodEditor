Attribute VB_Name = "WorkbookMacros"
Public Sub WorkbookOnOpen()
 
    'MsgBox ("Hello. Click OK to download the most up to date building blocks. This will happen in the background and take only a few seconds.")
 
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    
    On Error Resume Next
    ThisWorkbook.Worksheets("BuildingBlocks").Delete
    On Error GoTo 0
    
    ScriptPath = "C:\Program Files (x86)\HAMILTON\BAREB\Script\HamiltonVisualMethodEditor\HamiltonVisualMethodEditorConfiguration\BuildingBlocks\BuildingBlocks.xlsx"
    BuildingBlocksPath = Environ("USERPROFILE") & "\OneDrive - Pfizer\Documents\_ABN\BuildingBlocks\BuildingBlocks.xlsx"
    
    If Dir(ScriptPath) <> "" Then
        Set closedBook = Workbooks.Open(ScriptPath)
        closedBook.Sheets("BuildingBlocks").Copy Before:=ThisWorkbook.Sheets(1)
        closedBook.Close SaveChanges:=False
    ElseIf Dir(BuildingBlocksPath) <> "" Then
        Set closedBook = Workbooks.Open(BuildingBlocksPath)
        closedBook.Sheets("BuildingBlocks").Copy Before:=ThisWorkbook.Sheets(1)
        closedBook.Close SaveChanges:=False
    Else
        Dim Sheet As Worksheet
        Set Sheet = Sheets.Add(ThisWorkbook.Sheets(1))
        Sheet.name = "BuildingBlocks"
        ThisWorkbook.Worksheets("BuildingBlocks").Visible = xlSheetHidden
        ThisWorkbook.Worksheets("Method").Activate
        MsgBox ("ABN Building blocks were not found on this system. The following document is read only. You may install building blocks in the ribbon if you would like to build a method.")
        Exit Sub
    End If
    
    ThisWorkbook.Worksheets("BuildingBlocks").Visible = xlSheetHidden
    ThisWorkbook.Worksheets("Method").Activate

    LoadBuildingBlocks
    
    If GlobalBuildingBlockWorkingStatus = True Then
        'MsgBox ("Blocks are killin' it!")
    Else
        MsgBox ("There were issues found with the Building Blocks. You can either view this document as Read Only or, if you wanted to run the method, close the workbook and contact an Automation Bare Necessities SME to correct the issue.")
        Exit Sub
    End If
    
    Dim Selection As Range
    Set Selection = ThisWorkbook.Worksheets("Method").Range("A1:AZ100").Find("Comments")
    If Selection Is Nothing Then
        MsgBox ("Your Method sheet was completely empty. Either Sharon is using this tool or a huge error occured. Resetting Method sheet...")
        ResetMethod
        ThisWorkbook.Worksheets("Solutions").Activate
        LoadSolutions
        FindSolutions
        SaveSolutions
        DeleteSolutions
        ValidateSolutions
        PrintSolutions
        ThisWorkbook.Worksheets("Method").Activate
        Exit Sub
    Else
        SaveSteps
        DeleteMethod
        PrintSteps
    End If
    
    If GlobalOrganizerActionsValidated = True Then
        ThisWorkbook.Worksheets("Worklist").Activate
        'MsgBox ("Ready to go, Chief!")
    Else
        ThisWorkbook.Worksheets("Method").Activate
        MsgBox ("There were issues found with the method. Please check the method sheet for red highlighted cells. Click the effected step to update and correct the errors.")
        Exit Sub
    End If

    ThisWorkbook.Worksheets("Solutions").Activate
    LoadSolutions
    FindSolutions
    SaveSolutions
    DeleteSolutions
    ValidateSolutions
    PrintSolutions
    
    If GlobalSolutionsValidated = True Then
        ThisWorkbook.Worksheets("Worklist").Activate
        'MsgBox ("Ready to go, Chief!")
    Else
        ThisWorkbook.Worksheets("Solutions").Activate
        MsgBox ("There were issues found with the Solutions. Please check the Solutions sheet for red highlighted cells. Click the effected Solution to update and correct the errors.")
        Exit Sub
    End If

    Application.ScreenUpdating = True
    Application.DisplayAlerts = True
    
End Sub

Public Sub WorkbookBeforeClose(Cancel As Boolean)
    CloseWordDocument
    
End Sub

