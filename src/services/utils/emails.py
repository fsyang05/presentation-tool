import smtplib
import ssl
import os
from dotenv import load_dotenv
from pathlib import Path
from email.message import EmailMessage

load_dotenv()
FROM_EMAIL = os.getenv("FROM_EMAIL")
APP_PASS = os.getenv("GOOGLE_APP_PASSWORD")

PDF_PATH = Path(__file__).resolve().parents[2] / "presentation.pdf"

async def send_presentation_email(
    to_email: str,
) -> str:
    """Send an email with a single PDF attachment.

    Returns the Message-ID on success.
    """
    pdf_path = Path(PDF_PATH)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    msg = EmailMessage()
    msg["From"]     = FROM_EMAIL
    msg["To"]       = to_email
    msg["Subject"]  = "Presentation for Wahl Heating, Cooling, and Plumbing"
    msg.set_content("Here is your presentation.")

    msg.add_attachment(
        pdf_path.read_bytes(),
        maintype="application",
        subtype="pdf",
        filename=pdf_path.name
    )

    context = ssl.create_default_context()
    with smtplib.SMTP(host="smtp.gmail.com", port=587) as server:
        server.starttls(context=context)
        server.login(FROM_EMAIL, APP_PASS)
        response = server.send_message(msg)

    if response:  # any failed recipients
        raise smtplib.SMTPException(f"Failed to deliver to: {list(response.keys())}")

    return msg.get("Message-ID", "")

