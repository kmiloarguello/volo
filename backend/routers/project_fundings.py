"""
Project Company Funding management endpoints
Handles pre-approval of projects by companies for targeted funding
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from database.connection import get_db
from database.models import (
    ProjectCompanyFunding as ProjectCompanyFundingModel, 
    Project as ProjectModel,
    Company as CompanyModel
)
from schemas import ProjectCompanyFunding, ProjectCompanyFundingCreate, ProjectCompanyFundingUpdate

router = APIRouter()

@router.post("/", response_model=ProjectCompanyFunding)
def approve_project_funding(
    funding: ProjectCompanyFundingCreate,
    db: Session = Depends(get_db)
):
    """
    Company pre-approves funding for a specific project
    
    Example:
    L'Oréal approves €10,000 funding for "Urban Tree Planting Initiative"
    """
    # Validate project exists
    project = db.query(ProjectModel).filter(ProjectModel.id == funding.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Validate company exists
    company = db.query(CompanyModel).filter(CompanyModel.id == funding.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check for existing funding approval
    existing = db.query(ProjectCompanyFundingModel).filter(
        ProjectCompanyFundingModel.project_id == funding.project_id,
        ProjectCompanyFundingModel.company_id == funding.company_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Company has already approved funding for this project")
    
    # Create funding approval
    db_funding = ProjectCompanyFundingModel(**funding.model_dump())
    db.add(db_funding)
    db.commit()
    db.refresh(db_funding)
    return db_funding

@router.get("/", response_model=List[ProjectCompanyFunding])
def list_project_fundings(
    project_id: Optional[UUID] = Query(None),
    company_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query("ACTIVE"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    List project funding approvals with optional filtering
    """
    query = db.query(ProjectCompanyFundingModel)
    
    if project_id:
        query = query.filter(ProjectCompanyFundingModel.project_id == project_id)
    
    if company_id:
        query = query.filter(ProjectCompanyFundingModel.company_id == company_id)
    
    if status:
        query = query.filter(ProjectCompanyFundingModel.status == status)
    
    fundings = query.order_by(ProjectCompanyFundingModel.approved_at.desc()).offset(skip).limit(limit).all()
    return fundings

@router.get("/{funding_id}", response_model=ProjectCompanyFunding)
def get_project_funding(funding_id: UUID, db: Session = Depends(get_db)):
    """Get specific project funding approval"""
    funding = db.query(ProjectCompanyFundingModel).filter(ProjectCompanyFundingModel.id == funding_id).first()
    if not funding:
        raise HTTPException(status_code=404, detail="Project funding not found")
    return funding

@router.put("/{funding_id}", response_model=ProjectCompanyFunding)
def update_project_funding(
    funding_id: UUID,
    updates: ProjectCompanyFundingUpdate,
    db: Session = Depends(get_db)
):
    """
    Update project funding approval
    Useful for adjusting budgets, changing status, or adding notes
    """
    funding = db.query(ProjectCompanyFundingModel).filter(ProjectCompanyFundingModel.id == funding_id).first()
    if not funding:
        raise HTTPException(status_code=404, detail="Project funding not found")
    
    update_data = updates.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    
    # Validate budget constraints
    if "max_budget" in update_data:
        if update_data["max_budget"] < funding.allocated_budget:
            raise HTTPException(
                status_code=400, 
                detail=f"Max budget cannot be less than already allocated budget (${funding.allocated_budget})"
            )
    
    for field, value in update_data.items():
        setattr(funding, field, value)
    
    db.commit()
    db.refresh(funding)
    return funding

@router.delete("/{funding_id}")
def revoke_project_funding(funding_id: UUID, db: Session = Depends(get_db)):
    """
    Revoke project funding approval
    Note: This will prevent future allocations but won't affect existing ones
    """
    funding = db.query(ProjectCompanyFundingModel).filter(ProjectCompanyFundingModel.id == funding_id).first()
    if not funding:
        raise HTTPException(status_code=404, detail="Project funding not found")
    
    if funding.allocated_budget > 0:
        # Don't delete if money has been allocated, just deactivate
        funding.status = "CANCELLED"
        db.commit()
        return {"message": "Project funding cancelled (existing allocations preserved)"}
    else:
        # Safe to delete if no allocations made yet
        db.delete(funding)
        db.commit()
        return {"message": "Project funding revoked"}

@router.get("/company/{company_id}/approved-projects")
def get_company_approved_projects(
    company_id: UUID,
    status: str = Query("ACTIVE"),
    db: Session = Depends(get_db)
):
    """
    Get all projects that a company has pre-approved for funding
    Used by allocation logic to validate funding availability
    """
    query = db.query(ProjectCompanyFundingModel).join(ProjectModel).filter(
        ProjectCompanyFundingModel.company_id == company_id,
        ProjectCompanyFundingModel.status == status
    )
    
    approved_projects = []
    for funding in query.all():
        budget_remaining = funding.max_budget - funding.allocated_budget
        approved_projects.append({
            "funding_id": funding.id,
            "project_id": funding.project_id,
            "project_name": funding.project.name,
            "organization_name": funding.project.ngo.name,
            "max_budget": funding.max_budget,
            "allocated_budget": funding.allocated_budget,
            "budget_remaining": budget_remaining,
            "utilization_percentage": round((funding.allocated_budget / funding.max_budget) * 100, 2) if funding.max_budget > 0 else 0,
            "approved_at": funding.approved_at,
            "approved_by": funding.approved_by
        })
    
    return {
        "company_id": company_id,
        "approved_projects": approved_projects,
        "total_approved": len(approved_projects),
        "total_budget_committed": sum(p["max_budget"] for p in approved_projects),
        "total_budget_allocated": sum(p["allocated_budget"] for p in approved_projects)
    }

@router.post("/validate-allocation")
def validate_allocation_funding(
    project_id: UUID,
    company_id: UUID,
    amount: Decimal,
    db: Session = Depends(get_db)
):
    """
    Validate if a company can fund a specific allocation amount for a project
    Used by allocation creation logic
    """
    funding = db.query(ProjectCompanyFundingModel).filter(
        ProjectCompanyFundingModel.project_id == project_id,
        ProjectCompanyFundingModel.company_id == company_id,
        ProjectCompanyFundingModel.status == "ACTIVE"
    ).first()
    
    if not funding:
        return {
            "valid": False,
            "reason": "Company has not pre-approved funding for this project"
        }
    
    budget_remaining = funding.max_budget - funding.allocated_budget
    
    if amount > budget_remaining:
        return {
            "valid": False,
            "reason": f"Insufficient budget. Requested: ${amount}, Available: ${budget_remaining}"
        }
    
    return {
        "valid": True,
        "funding_id": funding.id,
        "budget_remaining": budget_remaining,
        "max_budget": funding.max_budget,
        "allocated_budget": funding.allocated_budget
    }