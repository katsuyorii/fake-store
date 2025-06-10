import asyncio

import aiosmtplib

from email.message import EmailMessage

from src.celery import celery_app
from src.settings import smtp_settings


async def async_send_email(to_email: str, subject: str, body: str) -> None:
    message = EmailMessage()
    message["From"] = smtp_settings.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.add_alternative(body, subtype="html")

    await aiosmtplib.send(
        message,
        hostname=smtp_settings.SMTP_HOST,
        port=smtp_settings.SMTP_PORT,
        start_tls=True,
        username=smtp_settings.SMTP_USER,
        password=smtp_settings.SMTP_PASSWORD,
    )

@celery_app.task
def send_email_task(to_email: str, subject: str, body: str) -> None:
    asyncio.run(async_send_email(to_email, subject, body))