import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")

NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))


def send_notification(email: str):
    if not all([NOTIFY_EMAIL, SMTP_USER, SMTP_PASS]):
        print("⚠️  SMTP env vars not set — skipping email notification.")
        return

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🎉 New Waitlist Signup: {email}"
    msg["From"] = SMTP_USER
    msg["To"] = NOTIFY_EMAIL

    html = f"""
    <html><body style="font-family:sans-serif;padding:20px;">
      <h2 style="color:#4285F4;">New Waitlist Signup!</h2>
      <p>Someone just joined the <strong>Gmail for Alexa</strong> waitlist:</p>
      <p style="font-size:18px;background:#f1f3f4;padding:12px 16px;border-radius:8px;">
        📧 <strong>{email}</strong>
      </p>
    </body></html>
    """
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, NOTIFY_EMAIL, msg.as_string())


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/signup")
async def signup(email: str = Form(...)):
    print(f"[WAITLIST] New signup: {email}")
    try:
        send_notification(email)
        print(f"[WAITLIST] Notification sent for: {email}")
    except Exception as e:
        print(f"[WAITLIST] Email notification failed: {e}")
    return JSONResponse({"success": True, "message": "You're on the list!"})
