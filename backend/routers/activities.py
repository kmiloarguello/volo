from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Activity as ActivityModel
from schemas import Activity, ActivityCreate, ActivityUpdate, ActivitiesResponse

router = APIRouter()

@router.post("/", response_model=Activity)
def create_activity(
    activity: ActivityCreate,
    db: Session = Depends(get_db)
):
    # Validate that end time is after start time
    if activity.ends_at <= activity.starts_at:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    db_activity = ActivityModel(**activity.model_dump())
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.get("/", response_model=ActivitiesResponse)
def read_activities(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    project_id: Optional[UUID] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ActivityModel)
    
    if project_id:
        query = query.filter(ActivityModel.project_id == project_id)
    
    if status:
        query = query.filter(ActivityModel.status == status)
    
    total = query.count()
    activities = query.offset(skip).limit(limit).all()
    
    return {
        "activities": activities,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{activity_id}", response_model=Activity)
def read_activity(activity_id: UUID, db: Session = Depends(get_db)):
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/{activity_id}", response_model=Activity)
def update_activity(
    activity_id: UUID,
    activity: ActivityUpdate,
    db: Session = Depends(get_db)
):
    db_activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if db_activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity_data = activity.model_dump(exclude_unset=True)
    
    # Validate time constraints if both times are provided
    starts_at = activity_data.get('starts_at', db_activity.starts_at)
    ends_at = activity_data.get('ends_at', db_activity.ends_at)
    
    if ends_at <= starts_at:
        raise HTTPException(status_code=400, detail="End time must be after start time")
    
    for key, value in activity_data.items():
        setattr(db_activity, key, value)
    
    db.commit()
    db.refresh(db_activity)
    return db_activity

@router.delete("/{activity_id}")
def delete_activity(activity_id: UUID, db: Session = Depends(get_db)):
    activity = db.query(ActivityModel).filter(ActivityModel.id == activity_id).first()
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    db.delete(activity)
    db.commit()
    return {"message": "Activity deleted successfully"}

@router.get("/{activity_id}/summary")
def get_activity_summary(activity_id: UUID, db: Session = Depends(get_db)):
    # Use the activity_summary view
    result = db.execute(
        """
        SELECT activity_id, starts_at, ends_at, location, capacity, status,
               project_name, organization_name, region_name, 
               registered_volunteers, verified_attendances
        FROM activity_summary 
        WHERE activity_id = :activity_id
        """,
        {"activity_id": activity_id}
    ).first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    return {
        "activity_id": result.activity_id,
        "starts_at": result.starts_at,
        "ends_at": result.ends_at,
        "location": result.location,
        "capacity": result.capacity,
        "status": result.status,
        "project_name": result.project_name,
        "organization_name": result.organization_name,
        "region_name": result.region_name,
        "registered_volunteers": result.registered_volunteers,
        "verified_attendances": result.verified_attendances
    }