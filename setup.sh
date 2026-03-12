#!/bin/bash
echo "============================================"
echo " AI Cyber Risk Detector - Auto Setup"
echo " Mac/Linux ke liye automatic setup script"
echo "============================================"
echo ""

echo "[1/5] Checking Python installation..."
python3 --version
if [ $? -ne 0 ]; then
    echo "ERROR: Python install nahi hai!"
    echo "Download: https://www.python.org/downloads/"
    exit 1
fi

echo ""
echo "[2/5] Installing Tesseract OCR..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        brew install tesseract
    else
        echo "Homebrew install karo pehle: https://brew.sh"
        echo "Phir: brew install tesseract"
    fi
else
    # Linux (Ubuntu/Debian)
    sudo apt update
    sudo apt install -y tesseract-ocr
fi

echo ""
echo "[3/5] Creating virtual environment..."
python3 -m venv venv
echo "Virtual environment created!"

echo ""
echo "[4/5] Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"

echo ""
echo "[5/5] Installing required libraries..."
pip install -r requirements.txt

echo ""
echo "============================================"
echo " Setup Complete!"
echo "============================================"
echo ""
echo " App run karne ke liye:"
echo " source venv/bin/activate"
echo " streamlit run app.py"
echo ""
echo " Browser mein open karo:"
echo " http://localhost:8501"
echo ""
