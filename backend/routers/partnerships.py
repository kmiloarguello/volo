"""
Company Partnership management endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import CompanyPartnership as CompanyPartnershipModel, Company as CompanyModel, Organization as OrganizationModel
from schemas import CompanyPartnership, CompanyPartnershipCreate, CompanyPartnershipUpdate

router = APIRouter()

# ===== CRUD OPERATIONS =====

@router.post("/", response_model=CompanyPartnership)
def create_partnership(
    partnership: CompanyPartnershipCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new company-NGO partnership
    
    Example:
    L'Oréal partners with Urban Forest Paris for €50K environmental projects
    """
    # Validate that company and organization exist
    company = db.query(CompanyModel).filter(CompanyModel.id == partnership.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    organization = db.query(OrganizationModel).filter(OrganizationModel.id == partnership.organization_id).first()
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    # Check for existing partnership
    existing = db.query(CompanyPartnershipModel).filter(
        CompanyPartnershipModel.company_id == partnership.company_id,
        CompanyPartnershipModel.organization_id == partnership.organization_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Partnership between this company and organization already exists")
    
    # Create new partnership
    db_partnership = CompanyPartnershipModel(**partnership.model_dump())
    db.add(db_partnership)
    db.commit()
    db.refresh(db_partnership)
    return db_partnership

@router.get("/", response_model=List[CompanyPartnership])
def list_partnerships(
    company_id: Optional[UUID] = Query(None),
    organization_id: Optional[UUID] = Query(None),
    active_only: bool = Query(True),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List all company partnerships with optional filtering
    """
    query = db.query(CompanyPartnershipModel)
    
    if company_id:
        query = query.filter(CompanyPartnershipModel.company_id == company_id)
    
    if organization_id:
        query = query.filter(CompanyPartnershipModel.organization_id == organization_id)
    
    if active_only:
        from datetime import datetime
        now = datetime.now()
        query = query.filter(
            (CompanyPartnershipModel.active_to.is_(None)) | 
            (CompanyPartnershipModel.active_to >= now),
            CompanyPartnershipModel.active_from <= now
        )
    
    partnerships = query.order_by(CompanyPartnershipModel.created_at.desc()).offset(skip).limit(limit).all()
    return partnerships

@router.get("/{partnership_id}", response_model=CompanyPartnership)
def get_partnership(partnership_id: UUID, db: Session = Depends(get_db)):
    """Get a specific partnership by ID"""
    partnership = db.query(CompanyPartnershipModel).filter(CompanyPartnershipModel.id == partnership_id).first()
    if not partnership:
        raise HTTPException(status_code=404, detail="Partnership not found")
    return partnership

@router.put("/{partnership_id}", response_model=CompanyPartnership)
def update_partnership(
    partnership_id: UUID, 
    updates: CompanyPartnershipUpdate, 
    db: Session = Depends(get_db)
):
    """
    Update an existing partnership
    Useful for adjusting budgets, extending duration, etc.
    """
    partnership = db.query(CompanyPartnershipModel).filter(CompanyPartnershipModel.id == partnership_id).first()
    if not partnership:
        raise HTTPException(status_code=404, detail="Partnership not found")
    
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    for field, value in update_data.items():
        setattr(partnership, field, value)
    
    db.commit()
    db.refresh(partnership)
    return partnership

@router.delete("/{partnership_id}")
def delete_partnership(partnership_id: UUID, db: Session = Depends(get_db)):
    """
    Delete a partnership
    Note: This will not affect existing allocations, only prevent new ones
    """
    partnership = db.query(CompanyPartnershipModel).filter(CompanyPartnershipModel.id == partnership_id).first()
    if not partnership:
        raise HTTPException(status_code=404, detail="Partnership not found")
    
    db.delete(partnership)
    db.commit()
    return {"message": "Partnership deleted successfully"}