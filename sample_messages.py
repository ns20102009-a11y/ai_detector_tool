# 🧪 Sample Test Messages — Hackathon Demo Ke Liye
# In messages ko app mein paste karke demo karo

# ============================================================
# 🔴 HIGH RISK EXAMPLES (Score 50+)
# ============================================================

HIGH_RISK_1 = """
URGENT!!! Aapka SBI bank account BLOCK ho jayega 24 ghante mein!
Abhi is APK file ko download karo aur install karo: bit.ly/sbi-kyc-fix
Turant apna OTP share karo 9876543210 pe.
LAST CHANCE! Account permanently delete ho jayega.
FREE RECHARGE bhi milega install karne ke baad!
"""

HIGH_RISK_2 = """
Your account will be blocked immediately. VERIFY NOW!
Download this APK: tinyurl.com/bank-update-apk
Send OTP to complete verification. Income tax notice issued.
URGENT action required or arrest warrant will be issued.
abhi install karo — last warning!
"""

HIGH_RISK_3 = """
Congratulations! Aapka naam lucky draw mein select hua hai!
You have WON Rs 5,00,000! Claim karo abhi:
bit.ly/lucky-winner-claim
Ye link sirf 2 ghante ke liye valid hai. TURANT KARO!
Free recharge aur unlimited data bhi milega!
"""

# ============================================================
# 🟡 SUSPICIOUS EXAMPLES (Score 20-49)
# ============================================================

SUSPICIOUS_1 = """
Congratulations! You have been selected as lucky winner.
Claim your prize of Rs 50,000 by clicking this link: tinyurl.com/claim-now
Limited time offer — act now before it expires!
Download the PDF form and fill it urgently.
"""

SUSPICIOUS_2 = """
Government notice: Your loan of Rs 2,00,000 has been approved!
Act now — limited time offer expires today.
Click here to proceed: bit.ly/loan-approved-form
Fill the form and upload your documents.
"""

SUSPICIOUS_3 = """
Ek baar click karo is telegram link pe — bahut bada opportunity hai!
Sirf aaj ke liye offer — unlimited earning from home.
t.me/earn-daily-1000
Join karo abhi — offer khatam ho jaayega!
"""

# ============================================================
# 🟢 SAFE EXAMPLES (Score 0-19)
# ============================================================

SAFE_1 = """
Dear Customer, your appointment is confirmed for tomorrow at 3:00 PM.
Please visit our official website https://apollo.gov.in for directions.
Contact our verified customer care at support@apollohospital.com
for any queries. Thank you.
"""

SAFE_2 = """
Hi Rahul, this is a reminder from HDFC Bank.
Your credit card statement is ready. Please visit our official website
https://www.hdfcbank.com to view your statement.
Do not share your password or OTP with anyone including bank employees.
"""

SAFE_3 = """
Your package has been dispatched. Expected delivery: Tomorrow by 6 PM.
Track at: https://www.amazon.in/track (official Amazon website)
For support: 1800-419-7355 (toll free)
Thank you for shopping with us.
"""

# ============================================================
# 🇮🇳 HINGLISH HIGH RISK EXAMPLE
# ============================================================

HINGLISH_HIGH_RISK = """
Bhai sun! Ek dum mast offer hai aaj ke liye.
Ye APK download karo aur free mein paisa kamao!
bit.ly/kamao-ghar-baithe
Turant karo warna offer khatam — sirf 100 log ko milega!
OTP aayega toh mujhe bhej do — main activate kar dunga.
"""

# HOW TO USE:
# 1. app.py run karo: streamlit run app.py
# 2. In messages ko copy karo
# 3. App ke text box mein paste karo
# 4. "Analyze" button click karo
# 5. Results dekho — judges ko impress karo!
