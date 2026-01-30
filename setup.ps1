<#
PowerShell setup script for CalculadoraPrecalculo
Usage (PowerShell as Admin recommended for winget):
.
#>

Write-Host "=== Setting up CalculadoraPrecalculo environment ==="

# 1) Create venv if it doesn't exist
if (-not (Test-Path .\venv)) {
    Write-Host "Creating virtual environment..."
    py -3 -m venv venv
} else {
    Write-Host "Virtual environment already exists."
}

# 2) Activate venv for the duration of this script
Write-Host "Activating virtual environment..."
. .\venv\Scripts\Activate.ps1

# 3) Upgrade pip and install requirements
Write-Host "Upgrading pip and installing Python requirements..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# 4) Install Tesseract OCR via winget (if available)
Write-Host "Attempting to install Tesseract-OCR via winget (requires winget and admin rights)..."
try {
    winget install tesseract-ocr.tesseract -e --accept-package-agreements --accept-source-agreements -h
    Write-Host "Tesseract installer launched via winget (check output for success)."
} catch {
    Write-Warning "winget not available or installation failed. Please install Tesseract manually from https://github.com/tesseract-ocr/tesseract/releases"
}

Write-Host "\nSetup complete. To run demo: .\venv\Scripts\python.exe demo_ocr.py"
Write-Host "To run full calculator: .\venv\Scripts\python.exe calculadora_completa.py"
