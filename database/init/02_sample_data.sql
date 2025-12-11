-- ===== COMPREHENSIVE SAMPLE DATA FOR VOLO DATABASE =====
-- This script populates the database with realistic test data for development and testing
-- Following the same comprehensive approach as 01_schema.sql
--
-- Data includes:
-- - Multiple regions covering global areas
-- - Diverse organizations (NGOs and NBEs)
-- - Corporate partners with various industries  
-- - Volunteer base with different demographics
-- - Projects spanning multiple causes
-- - Activities with realistic scheduling
-- - Complete volunteer workflow examples
-- - Company funding and partnership data
-- - Full credit allocation and exchange scenarios

-- ==========================================
-- REGIONS - Geographic areas for volunteer activities
-- ==========================================

INSERT INTO regions (id, name) VALUES 
    ('11111111-1111-1111-1111-111111111111', 'North America'),
    ('22222222-2222-2222-2222-222222222222', 'South America'),
    ('33333333-3333-3333-3333-333333333333', 'Europe'),
    ('44444444-4444-4444-4444-444444444444', 'Asia Pacific'),
    ('55555555-5555-5555-5555-555555555555', 'Africa'),
    ('66666666-6666-6666-6666-666666666666', 'Middle East'),
    ('77777777-7777-7777-7777-777777777777', 'Caribbean'),
    ('88888888-8888-8888-8888-888888888888', 'Oceania'),
    ('99999999-9999-9999-9999-999999999999', 'Central Asia'),
    ('00000000-0000-0000-0000-000000000000', 'Nordic Region');

-- ==========================================
-- ORGANIZATIONS - NGOs and NBEs providing volunteer opportunities
-- ==========================================

INSERT INTO organizations (id, type, name) VALUES 
    -- Primary organizations for core testing
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'NGO', 'Green Earth Foundation'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'NGO', 'Education for All'),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'NGO', 'Clean Water Initiative'),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'NBE', 'Community Health Network'),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'NBE', 'Youth Development Center'),
    ('ffffffff-ffff-ffff-ffff-ffffffffffff', 'NGO', 'Animal Welfare Society'),
    ('12345678-1234-1234-1234-123456789abc', 'NGO', 'Disaster Relief Corps'),
    
    -- Additional organizations for comprehensive testing
    ('12345678-1234-1234-1234-123456789012', 'NGO', 'Environmental Stewards'),
    ('23456789-2345-2345-2345-234567890123', 'NBE', 'Senior Support Services'),
    ('34567890-3456-3456-3456-345678901234', 'NGO', 'Food Security Alliance'),
    ('45678901-4567-4567-4567-456789012345', 'NGO', 'Housing Justice Collective'),
    ('56789012-5678-5678-5678-567890123456', 'NBE', 'Mental Health Advocates'),
    ('67890123-6789-6789-6789-678901234567', 'NGO', 'Arts for Change'),
    ('78901234-7890-7890-7890-789012345678', 'NGO', 'Technology for Good'),
    ('89012345-8901-8901-8901-890123456789', 'NBE', 'Climate Action Group');

-- ==========================================
-- COMPANIES - Corporate partners providing branding and funding
-- ==========================================

INSERT INTO companies (id, name) VALUES 
    -- Primary companies for core testing scenarios
    ('01111111-1111-1111-1111-111111111111', 'TechCorp Solutions'),
    ('02222222-2222-2222-2222-222222222222', 'Green Energy Ltd'),
    ('03333333-3333-3333-3333-333333333333', 'Global Finance Bank'),
    ('04444444-4444-4444-4444-444444444444', 'Sustainable Foods Co'),
    ('05555555-5555-5555-5555-555555555555', 'Innovation Labs Inc'),
    
    -- Additional companies for diverse partnership scenarios
    ('06666666-6666-6666-6666-666666666666', 'HealthFirst Medical'),
    ('07777777-7777-7777-7777-777777777777', 'EcoManufacturing Corp'),
    ('08888888-8888-8888-8888-888888888888', 'Digital Consulting Group'),
    ('09999999-9999-9999-9999-999999999999', 'Renewable Resources Inc'),
    ('10000000-0000-0000-0000-000000000000', 'Community Investment Bank'),
    ('11000000-0000-0000-0000-000000000001', 'Smart Logistics Ltd'),
    ('12000000-0000-0000-0000-000000000002', 'Future Tech Ventures'),
    ('13000000-0000-0000-0000-000000000003', 'Sustainable Retail Chain'),
    ('14000000-0000-0000-0000-000000000004', 'Clean Transport Solutions'),
    ('15000000-0000-0000-0000-000000000005', 'Social Impact Capital');

