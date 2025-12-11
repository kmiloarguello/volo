-- ===== VOLO DATABASE SCHEMA =====
-- Based on the class diagram provided

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ===== ENUMS =====
CREATE TYPE activity_status AS ENUM ('Scheduled', 'Completed', 'Cancelled');
CREATE TYPE organization_type AS ENUM ('NGO', 'NBE');
CREATE TYPE attendance_status AS ENUM ('Pending', 'Verified', 'Rejected');
CREATE TYPE credit_status AS ENUM ('Available', 'Allocated', 'Expired');
CREATE TYPE allocation_kind AS ENUM ('MANDATORY_50', 'FREE_CHOICE_50');

-- ===== CORE TABLES =====

-- Regions table
CREATE TABLE regions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Organizations table (NGOs and NBEs)
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    type organization_type NOT NULL,
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Companies table (for branding and funding)
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Volunteers table
CREATE TABLE volunteers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INTEGER CHECK (age >= 13 AND age <= 100),
    region_id UUID NOT NULL REFERENCES regions(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Volunteer profiles (aggregated data)
CREATE TABLE profiles (
    volunteer_id UUID PRIMARY KEY REFERENCES volunteers(id) ON DELETE CASCADE,
    total_hours DECIMAL(10,2) DEFAULT 0.00,
    total_credits_earned DECIMAL(10,2) DEFAULT 0.00,
    total_credits_allocated DECIMAL(10,2) DEFAULT 0.00,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ngo_id UUID NOT NULL REFERENCES organizations(id),
    region_id UUID NOT NULL REFERENCES regions(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Activities table
CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id),
    starts_at TIMESTAMP WITH TIME ZONE NOT NULL,
    ends_at TIMESTAMP WITH TIME ZONE NOT NULL,
    location VARCHAR(255),
    capacity INTEGER CHECK (capacity > 0),
    status activity_status DEFAULT 'Scheduled',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_activity_duration CHECK (ends_at > starts_at)
);

-- Attendance table
CREATE TABLE attendances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    volunteer_id UUID NOT NULL REFERENCES volunteers(id),
    activity_id UUID NOT NULL REFERENCES activities(id),
    check_in_at TIMESTAMP WITH TIME ZONE,
    check_out_at TIMESTAMP WITH TIME ZONE,
    verified_by_user_id UUID, -- Reference to NGO/NBE representative (could be a separate users table)
    status attendance_status DEFAULT 'Pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_attendance_duration CHECK (check_out_at IS NULL OR check_out_at > check_in_at),
    UNIQUE(volunteer_id, activity_id) -- One attendance record per volunteer per activity
);

-- Volo Credits table
CREATE TABLE volo_credits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    volunteer_id UUID NOT NULL REFERENCES volunteers(id),
    source_attendance_id UUID REFERENCES attendances(id),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    status credit_status DEFAULT 'Available',
    granted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Brand Messages table
CREATE TABLE brand_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id),
    content TEXT NOT NULL,
    image_url VARCHAR(500),
    active_from TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    active_to TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Allocations table
