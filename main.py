import os
import resend  # Replaced smtplib
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Configure Resend
resend.api_key = os.getenv("RESEND_API_KEY")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL")
# We use 'onboarding@resend.dev' if you haven't verified a custom domain yet
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

def send_notification(user_email: str):
    if not resend.api_key or not NOTIFY_EMAIL:
        print("⚠️  Resend API Key or Notify Email not set — skipping.")
        return

    # Modern HTML content for the notification
    html_content = f"""
    <html><body style="font-family:sans-serif;padding:20px;color:#1a2744;">
      <h2 style="color:#1a73e8;">🚀 New Waitlist Signup!</h2>
      <p>A new user just joined the <strong>Gmail for Alexa</strong> waitlist:</p>
      <div style="background:#f1f3f4;padding:15px;border-radius:8px;font-size:18px;border:1px solid #dee2e6;">
        <strong>Email:</strong> {user_email}
      </div>
      <p style="font-size:12px;color:#5f6368;margin-top:20px;">Sent via Resend API (Port 443)</p>
    </body></html>
    """

    params = {
        "from": FROM_EMAIL,
        "to": [NOTIFY_EMAIL],
        "subject": f"🎉 New Waitlist Signup: {user_email}",
        "html": html_content,
    }

    # Resend sends via HTTPS (443), which works on Railway
    resend.Emails.send(params)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/signup")
async def signup(email: str = Form(...)):
    print(f"[WAITLIST] New signup: {email}")
    try:
        send_notification(email)
        print(f"[WAITLIST] Notification successfully sent to {NOTIFY_EMAIL}")
    except Exception as e:
        print(f"[WAITLIST] Notification error: {e}")
    
    return JSONResponse({"success": True, "message": "You're on the list!"})