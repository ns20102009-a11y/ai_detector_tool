# ============================================================
# 🛡️ AI Cyber Risk & Malicious File Detector
# Ek web app jo scam messages aur dangerous files detect karta hai
# Hackathon Demo Version — Beginner Friendly Code
# ============================================================

import streamlit as st          # Web UI banane ke liye
from PIL import Image           # Image open karne ke liye
import pytesseract              # Image se text nikalne ke liye (OCR)
from langdetect import detect   # Language detect karne ke liye
from reportlab.lib.pagesizes import letter   # PDF page size
from reportlab.pdfgen import canvas          # PDF generate karne ke liye
from reportlab.lib import colors             # PDF mein color ke liye
import io                       # PDF ko memory mein store karne ke liye
import re                       # Regular expressions (pattern matching)
import os                       # OS level operations
import platform                 # OS check karne ke liye

# ============================================================
# TESSERACT PATH SET KARO
# Windows: default install path
# Mac/Linux: usually in PATH already
# ============================================================
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Mac users: brew install tesseract
# Linux users: sudo apt install tesseract-ocr

# ============================================================
# RISK DETECTION ENGINE
# Ye words/patterns dekhkar risk decide karta hai
# ============================================================

# HIGH RISK keywords — ye dekhe toh bahut danger hai
HIGH_RISK_KEYWORDS = [
    "download now", "click here to download", "install apk",
    "free money", "you have won", "claim your prize",
    "your account will be blocked", "verify immediately",
    "send otp", "share otp", "abhi download karo",
    "turant karo", "last chance", "expire ho jayega",
    "bank account blocked", "emi failed", ".apk", ".exe download",
    "whatsapp mod", "unlimited free", "hack karo", "free recharge trick",
    "account suspend", "kyc update", "re-kyc", "verify your account",
    "aadhar link", "pan card blocked", "income tax notice",
    "police case", "arrest warrant", "legal action",
    "immediate action required", "account deactivated"
]

# SUSPICIOUS keywords — ye dekhe toh thoda doubt karo
SUSPICIOUS_KEYWORDS = [
    "limited time", "act now", "urgent", "warning", "alert",
    "congratulations", "selected", "winner", "lucky draw",
    "government notice", "income tax", "loan approved",
    "ek baar click karo", "sirf aaj", "offer khatam",
    "pdf download", "link open karo", "form bharo",
    ".pdf", ".zip", "bit.ly", "tinyurl", "t.me/",
    "whatsapp group join", "telegram link", "refer and earn",
    "cashback", "lottery", "jackpot", "prize money",
    "click the link", "open link", "tap here", "swipe up",
    "password reset", "login here", "verify now"
]

# SAFE indicators — agar ye words hain toh likely safe hai
SAFE_INDICATORS = [
    "official website", "verified", "https://",
    "customer care", "support@", "noreply@",
    ".gov.in", ".edu", "registered company",
    "toll free", "helpline"
]

# Dangerous file extensions
DANGEROUS_EXTENSIONS = [
    '.apk', '.exe', '.bat', '.cmd', '.scr',
    '.vbs', '.ps1', '.msi', '.dll', '.jar',
    '.sh', '.dmg', '.pkg'
]

# Hinglish detection words
HINGLISH_WORDS = [
    'karo', 'yaha', 'abhi', 'turant', 'mera', 'tumhara',
    'hai', 'nahi', 'hoga', 'click', 'download', 'free',
    'aap', 'aapka', 'paisa', 'rupaye', 'jaldi', 'link',
    'bhejo', 'dekho', 'lo', 'do', 'lena', 'dena', 'wala',
    'baar', 'bata', 'kya', 'toh', 'bhi', 'sirf', 'sab',
    'agar', 'lekin', 'kyunki', 'isliye', 'matlab', 'samjho'
]


