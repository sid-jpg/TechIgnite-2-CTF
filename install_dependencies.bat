@echo off
echo Installing system dependencies...
py -3.9 -m pip install --upgrade pip setuptools wheel

echo Installing core dependencies first...
py -3.9 -m pip install numpy==1.24.3
py -3.9 -m pip install pandas==1.5.3

echo Installing remaining dependencies...
py -3.9 -m pip install -r requirements.txt

echo Installation complete!
