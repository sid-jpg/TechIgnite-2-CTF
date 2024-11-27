@echo off
echo Starting the CTF Platform...

:: Activate Anaconda environment
call C:\Users\a2z\anaconda3\Scripts\activate.bat

:: Run the Streamlit app
echo Running Streamlit application...
C:\Users\a2z\anaconda3\python.exe -m streamlit run app.py

pause
