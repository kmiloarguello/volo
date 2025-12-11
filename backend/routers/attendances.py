from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from database.connection import get_db
from database.models import Attendance as AttendanceModel
from schemas import Attendance, AttendanceCreate, AttendanceUpdate, AttendancesResponse

router = APIRouter()

@router.post("/", response_model=Attendance)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    # Check if attendance already exists for this volunteer and activity
    existing = db.query(AttendanceModel).filter(
        AttendanceModel.volunteer_id == attendance.volunteer_id,
        AttendanceModel.activity_id == attendance.activity_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Attendance record already exists for this volunteer and activity"
        )
    
    db_attendance = AttendanceModel(**attendance.model_dump())
    db.add(db_attendance)
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.get("/", response_model=AttendancesResponse)
def read_attendances(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    volunteer_id: Optional[UUID] = None,
    activity_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AttendanceModel)
    
    if volunteer_id:
        query = query.filter(AttendanceModel.volunteer_id == volunteer_id)
    
    if activity_id:
        query = query.filter(AttendanceModel.activity_id == activity_id)
    
    if status:
        query = query.filter(AttendanceModel.status == status)
    
    total = query.count()
    attendances = query.offset(skip).limit(limit).all()
    
    return {
        "attendances": attendances,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{attendance_id}", response_model=Attendance)
def read_attendance(attendance_id: UUID, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    return attendance

@router.put("/{attendance_id}", response_model=Attendance)
def update_attendance(
    attendance_id: UUID,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    db_attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if db_attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    attendance_data = attendance.model_dump(exclude_unset=True)
    
    # Validate time constraints if both times are provided
    check_in_at = attendance_data.get('check_in_at', db_attendance.check_in_at)
    check_out_at = attendance_data.get('check_out_at', db_attendance.check_out_at)
    
    if check_in_at and check_out_at and check_out_at <= check_in_at:
        raise HTTPException(status_code=400, detail="Check-out time must be after check-in time")
    
    for key, value in attendance_data.items():
        setattr(db_attendance, key, value)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.post("/{attendance_id}/check-in")
def check_in(attendance_id: UUID, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    if attendance.check_in_at is not None:
        raise HTTPException(status_code=400, detail="Already checked in")
    
    attendance.check_in_at = datetime.utcnow()
    db.commit()
    db.refresh(attendance)
    
    return {"message": "Check-in successful", "check_in_at": attendance.check_in_at}

@router.post("/{attendance_id}/check-out")
def check_out(attendance_id: UUID, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    if attendance.check_in_at is None:
        raise HTTPException(status_code=400, detail="Must check in first")
    
    if attendance.check_out_at is not None:
        raise HTTPException(status_code=400, detail="Already checked out")
    
    attendance.check_out_at = datetime.utcnow()
    db.commit()
    db.refresh(attendance)
    
    return {"message": "Check-out successful", "check_out_at": attendance.check_out_at}

@router.post("/{attendance_id}/verify")
def verify_attendance(
    attendance_id: UUID,
    verified_by_user_id: UUID,
    db: Session = Depends(get_db)
):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    if attendance.check_in_at is None or attendance.check_out_at is None:
        raise HTTPException(status_code=400, detail="Attendance must have both check-in and check-out times")
    
    attendance.status = "Verified"
    attendance.verified_by_user_id = verified_by_user_id
    db.commit()
    db.refresh(attendance)
    
    return {"message": "Attendance verified successfully"}

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: UUID, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    db.delete(attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}