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
      <p>A new user just joined the <strong>Email for Alexa</strong> waitlist:</p>
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

# --- PRIVACY POLICY ROUTE ---
@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Privacy Policy - EmailForAlexa</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                line-height: 1.6; 
                max-width: 800px; 
                margin: 40px auto; 
                padding: 0 20px; 
                color: #243156; 
            }
            h1, h2 { color: #243156; }
            .limited-use { background-color: #f8f9fa; padding: 15px; border-left: 4px solid #1a73e8; margin: 20px 0; border-radius: 4px; }
        </style>
    </head>
    <body>
        <h1>Privacy Policy for Email For Alexa</h1>
        <p><strong>Last Updated:</strong> March 2026</p>

        <h2>1. Information We Collect</h2>
        <p>Student OS accesses your Gmail account (read, compose, send) and basic profile information solely for the purpose of Account Linking and providing the core voice assistant features.</p>

        <h2>2. How We Use Information</h2>
        <p>Your data is used exclusively to facilitate voice-activated email summaries and drafting via Alexa. We do not use your data for advertising or sell it to third parties.</p>

        <div class="limited-use">
            <strong>Google API Limited Use Disclosure:</strong>
            <p>Student OS's use and transfer to any other app of information received from Google APIs will adhere to the <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank">Google API Services User Data Policy</a>, including the Limited Use requirements.</p>
        </div>

        <h2>3. Data Sharing & AI Processing</h2>
        <p>To generate email summaries and draft responses, email content is temporarily transmitted to a third-party AI provider (OpenRouter/Large Language Models). This data is processed in memory to generate the requested text and is not permanently stored or used to train public AI models.</p>

        <h2>4. Data Storage & Security</h2>
        <p>Student OS does not permanently store your emails, passwords, or personal correspondence on our servers. We only retain secure, temporary OAuth tokens required to maintain the connection between your Alexa account and your Google account.</p>

        <h2>5. Contact Us</h2>
        <p>If you have any questions about this policy, please contact the developer at isong@westmont.edu.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# --- NEW TERMS OF SERVICE ROUTE ---
@app.get("/terms", response_class=HTMLResponse)
async def terms_of_service():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Terms of Service - EmailForAlexa</title>
        <style>
            body { 
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
                line-height: 1.6; 
                max-width: 800px; 
                margin: 40px auto; 
                padding: 0 20px; 
                color: #243156; 
            }
            h1, h2 { color: #243156; }
        </style>
    </head>
    <body>
        <h1>Terms of Service for Email For Alexa</h1>
        <p><strong>Last Updated:</strong> March 2026</p>

        <h2>1. Acceptance of Terms</h2>
        <p>By accessing and using EmailForAlexa (the "Service"), you accept and agree to be bound by the terms and provision of this agreement. If you do not agree to abide by these terms, please do not use this Service.</p>

        <h2>2. Description of Service</h2>
        <p>EmailForAlexa is an experimental, voice-activated application that connects Amazon Alexa to your Gmail account. It utilizes third-party Large Language Models (LLMs) to summarize and draft emails on your behalf.</p>

        <h2>3. User Responsibilities</h2>
        <p>You are responsible for maintaining the confidentiality of your connected accounts. Because this Service uses Generative AI, you agree to independently verify any drafted emails before allowing the Service to send them. The developer is not responsible for the content of emails generated or sent via the Service.</p>

        <h2>4. Disclaimer of Warranties (As-Is)</h2>
        <p>The Service is provided on an "AS IS" and "AS AVAILABLE" basis. As an academic/beta project, the Service makes no guarantees regarding uptime, reliability, or accuracy of the AI-generated responses.</p>

        <h2>5. Limitation of Liability</h2>
        <p>In no event shall the developer be liable for any indirect, incidental, special, or consequential damages arising out of or in connection with your use of the Service, including but not limited to lost emails, unintended communications, or data loss.</p>

        <h2>6. Contact</h2>
        <p>If you have any questions regarding these Terms, please contact isong@westmont.edu.</p>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)
# --------------------------------

@app.post("/signup")
async def signup(email: str = Form(...)):
    print(f"[WAITLIST] New signup: {email}")
    try:
        send_notification(email)
        print(f"[WAITLIST] Notification successfully sent to {NOTIFY_EMAIL}")
    except Exception as e:
        print(f"[WAITLIST] Notification error: {e}")
    
    return JSONResponse({"success": True, "message": "You're on the list!"})