# ============================================================
# LANGUAGE DETECTION FUNCTION
# ============================================================
def detect_language(text):
    """
    Text ki language detect karta hai
    Returns: 'Hindi', 'Hinglish', ya 'English'
    """
    text_lower = text.lower()

    # Devanagari script check karo (pure Hindi)
    devanagari_pattern = re.compile(r'[\u0900-\u097F]')
    if devanagari_pattern.search(text):
        return "🇮🇳 Hindi (Devanagari)"

    # Hinglish words count karo
    hinglish_count = sum(1 for word in HINGLISH_WORDS if word in text_lower)
    if hinglish_count >= 2:
        return "🇮🇳 Hinglish (Hindi+English)"

    # langdetect library se try karo
    try:
        lang = detect(text)
        lang_map = {
            'hi': '🇮🇳 Hindi',
            'en': '🌐 English',
            'mr': '🇮🇳 Marathi',
            'gu': '🇮🇳 Gujarati',
            'ta': '🇮🇳 Tamil',
            'te': '🇮🇳 Telugu',
            'bn': '🇮🇳 Bengali',
        }
        return lang_map.get(lang, f'🌐 Other ({lang})')
    except Exception:
        return "🌐 English (default)"


# ============================================================
# MAIN RISK ANALYSIS FUNCTION
# ============================================================
def analyze_risk(text):
    """
    Text ko analyze karke risk level, score, aur reasons return karta hai
    """
    text_lower = text.lower()

    matched_high = []
    matched_suspicious = []
    matched_safe = []
    reasons = []
    score = 0  # 0 = safe, 100 = max danger

    # HIGH RISK keywords check karo
    for keyword in HIGH_RISK_KEYWORDS:
        if keyword.lower() in text_lower:
            matched_high.append(keyword)
            score += 20

    # SUSPICIOUS keywords check karo
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword.lower() in text_lower:
            matched_suspicious.append(keyword)
            score += 10

    # SAFE indicators check karo
    for indicator in SAFE_INDICATORS:
        if indicator.lower() in text_lower:
            matched_safe.append(indicator)
            score -= 8

    # Dangerous file extensions check karo
    for ext in DANGEROUS_EXTENSIONS:
        if ext in text_lower:
            score += 30
            reasons.append(f"⚠️ Dangerous file type found: {ext.upper()}")

    # Short URL check (often used to hide real URLs)
    short_url_patterns = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly']
    for pattern in short_url_patterns:
        if pattern in text_lower:
            score += 15
            reasons.append(f"🔗 Shortened/hidden URL detected: {pattern}")
            break

    # OTP mention — legitimate services NEVER ask OTP via message
    if 'otp' in text_lower:
        score += 30
        reasons.append("🔐 OTP mentioned — NEVER share OTP with anyone!")

    # All caps words — urgency trick
    caps_words = re.findall(r'\b[A-Z]{4,}\b', text)
    if len(caps_words) >= 2:
        score += 10
        reasons.append(f"📢 ALL CAPS urgency detected: {', '.join(caps_words[:3])}")

    # Exclamation marks — pressure tactic
    exclamation_count = text.count('!')
    if exclamation_count >= 3:
        score += 8
        reasons.append(f"❗ Multiple exclamation marks ({exclamation_count}) — pressure tactic")

    # Score ko 0-100 range mein rakho
    score = max(0, min(100, score))

    # Risk level decide karo
    if score >= 50:
        risk_level = "HIGH RISK"
    elif score >= 20:
        risk_level = "SUSPICIOUS"
    else:
        risk_level = "SAFE"

    # Detailed reasons add karo
    if matched_high:
        top_high = matched_high[:4]
        reasons.insert(0, f"❌ High-risk phrases found: {', '.join(top_high)}")
    if matched_suspicious:
        top_sus = matched_suspicious[:4]
        reasons.insert(1, f"⚠️ Suspicious phrases found: {', '.join(top_sus)}")
    if matched_safe:
        reasons.append(f"✅ Some safe indicators present: {', '.join(matched_safe)}")
    if not reasons:
        reasons.append("✅ No dangerous patterns detected in this text")
    if not matched_high and not matched_suspicious:
        reasons.append("✅ No scam keywords or dangerous links found")

    return risk_level, score, reasons


