from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from decimal import Decimal

from database.connection import get_db
from database.models import Allocation as AllocationModel, VoloCredit as VoloCreditModel
from schemas import Allocation, AllocationCreate, AllocationUpdate

router = APIRouter()

@router.post("/", response_model=Allocation)
def create_allocation(
    allocation: AllocationCreate,
    db: Session = Depends(get_db)
):
    # Validate that the credit exists and has sufficient balance
    if allocation.source_credit_id:
        credit = db.query(VoloCreditModel).filter(VoloCreditModel.id == allocation.source_credit_id).first()
        if not credit:
            raise HTTPException(status_code=404, detail="Source credit not found")
        
        if credit.status != "Available":
            raise HTTPException(status_code=400, detail="Credit is not available for allocation")
        
        # Check if volunteer owns the credit
        if credit.volunteer_id != allocation.volunteer_id:
            raise HTTPException(status_code=400, detail="Credit does not belong to this volunteer")
    
    db_allocation = AllocationModel(**allocation.model_dump())
    db.add(db_allocation)
    
    # Update credit status if specified
    if allocation.source_credit_id:
        credit.status = "Allocated"
    
    db.commit()
    db.refresh(db_allocation)
    return db_allocation

@router.get("/", response_model=List[Allocation])
def read_allocations(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    volunteer_id: Optional[UUID] = None,
    project_id: Optional[UUID] = None,
    kind: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(AllocationModel)
    
    if volunteer_id:
        query = query.filter(AllocationModel.volunteer_id == volunteer_id)
    
    if project_id:
        query = query.filter(AllocationModel.project_id == project_id)
    
    if kind:
        query = query.filter(AllocationModel.kind == kind)
    
    allocations = query.offset(skip).limit(limit).all()
    return allocations

@router.get("/{allocation_id}", response_model=Allocation)
def read_allocation(allocation_id: UUID, db: Session = Depends(get_db)):
    allocation = db.query(AllocationModel).filter(AllocationModel.id == allocation_id).first()
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return allocation

@router.put("/{allocation_id}", response_model=Allocation)
def update_allocation(
    allocation_id: UUID,
    allocation: AllocationUpdate,
    db: Session = Depends(get_db)
):
    db_allocation = db.query(AllocationModel).filter(AllocationModel.id == allocation_id).first()
    if db_allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")
    
    allocation_data = allocation.model_dump(exclude_unset=True)
    for key, value in allocation_data.items():
        setattr(db_allocation, key, value)
    
    db.commit()
    db.refresh(db_allocation)
    return db_allocation

@router.delete("/{allocation_id}")
def delete_allocation(allocation_id: UUID, db: Session = Depends(get_db)):
    allocation = db.query(AllocationModel).filter(AllocationModel.id == allocation_id).first()
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")
    
    # If allocation had a source credit, make it available again
    if allocation.source_credit_id:
        credit = db.query(VoloCreditModel).filter(VoloCreditModel.id == allocation.source_credit_id).first()
        if credit:
            credit.status = "Available"
    
    db.delete(allocation)
    db.commit()
    return {"message": "Allocation deleted successfully"}

@router.get("/volunteer/{volunteer_id}/summary")
def get_volunteer_allocation_summary(volunteer_id: UUID, db: Session = Depends(get_db)):
    """Get allocation summary for a volunteer"""
    
    # Get total allocations by kind
    mandatory_total = db.query(AllocationModel).filter(
        AllocationModel.volunteer_id == volunteer_id,
        AllocationModel.kind == "MANDATORY_50"
    ).count()
    
    free_choice_total = db.query(AllocationModel).filter(
        AllocationModel.volunteer_id == volunteer_id,
        AllocationModel.kind == "FREE_CHOICE_50"
    ).count()
    
    # Get total amounts by kind
    mandatory_amount = db.query(AllocationModel).filter(
        AllocationModel.volunteer_id == volunteer_id,
        AllocationModel.kind == "MANDATORY_50"
    ).with_entities(db.func.sum(AllocationModel.amount)).scalar() or Decimal('0')
    
    free_choice_amount = db.query(AllocationModel).filter(
        AllocationModel.volunteer_id == volunteer_id,
        AllocationModel.kind == "FREE_CHOICE_50"
    ).with_entities(db.func.sum(AllocationModel.amount)).scalar() or Decimal('0')
    
    return {
        "volunteer_id": volunteer_id,
        "mandatory_allocations": {
            "count": mandatory_total,
            "total_amount": float(mandatory_amount)
        },
        "free_choice_allocations": {
            "count": free_choice_total,
            "total_amount": float(free_choice_amount)
        },
        "total_allocated": float(mandatory_amount + free_choice_amount)
    }