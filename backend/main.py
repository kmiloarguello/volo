from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.connection import get_db
from routers import volunteers, activities, organizations, projects, attendances, allocations, regions, companies, partnerships, project_fundings
from database.models import Base
from database.connection import engine
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Volo API",
    description="API for the Volo volunteer credit allocation system",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(volunteers.router, prefix="/api/v1/volunteers", tags=["volunteers"])
app.include_router(activities.router, prefix="/api/v1/activities", tags=["activities"])
app.include_router(organizations.router, prefix="/api/v1/organizations", tags=["organizations"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(attendances.router, prefix="/api/v1/attendances", tags=["attendances"])
app.include_router(allocations.router, prefix="/api/v1/allocations", tags=["allocations"])
app.include_router(regions.router, prefix="/api/v1/regions", tags=["regions"])
app.include_router(companies.router, prefix="/api/v1/companies", tags=["companies"])
app.include_router(partnerships.router, prefix="/api/v1/partnerships", tags=["partnerships"])
app.include_router(project_fundings.router, prefix="/api/v1/project-fundings", tags=["project-fundings"])

@app.get("/")
async def root():
    return {"message": "Welcome to Volo API", "version": "1.0.0"}

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Simple database connection test
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)