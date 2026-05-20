from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
from typing import List
from pydantic import BaseModel
from core.database import get_db
from models.models import User, Event, Registration, Abstract

router = APIRouter()


class EventSummary(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    participants: int
    status: str


class EventStatRow(BaseModel):
    id: int
    name: str
    registrations: int
    abstracts: int
    status: str


class DashboardResponse(BaseModel):
    total_users: int
    upcoming_events_count: int
    completed_events_count: int
    total_abstracts: int
    total_registrations: int
    recent_events: List[EventSummary]
    event_stats: List[EventStatRow]


@router.get("", response_model=DashboardResponse)
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

    total_abstracts = db.query(Abstract).filter(Abstract.deleted_at == None).count()

    total_registrations = (
        db.query(Registration).filter(Registration.deleted_at == None).count()
    )

    all_events = (
        db.query(Event)
        .filter(Event.deleted_at == None)
        .order_by(Event.start_date.desc())
        .all()
    )

    recent_events = []
    event_stats = []

    for event in all_events:
        reg_count = (
            db.query(Registration)
            .filter(Registration.event_id == event.id, Registration.deleted_at == None)
            .count()
        )
        abstract_count = (
            db.query(Abstract)
            .filter(Abstract.event_id == event.id, Abstract.deleted_at == None)
            .count()
        )
        status = "upcoming" if event.start_date >= today else "completed"

        event_stats.append(
            EventStatRow(
                id=event.id,
                name=event.event,
                registrations=reg_count,
                abstracts=abstract_count,
                status=status,
            )
        )

    # recent_events still uses the top 5 for the full-admin view
    for event in all_events[:5]:
        reg_count = next(
            (s.registrations for s in event_stats if s.id == event.id), 0
        )
        status = "upcoming" if event.start_date >= today else "completed"
        recent_events.append(
            EventSummary(
                id=event.id,
                name=event.event,
                start_date=event.start_date.date(),
                end_date=event.end_date.date(),
                participants=reg_count,
                status=status,
            )
        )

    return DashboardResponse(
        total_users=total_users,
        upcoming_events_count=upcoming_events_count,
        completed_events_count=completed_events_count,
        total_abstracts=total_abstracts,
        total_registrations=total_registrations,
        recent_events=recent_events,
        event_stats=event_stats,
    )
