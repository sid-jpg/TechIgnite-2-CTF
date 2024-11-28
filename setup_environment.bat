@echo off
echo Setting up Python environment for TechIgnite CTF...

REM Try to find Python installation
where python >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python from https://www.python.org/downloads/
    echo After installation, run this script again.
    pause
    exit
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate

echo Installing dependencies...
python -m pip install --upgrade pip setuptools wheel

echo Installing core dependencies...
python -m pip install numpy==1.24.3
python -m pip install pandas==1.5.3

echo Installing remaining dependencies...
python -m pip install -r requirements.txt

echo Environment setup complete!
echo Run 'venv\Scripts\activate' to activate the virtual environment
echo Then run 'streamlit run app.py' to start the application

pause
