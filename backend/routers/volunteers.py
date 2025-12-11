from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Volunteer as VolunteerModel, Profile as ProfileModel
from schemas import (
    Volunteer, VolunteerCreate, VolunteerUpdate, VolunteersResponse,
    Profile, ImpactDashboard
)

router = APIRouter()

@router.post("/", response_model=Volunteer)
def create_volunteer(
    volunteer: VolunteerCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    db_volunteer = db.query(VolunteerModel).filter(VolunteerModel.email == volunteer.email).first()
    if db_volunteer:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_volunteer = VolunteerModel(**volunteer.model_dump())
    db.add(db_volunteer)
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

@router.get("/", response_model=VolunteersResponse)
def read_volunteers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    region_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(VolunteerModel)
    
    if region_id:
        query = query.filter(VolunteerModel.region_id == region_id)
    
    total = query.count()
    volunteers = query.offset(skip).limit(limit).all()
    
    return {
        "volunteers": volunteers,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{volunteer_id}", response_model=Volunteer)
def read_volunteer(volunteer_id: UUID, db: Session = Depends(get_db)):
    volunteer = db.query(VolunteerModel).filter(VolunteerModel.id == volunteer_id).first()
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return volunteer

@router.put("/{volunteer_id}", response_model=Volunteer)
def update_volunteer(
    volunteer_id: UUID,
    volunteer: VolunteerUpdate,
    db: Session = Depends(get_db)
):
    db_volunteer = db.query(VolunteerModel).filter(VolunteerModel.id == volunteer_id).first()
    if db_volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    volunteer_data = volunteer.model_dump(exclude_unset=True)
    for key, value in volunteer_data.items():
        setattr(db_volunteer, key, value)
    
    db.commit()
    db.refresh(db_volunteer)
    return db_volunteer

@router.delete("/{volunteer_id}")
def delete_volunteer(volunteer_id: UUID, db: Session = Depends(get_db)):
    volunteer = db.query(VolunteerModel).filter(VolunteerModel.id == volunteer_id).first()
    if volunteer is None:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    db.delete(volunteer)
    db.commit()
    return {"message": "Volunteer deleted successfully"}

@router.get("/{volunteer_id}/profile", response_model=Profile)
def read_volunteer_profile(volunteer_id: UUID, db: Session = Depends(get_db)):
    profile = db.query(ProfileModel).filter(ProfileModel.volunteer_id == volunteer_id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Volunteer profile not found")
    return profile

@router.get("/{volunteer_id}/dashboard", response_model=ImpactDashboard)
def read_volunteer_dashboard(volunteer_id: UUID, db: Session = Depends(get_db)):
    # Use the impact_dashboard view
    result = db.execute(
        """
        SELECT volunteer_id, volunteer_name, total_hours, total_credits_earned, 
               total_credits_allocated, projects_supported, region_name
        FROM impact_dashboard 
        WHERE volunteer_id = :volunteer_id
        """,
        {"volunteer_id": volunteer_id}
    ).first()
    
    if result is None:
        raise HTTPException(status_code=404, detail="Volunteer dashboard not found")
    
    return {
        "volunteer_id": result.volunteer_id,
        "volunteer_name": result.volunteer_name,
        "total_hours": result.total_hours,
        "total_credits_earned": result.total_credits_earned,
        "total_credits_allocated": result.total_credits_allocated,
        "projects_supported": result.projects_supported,
        "region_name": result.region_name
    }