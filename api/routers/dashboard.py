from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List
from pydantic import BaseModel
from core.database import get_db
from models.models import User, Event, Registration

router = APIRouter()


# Pydantic schema for a single event
class EventSummary(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    participants: int
    status: str  # upcoming or completed


# Dashboard response
class DashboardResponse(BaseModel):
    total_users: int
    upcoming_events_count: int
    completed_events_count: int
    recent_events: List[EventSummary]


@router.get("/", response_model=DashboardResponse)
def get_dashboard(db: Session = Depends(get_db)):
    today = datetime.utcnow()

    total_users = db.query(User).filter(User.deleted_at == None).count()

    upcoming_events_count = (
        db.query(Event)
        .filter(Event.start_date >= today, Event.deleted_at == None)
        .count()
    )

    completed_events_count = (
        db.query(Event).filter(Event.end_date < today, Event.deleted_at == None).count()
    )

    recent_events_db = (
        db.query(Event)
        .filter(Event.deleted_at == None)
        .order_by(Event.start_date.desc())
        .limit(5)
        .all()
    )

    recent_events = []
    for event in recent_events_db:
        participant_count = (
            db.query(Registration)
            .filter(Registration.event_id == event.id, Registration.deleted_at == None)
            .count()
        )

        status = "upcoming" if event.start_date >= today else "completed"

        recent_events.append(
            EventSummary(
                id=event.id,
                name=event.event,
                start_date=event.start_date.date(),
                end_date=event.end_date.date(),
                participants=participant_count,
                status=status,
            )
        )

    return DashboardResponse(
        total_users=total_users,
        upcoming_events_count=upcoming_events_count,
        completed_events_count=completed_events_count,
        recent_events=recent_events,
    )
