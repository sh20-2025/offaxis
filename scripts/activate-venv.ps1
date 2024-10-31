$venvLocation = "C:\Users\Public\sh20-main-venv"
$activateScript = $venvLocation + "\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host "Running activation script..."
    & $activateScript
    Write-Host "Activated venv successfully"
} else {
    Write-Host "Could not find activation script, failed to activate venv"
    Exit
}
