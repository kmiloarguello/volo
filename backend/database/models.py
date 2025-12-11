from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, Enum, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
import uuid

Base = declarative_base()

# Enum definitions
class ActivityStatus(str, enum.Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class OrganizationType(str, enum.Enum):
    NGO = "NGO"
    NBE = "NBE"

class AttendanceStatus(str, enum.Enum):
    PENDING = "Pending"
    VERIFIED = "Verified"
    REJECTED = "Rejected"

class CreditStatus(str, enum.Enum):
    AVAILABLE = "Available"
    ALLOCATED = "Allocated"
    EXPIRED = "Expired"

class AllocationKind(str, enum.Enum):
    MANDATORY_50 = "MANDATORY_50"
    FREE_CHOICE_50 = "FREE_CHOICE_50"

# Models
class Region(Base):
    __tablename__ = "regions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    volunteers = relationship("Volunteer", back_populates="region")
    projects = relationship("Project", back_populates="region")

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = Column(Enum(OrganizationType), nullable=False)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="ngo")
    ledger_relationships = relationship("LedgerCompanyNGO", back_populates="organization")

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    brand_messages = relationship("BrandMessage", back_populates="company")
    allocations = relationship("Allocation", back_populates="company")
    ledger_relationships = relationship("LedgerCompanyNGO", back_populates="company")

class Volunteer(Base):
    __tablename__ = "volunteers"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    age = Column(Integer, CheckConstraint('age >= 13 AND age <= 100'))
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    region = relationship("Region", back_populates="volunteers")
    profile = relationship("Profile", back_populates="volunteer", uselist=False)
    attendances = relationship("Attendance", back_populates="volunteer")
    volo_credits = relationship("VoloCredit", back_populates="volunteer")
    allocations = relationship("Allocation", back_populates="volunteer")
    notifications = relationship("Notification", back_populates="volunteer")

class Profile(Base):
    __tablename__ = "profiles"
    
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id", ondelete="CASCADE"), primary_key=True)
    total_hours = Column(DECIMAL(10,2), default=0.00)
    total_credits_earned = Column(DECIMAL(10,2), default=0.00)
    total_credits_allocated = Column(DECIMAL(10,2), default=0.00)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="profile")

class Project(Base):
    __tablename__ = "projects"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ngo_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"), nullable=False)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    ngo = relationship("Organization", back_populates="projects")
    region = relationship("Region", back_populates="projects")
    activities = relationship("Activity", back_populates="project")
    allocations = relationship("Allocation", back_populates="project")
    credit_exchanges = relationship("CreditExchange", back_populates="project")

class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    starts_at = Column(DateTime(timezone=True), nullable=False)
    ends_at = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(255))
    capacity = Column(Integer, CheckConstraint('capacity > 0'))
    status = Column(Enum(ActivityStatus), default=ActivityStatus.SCHEDULED)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    project = relationship("Project", back_populates="activities")
    attendances = relationship("Attendance", back_populates="activity")
    
    __table_args__ = (
        CheckConstraint('ends_at > starts_at', name='valid_activity_duration'),
    )

class Attendance(Base):
    __tablename__ = "attendances"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), nullable=False)
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activities.id"), nullable=False)
    check_in_at = Column(DateTime(timezone=True))
    check_out_at = Column(DateTime(timezone=True))
    verified_by_user_id = Column(UUID(as_uuid=True))  # NGO/NBE representative
    status = Column(Enum(AttendanceStatus), default=AttendanceStatus.PENDING)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="attendances")
    activity = relationship("Activity", back_populates="attendances")
    volo_credits = relationship("VoloCredit", back_populates="source_attendance")
    
    __table_args__ = (
        CheckConstraint('check_out_at IS NULL OR check_out_at > check_in_at', name='valid_attendance_duration'),
    )

class VoloCredit(Base):
    __tablename__ = "volo_credits"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), nullable=False)
    source_attendance_id = Column(UUID(as_uuid=True), ForeignKey("attendances.id"))
    amount = Column(DECIMAL(10,2), nullable=False)
    status = Column(Enum(CreditStatus), default=CreditStatus.AVAILABLE)
    granted_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="volo_credits")
    source_attendance = relationship("Attendance", back_populates="volo_credits")
    allocations = relationship("Allocation", back_populates="source_credit")

class BrandMessage(Base):
    __tablename__ = "brand_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    content = Column(Text, nullable=False)
    image_url = Column(String(500))
    active_from = Column(DateTime(timezone=True), server_default=func.now())
    active_to = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="brand_messages")

class Allocation(Base):
    __tablename__ = "allocations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    source_credit_id = Column(UUID(as_uuid=True), ForeignKey("volo_credits.id"))
    amount = Column(DECIMAL(10,2), nullable=False)
    kind = Column(Enum(AllocationKind), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="allocations")
    project = relationship("Project", back_populates="allocations")
    company = relationship("Company", back_populates="allocations")
    source_credit = relationship("VoloCredit", back_populates="allocations")
    credit_exchanges = relationship("CreditExchange", back_populates="allocation")

class CreditExchange(Base):
    __tablename__ = "credit_exchanges"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    allocation_id = Column(UUID(as_uuid=True), ForeignKey("allocations.id"), nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("projects.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    allocation = relationship("Allocation", back_populates="credit_exchanges")
    project = relationship("Project", back_populates="credit_exchanges")

class LedgerCompanyNGO(Base):
    __tablename__ = "ledger_company_ngo"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"), nullable=False)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    company = relationship("Company", back_populates="ledger_relationships")
    organization = relationship("Organization", back_populates="ledger_relationships")

class LedgerEntry(Base):
    __tablename__ = "ledger_entries"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ref_type = Column(String(50), nullable=False)  # e.g., 'Attendance', 'VoloCredit', 'Allocation'
    ref_id = Column(UUID(as_uuid=True), nullable=False)
    hash = Column(String(64), nullable=False)
    prev_hash = Column(String(64))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class Notification(Base):
    __tablename__ = "notifications"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    volunteer_id = Column(UUID(as_uuid=True), ForeignKey("volunteers.id"), nullable=False)
    message = Column(Text, nullable=False)
    read = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    volunteer = relationship("Volunteer", back_populates="notifications")

# Add table constraints that couldn't be added inline
VoloCredit.__table_args__ = (
    CheckConstraint('amount > 0', name='volo_credit_amount_positive'),
)

Allocation.__table_args__ = (
    CheckConstraint('amount > 0', name='allocation_amount_positive'),
)