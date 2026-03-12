@echo off
echo ============================================
echo  AI Cyber Risk Detector - Auto Setup
echo  Windows ke liye automatic setup script
echo ============================================
echo.

echo [1/4] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python install nahi hai!
    echo Download karo: https://www.python.org/downloads/
    echo ADD TO PATH checkbox ZAROOR tick karo!
    pause
    exit
)

echo.
echo [2/4] Creating virtual environment...
python -m venv venv
echo Virtual environment created!

echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated!

echo.
echo [4/4] Installing required libraries...
pip install -r requirements.txt
echo.
echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo  App run karne ke liye:
echo  streamlit run app.py
echo.
echo  Browser mein open karo:
echo  http://localhost:8501
echo.
echo  ⚠️  REMINDER: Tesseract OCR bhi install karo
echo  Screenshot feature ke liye zaroori hai:
echo  https://github.com/UB-Mannheim/tesseract/wiki
echo.
pause