# ============================================================
# SAFETY TIPS GENERATOR
# ============================================================
def get_safety_tips(risk_level):
    """Risk level ke hisaab se personalized safety tips"""

    if risk_level == "HIGH RISK":
        return [
            "🚫 Is message/file ko BILKUL download mat karo",
            "📵 Is link pe KABHI click mat karo — window band karo",
            "👨‍👩‍👦 Apne family members ko turant warn karo",
            "🏦 Agar bank related hai — turant bank helpline call karo",
            "🗑️ Is message ko delete karo aur sender ko BLOCK karo",
            "📢 Cybercrime portal pe report karo: cybercrime.gov.in",
            "🔐 Apna bank password aur UPI PIN turant change karo",
            "📱 Agar APK already download ki hai — phone factory reset karo",
            "🚨 Cyber Helpline: 1930 (24x7 available)",
        ]
    elif risk_level == "SUSPICIOUS":
        return [
            "🤔 Pehle sender ki identity verify karo — official number se call karo",
            "🔍 Is link ko Google pe search karo — 'scam' word ke saath",
            "⏳ 'Urgent' ya 'Limited time' pressure mein BILKUL mat aao",
            "📞 Official website pe directly jao — diye gaye link pe mat jao",
            "👥 Trusted person (family/friend) se poocho pehle koi action lo",
            "🔒 Apna antivirus scan chalaao abhi",
            "💡 Yaad rakho: Koi bhi legitimate company OTP nahi maangti",
            "📧 Agar email hai — sender ka email address carefully check karo",
        ]
    else:
        return [
            "✅ Ye message relatively safe lag raha hai",
            "💡 Phir bhi, unknown links pe hamesha alert raho",
            "🔄 Apna phone aur apps updated rakho",
            "🔐 Strong passwords use karo — har account ke liye alag",
            "📚 2FA (Two Factor Authentication) enable karo sab accounts pe",
            "🛡️ Apne dosto aur family ko cyber safety ke baare mein batao",
        ]


# ============================================================
# OCR — IMAGE SE TEXT EXTRACT KARO
# ============================================================
def extract_text_from_image(image):
    """Pytesseract use karke image se text extract karta hai"""
    try:
        # Grayscale conversion — OCR accuracy better hoti hai
        gray_image = image.convert('L')
        # English text extract karo
        extracted_text = pytesseract.image_to_string(gray_image, lang='eng')
        return extracted_text.strip()
    except Exception as e:
        error_msg = str(e)
        if "tesseract" in error_msg.lower():
            return "OCR_ERROR: Tesseract install nahi hai ya path galat hai. Step 6 check karo."
        return f"OCR_ERROR: {error_msg}"


