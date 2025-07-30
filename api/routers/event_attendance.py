from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.events_space import AttendanceCreate, AttendanceRead
from crud import crud_event_attendance
from core.database import get_db

router = APIRouter(prefix="/events", tags=["EventAttendance"])


@router.post("/{event_id}/attendance", response_model=AttendanceRead)
def register_attendance(
    event_id: int, data: AttendanceCreate, db: Session = Depends(get_db)
):
    try:
        return crud_event_attendance.create_attendance(db, data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/attendance/{attendance_id}", response_model=AttendanceRead)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = crud_event_attendance.get_attendance(db, attendance_id)
    if not attendance:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance


@router.get("/attendance/", response_model=list[AttendanceRead])
def list_attendances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud_event_attendance.get_all_attendances(db, skip=skip, limit=limit)


@router.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    success = crud_event_attendance.delete_attendance(db, attendance_id)
    if not success:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return {"detail": "Attendance deleted"}
