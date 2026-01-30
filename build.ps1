<#
Local build helper: Creates the single-file executable using PyInstaller and runs tests.
Usage (PowerShell):
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  .\build.ps1
#>

Write-Host "=== Local build: CalculadoraCLI ==="

if (-not (Test-Path .\venv)) {
    Write-Host "Virtual environment not found. Run setup.ps1 first to create and install dependencies." -ForegroundColor Yellow
    exit 1
}

Write-Host "Activating venv..."
. .\venv\Scripts\Activate.ps1

Write-Host "Upgrading pip and installing build deps..."
python -m pip install --upgrade pip
python -m pip install pyinstaller

Write-Host "Running tests..."
python -m pytest -q

if ($LASTEXITCODE -ne 0) {
    Write-Host "Tests failed. Aborting build." -ForegroundColor Red
    exit 1
}

Write-Host "Building executable (onefile)..."
pyinstaller --noconfirm --onefile --name CalculadoraCLI calculadora_cli.py

if (Test-Path .\dist\CalculadoraCLI.exe) {
    Write-Host "Build succeeded: .\dist\CalculadoraCLI.exe" -ForegroundColor Green
} else {
    Write-Host "Build failed (no exe found). Check PyInstaller logs in build/" -ForegroundColor Red
    exit 1
}
