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

FROM_NAME  = "ECSA Events"
FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", "admission@cosecsa.org")

# --- PASSWORD UTILS ---


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)


# --- CORE EMAIL SENDER ---


logger = logging.getLogger(__name__)


def _log_email(db, recipient_email, subject, email_type, sent_by_user_id, reply_to_email, status, error_message=None):
    """Persist a record of every email attempt to email_log."""
    try:
        from models.models import EmailLog
        record = EmailLog(
            recipient_email=recipient_email,
            subject=subject,
            email_type=email_type,
            sent_by_user_id=sent_by_user_id,
            reply_to_email=reply_to_email,
            status=status,
            error_message=error_message,
        )
        db.add(record)
        db.commit()
    except Exception as log_err:
        logger.error("Failed to write email log: %s", log_err)


def send_email(recipient_email, subject, email_body, reply_to_email=None,
               email_type="general", sent_by_user_id=None, db=None):
    smtp_host     = os.getenv("SMTP_HOST", "")
    smtp_port     = os.getenv("SMTP_PORT", "")
    smtp_username = os.getenv("SMTP_USERNAME", "")
    smtp_password = os.getenv("SMTP_PASSWORD", "")

    if not smtp_host or not smtp_port:
        logger.error("SMTP host and port must be set in environment variables.")
        if db:
            _log_email(db, recipient_email, subject, email_type, sent_by_user_id,
                       reply_to_email, "failed", "SMTP not configured")
        return

    try:
        smtp_port = int(smtp_port)
    except ValueError:
        logger.error("SMTP_PORT must be an integer.")
        return

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            message = MIMEMultipart()
            message["From"]    = f"{FROM_NAME} <{FROM_EMAIL}>"
            message["To"]      = recipient_email
            message["Subject"] = subject
            if reply_to_email:
                message["Reply-To"] = reply_to_email
            message.attach(MIMEText(email_body, "html"))
            server.sendmail(smtp_username, recipient_email, message.as_string())
            logger.info("Email sent successfully to %s", recipient_email)
            if db:
                _log_email(db, recipient_email, subject, email_type, sent_by_user_id,
                           reply_to_email, "sent")
    except Exception as e:
        logger.error("Failed to send email to %s: %s", recipient_email, str(e))
        if db:
            _log_email(db, recipient_email, subject, email_type, sent_by_user_id,
                       reply_to_email, "failed", str(e))


# --- BACKGROUND TASK WRAPPER ---
def send_email_backgroundable(
    recipient_email, subject, email_body, background_tasks: BackgroundTasks = None,
    reply_to_email=None, email_type="general", sent_by_user_id=None, db=None,
):
    if background_tasks:
        background_tasks.add_task(
            send_email, recipient_email, subject, email_body,
            reply_to_email, email_type, sent_by_user_id, db,
        )
    else:
        send_email(recipient_email, subject, email_body,
                   reply_to_email, email_type, sent_by_user_id, db)


# --- EMAIL FUNCTIONS ---


def new_account_email(
    recipient_email, firstname, password, event_name=None, background_tasks: BackgroundTasks = None
):
    subject = "Welcome to ECSA Events Portal – Your Account Details"
    template = templates.get_template("acount_creation_template.html")
    email_body = template.render(
        subject=subject,
        username=recipient_email,
        password=password,
        firstname=firstname,
        event_name=event_name,
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


def payment_reminder_email(
    recipient_email,
    firstname,
    event_name,
    payment_url="https://ecsahc.org/payment_bpf2026/",
    portal_url="https://events.ecsahc.org",
    background_tasks: BackgroundTasks = None,
):
    subject = f"Action Required: Complete Your Payment – {event_name}"
    template = templates.get_template("payment_reminder_template.html")
    email_body = template.render(
        subject=subject,
        firstname=firstname,
        event_name=event_name,
        payment_url=payment_url,
        portal_url=portal_url,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def event_invitation_email(
    recipient_email,
    firstname,
    event_name,
    participation_role,
    event_location=None,
    event_dates=None,
    is_new_user=False,
    password=None,
    no_payment=False,
    portal_url="https://events.ecsahc.org",
    payment_url="https://ecsahc.org/payment_bpf2026/",
    background_tasks: BackgroundTasks = None,
):
    subject = f"You Have Been Registered for {event_name} – ECSA Events Portal"
    template = templates.get_template("event_invitation_template.html")
    email_body = template.render(
        subject=subject,
        firstname=firstname,
        email=recipient_email,
        event_name=event_name,
        participation_role=participation_role,
        event_location=event_location,
        event_dates=event_dates,
        is_new_user=is_new_user,
        password=password,
        no_payment=no_payment,
        portal_url=portal_url,
        payment_url=payment_url,
        year=YEAR,
    )
    send_email_backgroundable(recipient_email, subject, email_body, background_tasks)


def reviewer_assignment_email(
    recipient_email,
    firstname,
    password,
    abstract_title,
    event_name=None,
    assigned_by_name=None,
    sent_by_user_id=None,
    background_tasks: BackgroundTasks = None,
    db=None,
):
    subject = "You Have Been Assigned an Abstract to Review – ECSA Events Portal"
    template = templates.get_template("reviewer_assignment_template.html")
    email_body = template.render(
        subject=subject,
        username=recipient_email,
        firstname=firstname,
        password=password,
        abstract_title=abstract_title,
        event_name=event_name,
        assigned_by_name=assigned_by_name or "ECSA Secretariat",
        year=YEAR,
    )
    send_email_backgroundable(
        recipient_email, subject, email_body, background_tasks,
        email_type="reviewer_assignment",
        sent_by_user_id=sent_by_user_id,
        db=db,
    )
