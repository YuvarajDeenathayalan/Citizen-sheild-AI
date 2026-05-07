from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import smtplib
from email.message import EmailMessage

app = FastAPI()

# Allow frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class ScamMessage(BaseModel):
    message: str

class LoginUser(BaseModel):
    username: str
    password: str

# --- Email Sending Function ---
def send_login_notification(username: str):
    # --- Email Configuration ---
    # IMPORTANT: Replace with your email and an "App Password" from your Google Account.
    # DO NOT use your regular Google password.
    # How to generate an App Password: https://support.google.com/accounts/answer/185833
    SENDER_EMAIL = "your_email@gmail.com"  # Replace with your full Gmail address
    SENDER_PASSWORD = "your_app_password"    # Replace with your 16-character app password
    RECIPIENT_EMAIL = "yuvaraj200924@gmail.com"

    # --- Create Email Message ---
    msg = EmailMessage()
    msg['Subject'] = "✅ Successful Login to Citizen Safety Platform"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg.set_content(f"User '{username}' just logged into the application.")

    # --- Send Email ---
    try:
        print("Connecting to email server...")
        # Connect to Gmail's SMTP server
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            smtp.send_message(msg)
        print("Email notification sent successfully!")

    except Exception as e:
        print(f"--- FAILED TO SEND EMAIL ---")
        print(f"An error occurred: {e}")
        print(f"Please check your email configuration in backend/main.py")
        print(f"--------------------------")


# Scam Detection Route
@app.post("/detect-scam")
def detect_scam(data: ScamMessage):

    text = data.message.lower()

    scam_words = [
        "urgent",
        "bank",
        "otp",
        "click",
        "verify",
        "blocked",
        "lottery",
        "upi",
        "password",
        "link"
    ]

    score = 0

    for word in scam_words:

        if word in text:
            score += 15

    # Risk Logic
    if score >= 45:
        risk = "🚨 High Scam Probability"

    elif score >= 20:
        risk = "⚠️ Suspicious Message"

    else:
        risk = "✅ Looks Safe"

    return {
        "risk": risk,
        "score": score
    }

# Login Route
@app.post("/login")
def login(user: LoginUser):
    if user.username == "admin" and user.password == "password":
        print(f"Successful login for user: {user.username}")
        send_login_notification(user.username)
        return {"status": "success"}
    else:
        print(f"Failed login attempt for user: {user.username}")
        return {"status": "error", "message": "Invalid credentials"}


# Health check for the backend
@app.get("/api/health")
def health_check():
    return {"message": "CitizenShield AI Backend Running"}

# Mount the static files directory
app.mount("/", StaticFiles(directory=".", html = True), name="static")