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
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")

def send_notification(user_email: str):
    if not resend.api_key or not NOTIFY_EMAIL:
        print("⚠️  Resend API Key or Notify Email not set — skipping.")
        return

    html_content = f"""
    <html><body style="font-family:sans-serif;padding:20px;color:#1a2744;">
      <h2 style="color:#1a73e8;">🚀 New Waitlist Signup!</h2>
      <p>A new user just joined the <strong>Mail Brief</strong> waitlist:</p>
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

    resend.Emails.send(params)

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


SHARED_STYLES = """
    @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@600;700&family=DM+Sans:wght@400;500&display=swap');

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        font-family: 'DM Sans', sans-serif;
        background-color: #f8f9fb;
        color: #1a2744;
        line-height: 1.7;
    }

    header {
        background-color: #1a2744;
        padding: 18px 40px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    header .logo {
        font-family: 'Nunito', sans-serif;
        font-weight: 700;
        font-size: 20px;
        color: #ffffff;
        text-decoration: none;
    }

    header .logo span {
        color: #f59e0b;
    }

    .page-hero {
        background-color: #1a2744;
        padding: 56px 40px 48px;
        text-align: center;
    }

    .page-hero h1 {
        font-family: 'Nunito', sans-serif;
        font-size: 36px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 10px;
    }

    .page-hero .underline-bar {
        width: 52px;
        height: 3px;
        background: #f59e0b;
        border-radius: 2px;
        margin: 0 auto 16px;
    }

    .page-hero p {
        color: rgba(255,255,255,0.65);
        font-size: 15px;
    }

    .content-wrap {
        max-width: 780px;
        margin: 0 auto;
        padding: 56px 24px 80px;
    }

    h2 {
        font-family: 'Nunito', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #1a2744;
        margin-top: 40px;
        margin-bottom: 10px;
    }

    p, li {
        font-size: 15px;
        color: #374151;
        margin-bottom: 12px;
    }

    ul {
        padding-left: 20px;
        margin-bottom: 12px;
    }

    a {
        color: #1a2744;
        text-decoration: underline;
        text-underline-offset: 3px;
    }

    a:hover { color: #f59e0b; }

    .highlight-box {
        background: #fff;
        border-left: 4px solid #f59e0b;
        border-radius: 0 8px 8px 0;
        padding: 18px 22px;
        margin: 28px 0;
        box-shadow: 0 1px 4px rgba(26,39,68,0.07);
    }

    .highlight-box p { margin-bottom: 0; }

    .highlight-box strong {
        display: block;
        font-family: 'Nunito', sans-serif;
        font-size: 14px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #1a2744;
        margin-bottom: 8px;
    }

    .divider {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 36px 0;
    }

    footer {
        background-color: #1a2744;
        text-align: center;
        padding: 24px;
        font-size: 13px;
        color: rgba(255,255,255,0.45);
    }

    footer a { color: rgba(255,255,255,0.6); }
"""


# --- PRIVACY POLICY ROUTE ---
@app.get("/privacy", response_class=HTMLResponse)
async def privacy_policy():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Privacy Policy — Mail Brief</title>
    <style>{SHARED_STYLES}</style>
</head>
<body>

<header>
    <a class="logo" href="/">Mail<span>Brief</span></a>
</header>

<div class="page-hero">
    <h1>Privacy Policy</h1>
    <div class="underline-bar"></div>
    <p>Last updated: March 2026</p>
</div>

<div class="content-wrap">

    <p>Mail Brief ("we," "us," or "our") is committed to protecting your privacy. This policy explains what information we collect, how we use it, and your rights in connection with our Alexa skill.</p>

    <h2>1. Information We Collect</h2>
    <p>When you link your Google account, Mail Brief requests access to your Gmail account using the <code>gmail.modify</code> scope. This allows the skill to:</p>
    <ul>
        <li>Read and summarize your emails</li>
        <li>Compose and send emails on your behalf</li>
        <li>Mark emails as read</li>
    </ul>
    <p>We also receive basic Google profile information (name, email address) as part of the OAuth authorization process.</p>

    <h2>2. How We Use Your Information</h2>
    <p>Your data is used exclusively to provide Mail Brief's core functionality — hands-free email management through Amazon Alexa. We do not use your data for advertising, analytics, or any purpose beyond delivering the service you requested.</p>

    <div class="highlight-box">
        <strong>Google API Limited Use Disclosure</strong>
        <p>Mail Brief's use and transfer of information received from Google APIs to any other app will adhere to the <a href="https://developers.google.com/terms/api-services-user-data-policy" target="_blank">Google API Services User Data Policy</a>, including the Limited Use requirements. We do not use Google user data to develop, improve, or train generalized AI or ML models.</p>
    </div>

    <h2>3. AI Processing</h2>
    <p>To generate email summaries and draft responses, email content is temporarily transmitted to a third-party AI provider (OpenRouter) for processing. This data is handled in memory only and is not permanently stored, sold, or used to train AI models.</p>

    <h2>4. Data Storage & Security</h2>
    <p>Mail Brief does not permanently store your emails or personal correspondence. We retain only the OAuth tokens necessary to maintain your Google account connection. These tokens are stored securely and never logged or shared.</p>

    <h2>5. Data Sharing</h2>
    <p>We do not sell, rent, or share your personal information with third parties except as necessary to operate the service (e.g., our AI processing provider), or as required by law.</p>

    <h2>6. Revoking Access</h2>
    <p>You can revoke Mail Brief's access to your Google account at any time by visiting <a href="https://myaccount.google.com/permissions" target="_blank">Google Account Permissions</a> and removing Mail Brief. You can also disable the skill in the Alexa app.</p>

    <h2>7. Contact</h2>
    <p>If you have questions or concerns about this policy, please contact us at <a href="mailto:isong@westmont.edu">isong@westmont.edu</a>.</p>

    <hr class="divider">
    <p style="font-size:13px; color:#9ca3af;">This policy applies to the Mail Brief Alexa skill and its associated backend service hosted on Railway.</p>

</div>

<footer>
    &copy; 2026 Mail Brief &nbsp;|&nbsp; <a href="/privacy">Privacy</a> &nbsp;|&nbsp; <a href="/terms">Terms</a>
</footer>

</body>
</html>"""
    return HTMLResponse(content=html_content, status_code=200)


# --- TERMS OF SERVICE ROUTE ---
@app.get("/terms", response_class=HTMLResponse)
async def terms_of_service():
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Terms of Service — Mail Brief</title>
    <style>{SHARED_STYLES}</style>
</head>
<body>

<header>
    <a class="logo" href="/">Mail<span>Brief</span></a>
</header>

<div class="page-hero">
    <h1>Terms of Service</h1>
    <div class="underline-bar"></div>
    <p>Last updated: March 2026</p>
</div>

<div class="content-wrap">

    <p>These Terms of Service govern your use of Mail Brief (the "Service"), an Alexa skill that connects Amazon Alexa to your Gmail account. By enabling the skill, you agree to these terms.</p>

    <h2>1. Description of Service</h2>
    <p>Mail Brief is a voice-activated application that uses your linked Google account to read, summarize, compose, and send emails via Amazon Alexa. It uses third-party large language models (LLMs) to generate summaries and draft email content on your behalf.</p>

    <h2>2. Account Linking & Eligibility</h2>
    <p>To use Mail Brief, you must link a valid Google account through the Alexa app. You must own or have authorization to use any Google account you connect. You must be 13 years or older to use this Service.</p>

    <h2>3. User Responsibilities</h2>
    <ul>
        <li>You are responsible for maintaining the security of your connected Google account.</li>
        <li>Because Mail Brief uses generative AI, responses may occasionally be inaccurate. You agree to review any drafted email before allowing the Service to send it on your behalf.</li>
        <li>You agree not to use the Service for spam, harassment, phishing, or any unlawful purpose.</li>
    </ul>

    <div class="highlight-box">
        <strong>AI-Generated Content Notice</strong>
        <p>Mail Brief uses AI to summarize and draft emails. AI-generated content may contain errors or omissions. The developer is not responsible for any consequences arising from AI-generated content that is sent without review.</p>
    </div>

    <h2>4. Disclaimer of Warranties</h2>
    <p>The Service is provided on an "AS IS" and "AS AVAILABLE" basis. As a beta-stage project, Mail Brief makes no guarantees regarding uptime, reliability, or the accuracy of AI-generated content. We reserve the right to modify or discontinue the Service at any time without notice.</p>

    <h2>5. Limitation of Liability</h2>
    <p>To the fullest extent permitted by law, the developer shall not be liable for any indirect, incidental, special, or consequential damages arising from your use of the Service, including but not limited to lost emails, unintended communications, account access issues, or data loss.</p>

    <h2>6. Third-Party Services</h2>
    <p>Mail Brief integrates with Google Gmail, Amazon Alexa, and third-party AI providers. Your use of those services is governed by their respective terms. We are not responsible for the availability or actions of those third-party platforms.</p>

    <h2>7. Changes to These Terms</h2>
    <p>We may update these terms from time to time. Continued use of the Service after changes are posted constitutes your acceptance of the revised terms. The "Last Updated" date at the top of this page reflects the most recent revision.</p>

    <h2>8. Contact</h2>
    <p>Questions about these Terms? Reach us at <a href="mailto:isong@westmont.edu">isong@westmont.edu</a>.</p>

    <hr class="divider">
    <p style="font-size:13px; color:#9ca3af;">These terms apply to the Mail Brief Alexa skill and its associated backend service.</p>

</div>

<footer>
    &copy; 2026 Mail Brief &nbsp;|&nbsp; <a href="/privacy">Privacy</a> &nbsp;|&nbsp; <a href="/terms">Terms</a>
</footer>

</body>
</html>"""
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