-- ==========================================
-- VOLUNTEERS - Individual contributors to volunteer activities
-- ==========================================

INSERT INTO volunteers (id, name, email, age, region_id) VALUES 
    -- Primary volunteers for core testing scenarios
    ('10111111-1111-1111-1111-111111111111', 'Alice Johnson', 'alice.johnson@email.com', 28, '11111111-1111-1111-1111-111111111111'),
    ('10222222-2222-2222-2222-222222222222', 'Bob Smith', 'bob.smith@email.com', 35, '11111111-1111-1111-1111-111111111111'),
    ('10333333-3333-3333-3333-333333333333', 'Carmen Rodriguez', 'carmen.rodriguez@email.com', 24, '22222222-2222-2222-2222-222222222222'),
    ('10444444-4444-4444-4444-444444444444', 'David Chen', 'david.chen@email.com', 31, '44444444-4444-4444-4444-444444444444'),
    ('10555555-5555-5555-5555-555555555555', 'Emma Thompson', 'emma.thompson@email.com', 27, '33333333-3333-3333-3333-333333333333'),
    ('10666666-6666-6666-6666-666666666666', 'Frank Wilson', 'frank.wilson@email.com', 42, '11111111-1111-1111-1111-111111111111'),
    ('10777777-7777-7777-7777-777777777777', 'Grace Kim', 'grace.kim@email.com', 29, '44444444-4444-4444-4444-444444444444'),
    ('10888888-8888-8888-8888-888888888888', 'Hassan Al-Rashid', 'hassan.alrashid@email.com', 33, '55555555-5555-5555-5555-555555555555'),
    ('10999999-9999-9999-9999-999999999999', 'Isabella Garcia', 'isabella.garcia@email.com', 26, '22222222-2222-2222-2222-222222222222'),
    ('10000000-0000-0000-0000-000000000000', 'Jack Turner', 'jack.turner@email.com', 38, '33333333-3333-3333-3333-333333333333'),
    
    -- Additional volunteers for comprehensive testing
    ('11111111-1111-1111-1111-111111111110', 'Sarah Mitchell', 'sarah.mitchell@email.com', 23, '66666666-6666-6666-6666-666666666666'),
    ('11111111-1111-1111-1111-111111111120', 'Mike O''Connor', 'mike.oconnor@email.com', 45, '77777777-7777-7777-7777-777777777777'),
    ('11111111-1111-1111-1111-111111111130', 'Priya Patel', 'priya.patel@email.com', 30, '88888888-8888-8888-8888-888888888888'),
    ('11111111-1111-1111-1111-111111111140', 'Ahmed Hassan', 'ahmed.hassan@email.com', 36, '99999999-9999-9999-9999-999999999999'),
    ('11111111-1111-1111-1111-111111111150', 'Elena Volkov', 'elena.volkov@email.com', 41, '00000000-0000-0000-0000-000000000000'),
    ('11111111-1111-1111-1111-111111111160', 'Carlos Santos', 'carlos.santos@email.com', 25, '22222222-2222-2222-2222-222222222222'),
    ('11111111-1111-1111-1111-111111111170', 'Yuki Tanaka', 'yuki.tanaka@email.com', 32, '44444444-4444-4444-4444-444444444444'),
    ('11111111-1111-1111-1111-111111111180', 'Fatima Al-Zahra', 'fatima.alzahra@email.com', 27, '55555555-5555-5555-5555-555555555555'),
    ('11111111-1111-1111-1111-111111111190', 'James Anderson', 'james.anderson@email.com', 39, '11111111-1111-1111-1111-111111111111'),
    ('11111111-1111-1111-1111-111111111200', 'Maria Silva', 'maria.silva@email.com', 34, '33333333-3333-3333-3333-333333333333');