# ============================================================
# PDF REPORT GENERATOR
# ============================================================
def generate_pdf_report(input_text, language, risk_level, score, reasons, safety_tips, source_type):
    """
    Professional PDF report generate karta hai
    Returns: PDF bytes (download ke liye)
    """
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter  # 612 x 792 points

    # ---- COLOR SCHEME ----
    dark_bg     = colors.HexColor('#1a1a2e')
    accent_red  = colors.HexColor('#e94560')
    risk_red    = colors.HexColor('#ff4444')
    risk_orange = colors.HexColor('#ff9900')
    risk_green  = colors.HexColor('#00aa44')
    light_gray  = colors.HexColor('#f5f5f5')
    dark_text   = colors.HexColor('#222222')
    mid_gray    = colors.HexColor('#555555')

    # ---- HEADER BACKGROUND ----
    pdf.setFillColor(dark_bg)
    pdf.rect(0, height - 90, width, 90, fill=True, stroke=False)

    # Header accent line
    pdf.setFillColor(accent_red)
    pdf.rect(0, height - 93, width, 3, fill=True, stroke=False)

    # Header text
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 20)
    pdf.drawString(30, height - 40, "AI Cyber Risk & Malicious File Detector")
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(colors.HexColor('#aaaaaa'))
    pdf.drawString(30, height - 62, "Security Analysis Report  |  cybercrime.gov.in  |  Helpline: 1930")

    # Shield icon text
    pdf.setFont("Helvetica-Bold", 28)
    pdf.setFillColor(accent_red)
    pdf.drawString(width - 60, height - 55, "🛡")

    y = height - 120

    # ---- VERDICT BOX ----
    if risk_level == "HIGH RISK":
        box_color = risk_red
        verdict_text = "HIGH RISK"
        emoji = "[HIGH RISK]"
    elif risk_level == "SUSPICIOUS":
        box_color = risk_orange
        verdict_text = "SUSPICIOUS"
        emoji = "[SUSPICIOUS]"
    else:
        box_color = risk_green
        verdict_text = "SAFE"
        emoji = "[SAFE]"

    pdf.setFillColor(box_color)
    pdf.roundRect(30, y - 45, width - 60, 50, 10, fill=True, stroke=False)
    pdf.setFillColor(colors.white)
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y - 25, f"VERDICT: {emoji}  {verdict_text}   |   Risk Score: {score}/100")

    y -= 75

    # ---- RISK SCORE BAR ----
    pdf.setFillColor(colors.HexColor('#eeeeee'))
    pdf.roundRect(30, y - 18, width - 60, 18, 4, fill=True, stroke=False)
    bar_width = int(((width - 60) * score) / 100)
    pdf.setFillColor(box_color)
    pdf.roundRect(30, y - 18, bar_width, 18, 4, fill=True, stroke=False)
    pdf.setFillColor(dark_text)
    pdf.setFont("Helvetica-Bold", 9)
    pdf.drawString(32, y - 13, f"Risk Level: {score}%")

    y -= 40

    # ---- DIVIDER ----
    def draw_section_header(pdf, title, y_pos):
        pdf.setFillColor(dark_bg)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(30, y_pos, title)
        pdf.setStrokeColor(accent_red)
        pdf.setLineWidth(1.5)
        pdf.line(30, y_pos - 4, width - 30, y_pos - 4)
        return y_pos - 22

    # ---- ANALYSIS DETAILS ----
    y = draw_section_header(pdf, "Analysis Details", y)
    pdf.setFont("Helvetica", 11)
    pdf.setFillColor(dark_text)

    details = [
        ("Source Type:", source_type),
        ("Language Detected:", language),
        ("Risk Level:", verdict_text),
        ("Risk Score:", f"{score} / 100"),
    ]
    for label, value in details:
        pdf.setFont("Helvetica-Bold", 11)
        pdf.setFillColor(mid_gray)
        pdf.drawString(35, y, label)
        pdf.setFont("Helvetica", 11)
        pdf.setFillColor(dark_text)
        pdf.drawString(165, y, value)
        y -= 18

    y -= 15

    # ---- INPUT SUMMARY ----
    y = draw_section_header(pdf, "Input Text Summary", y)
    pdf.setFillColor(light_gray)
    pdf.roundRect(30, y - 55, width - 60, 60, 5, fill=True, stroke=False)

    preview = input_text[:250].replace('\n', ' ')
    if len(input_text) > 250:
        preview += "..."
    clean_preview = preview.encode('ascii', 'ignore').decode('ascii')

    pdf.setFont("Helvetica", 10)
    pdf.setFillColor(dark_text)
    # Simple word wrap for preview
    words = clean_preview.split()
    line, line_y = "", y - 15
    for word in words:
        if len(line) + len(word) + 1 < 90:
            line += word + " "
        else:
            pdf.drawString(38, line_y, line.strip())
            line_y -= 14
            line = word + " "
            if line_y < y - 55:
                break
    if line:
        pdf.drawString(38, line_y, line.strip())

    y -= 75

    # ---- DETECTION REASONS ----
    y = draw_section_header(pdf, "Detection Reasons", y)
    pdf.setFont("Helvetica", 10)
    for i, reason in enumerate(reasons):
        if y < 80:
            pdf.showPage()
            y = height - 50
        clean_reason = reason.encode('ascii', 'ignore').decode('ascii')
        # Alternating row background
        if i % 2 == 0:
            pdf.setFillColor(colors.HexColor('#f9f9f9'))
            pdf.rect(30, y - 4, width - 60, 16, fill=True, stroke=False)
        pdf.setFillColor(dark_text)
        pdf.drawString(38, y, f"{clean_reason}")
        y -= 18

    y -= 15

    # ---- SAFETY TIPS ----
    if y < 150:
        pdf.showPage()
        y = height - 50

    y = draw_section_header(pdf, "Safety Recommendations", y)

    for tip in safety_tips:
        if y < 80:
            pdf.showPage()
            y = height - 50
        clean_tip = tip.encode('ascii', 'ignore').decode('ascii')
        pdf.setFillColor(colors.HexColor('#e8f5e9'))
        pdf.rect(30, y - 4, width - 60, 16, fill=True, stroke=False)
        pdf.setFillColor(colors.HexColor('#006600'))
        pdf.setFont("Helvetica", 10)
        pdf.drawString(38, y, clean_tip)
        y -= 18

    # ---- FOOTER ----
    pdf.setFillColor(dark_bg)
    pdf.rect(0, 0, width, 40, fill=True, stroke=False)
    pdf.setFillColor(colors.HexColor('#888888'))
    pdf.setFont("Helvetica", 8)
    pdf.drawString(30, 25, "Generated by AI Cyber Risk Detector | For educational & demo purposes only")
    pdf.drawString(30, 12, "Report any cybercrime at cybercrime.gov.in | National Cyber Helpline: 1930")
    pdf.setFillColor(accent_red)
    pdf.setFont("Helvetica-Bold", 8)
    pdf.drawString(width - 120, 18, "Stay Safe Online!")

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# STREAMLIT UI — WEB APP STARTS HERE
# ============================================================
def main():
    # Page config
    st.set_page_config(
        page_title="AI Cyber Risk Detector",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # ---- CUSTOM CSS ----
    st.markdown("""
    <style>
        /* Dark theme background */
        .stApp {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        }

        /* Main header */
        .main-header {
            background: linear-gradient(135deg, #0f3460 0%, #1a1a2e 50%, #e94560 100%);
            padding: 30px 35px;
            border-radius: 16px;
            margin-bottom: 28px;
            text-align: center;
            border: 1px solid rgba(233,69,96,0.3);
            box-shadow: 0 8px 32px rgba(233,69,96,0.2);
        }
        .main-header h1 {
            color: white;
            font-size: 2.3em;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 8px rgba(0,0,0,0.5);
        }
        .main-header p {
            color: #cccccc;
            margin: 0;
            font-size: 1.05em;
        }

        /* Risk verdict cards */
        .risk-high {
            background: linear-gradient(135deg, #ff2244, #aa0022);
            padding: 22px 25px;
            border-radius: 14px;
            border-left: 6px solid #ff0033;
            color: white;
            font-size: 1.4em;
            font-weight: bold;
            box-shadow: 0 4px 20px rgba(255,34,68,0.4);
            margin: 10px 0;
        }
        .risk-suspicious {
            background: linear-gradient(135deg, #ff9900, #cc6600);
            padding: 22px 25px;
            border-radius: 14px;
            border-left: 6px solid #ffaa00;
            color: white;
            font-size: 1.4em;
            font-weight: bold;
            box-shadow: 0 4px 20px rgba(255,153,0,0.4);
            margin: 10px 0;
        }
        .risk-safe {
            background: linear-gradient(135deg, #00bb44, #007722);
            padding: 22px 25px;
            border-radius: 14px;
            border-left: 6px solid #00ff66;
            color: white;
            font-size: 1.4em;
            font-weight: bold;
            box-shadow: 0 4px 20px rgba(0,187,68,0.4);
            margin: 10px 0;
        }

        /* Info reason boxes */
        .info-box {
            background: rgba(14, 52, 96, 0.6);
            border-left: 4px solid #e94560;
            padding: 12px 16px;
            border-radius: 0 10px 10px 0;
            margin: 6px 0;
            color: #eeeeee;
            font-size: 0.95em;
        }

        /* Safety tip boxes */
        .tip-item {
            background: rgba(0, 100, 40, 0.3);
            border-left: 4px solid #00aa44;
            padding: 10px 14px;
            margin: 5px 0;
            border-radius: 0 8px 8px 0;
            color: #ccffcc;
            font-size: 0.93em;
        }

        /* Metric boxes in sidebar */
        .metric-box {
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 12px 15px;
            text-align: center;
            margin: 5px 0;
        }

        /* Example buttons */
        .stButton > button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.2s ease;
            border: 1px solid rgba(233,69,96,0.4);
        }

        /* Analyze main button */
        div[data-testid="stButton"]:last-of-type > button {
            background: linear-gradient(90deg, #e94560, #0f3460) !important;
            color: white !important;
            font-size: 1.1em !important;
            padding: 14px !important;
            border: none !important;
        }

        /* Text area */
        .stTextArea textarea {
            background: rgba(255,255,255,0.08) !important;
            color: #eeeeee !important;
            border: 1px solid rgba(233,69,96,0.3) !important;
            border-radius: 10px !important;
        }

        /* Section headers */
        h3 {
            color: #e94560 !important;
        }

        /* Streamlit metric labels */
        [data-testid="stMetricLabel"] {
            color: #aaaaaa !important;
        }
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---- HEADER ----
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ AI Cyber Risk & Malicious File Detector</h1>
        <p>Scam messages, fake APK links, aur phishing attacks se khud ko aur apni family ko bachao</p>
    </div>
    """, unsafe_allow_html=True)

    # ---- SIDEBAR ----
    with st.sidebar:
        st.markdown("## 🔍 Analysis Mode")

        analysis_mode = st.radio(
            "Input type choose karo:",
            ["📝 Text Input", "🖼️ Screenshot Upload"],
            help="Text paste karo ya suspicious screenshot upload karo"
        )

        st.markdown("---")
        st.markdown("## 📊 Risk Levels")

        st.markdown("""
        <div class="metric-box">
            <p style='color:#ff4444;font-size:1.3em;margin:0;font-weight:bold'>🔴 HIGH RISK</p>
            <p style='color:#999;font-size:0.8em;margin:4px 0 0'>Score ≥ 50/100</p>
        </div>
        <div class="metric-box">
            <p style='color:#ff9900;font-size:1.3em;margin:0;font-weight:bold'>🟡 SUSPICIOUS</p>
            <p style='color:#999;font-size:0.8em;margin:4px 0 0'>Score 20–49/100</p>
        </div>
        <div class="metric-box">
            <p style='color:#00bb44;font-size:1.3em;margin:0;font-weight:bold'>🟢 SAFE</p>
            <p style='color:#999;font-size:0.8em;margin:4px 0 0'>Score 0–19/100</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("## 🚨 Emergency Helplines")
        st.error("**Cyber Crime Helpline**\n\n📞 **1930** (24x7 Free)")
        st.info("🌐 **cybercrime.gov.in**\nOnline complaint darz karo")

        st.markdown("---")
        st.markdown("## ℹ️ About This App")
        st.caption(
            "Ye app rule-based AI use karta hai scam patterns detect karne ke liye. "
            "Hackathon demo version. "
            "Real-world deployment ke liye ML model add karna hoga."
        )

    # ---- VARIABLES ----
    input_text = ""
    source_type = ""

    # ============================================================
    # TEXT INPUT MODE
    # ============================================================
    if "Text Input" in analysis_mode:
        source_type = "Direct Text Input"

        st.markdown("### 📝 Suspicious Message Yahan Paste Karo")
        st.caption("WhatsApp message, SMS, email content, ya koi bhi suspicious text paste karo")

        # Quick example buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🔴 High Risk Demo", use_container_width=True):
                st.session_state['demo_text'] = (
                    "URGENT!!! Aapka SBI bank account BLOCK ho jayega 24 ghante mein! "
                    "Abhi is APK file ko download karo aur install karo: bit.ly/sbi-kyc-fix "
                    "Turant apna OTP share karo 9876543210 pe. LAST CHANCE! "
                    "Account permanently delete ho jayega. FREE RECHARGE bhi milega!"
                )
        with col2:
            if st.button("🟡 Suspicious Demo", use_container_width=True):
                st.session_state['demo_text'] = (
                    "Congratulations! You have been SELECTED as lucky winner. "
                    "Claim your prize of Rs 50,000 by clicking this link: tinyurl.com/claim-now "
                    "Limited time offer — act now before it expires! "
                    "Download the form PDF and fill it urgently."
                )
        with col3:
            if st.button("🟢 Safe Demo", use_container_width=True):
                st.session_state['demo_text'] = (
                    "Dear Customer, your appointment is confirmed for tomorrow at 3:00 PM. "
                    "Please visit our official website https://apollo.gov.in for directions. "
                    "Contact our verified customer care at support@apollohospital.com "
                    "for any queries. Thank you."
                )

        # Text area
        demo_val = st.session_state.get('demo_text', '')
        input_text = st.text_area(
            "Message yahan paste karo:",
            value=demo_val,
            height=180,
            placeholder=(
                "Example: Aapka account band ho jayega, turant is link pe click karo, "
                "OTP share karo...\n\nYa upar wale demo buttons try karo! 👆"
            )
        )

    # ============================================================
    # IMAGE UPLOAD MODE
    # ============================================================
    else:
        source_type = "Screenshot (OCR Extracted)"

        st.markdown("### 🖼️ Suspicious Screenshot Upload Karo")
        st.caption("Koi bhi scam message ka screenshot upload karo — OCR automatically text nikaal lega")

        col_upload, col_preview = st.columns([1, 1])

        with col_upload:
            uploaded_file = st.file_uploader(
                "Image upload karo:",
                type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
                help="PNG ya JPG format best hota hai clear text extraction ke liye"
            )

            if uploaded_file:
                st.success(f"✅ File uploaded: {uploaded_file.name}")
                st.info(
                    "💡 **OCR Tips:**\n"
                    "- Clear, high-resolution images best hote hain\n"
                    "- Dark text on light background ideal hai\n"
                    "- Blurry ya rotated images mein accuracy kam hoti hai"
                )

        with col_preview:
            if uploaded_file is not None:
                image = Image.open(uploaded_file)
                st.image(image, caption="📸 Uploaded Screenshot", use_container_width=True)

                st.markdown("**🔄 OCR Processing...**")
                with st.spinner("Image se text extract ho raha hai..."):
                    extracted = extract_text_from_image(image)

                if extracted.startswith("OCR_ERROR"):
                    st.error(f"❌ {extracted}")
                    st.warning(
                        "**Fix karo:**\n"
                        "1. Tesseract install hai? → Step 6 check karo\n"
                        "2. Windows: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe` exist karta hai?\n"
                        "3. Mac: `brew install tesseract` run karo\n"
                        "4. Linux: `sudo apt install tesseract-ocr` run karo"
                    )
                    input_text = ""
                elif not extracted:
                    st.warning("⚠️ Koi text nahi mila. Clear image try karo.")
                    input_text = ""
                else:
                    input_text = extracted
                    st.success(f"✅ {len(extracted)} characters extracted!")
                    with st.expander("📖 Extracted Text Dekho"):
                        st.text_area("OCR Output:", value=extracted, height=120)

    # ---- DIVIDER ----
    st.markdown("---")

    # ============================================================
    # ANALYZE BUTTON
    # ============================================================
    analyze_btn = st.button(
        "🔍 ANALYZE NOW — Risk Check Karo",
        use_container_width=True,
        type="primary"
    )

    # ============================================================
    # RESULTS SECTION
    # ============================================================
    if analyze_btn:
        if not input_text or len(input_text.strip()) < 5:
            st.warning("⚠️ Pehle kuch text enter karo ya image upload karo!")
            st.stop()

        # Run analysis
        with st.spinner("🔄 AI analyzing... ek second..."):
            language    = detect_language(input_text)
            risk_level, score, reasons = analyze_risk(input_text)
            safety_tips = get_safety_tips(risk_level)

        st.markdown("---")
        st.markdown("## 📊 Analysis Results")

        # ---- VERDICT CARD ----
        if risk_level == "HIGH RISK":
            st.markdown(
                f'<div class="risk-high">'
                f'🔴 VERDICT: HIGH RISK &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'Danger Score: {score}/100'
                f'</div>',
                unsafe_allow_html=True
            )
        elif risk_level == "SUSPICIOUS":
            st.markdown(
                f'<div class="risk-suspicious">'
                f'🟡 VERDICT: SUSPICIOUS &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'Risk Score: {score}/100'
                f'</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="risk-safe">'
                f'🟢 VERDICT: SAFE &nbsp;&nbsp;|&nbsp;&nbsp; '
                f'Risk Score: {score}/100'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # ---- METRICS ROW ----
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("🌐 Language", language)
        with m2:
            st.metric("📊 Risk Score", f"{score}/100")
        with m3:
            st.metric("📁 Source", source_type)
        with m4:
            st.metric("🔍 Reasons Found", len(reasons))

        # ---- RISK METER ----
        st.markdown("### 📈 Risk Meter")
        st.progress(score / 100)

        if score >= 70:
            st.error("🚨 EXTREMELY DANGEROUS! Kuch bhi mat karo — seedha block karo!")
        elif score >= 50:
            st.error("🔴 HIGH RISK! Bahut savdhan raho — kisi ko bhi OTP ya details mat do!")
        elif score >= 20:
            st.warning("🟡 SUSPICIOUS! Verify karo pehle koi bhi action lo!")
        else:
            st.success("🟢 Relatively SAFE — phir bhi unknown links pe hamesha alert raho!")

        # ---- TWO COLUMNS LAYOUT ----
        left_col, right_col = st.columns([1, 1])

        with left_col:
            st.markdown("### 🔎 Detection Reasons")
            for reason in reasons:
                st.markdown(f'<div class="info-box">{reason}</div>', unsafe_allow_html=True)

        with right_col:
            st.markdown("### 💡 Safety Tips")
            for tip in safety_tips:
                st.markdown(f'<div class="tip-item">{tip}</div>', unsafe_allow_html=True)

        # ---- PDF DOWNLOAD ----
        st.markdown("---")
        st.markdown("### 📄 Download Full Report")

        col_pdf, col_share = st.columns([2, 1])

        with col_pdf:
            with st.spinner("PDF generate ho raha hai..."):
                pdf_bytes = generate_pdf_report(
                    input_text, language, risk_level,
                    score, reasons, safety_tips, source_type
                )

            st.download_button(
                label="⬇️ PDF Report Download Karo",
                data=pdf_bytes,
                file_name="cyber_risk_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col_share:
            st.info(
                "📋 **Report mein hai:**\n"
                "- Risk verdict\n"
                "- Detection reasons\n"
                "- Safety tips\n"
                "- Helpline numbers"
            )

        st.caption(
            "💡 PDF report save karo — judges ko dikhao ya cybercrime.gov.in pe complaint ke saath attach karo."
        )


# ============================================================
# ENTRY POINT
# ============================================================
if __name__ == "__main__":
    main()
