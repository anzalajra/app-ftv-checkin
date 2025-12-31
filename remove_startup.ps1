# PowerShell script to remove Task Scheduler entry for Film dan Televisi Check-In App

$TaskName = "FTV-CheckIn-Startup"

# Check if task exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "Removing Task Scheduler entry for $TaskName..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    Write-Host "Task Scheduler entry removed successfully!" -ForegroundColor Green
} else {
    Write-Host "Task '$TaskName' not found. Nothing to remove." -ForegroundColor Yellow
}
