from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from database.connection import get_db
from database.models import Project as ProjectModel
from schemas import Project, ProjectCreate, ProjectUpdate, ProjectsResponse

router = APIRouter()

@router.post("/", response_model=Project)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    db_project = ProjectModel(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/", response_model=ProjectsResponse)
def read_projects(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    region_id: Optional[UUID] = None,
    ngo_id: Optional[UUID] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ProjectModel)
    
    if region_id:
        query = query.filter(ProjectModel.region_id == region_id)
    
    if ngo_id:
        query = query.filter(ProjectModel.ngo_id == ngo_id)
    
    total = query.count()
    projects = query.offset(skip).limit(limit).all()
    
    return {
        "projects": projects,
        "total": total,
        "page": (skip // limit) + 1,
        "per_page": limit
    }

@router.get("/{project_id}", response_model=Project)
def read_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/{project_id}", response_model=Project)
def update_project(
    project_id: UUID,
    project: ProjectUpdate,
    db: Session = Depends(get_db)
):
    db_project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project_data = project.model_dump(exclude_unset=True)
    for key, value in project_data.items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

@router.delete("/{project_id}")
def delete_project(project_id: UUID, db: Session = Depends(get_db)):
    project = db.query(ProjectModel).filter(ProjectModel.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}