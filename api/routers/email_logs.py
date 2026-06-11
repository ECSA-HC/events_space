from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from core.database import get_db
from dependencies.auth_dependency import Auth, get_current_user
from models.models import EmailLog

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_auth_dep(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


@router.get("/")
def list_email_logs(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    skip: int = 0,
    limit: int = 500,
    email_type: str = None,
):
    auth_dependency.secure_access("VIEW_USER", current_user["user_id"])
    q = db.query(EmailLog).options(joinedload(EmailLog.sent_by))
    if email_type:
        q = q.filter(EmailLog.email_type == email_type)
    total = q.count()
    logs = q.order_by(EmailLog.sent_at.desc()).offset(skip).limit(limit).all()
    return {
        "total": total,
        "data": [
            {
                "id": log.id,
                "recipient_email": log.recipient_email,
                "subject": log.subject,
                "email_type": log.email_type,
                "sent_by": f"{log.sent_by.firstname} {log.sent_by.lastname}" if log.sent_by else None,
                "sent_by_email": log.sent_by.email if log.sent_by else None,
                "reply_to_email": log.reply_to_email,
                "status": log.status,
                "error_message": log.error_message,
                "sent_at": log.sent_at,
            }
            for log in logs
        ],
    }
