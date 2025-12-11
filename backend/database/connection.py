from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://volo_user:volo_password@localhost:5432/volo_db"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)  # Set echo=False in production

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()