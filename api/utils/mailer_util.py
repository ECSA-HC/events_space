import os
import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from passlib.context import CryptContext
from starlette.templating import Jinja2Templates
from dotenv import load_dotenv
from fastapi import HTTPException, BackgroundTasks
from datetime import datetime

load_dotenv()

YEAR = datetime.now().year
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
templates = Jinja2Templates(directory="templates")

# --- PASSWORD UTILS ---


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# --- CORE EMAIL SENDER ---


def send_email(recipient_email, subject, email_body):
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = os.getenv("SMTP_PORT", "")
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")

    if not smtp_host or not smtp_port:
        raise HTTPException(
            status_code=500,
            detail="SMTP host and port must be set in environment variables.",
        )

    try:
        smtp_port = int(smtp_port)
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="SMTP_PORT must be an integer.",
        )

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            message = MIMEMultipart()
            message["From"] = smtp_username
            message["To"] = recipient_email
            message["Subject"] = subject
            message.attach(MIMEText(email_body, "html"))
            server.sendmail(smtp_username, recipient_email, message.as_string())
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to send email. Error: {str(e)}"
        )


# --- BACKGROUND TASK WRAPPER ---
def send_email_backgroundable(
    recipient_email, subject, email_body, background_tasks: BackgroundTasks = None
):
    if background_tasks:
        background_tasks.add_task(send_email, recipient_email, subject, email_body)
    else:
        send_email(recipient_email, subject, email_body)


# --- EMAIL FUNCTIONS ---


def new_account_email(
    recipient_email, firstname, password, background_tasks: BackgroundTasks = None
):
    subject = "Welcome to ECSA-HC Event Spaces"
    template = templates.get_template("acount_creation_template.html")
    email_body = template.render(
        subject=subject,
        username=recipient_email,
        password=password,
        firstname=firstname,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def reset_password_request_email(
    recipient_email, firstname, reset_token, background_tasks: BackgroundTasks = None
):
    subject = "Password Reset Request"
    template = templates.get_template("password_reset_request_template.html")
    email_body = template.render(
        subject=subject,
        username=recipient_email,
        firstname=firstname,
        reset_token=reset_token,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def password_reset_email(
    recipient_email, firstname, background_tasks: BackgroundTasks = None
):
    subject = "Your ECSA-HC Event Spaces Account password has been reset"
    template = templates.get_template("password_reset_template.html")
    email_body = template.render(
        subject=subject,
        firstname=firstname,
        email=recipient_email,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def account_verification_email(
    recipient_email, firstname, background_tasks: BackgroundTasks = None
):
    subject = "Your ECSA-HC Event Spaces Account has been verified"
    template = templates.get_template("account_verification_template.html")
    email_body = template.render(
        subject=subject,
        email=recipient_email,
        firstname=firstname,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def account_verification_request_email(
    recipient_email,
    firstname,
    verification_token,
    background_tasks: BackgroundTasks = None,
):
    subject = "Account Verification Request"
    template = templates.get_template("account_verification_request_template.html")
    email_body = template.render(
        subject=subject,
        email=recipient_email,
        firstname=firstname,
        verification_token=verification_token,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def organisation_verification_request_email(
    recipient_email, firstname, organisation, background_tasks: BackgroundTasks = None
):
    subject = "Organisation Verification Request"
    template = templates.get_template("organisation_verification_request_template.html")
    email_body = template.render(
        subject=subject,
        email=recipient_email,
        firstname=firstname,
        organisation=organisation.organisation,
        organisation_id=organisation.id,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def organisation_approval_status_email(
    recipient_email,
    firstname,
    organisation,
    status,
    background_tasks: BackgroundTasks = None,
):
    subject = "Organisation Approval Status"
    template = templates.get_template("organisation_approval_status_template.html")
    email_body = template.render(
        subject=subject,
        email=recipient_email,
        firstname=firstname,
        organisation=organisation.organisation,
        organisation_id=organisation.id,
        status=status,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)
