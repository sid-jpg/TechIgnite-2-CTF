@echo off
echo Installing Microsoft Visual C++ Build Tools...
curl -L "https://aka.ms/vs/17/release/vs_BuildTools.exe" --output vs_BuildTools.exe
vs_BuildTools.exe --quiet --wait --norestart --nocache ^
    --installPath "%ProgramFiles(x86)%\Microsoft Visual Studio\2022\BuildTools" ^
    --add Microsoft.VisualStudio.Workload.VCTools ^
    --includeRecommended

echo Installing Python packages...
"C:\Users\a2z\anaconda3\python.exe" -m pip install --upgrade pip
"C:\Users\a2z\anaconda3\python.exe" -m pip install streamlit==1.24.0
"C:\Users\a2z\anaconda3\python.exe" -m pip install firebase-admin==6.2.0
"C:\Users\a2z\anaconda3\python.exe" -m pip install python-dotenv==1.0.0
"C:\Users\a2z\anaconda3\python.exe" -m pip install pandas
"C:\Users\a2z\anaconda3\python.exe" -m pip install pyrebase4==4.7.1
"C:\Users\a2z\anaconda3\python.exe" -m pip install plotly==5.15.0

echo Done installing requirements!
pause
