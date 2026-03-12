# 🛡️ AI Cyber Risk & Malicious File Detector

> Scam messages, fake APK links, aur phishing attacks detect karne wala web app
> Built with Python + Streamlit | Hackathon Demo Project

---

## 📁 Project Structure

```
cyber_detector/
│
├── app.py               ← Main application file (poora code yahan hai)
├── requirements.txt     ← Python libraries list
├── README.md            ← Ye file (setup guide)
├── setup.bat            ← Windows auto-setup script
└── venv/                ← Virtual environment (auto-create hoga)
```

---

## ⚡ Quick Start (5 Steps)

### Step 1 — Python Install Karo
Download from: https://www.python.org/downloads/
> ⚠️ IMPORTANT: "Add Python to PATH" checkbox ZAROOR tick karo!

### Step 2 — Tesseract OCR Install Karo (Screenshot feature ke liye)
Windows: https://github.com/UB-Mannheim/tesseract/wiki
```
Default install path: C:\Program Files\Tesseract-OCR\
```
Mac:
```bash
brew install tesseract
```
Linux:
```bash
sudo apt install tesseract-ocr
```

### Step 3 — VS Code mein folder open karo
```
File → Open Folder → cyber_detector folder select karo
```

### Step 4 — Virtual Environment Setup Karo
VS Code terminal mein (Terminal → New Terminal):

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 5 — App Run Karo
```bash
streamlit run app.py
```
Browser mein open hoga: **http://localhost:8501**

---

## 🎯 Features

| Feature | Description |
|---------|-------------|
| 📝 Text Analysis | Paste any message — instant risk check |
| 🖼️ Screenshot OCR | Upload image — auto text extract + analyze |
| 🌐 Language Detection | Hindi, Hinglish, English support |
| 📊 Risk Scoring | 0–100 score with color-coded verdict |
| 💡 Safety Tips | Personalized advice based on risk level |
| 📄 PDF Report | Downloadable professional report |

---

## 🔴 Risk Levels Explained

| Level | Score | Meaning |
|-------|-------|---------|
| 🟢 SAFE | 0–19 | Message safe lag raha hai |
| 🟡 SUSPICIOUS | 20–49 | Verify karo pehle action lo |
| 🔴 HIGH RISK | 50–100 | Bahut khatarnak — avoid karo |

---

## 🧰 Tech Stack

| Library | Use |
|---------|-----|
| `streamlit` | Web UI |
| `pytesseract` | OCR (image → text) |
| `Pillow` | Image processing |
| `langdetect` | Language detection |
| `reportlab` | PDF generation |
| `re` | Pattern matching |

---

## 🚨 Common Errors & Fixes

**Error: TesseractNotFoundError**
```
Fix: app.py mein line 20 check karo
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
Apna actual install path daalo
```

**Error: ModuleNotFoundError**
```bash
# venv activate karo pehle:
venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

**Error: Port already in use**
```bash

y --server.port 8502
```

---

## 🎤 Hackathon Pitch (1 Minute)

> "India mein har din lakho log WhatsApp scams ka shikar hote hain.
> Hamara AI Cyber Risk Detector ek message paste karne ya screenshot upload karne par
> turant bata deta hai — SAFE hai, SUSPICIOUS hai, ya HIGH RISK hai.
> Hindi, Hinglish, English — teeno languages support karta hai.
> Safety tips + PDF report bhi generate karta hai.
> Goal: Digital India ko safer banana — ek message at a time."

---

## 📞 Cyber Safety Helplines

- 🚨 **National Cyber Helpline: 1930** (24x7 Free)
- 🌐 **cybercrime.gov.in** — Online complaint
- 📧 **cybercell@gov.in**

---

## 👨‍💻 Made with ❤️ for Hackathon Demo
