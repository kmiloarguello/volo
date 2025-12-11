from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from uuid import UUID
import enum

# Enum definitions for schemas
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

# Base schemas
class RegionBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class RegionCreate(RegionBase):
    pass

class RegionUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class Region(RegionBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime

# Organization schemas
class OrganizationBase(BaseModel):
    type: OrganizationType
    name: str = Field(..., min_length=1, max_length=200)

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationUpdate(BaseModel):
    type: Optional[OrganizationType] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)

class Organization(OrganizationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime

# Company schemas
class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)

class CompanyCreate(CompanyBase):
    pass

class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)

class Company(CompanyBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime

# Volunteer schemas
class VolunteerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=13, le=100)
    region_id: UUID

class VolunteerCreate(VolunteerBase):
    pass

class VolunteerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=13, le=100)
    region_id: Optional[UUID] = None

class Volunteer(VolunteerBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    region: Optional[Region] = None

# Profile schemas
class ProfileBase(BaseModel):
    total_hours: Decimal = Field(default=Decimal('0.00'), ge=0)
    total_credits_earned: Decimal = Field(default=Decimal('0.00'), ge=0)
    total_credits_allocated: Decimal = Field(default=Decimal('0.00'), ge=0)

class ProfileUpdate(ProfileBase):
    pass

class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)
    
    volunteer_id: UUID
    updated_at: datetime

# Project schemas
class ProjectBase(BaseModel):
    ngo_id: UUID
    region_id: UUID
    name: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    ngo_id: Optional[UUID] = None
    region_id: Optional[UUID] = None
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None

class Project(ProjectBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    ngo: Optional[Organization] = None
    region: Optional[Region] = None

# Activity schemas
class ActivityBase(BaseModel):
    project_id: UUID
    starts_at: datetime
    ends_at: datetime
    location: Optional[str] = Field(None, max_length=255)
    capacity: Optional[int] = Field(None, gt=0)
    status: ActivityStatus = ActivityStatus.SCHEDULED

class ActivityCreate(ActivityBase):
    pass

class ActivityUpdate(BaseModel):
    project_id: Optional[UUID] = None
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    location: Optional[str] = Field(None, max_length=255)
    capacity: Optional[int] = Field(None, gt=0)
    status: Optional[ActivityStatus] = None

class Activity(ActivityBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    project: Optional[Project] = None

# Attendance schemas
class AttendanceBase(BaseModel):
    volunteer_id: UUID
    activity_id: UUID
    check_in_at: Optional[datetime] = None
    check_out_at: Optional[datetime] = None
    verified_by_user_id: Optional[UUID] = None
    status: AttendanceStatus = AttendanceStatus.PENDING

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    check_in_at: Optional[datetime] = None
    check_out_at: Optional[datetime] = None
    verified_by_user_id: Optional[UUID] = None
    status: Optional[AttendanceStatus] = None

class Attendance(AttendanceBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    volunteer: Optional[Volunteer] = None
    activity: Optional[Activity] = None

# VoloCredit schemas
class VoloCreditBase(BaseModel):
    volunteer_id: UUID
    source_attendance_id: Optional[UUID] = None
    amount: Decimal = Field(..., gt=0)
    status: CreditStatus = CreditStatus.AVAILABLE
    granted_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None

class VoloCreditCreate(VoloCreditBase):
    pass

class VoloCreditUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    status: Optional[CreditStatus] = None
    expires_at: Optional[datetime] = None

class VoloCredit(VoloCreditBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    volunteer: Optional[Volunteer] = None

# BrandMessage schemas
class BrandMessageBase(BaseModel):
    company_id: UUID
    content: str = Field(..., min_length=1)
    image_url: Optional[str] = Field(None, max_length=500)
    active_from: Optional[datetime] = None
    active_to: Optional[datetime] = None

class BrandMessageCreate(BrandMessageBase):
    pass

class BrandMessageUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1)
    image_url: Optional[str] = Field(None, max_length=500)
    active_from: Optional[datetime] = None
    active_to: Optional[datetime] = None

class BrandMessage(BrandMessageBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    updated_at: datetime
    company: Optional[Company] = None

# Allocation schemas
class AllocationBase(BaseModel):
    volunteer_id: UUID
    project_id: UUID
    company_id: Optional[UUID] = None
    source_credit_id: Optional[UUID] = None
    amount: Decimal = Field(..., gt=0)
    kind: AllocationKind

class AllocationCreate(AllocationBase):
    pass

class AllocationUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    kind: Optional[AllocationKind] = None

class Allocation(AllocationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime
    volunteer: Optional[Volunteer] = None
    project: Optional[Project] = None
    company: Optional[Company] = None

# Notification schemas
class NotificationBase(BaseModel):
    volunteer_id: UUID
    message: str = Field(..., min_length=1)
    read: bool = False

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(BaseModel):
    read: Optional[bool] = None

class Notification(NotificationBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    created_at: datetime

# Dashboard schemas
class ImpactDashboard(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    volunteer_id: UUID
    volunteer_name: str
    total_hours: Optional[Decimal]
    total_credits_earned: Optional[Decimal]
    total_credits_allocated: Optional[Decimal]
    projects_supported: int
    region_name: str

# Response schemas for lists
class VolunteersResponse(BaseModel):
    volunteers: List[Volunteer]
    total: int
    page: int
    per_page: int

class ActivitiesResponse(BaseModel):
    activities: List[Activity]
    total: int
    page: int
    per_page: int

class ProjectsResponse(BaseModel):
    projects: List[Project]
    total: int
    page: int
    per_page: int

class AttendancesResponse(BaseModel):
    attendances: List[Attendance]
    total: int
    page: int
    per_page: int

# Company Partnership schemas
class CompanyPartnershipBase(BaseModel):
    company_id: UUID
    organization_id: UUID
    partnership_type: str = "FUNDING"
    budget_committed: Optional[Decimal] = None
    active_from: datetime
    active_to: Optional[datetime] = None
    description: Optional[str] = None

class CompanyPartnershipCreate(CompanyPartnershipBase):
    pass

class CompanyPartnershipUpdate(BaseModel):
    partnership_type: Optional[str] = None
    budget_committed: Optional[Decimal] = None
    budget_allocated: Optional[Decimal] = None
    active_from: Optional[datetime] = None
    active_to: Optional[datetime] = None
    description: Optional[str] = None

class CompanyPartnership(CompanyPartnershipBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: UUID
    budget_allocated: Decimal
    created_at: datetime
    updated_at: datetime

class CompanyPartnershipUtilization(BaseModel):
    partnership_id: UUID
    company_name: str
    organization_name: str
    partnership_type: str
    budget_committed: Optional[Decimal]
    budget_allocated: Decimal
    budget_remaining: Optional[Decimal]
    utilization_percentage: Optional[Decimal]
    active_from: datetime
    active_to: Optional[datetime]
    status: str
    total_allocations: int
    projects_funded: int