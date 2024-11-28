# PowerShell script to install Python and set up environment
Write-Host "Installing Python and setting up environment..."

# Download Python installer
$pythonUrl = "https://www.python.org/ftp/python/3.9.13/python-3.9.13-amd64.exe"
$installerPath = "python-installer.exe"

Write-Host "Downloading Python installer..."
Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath

# Install Python
Write-Host "Installing Python..."
Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1" -Wait

# Refresh environment variables
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

# Create virtual environment and install dependencies
Write-Host "Setting up virtual environment..."
python -m venv venv
.\venv\Scripts\Activate.ps1

Write-Host "Installing dependencies..."
python -m pip install --upgrade pip setuptools wheel
python -m pip install numpy==1.24.3
python -m pip install pandas==1.5.3
python -m pip install -r requirements.txt

Write-Host "Setup complete!"