CREATE TABLE allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    volunteer_id UUID NOT NULL REFERENCES volunteers(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    company_id UUID REFERENCES companies(id), -- funding brand shown at allocation
    source_credit_id UUID REFERENCES volo_credits(id),
    amount DECIMAL(10,2) NOT NULL CHECK (amount > 0),
    kind allocation_kind NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Credit Exchange (many-to-many between allocations and projects)
CREATE TABLE credit_exchanges (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    allocation_id UUID NOT NULL REFERENCES allocations(id),
    project_id UUID NOT NULL REFERENCES projects(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Company Partnerships (targeted funding relationships)
CREATE TABLE company_partnerships (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    partnership_type VARCHAR(50) DEFAULT 'FUNDING', -- FUNDING, SPONSORSHIP, STRATEGIC
    budget_committed DECIMAL(12,2), -- €50,000 - total committed budget
    budget_allocated DECIMAL(12,2) DEFAULT 0.00, -- Track utilization
    active_from DATE NOT NULL DEFAULT CURRENT_DATE,
    active_to DATE, -- NULL means indefinite
    description TEXT, -- Partnership details and objectives
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(company_id, organization_id),
    CONSTRAINT valid_budget CHECK (budget_allocated <= budget_committed),
    CONSTRAINT valid_partnership_duration CHECK (active_to IS NULL OR active_to >= active_from)
);

-- Ledger Entries (immutable audit trail)
CREATE TABLE ledger_entries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ref_type VARCHAR(50) NOT NULL, -- e.g., 'Attendance', 'VoloCredit', 'Allocation'
    ref_id UUID NOT NULL,
    hash VARCHAR(64) NOT NULL,
    prev_hash VARCHAR(64),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Notifications table
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    volunteer_id UUID NOT NULL REFERENCES volunteers(id),
    message TEXT NOT NULL,
    read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- ===== INDEXES =====

-- Performance indexes
CREATE INDEX idx_volunteers_region_id ON volunteers(region_id);
CREATE INDEX idx_volunteers_email ON volunteers(email);
CREATE INDEX idx_projects_ngo_id ON projects(ngo_id);
CREATE INDEX idx_projects_region_id ON projects(region_id);
CREATE INDEX idx_activities_project_id ON activities(project_id);
CREATE INDEX idx_activities_starts_at ON activities(starts_at);
CREATE INDEX idx_activities_status ON activities(status);
CREATE INDEX idx_attendances_volunteer_id ON attendances(volunteer_id);
CREATE INDEX idx_attendances_activity_id ON attendances(activity_id);
CREATE INDEX idx_attendances_status ON attendances(status);
CREATE INDEX idx_volo_credits_volunteer_id ON volo_credits(volunteer_id);
CREATE INDEX idx_volo_credits_status ON volo_credits(status);
CREATE INDEX idx_allocations_volunteer_id ON allocations(volunteer_id);
CREATE INDEX idx_allocations_project_id ON allocations(project_id);
CREATE INDEX idx_ledger_entries_ref_type ON ledger_entries(ref_type);
CREATE INDEX idx_ledger_entries_ref_id ON ledger_entries(ref_id);
CREATE INDEX idx_notifications_volunteer_id ON notifications(volunteer_id);
CREATE INDEX idx_notifications_read ON notifications(read);
CREATE INDEX idx_company_partnerships_company_id ON company_partnerships(company_id);
CREATE INDEX idx_company_partnerships_organization_id ON company_partnerships(organization_id);
CREATE INDEX idx_company_partnerships_active ON company_partnerships(active_from, active_to);

-- ===== TRIGGERS =====

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply update triggers to tables with updated_at
CREATE TRIGGER update_regions_updated_at BEFORE UPDATE ON regions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_companies_updated_at BEFORE UPDATE ON companies FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_volunteers_updated_at BEFORE UPDATE ON volunteers FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON activities FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_attendances_updated_at BEFORE UPDATE ON attendances FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_brand_messages_updated_at BEFORE UPDATE ON brand_messages FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_company_partnerships_updated_at BEFORE UPDATE ON company_partnerships FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Automatically create profile for new volunteers
CREATE OR REPLACE FUNCTION create_volunteer_profile()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO profiles (volunteer_id) VALUES (NEW.id);
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER create_profile_for_new_volunteer 
    AFTER INSERT ON volunteers 
    FOR EACH ROW 
    EXECUTE FUNCTION create_volunteer_profile();

-- ===== VIEWS =====

-- Impact Dashboard view (read model)
CREATE VIEW impact_dashboard AS
SELECT 
    v.id as volunteer_id,
    v.name as volunteer_name,
    p.total_hours,
    p.total_credits_earned,
    p.total_credits_allocated,
    COUNT(DISTINCT a.project_id) as projects_supported,
    r.name as region_name
FROM volunteers v
JOIN profiles p ON v.id = p.volunteer_id
JOIN regions r ON v.region_id = r.id
LEFT JOIN allocations a ON v.id = a.volunteer_id
GROUP BY v.id, v.name, p.total_hours, p.total_credits_earned, p.total_credits_allocated, r.name;

-- Activity summary view
CREATE VIEW activity_summary AS
SELECT 
    act.id as activity_id,
    act.starts_at,
    act.ends_at,
    act.location,
    act.capacity,
    act.status,
    p.name as project_name,
    o.name as organization_name,
    r.name as region_name,
    COUNT(att.id) as registered_volunteers,
    COUNT(CASE WHEN att.status = 'Verified' THEN 1 END) as verified_attendances
FROM activities act
JOIN projects p ON act.project_id = p.id
JOIN organizations o ON p.ngo_id = o.id
JOIN regions r ON p.region_id = r.id
LEFT JOIN attendances att ON act.id = att.activity_id
GROUP BY act.id, act.starts_at, act.ends_at, act.location, act.capacity, act.status, 
         p.name, o.name, r.name;

-- Partnership utilization view
CREATE VIEW partnership_utilization AS
SELECT 
    cp.id as partnership_id,
    c.name as company_name,
    o.name as organization_name,
    cp.partnership_type,
    cp.budget_committed,
    cp.budget_allocated,
    (cp.budget_committed - cp.budget_allocated) as budget_remaining,
    ROUND((cp.budget_allocated / NULLIF(cp.budget_committed, 0)) * 100, 2) as utilization_percentage,
    cp.active_from,
    cp.active_to,
    CASE 
        WHEN cp.active_to IS NULL THEN 'ACTIVE'
        WHEN cp.active_to < CURRENT_DATE THEN 'EXPIRED'
        WHEN cp.active_from > CURRENT_DATE THEN 'FUTURE'
        ELSE 'ACTIVE'
    END as status,
    COUNT(DISTINCT a.id) as total_allocations,
    COUNT(DISTINCT p.id) as projects_funded
FROM company_partnerships cp
JOIN companies c ON cp.company_id = c.id
JOIN organizations o ON cp.organization_id = o.id
LEFT JOIN projects p ON o.id = p.ngo_id
LEFT JOIN allocations a ON p.id = a.project_id AND a.company_id = c.id
GROUP BY cp.id, c.name, o.name, cp.partnership_type, cp.budget_committed, 
         cp.budget_allocated, cp.active_from, cp.active_to;