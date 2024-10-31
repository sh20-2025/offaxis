$prefix = "[SH20-main SETUP]"

Write-Host $prefix "Setting up python environment for SH20-main"

Write-Host $prefix "Checking python version..."

$pythonVersion = python --version
if (!$pythonVersion.Contains("3.12")) {
    Write-Host $prefix "You must have python 3.12 installed for this project."
    Exit
}

Write-Host $prefix "Python 3.12 found."

$venvLocation = "C:\Users\Public\sh20-main-venv"
Write-Host $prefix "Creating virtual environment in" $venvLocation

if (Test-Path $venvLocation) {
    Write-Host $prefix "Destroying existing venv at" $venvLocation
    Remove-Item $venvLocation -Recurse -Force
    Write-Host $prefix "Recreating venv at" $venvLocation
}

python -m venv $venvLocation

if ($LASTEXITCODE -ne 0) {
    Write-Host $prefix "Failed to create venv"
    Exit
}

Write-Host $prefix "Created venv successfully"

Write-Host $prefix "Activating venv"
$activateScript = $venvLocation + "\Scripts\Activate.ps1"

if (Test-Path $activateScript) {
    Write-Host $prefix "Running activation script..."
    & $activateScript
} else {
    Write-Host $prefix "Could not find activation script, failed to activate venv"
    Exit
}

Write-Host $prefix "Activated venv successfully"

Write-Host $prefix "Installing dependencies"
pip install -r .\requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host $prefix "Failed to install dependencies"
    Exit
}

Write-Host $prefix "Dependencies installed successfully"

Write-Host $prefix "Python setup for SH20-main complete"

Write-Host $prefix "Setting up git for SH20-main"

Write-Host $prefix "Checking pre-commit version..."

$preCommitVersion = pre-commit --version
if (!$preCommitVersion.Contains("4.0.1")) {
    Write-Host $prefix "You must have pre-commit 4.0.1 installed for this project."
    Exit
}

Write-Host $prefix "Pre-commit 4.0.1 found."

Write-Host $prefix "Installing pre-commit hooks"

pre-commit install

if ($LASTEXITCODE -ne 0) {
    Write-Host $prefix "Failed to install pre-commit hooks"
    Exit
}

Write-Host $prefix "Pre-commit hooks installed successfully"

Write-Host $prefix "Git setup for SH20-main complete"

Write-Host $prefix "Setup for SH20-main complete"
