from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Date
from models.models import (
    EventAttendance,
    Registration,
)  # Make sure Registration model is imported
from schemas.events_space import AttendanceCreate


def create_attendance(db: Session, data: AttendanceCreate):
    today = date.today()

    # Check if the registration exists
    registration = (
        db.query(Registration).filter(Registration.id == data.registration_id).first()
    )
    if not registration:
        raise ValueError("User not registered")

    # Check if attendance already exists for this registration today
    existing = (
        db.query(EventAttendance)
        .filter(
            EventAttendance.registration_id == data.registration_id,
            EventAttendance.created_at.cast(Date) == today,
        )
        .first()
    )
    if existing:
        raise ValueError("Attendance already recorded for today")

    attendance = EventAttendance(registration_id=data.registration_id)
    db.add(attendance)
    try:
        db.commit()
        db.refresh(attendance)
        return attendance
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Database error while recording attendance: {str(e.orig)}")


def get_attendance(db: Session, attendance_id: int):
    return db.query(EventAttendance).filter(EventAttendance.id == attendance_id).first()


def get_all_attendances(db: Session, skip: int = 0, limit: int = 100):
    return db.query(EventAttendance).offset(skip).limit(limit).all()


def delete_attendance(db: Session, attendance_id: int):
    attendance = (
        db.query(EventAttendance).filter(EventAttendance.id == attendance_id).first()
    )
    if attendance:
        db.delete(attendance)
        db.commit()
        return True
    return False
