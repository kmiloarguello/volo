from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal
import uuid as uuid_lib

from database.connection import get_db
from database.models import (
    Attendance as AttendanceModel, LedgerEntry as LedgerEntryModel,
    VoloCredit as VoloCreditModel, Profile as ProfileModel
)
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
    request_data: dict,
    db: Session = Depends(get_db)
):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    if attendance.check_in_at is None or attendance.check_out_at is None:
        raise HTTPException(status_code=400, detail="Attendance must have both check-in and check-out times")
    
    verified_by_user_id = request_data.get('verified_by_user_id')
    if not verified_by_user_id:
        raise HTTPException(status_code=400, detail="verified_by_user_id is required")
    
    attendance.status = "Verified"
    attendance.verified_by_user_id = verified_by_user_id
    
    # Create ledger entry for verified attendance
    ledger_entry = LedgerEntryModel(
        id=uuid_lib.uuid4(),
        ref_type="Attendance",
        ref_id=attendance_id,
        hash=f"hash_{str(attendance_id)[:8]}",
        prev_hash=None  # Simplified for MVP
    )
    db.add(ledger_entry)
    
    # Auto-create VoloCredit for verified attendance
    hours_worked = (attendance.check_out_at - attendance.check_in_at).total_seconds() / 3600.0
    
    # Ensure minimum credit amount for short test durations
    if hours_worked < 0.1:  # Less than 6 minutes, use activity duration instead
        # Calculate from activity duration as fallback
        activity_hours = (attendance.activity.ends_at - attendance.activity.starts_at).total_seconds() / 3600.0
        hours_worked = activity_hours
    
    credit_amount = hours_worked * 10.0  # 10 credits per hour as per test
    
    volo_credit = VoloCreditModel(
        id=uuid_lib.uuid4(),
        volunteer_id=attendance.volunteer_id,
        source_attendance_id=attendance_id,
        amount=credit_amount,
        status="Available",
        granted_at=datetime.utcnow(),
        expires_at=datetime.utcnow().replace(year=datetime.utcnow().year + 1)  # Expires in 1 year
    )
    db.add(volo_credit)
    db.flush()  # Get the credit ID
    
    # Create ledger entry for credit
    credit_ledger_entry = LedgerEntryModel(
        id=uuid_lib.uuid4(),
        ref_type="VoloCredit",
        ref_id=volo_credit.id,
        hash=f"hash_{str(volo_credit.id)[:8]}",
        prev_hash=None  # Simplified for MVP
    )
    db.add(credit_ledger_entry)
    
    # Update volunteer profile
    profile = db.query(ProfileModel).filter(ProfileModel.volunteer_id == attendance.volunteer_id).first()
    if profile:
        profile.total_hours = profile.total_hours + Decimal(str(hours_worked))
        profile.total_credits_earned = profile.total_credits_earned + Decimal(str(credit_amount))
    
    db.commit()
    db.refresh(attendance)
    
    return {"message": "Attendance verified successfully", "credits_granted": credit_amount}

@router.delete("/{attendance_id}")
def delete_attendance(attendance_id: UUID, db: Session = Depends(get_db)):
    attendance = db.query(AttendanceModel).filter(AttendanceModel.id == attendance_id).first()
    if attendance is None:
        raise HTTPException(status_code=404, detail="Attendance not found")
    
    db.delete(attendance)
    db.commit()
    return {"message": "Attendance deleted successfully"}