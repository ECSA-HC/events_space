from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
from typing import Optional

from core.database import get_db
from dependencies.auth_dependency import Auth, get_current_user
from models.models import ActivityLog, User

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


def get_auth_dep(db: Session = Depends(get_db)) -> Auth:
    return Auth(db)


@router.get("/")
def get_activity_log(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
    hours: int = Query(default=24, ge=1, le=168),
    action: str = Query(default=""),
    search: str = Query(default=""),
    limit: int = Query(default=300, le=500),
):
    auth_dependency.secure_access("VIEW_USER", current_user["user_id"])

    since = datetime.utcnow() - timedelta(hours=hours)

    q = (
        db.query(ActivityLog)
        .filter(ActivityLog.deleted_at == None, ActivityLog.created_at >= since)
    )

    if action:
        q = q.filter(ActivityLog.action == action)

    if search:
        user_ids_match = [
            u.id for u in db.query(User).filter(
                User.deleted_at == None,
                or_(
                    User.firstname.ilike(f"%{search}%"),
                    User.lastname.ilike(f"%{search}%"),
                    User.email.ilike(f"%{search}%"),
                )
            ).all()
        ]
        q = q.filter(ActivityLog.user_id.in_(user_ids_match))

    logs = q.order_by(ActivityLog.created_at.desc()).limit(limit).all()

    # Bulk-load users to avoid N+1
    user_ids = list({l.user_id for l in logs if l.user_id})
    users = {u.id: u for u in db.query(User).filter(User.id.in_(user_ids)).all()}

    serialized = [
        {
            "id":         l.id,
            "user_id":    l.user_id,
            "user_name":  (
                f"{users[l.user_id].firstname} {users[l.user_id].lastname}"
                if l.user_id and l.user_id in users else "System"
            ),
            "user_email": users[l.user_id].email if l.user_id and l.user_id in users else None,
            "action":     l.action,
            "target":     l.target,
            "ip_address": l.ip_address,
            "created_at": l.created_at.isoformat() if l.created_at else None,
        }
        for l in logs
    ]

    logins        = sum(1 for l in logs if l.action == "USER_LOGIN")
    registrations = sum(1 for l in logs if l.action == "USER_REGISTER")
    unique_users  = len({l.user_id for l in logs if l.user_id})
    total         = len(logs)

    return {
        "logs": serialized,
        "stats": {
            "total":         total,
            "logins":        logins,
            "registrations": registrations,
            "unique_users":  unique_users,
        },
    }


@router.get("/actions")
def get_action_types(
    current_user: user_dependency,
    db: Session = Depends(get_db),
    auth_dependency: Auth = Depends(get_auth_dep),
):
    """Return distinct action types for filter dropdown."""
    auth_dependency.secure_access("VIEW_USER", current_user["user_id"])
    rows = db.query(ActivityLog.action).filter(ActivityLog.deleted_at == None).distinct().all()
    return sorted([r[0] for r in rows])
