from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Company as CompanyModel
from schemas import Company, CompanyCreate, CompanyUpdate

router = APIRouter()

@router.post("/", response_model=Company)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = CompanyModel(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", response_model=List[Company])
def read_companies(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    companies = db.query(CompanyModel).offset(skip).limit(limit).all()
    return companies

@router.get("/{company_id}", response_model=Company)
def read_company(company_id: UUID, db: Session = Depends(get_db)):
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company

@router.put("/{company_id}", response_model=Company)
def update_company(
    company_id: UUID,
    company: CompanyUpdate,
    db: Session = Depends(get_db)
):
    db_company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if db_company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    company_data = company.model_dump(exclude_unset=True)
    for key, value in company_data.items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    return db_company

@router.delete("/{company_id}")
def delete_company(company_id: UUID, db: Session = Depends(get_db)):
    company = db.query(CompanyModel).filter(CompanyModel.id == company_id).first()
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    
    db.delete(company)
    db.commit()
    return {"message": "Company deleted successfully"}