import smtplib
import os
from email.mime.text import MIMEText

# --- CONFIG ---
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER') 
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD') # Generate this in Google Account > Security > App Passwords

FROM_EMAIL = "Manyan IP Services <no.reply.manyan@gmail.com>"
TO_EMAIL = "ravi5258p@gmail.com"
# -------------

def send_test_email():
    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        print("❌ ERROR: Environment variables not set")
        print("Set EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
        return

    try:
        print("🔌 Connecting to Gmail SMTP...")
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()

        print("🔐 Logging in...")
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

        msg = MIMEText("This is a test email from Python SMTP script.")
        msg["Subject"] = "SMTP Test Successful"
        msg["From"] = FROM_EMAIL
        msg["To"] = TO_EMAIL

        print("📨 Sending email...")
        server.sendmail(EMAIL_HOST_USER, TO_EMAIL, msg.as_string())

        server.quit()
        print("✅ SUCCESS: Email sent successfully")

    except smtplib.SMTPAuthenticationError:
        print("❌ AUTH ERROR")
        print("✔ Use 16-digit Gmail App Password")
        print("✔ Enable 2-Step Verification")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    send_test_email()
