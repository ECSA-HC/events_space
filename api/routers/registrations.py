from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.models import Registration
from sqlalchemy.orm import joinedload

router = APIRouter()


def get_participant_event_status(db: Session, registration_id: int):
    registration = (
        db.query(Registration)
        .options(
            joinedload(Registration.user),
            joinedload(Registration.payment),
            joinedload(Registration.event_attendance),
        )
        .filter(Registration.id == registration_id)
        .first()
    )

    if not registration:
        return None

    user = registration.user
    payment = registration.payment
    attendance_records = registration.event_attendance
    attendance_dates = [att.attendance_date.date() for att in attendance_records]

    result = {
        "registration_id": registration.id,
        "participation_role": (
            registration.participation_role.name
            if registration.participation_role
            else None
        ),
        "paid": registration.paid,
        "user": {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "phone": user.phone,
            "email": user.email,
        },
        "payment": (
            {
                "id": payment.id if payment else None,
                "amount": getattr(payment, "amount", None),
                "status": getattr(payment, "status", None),
                "paid_at": getattr(payment, "paid_at", None),
            }
            if payment
            else None
        ),
        "attendance": {
            "count": len(attendance_records),
            "dates": attendance_dates,
        },
    }
    return result


@router.get("/participant_status/{registration_id}")
def participant_status(registration_id: int, db: Session = Depends(get_db)):
    data = get_participant_event_status(db, registration_id)
    if not data:
        raise HTTPException(status_code=404, detail="Registration not found")
    return data
