from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Organization as OrganizationModel
from schemas import Organization, OrganizationCreate, OrganizationUpdate

router = APIRouter()

@router.post("/", response_model=Organization)
def create_organization(
    organization: OrganizationCreate,
    db: Session = Depends(get_db)
):
    db_organization = OrganizationModel(**organization.model_dump())
    db.add(db_organization)
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.get("/", response_model=List[Organization])
def read_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    org_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(OrganizationModel)
    
    if org_type:
        query = query.filter(OrganizationModel.type == org_type)
    
    organizations = query.offset(skip).limit(limit).all()
    return organizations

@router.get("/{organization_id}", response_model=Organization)
def read_organization(organization_id: UUID, db: Session = Depends(get_db)):
    organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization

@router.put("/{organization_id}", response_model=Organization)
def update_organization(
    organization_id: UUID,
    organization: OrganizationUpdate,
    db: Session = Depends(get_db)
):
    db_organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if db_organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    organization_data = organization.model_dump(exclude_unset=True)
    for key, value in organization_data.items():
        setattr(db_organization, key, value)
    
    db.commit()
    db.refresh(db_organization)
    return db_organization

@router.delete("/{organization_id}")
def delete_organization(organization_id: UUID, db: Session = Depends(get_db)):
    organization = db.query(OrganizationModel).filter(OrganizationModel.id == organization_id).first()
    if organization is None:
        raise HTTPException(status_code=404, detail="Organization not found")
    
    db.delete(organization)
    db.commit()
    return {"message": "Organization deleted successfully"}