if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install it and re-run this script." -ForegroundColor Red
    exit
}

if (-not (Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "Pip is not installed. Please install it and re-run this script." -ForegroundColor Red
    exit
}

# Get the directory of the current script
$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition

# Navigate to the project directory
Set-Location -Path $scriptPath

# Install project requirements
pip install -r .\requirements.txt

# Add 'task-cli' command to Windows User Environment Variables permanently
[Environment]::SetEnvironmentVariable("task-cli", "python `"$scriptPath\task_tracker.py`"", "User")

Write-Host "Operation completed! Please restart your command line for changes to take effect." -ForegroundColor Green