-- ==========================================
-- PROJECTS - Volunteer initiatives organized by NGOs/NBEs
-- ==========================================

INSERT INTO projects (id, ngo_id, region_id, name, description) VALUES 
    -- Core projects for primary testing scenarios
    ('20111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'Urban Tree Planting', 'Plant and maintain trees in urban areas to improve air quality and combat climate change'),
    ('20222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', 'Adult Literacy Program', 'Teaching basic reading and writing skills to adults who missed formal education opportunities'),
    ('20333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '22222222-2222-2222-2222-222222222222', 'Clean Water Access', 'Installing water purification systems in rural communities without access to clean drinking water'),
    ('20444444-4444-4444-4444-444444444444', 'dddddddd-dddd-dddd-dddd-dddddddddddd', '44444444-4444-4444-4444-444444444444', 'Community Health Screening', 'Free health checkups and basic medical services for underserved populations'),
    ('20555555-5555-5555-5555-555555555555', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '33333333-3333-3333-3333-333333333333', 'Youth Mentorship', 'Mentoring at-risk youth and providing career guidance and life skills training'),
    ('20666666-6666-6666-6666-666666666666', 'ffffffff-ffff-ffff-ffff-ffffffffffff', '55555555-5555-5555-5555-555555555555', 'Animal Rescue', 'Rescuing and rehabilitating abandoned animals while promoting responsible pet ownership'),
    ('20777777-7777-7777-7777-777777777777', '12345678-1234-1234-1234-123456789abc', '11111111-1111-1111-1111-111111111111', 'Emergency Food Distribution', 'Distributing food to disaster-affected communities and families in crisis'),
    
    -- Additional projects for comprehensive testing
    ('21111111-1111-1111-1111-111111111111', '12345678-1234-1234-1234-123456789012', '66666666-6666-6666-6666-666666666666', 'Desert Reforestation', 'Combating desertification through strategic tree planting and soil conservation'),
    ('21222222-2222-2222-2222-222222222222', '23456789-2345-2345-2345-234567890123', '77777777-7777-7777-7777-777777777777', 'Senior Companion Program', 'Providing companionship and support services to isolated elderly community members'),
    ('21333333-3333-3333-3333-333333333333', '34567890-3456-3456-3456-345678901234', '88888888-8888-8888-8888-888888888888', 'Community Gardens Initiative', 'Establishing urban gardens to improve food security and community engagement'),
    ('21444444-4444-4444-4444-444444444444', '45678901-4567-4567-4567-456789012345', '99999999-9999-9999-9999-999999999999', 'Housing Rehabilitation', 'Renovating homes for low-income families and disaster recovery efforts'),
    ('21555555-5555-5555-5555-555555555555', '56789012-5678-5678-5678-567890123456', '00000000-0000-0000-0000-000000000000', 'Mental Health Support Groups', 'Facilitating peer support groups for mental health awareness and recovery');

-- ==========================================
-- ACTIVITIES - Scheduled volunteer events within projects
-- ==========================================

INSERT INTO activities (id, project_id, starts_at, ends_at, location, capacity, status) VALUES 
    -- Completed activities (for testing verified scenarios)
    ('30111111-1111-1111-1111-111111111111', '20222222-2222-2222-2222-222222222222', '2024-12-10 10:00:00+00', '2024-12-10 15:00:00+00', 'Community Center, Boston', 15, 'Completed'),
    ('30222222-2222-2222-2222-222222222222', '20333333-3333-3333-3333-333333333333', '2024-12-08 08:00:00+00', '2024-12-08 16:00:00+00', 'Rural Village, Peru', 12, 'Completed'),
    ('30333333-3333-3333-3333-333333333333', '20444444-4444-4444-4444-444444444444', '2024-12-12 07:00:00+00', '2024-12-12 14:00:00+00', 'Health Clinic, Singapore', 25, 'Completed'),
    ('30444444-4444-4444-4444-444444444444', '20666666-6666-6666-6666-666666666666', '2024-12-05 09:00:00+00', '2024-12-05 17:00:00+00', 'Animal Shelter, Nairobi', 8, 'Completed'),
    
    -- Scheduled activities (for testing future scenarios)
    ('30555555-5555-5555-5555-555555555555', '20111111-1111-1111-1111-111111111111', '2024-12-15 09:00:00+00', '2024-12-15 17:00:00+00', 'Central Park, New York', 20, 'Scheduled'),
    ('30666666-6666-6666-6666-666666666666', '20555555-5555-5555-5555-555555555555', '2024-12-20 13:00:00+00', '2024-12-20 18:00:00+00', 'Youth Center, London', 10, 'Scheduled'),
    ('30777777-7777-7777-7777-777777777777', '20777777-7777-7777-7777-777777777777', '2024-12-18 06:00:00+00', '2024-12-18 20:00:00+00', 'Disaster Zone, Miami', 30, 'Scheduled'),
    
    -- Additional activities for comprehensive testing
    ('31111111-1111-1111-1111-111111111111', '21111111-1111-1111-1111-111111111111', '2024-12-22 08:00:00+00', '2024-12-22 16:00:00+00', 'Desert Conservation Area, Dubai', 15, 'Scheduled'),
    ('31222222-2222-2222-2222-222222222222', '21222222-2222-2222-2222-222222222222', '2024-12-25 14:00:00+00', '2024-12-25 17:00:00+00', 'Senior Center, Jamaica', 12, 'Scheduled'),
    ('31333333-3333-3333-3333-333333333333', '21333333-3333-3333-3333-333333333333', '2024-12-28 10:00:00+00', '2024-12-28 15:00:00+00', 'Community Plot, Sydney', 20, 'Scheduled');

-- ==========================================
-- ATTENDANCES - Volunteer participation records
-- ==========================================

INSERT INTO attendances (id, volunteer_id, activity_id, check_in_at, check_out_at, verified_by_user_id, status) VALUES 
    -- Verified attendances for credit generation
    ('40111111-1111-1111-1111-111111111111', '10111111-1111-1111-1111-111111111111', '30111111-1111-1111-1111-111111111111', '2024-12-10 10:05:00+00', '2024-12-10 14:55:00+00', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Verified'),
    ('40222222-2222-2222-2222-222222222222', '10222222-2222-2222-2222-222222222222', '30111111-1111-1111-1111-111111111111', '2024-12-10 09:58:00+00', '2024-12-10 15:02:00+00', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Verified'),
    ('40333333-3333-3333-3333-333333333333', '10333333-3333-3333-3333-333333333333', '30222222-2222-2222-2222-222222222222', '2024-12-08 08:10:00+00', '2024-12-08 15:50:00+00', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'Verified'),
    ('40444444-4444-4444-4444-444444444444', '10444444-4444-4444-4444-444444444444', '30333333-3333-3333-3333-333333333333', '2024-12-12 07:05:00+00', '2024-12-12 13:45:00+00', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'Verified'),
    ('40555555-5555-5555-5555-555555555555', '10555555-5555-5555-5555-555555555555', '30444444-4444-4444-4444-444444444444', '2024-12-05 09:15:00+00', '2024-12-05 16:30:00+00', 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'Verified'),
    ('40666666-6666-6666-6666-666666666666', '10666666-6666-6666-6666-666666666666', '30333333-3333-3333-3333-333333333333', '2024-12-12 07:00:00+00', '2024-12-12 14:00:00+00', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'Verified'),
    
    -- Pending attendances for future activities
    ('40777777-7777-7777-7777-777777777777', '10111111-1111-1111-1111-111111111111', '30555555-5555-5555-5555-555555555555', '2024-12-15 09:00:00+00', NULL, NULL, 'Pending'),
    ('40888888-8888-8888-8888-888888888888', '10777777-7777-7777-7777-777777777777', '30666666-6666-6666-6666-666666666666', NULL, NULL, NULL, 'Pending');

-- ==========================================
-- VOLO CREDITS - Credits earned from verified attendances
-- ==========================================

INSERT INTO volo_credits (id, volunteer_id, source_attendance_id, amount, status, granted_at, expires_at) VALUES 
    -- Available credits ready for allocation
    ('50111111-1111-1111-1111-111111111111', '10111111-1111-1111-1111-111111111111', '40111111-1111-1111-1111-111111111111', 48.50, 'Available', '2024-12-10 15:00:00+00', '2025-12-10 15:00:00+00'),
    ('50333333-3333-3333-3333-333333333333', '10333333-3333-3333-3333-333333333333', '40333333-3333-3333-3333-333333333333', 77.50, 'Available', '2024-12-08 16:00:00+00', '2025-12-08 16:00:00+00'),
    ('50555555-5555-5555-5555-555555555555', '10555555-5555-5555-5555-555555555555', '40555555-5555-5555-5555-555555555555', 73.25, 'Available', '2024-12-05 17:00:00+00', '2025-12-05 17:00:00+00'),
    
    -- Allocated credits (used in allocation scenarios)
    ('50222222-2222-2222-2222-222222222222', '10222222-2222-2222-2222-222222222222', '40222222-2222-2222-2222-222222222222', 50.00, 'Allocated', '2024-12-10 15:05:00+00', '2025-12-10 15:05:00+00'),
    ('50444444-4444-4444-4444-444444444444', '10444444-4444-4444-4444-444444444444', '40444444-4444-4444-4444-444444444444', 67.00, 'Allocated', '2024-12-12 14:00:00+00', '2025-12-12 14:00:00+00'),
    ('50666666-6666-6666-6666-666666666666', '10666666-6666-6666-6666-666666666666', '40666666-6666-6666-6666-666666666666', 70.00, 'Allocated', '2024-12-12 14:15:00+00', '2025-12-12 14:15:00+00');

-- ==========================================
-- COMPANY PARTNERSHIPS - Formal partnerships between companies and organizations
-- ==========================================

INSERT INTO company_partnerships (id, company_id, organization_id, partnership_type, budget_committed, budget_allocated, active_from, active_to) VALUES 
    ('90111111-1111-1111-1111-111111111111', '01111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'FUNDING', 100000.00, 33.50, '2024-01-01', '2024-12-31'),
    ('90222222-2222-2222-2222-222222222222', '02222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'SPONSORSHIP', 75000.00, 25.00, '2024-01-01', '2024-12-31'),
    ('90333333-3333-3333-3333-333333333333', '03333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'STRATEGIC', 50000.00, 0.00, '2024-01-01', '2024-12-31'),
    ('90444444-4444-4444-4444-444444444444', '04444444-4444-4444-4444-444444444444', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'FUNDING', 120000.00, 0.00, '2024-01-01', '2024-12-31'),
    ('90555555-5555-5555-5555-555555555555', '05555555-5555-5555-5555-555555555555', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'SPONSORSHIP', 80000.00, 0.00, '2024-01-01', '2024-12-31'),
    ('90666666-6666-6666-6666-666666666666', '06666666-6666-6666-6666-666666666666', 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'FUNDING', 90000.00, 0.00, '2024-01-01', '2024-12-31'),
    ('90777777-7777-7777-7777-777777777777', '07777777-7777-7777-7777-777777777777', '12345678-1234-1234-1234-123456789abc', 'STRATEGIC', 60000.00, 0.00, '2024-01-01', '2024-12-31');

-- ==========================================
-- PROJECT COMPANY FUNDINGS - Company pre-approval system for project funding
-- ==========================================

INSERT INTO project_company_fundings (id, project_id, company_id, max_budget, allocated_budget, status, approved_at, approved_by) VALUES 
    -- Pre-approved funding for active projects
    ('95111111-1111-1111-1111-111111111111', '20111111-1111-1111-1111-111111111111', '01111111-1111-1111-1111-111111111111', 10000.00, 0.00, 'ACTIVE', '2024-12-01 10:00:00+00', 'TechCorp CSR Manager'),
    ('95222222-2222-2222-2222-222222222222', '20222222-2222-2222-2222-222222222222', '02222222-2222-2222-2222-222222222222', 15000.00, 25.00, 'ACTIVE', '2024-12-01 11:00:00+00', 'Green Energy Partnership Lead'),
    ('95333333-3333-3333-3333-333333333333', '20444444-4444-4444-4444-444444444444', '03333333-3333-3333-3333-333333333333', 20000.00, 33.50, 'ACTIVE', '2024-12-01 12:00:00+00', 'Global Finance Community Relations'),
    ('95444444-4444-4444-4444-444444444444', '20777777-7777-7777-7777-777777777777', '01111111-1111-1111-1111-111111111111', 12000.00, 33.50, 'ACTIVE', '2024-12-01 13:00:00+00', 'TechCorp Emergency Response Team'),
    ('95555555-5555-5555-5555-555555555555', '20666666-6666-6666-6666-666666666666', '04444444-4444-4444-4444-444444444444', 8000.00, 35.00, 'ACTIVE', '2024-12-01 14:00:00+00', 'Sustainable Foods CSR Director'),
    ('95666666-6666-6666-6666-666666666666', '20333333-3333-3333-3333-333333333333', '05555555-5555-5555-5555-555555555555', 18000.00, 0.00, 'ACTIVE', '2024-12-01 15:00:00+00', 'Innovation Labs Social Impact Lead');

-- ==========================================
-- BRAND MESSAGES - Corporate branding content for volunteer engagement
-- ==========================================

INSERT INTO brand_messages (id, company_id, content, image_url, active_from, active_to) VALUES 
    ('60111111-1111-1111-1111-111111111111', '01111111-1111-1111-1111-111111111111', 'TechCorp is proud to support environmental initiatives in your community!', 'https://example.com/techcorp-green.jpg', '2024-12-01 00:00:00+00', '2025-06-01 00:00:00+00'),
    ('60222222-2222-2222-2222-222222222222', '02222222-2222-2222-2222-222222222222', 'Green Energy Ltd: Powering a sustainable future together', 'https://example.com/green-energy.jpg', '2024-11-01 00:00:00+00', '2025-05-01 00:00:00+00'),
    ('60333333-3333-3333-3333-333333333333', '03333333-3333-3333-3333-333333333333', 'Global Finance Bank believes in investing in communities that matter', 'https://example.com/global-finance.jpg', '2024-12-15 00:00:00+00', '2025-07-15 00:00:00+00'),
    ('60444444-4444-4444-4444-444444444444', '04444444-4444-4444-4444-444444444444', 'Sustainable Foods Co: Nourishing communities, sustaining the planet', 'https://example.com/sustainable-foods.jpg', '2024-12-01 00:00:00+00', '2025-08-01 00:00:00+00'),
    ('60555555-5555-5555-5555-555555555555', '05555555-5555-5555-5555-555555555555', 'Innovation Labs Inc: Where technology meets social impact', 'https://example.com/innovation-labs.jpg', '2024-10-01 00:00:00+00', '2025-04-01 00:00:00+00');

-- ==========================================
-- ALLOCATIONS - Credit distributions following 50/50 rule
-- ==========================================

INSERT INTO allocations (id, volunteer_id, project_id, company_id, source_credit_id, amount, kind) VALUES 
    -- Bob's allocations (demonstrating 50/50 mandatory/free choice rule)
    ('70111111-1111-1111-1111-111111111111', '10222222-2222-2222-2222-222222222222', '20222222-2222-2222-2222-222222222222', '01111111-1111-1111-1111-111111111111', '50222222-2222-2222-2222-222222222222', 25.00, 'MANDATORY_50'),
    ('70222222-2222-2222-2222-222222222222', '10222222-2222-2222-2222-222222222222', '20111111-1111-1111-1111-111111111111', '02222222-2222-2222-2222-222222222222', '50222222-2222-2222-2222-222222222222', 25.00, 'FREE_CHOICE_50'),
    
    -- David's allocations (demonstrating multi-project allocation)
    ('70333333-3333-3333-3333-333333333333', '10444444-4444-4444-4444-444444444444', '20444444-4444-4444-4444-444444444444', '03333333-3333-3333-3333-333333333333', '50444444-4444-4444-4444-444444444444', 33.50, 'MANDATORY_50'),
    ('70444444-4444-4444-4444-444444444444', '10444444-4444-4444-4444-444444444444', '20777777-7777-7777-7777-777777777777', '01111111-1111-1111-1111-111111111111', '50444444-4444-4444-4444-444444444444', 33.50, 'FREE_CHOICE_50'),
    
    -- Frank's allocations (demonstrating cross-region support)
    ('70555555-5555-5555-5555-555555555555', '10666666-6666-6666-6666-666666666666', '20444444-4444-4444-4444-444444444444', '04444444-4444-4444-4444-444444444444', '50666666-6666-6666-6666-666666666666', 35.00, 'MANDATORY_50'),
    ('70666666-6666-6666-6666-666666666666', '10666666-6666-6666-6666-666666666666', '20222222-2222-2222-2222-222222222222', '05555555-5555-5555-5555-555555555555', '50666666-6666-6666-6666-666666666666', 35.00, 'FREE_CHOICE_50');

-- ==========================================
-- CREDIT EXCHANGES - Project funding from allocations
-- ==========================================

INSERT INTO credit_exchanges (id, allocation_id, project_id) VALUES 
    ('80111111-1111-1111-1111-111111111111', '70111111-1111-1111-1111-111111111111', '20222222-2222-2222-2222-222222222222'),
    ('80222222-2222-2222-2222-222222222222', '70222222-2222-2222-2222-222222222222', '20111111-1111-1111-1111-111111111111'),
    ('80333333-3333-3333-3333-333333333333', '70333333-3333-3333-3333-333333333333', '20444444-4444-4444-4444-444444444444'),
    ('80444444-4444-4444-4444-444444444444', '70444444-4444-4444-4444-444444444444', '20777777-7777-7777-7777-777777777777'),
    ('80555555-5555-5555-5555-555555555555', '70555555-5555-5555-5555-555555555555', '20444444-4444-4444-4444-444444444444'),
    ('80666666-6666-6666-6666-666666666666', '70666666-6666-6666-6666-666666666666', '20222222-2222-2222-2222-222222222222');

-- ==========================================
-- LEDGER ENTRIES - Audit trail for all transactions
-- ==========================================

INSERT INTO ledger_entries (id, ref_type, ref_id, hash, prev_hash) VALUES 
    ('98111111-1111-1111-1111-111111111111', 'Attendance', '40111111-1111-1111-1111-111111111111', 'abc123def456', NULL),
    ('98222222-2222-2222-2222-222222222222', 'VoloCredit', '50111111-1111-1111-1111-111111111111', 'def456ghi789', 'abc123def456'),
    ('98333333-3333-3333-3333-333333333333', 'Allocation', '70111111-1111-1111-1111-111111111111', 'ghi789jkl012', 'def456ghi789'),
    ('98444444-4444-4444-4444-444444444444', 'CreditExchange', '80111111-1111-1111-1111-111111111111', 'jkl012mno345', 'ghi789jkl012'),
    ('98555555-5555-5555-5555-555555555555', 'ProjectFunding', '95111111-1111-1111-1111-111111111111', 'mno345pqr678', 'jkl012mno345'),
    ('98666666-6666-6666-6666-666666666666', 'Partnership', '90111111-1111-1111-1111-111111111111', 'pqr678stu901', 'mno345pqr678'),
    ('98777777-7777-7777-7777-777777777777', 'BrandMessage', '60111111-1111-1111-1111-111111111111', 'stu901vwx234', 'pqr678stu901');

-- ==========================================
-- SUMMARY STATISTICS
-- ==========================================
-- This comprehensive sample data provides:
-- - 10 regions covering global volunteer opportunities
-- - 15 organizations (NGOs and NBEs) with diverse causes
-- - 15 companies representing various industries
-- - 20 volunteers with diverse demographics across regions
-- - 12 projects spanning multiple causes and regions
-- - 10 activities with realistic scheduling (completed and scheduled)
-- - 8 attendance records demonstrating various verification states
-- - 6 volo credit records showing available and allocated states
-- - 7 company partnerships with different partnership types
-- - 6 project funding pre-approvals demonstrating company control
-- - 5 brand messages for corporate engagement
-- - 6 credit allocations following 50/50 mandatory/free choice rule
-- - 6 credit exchanges showing project funding flow
-- - 7 ledger entries providing complete audit trail
--
-- This data supports comprehensive testing of:
-- - Complete volunteer workflow (attendance → credits → allocation → funding)
-- - Company pre-approval funding model
-- - 50/50 allocation rule enforcement
-- - Multi-region and multi-organization scenarios
-- - Partnership and branding integrations
-- - Audit trail and compliance tracking