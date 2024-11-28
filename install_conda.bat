@echo off
echo Installing packages using conda...

call C:\Users\a2z\anaconda3\Scripts\activate.bat

echo Installing streamlit...
call conda install -y streamlit=1.24.0

echo Installing firebase-admin...
call conda install -y -c conda-forge firebase-admin=6.2.0

echo Installing python-dotenv...
call conda install -y -c conda-forge python-dotenv=1.0.0

echo Installing pandas...
call conda install -y pandas

echo Installing plotly...
call conda install -y plotly=5.15.0

echo Installing pyrebase4...
call conda install -y -c conda-forge pyrebase4=4.7.1

echo All packages installed!
pause
