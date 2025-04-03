Dim NextRunTime As Date

Sub CheckRemotePY()
    Dim triggerRange As Range
    Dim outputRange As Range
    Dim aggregateOutputSheet As Worksheet
    Dim randomValue As Integer
    Dim newRow As ListObject
    Dim i as Integer
    Dim lastRow As Integer

    ' triggerRange is the cell that triggers the calculation.
    ' It is referred to by the python code as xl("execution_trigger")
    Set triggerRange = ThisWorkbook.Names("execution_trigger").RefersToRange

    ' outputRange is python returns the information from the remote server for every execution.
    Set outputRange = ThisWorkbook.Names("hunting_persistence").RefersToRange

    ' aggregateOutputSheet is where we aggregate the python results from every iteration
    Set aggregateOutputSheet = ThisWorkbook.Sheets("Hunting Results")

    ' Insert a new line into the output sheet and append the execution results
    lastRow = aggregateOutputSheet.Cells(aggregateOutputSheet.Rows.Count, 1).End(xlUp).Row + 1
    ' Loop through each cell in the named range and set values in the target sheet
    For i = 1 To outputRange.Columns.Count
        aggregateOutputSheet.Cells(lastRow, i).Value = outputRange.Cells(1, i).Value
    Next i

    'outputRange.Copy
    'aggregateOutputSheet.Cells(lastRow, 1).PasteSpecial Paste:=xlPasteValues
    'Application.CutCopyMode = False

    ' Write a random value to the input cell
    ' this will trigger the python code to recalculate
    Randomize
    randomValue = Rnd * 100
    triggerRange.Value = randomValue
    Calculate

    StartTimer
End Sub

Sub PauseUsingTimer(seconds As Double)
    Dim pauseTime As Double
    Dim startTime As Double

    ' Record the current time
    startTime = Timer
    ' Set the pause time to the specified number of seconds from now
    pauseTime = startTime + seconds

    ' Check if pauseTime exceeds 86400 seconds (the number of seconds in a day)
    If pauseTime >= 86400 Then
        pauseTime = pauseTime - 86400 ' Adjust for midnight rollover
    End If

    ' Loop until the desired amount of time has passed
    Do While Timer < pauseTime
        ' If we cross midnight, adjust condition to wait for the remaining time
        If Timer < startTime Then
            If Timer >= pauseTime Then Exit Do
        End If
        DoEvents ' Yield control so other processes can run
    Loop

    ' MsgBox seconds & " seconds pause is complete!"
End Sub

Sub StartTimer()
    ' Schedule the macro to run again in 10 minutes (600 seconds)
    NextRunTime = Now + TimeValue("00:10:00")
    Application.OnTime NextRunTime, "CheckRemotePY"
End Sub

Sub StopTimer()
    ' Stops the timer
    On Error Resume Next
    Application.OnTime NextRunTime, "CheckRemotePY", , False
End Sub

