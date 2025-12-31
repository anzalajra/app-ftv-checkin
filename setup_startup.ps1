# PowerShell script to set up Task Scheduler for Film dan Televisi Check-In App
# This ensures the application starts immediately during system startup

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PythonScript = Join-Path $ScriptDir "film_televisi_checkin.py"

# Find Python executable
$PythonPath = (Get-Command python -ErrorAction SilentlyContinue).Path
if (-not $PythonPath) {
    $PythonPath = (Get-Command py -ErrorAction SilentlyContinue).Path
}

if (-not $PythonPath) {
    Write-Host "Error: Python not found in PATH. Please install Python first." -ForegroundColor Red
    exit 1
}

# Task name
$TaskName = "FTV-CheckIn-Startup"

# Check if task already exists and remove it
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
if ($ExistingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
}

# Create action to run the Python script
$Action = New-ScheduledTaskAction -Execute $PythonPath -Argument "`"$PythonScript`"" -WorkingDirectory $ScriptDir

# Create trigger for startup (runs at logon)
$Trigger = New-ScheduledTaskTrigger -AtLogon

# Create principal to run with standard user privileges
# Using Interactive logon type to allow GUI display
$Principal = New-ScheduledTaskPrincipal -UserId "$env:USERDOMAIN\$env:USERNAME" -LogonType Interactive

# Create settings
# Explicitly set no execution time limit to allow continuous operation during user session
$Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Seconds 0)

# Register the scheduled task
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description "Film dan Televisi User Check-In Application - Starts immediately at logon"

Write-Host "Task Scheduler entry created successfully!" -ForegroundColor Green
Write-Host "Task Name: $TaskName" -ForegroundColor Cyan
Write-Host "The application will now start automatically when you log in to Windows." -ForegroundColor Green
Write-Host ""
Write-Host "To verify, open Task Scheduler and look for '$TaskName' task." -ForegroundColor Yellow
