from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Region as RegionModel
from schemas import Region, RegionCreate, RegionUpdate

router = APIRouter()

@router.post("/", response_model=Region)
def create_region(
    region: RegionCreate,
    db: Session = Depends(get_db)
):
    # Check if region name already exists
    db_region = db.query(RegionModel).filter(RegionModel.name == region.name).first()
    if db_region:
        raise HTTPException(status_code=400, detail="Region name already exists")
    
    db_region = RegionModel(**region.model_dump())
    db.add(db_region)
    db.commit()
    db.refresh(db_region)
    return db_region

@router.get("/", response_model=List[Region])
def read_regions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    regions = db.query(RegionModel).offset(skip).limit(limit).all()
    return regions

@router.get("/{region_id}", response_model=Region)
def read_region(region_id: UUID, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    return region

@router.put("/{region_id}", response_model=Region)
def update_region(
    region_id: UUID,
    region: RegionUpdate,
    db: Session = Depends(get_db)
):
    db_region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
    if db_region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    
    region_data = region.model_dump(exclude_unset=True)
    for key, value in region_data.items():
        setattr(db_region, key, value)
    
    db.commit()
    db.refresh(db_region)
    return db_region

@router.delete("/{region_id}")
def delete_region(region_id: UUID, db: Session = Depends(get_db)):
    region = db.query(RegionModel).filter(RegionModel.id == region_id).first()
    if region is None:
        raise HTTPException(status_code=404, detail="Region not found")
    
    db.delete(region)
    db.commit()
    return {"message": "Region deleted successfully"}