-- ===== SAMPLE DATA FOR VOLO DATABASE =====
-- This script populates the database with realistic test data

-- Insert Regions
INSERT INTO regions (id, name) VALUES 
    ('11111111-1111-1111-1111-111111111111', 'North America'),
    ('22222222-2222-2222-2222-222222222222', 'South America'),
    ('33333333-3333-3333-3333-333333333333', 'Europe'),
    ('44444444-4444-4444-4444-444444444444', 'Asia Pacific'),
    ('55555555-5555-5555-5555-555555555555', 'Africa');

-- Insert Organizations (NGOs and NBEs)
INSERT INTO organizations (id, type, name) VALUES 
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'NGO', 'Green Earth Foundation'),
    ('bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'NGO', 'Education for All'),
    ('cccccccc-cccc-cccc-cccc-cccccccccccc', 'NGO', 'Clean Water Initiative'),
    ('dddddddd-dddd-dddd-dddd-dddddddddddd', 'NBE', 'Community Health Network'),
    ('eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', 'NBE', 'Youth Development Center'),
    ('ffffffff-ffff-ffff-ffff-ffffffffffff', 'NGO', 'Animal Welfare Society'),
    ('gggggggg-gggg-gggg-gggg-gggggggggggg', 'NGO', 'Disaster Relief Corps');

-- Insert Companies (for branding and funding)
INSERT INTO companies (id, name) VALUES 
    ('c1111111-1111-1111-1111-111111111111', 'TechCorp Solutions'),
    ('c2222222-2222-2222-2222-222222222222', 'Green Energy Ltd'),
    ('c3333333-3333-3333-3333-333333333333', 'Global Finance Bank'),
    ('c4444444-4444-4444-4444-444444444444', 'Sustainable Foods Co'),
    ('c5555555-5555-5555-5555-555555555555', 'Innovation Labs Inc');

-- Insert Volunteers
INSERT INTO volunteers (id, name, email, age, region_id) VALUES 
    ('v1111111-1111-1111-1111-111111111111', 'Alice Johnson', 'alice.johnson@email.com', 28, '11111111-1111-1111-1111-111111111111'),
    ('v2222222-2222-2222-2222-222222222222', 'Bob Smith', 'bob.smith@email.com', 35, '11111111-1111-1111-1111-111111111111'),
    ('v3333333-3333-3333-3333-333333333333', 'Carmen Rodriguez', 'carmen.rodriguez@email.com', 24, '22222222-2222-2222-2222-222222222222'),
    ('v4444444-4444-4444-4444-444444444444', 'David Chen', 'david.chen@email.com', 31, '44444444-4444-4444-4444-444444444444'),
    ('v5555555-5555-5555-5555-555555555555', 'Emma Thompson', 'emma.thompson@email.com', 27, '33333333-3333-3333-3333-333333333333'),
    ('v6666666-6666-6666-6666-666666666666', 'Frank Wilson', 'frank.wilson@email.com', 42, '11111111-1111-1111-1111-111111111111'),
    ('v7777777-7777-7777-7777-777777777777', 'Grace Kim', 'grace.kim@email.com', 29, '44444444-4444-4444-4444-444444444444'),
    ('v8888888-8888-8888-8888-888888888888', 'Hassan Al-Rashid', 'hassan.alrashid@email.com', 33, '55555555-5555-5555-5555-555555555555'),
    ('v9999999-9999-9999-9999-999999999999', 'Isabella Garcia', 'isabella.garcia@email.com', 26, '22222222-2222-2222-2222-222222222222'),
    ('v0000000-0000-0000-0000-000000000000', 'Jack Turner', 'jack.turner@email.com', 38, '33333333-3333-3333-3333-333333333333');

-- Insert Projects
INSERT INTO projects (id, ngo_id, region_id, name, description) VALUES 
    ('p1111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '11111111-1111-1111-1111-111111111111', 'Urban Tree Planting', 'Plant and maintain trees in urban areas to improve air quality'),
    ('p2222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', '11111111-1111-1111-1111-111111111111', 'Adult Literacy Program', 'Teaching basic reading and writing skills to adults'),
    ('p3333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc', '22222222-2222-2222-2222-222222222222', 'Clean Water Access', 'Installing water purification systems in rural communities'),
    ('p4444444-4444-4444-4444-444444444444', 'dddddddd-dddd-dddd-dddd-dddddddddddd', '44444444-4444-4444-4444-444444444444', 'Community Health Screening', 'Free health checkups and basic medical services'),
    ('p5555555-5555-5555-5555-555555555555', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee', '33333333-3333-3333-3333-333333333333', 'Youth Mentorship', 'Mentoring at-risk youth and providing career guidance'),
    ('p6666666-6666-6666-6666-666666666666', 'ffffffff-ffff-ffff-ffff-ffffffffffff', '55555555-5555-5555-5555-555555555555', 'Animal Rescue', 'Rescuing and rehabilitating abandoned animals'),
    ('p7777777-7777-7777-7777-777777777777', 'gggggggg-gggg-gggg-gggg-gggggggggggg', '11111111-1111-1111-1111-111111111111', 'Emergency Food Distribution', 'Distributing food to disaster-affected communities');

-- Insert Activities
INSERT INTO activities (id, project_id, starts_at, ends_at, location, capacity, status) VALUES 
    ('a1111111-1111-1111-1111-111111111111', 'p1111111-1111-1111-1111-111111111111', '2024-12-15 09:00:00+00', '2024-12-15 17:00:00+00', 'Central Park, New York', 20, 'Scheduled'),
    ('a2222222-2222-2222-2222-222222222222', 'p2222222-2222-2222-2222-222222222222', '2024-12-10 10:00:00+00', '2024-12-10 15:00:00+00', 'Community Center, Boston', 15, 'Completed'),
    ('a3333333-3333-3333-3333-333333333333', 'p3333333-3333-3333-3333-333333333333', '2024-12-08 08:00:00+00', '2024-12-08 16:00:00+00', 'Rural Village, Peru', 12, 'Completed'),
    ('a4444444-4444-4444-4444-444444444444', 'p4444444-4444-4444-4444-444444444444', '2024-12-12 07:00:00+00', '2024-12-12 14:00:00+00', 'Health Clinic, Singapore', 25, 'Completed'),
    ('a5555555-5555-5555-5555-555555555555', 'p5555555-5555-5555-5555-555555555555', '2024-12-20 13:00:00+00', '2024-12-20 18:00:00+00', 'Youth Center, London', 10, 'Scheduled'),
    ('a6666666-6666-6666-6666-666666666666', 'p6666666-6666-6666-6666-666666666666', '2024-12-05 09:00:00+00', '2024-12-05 17:00:00+00', 'Animal Shelter, Nairobi', 8, 'Completed'),
    ('a7777777-7777-7777-7777-777777777777', 'p7777777-7777-7777-7777-777777777777', '2024-12-18 06:00:00+00', '2024-12-18 20:00:00+00', 'Disaster Zone, Miami', 30, 'Scheduled');

-- Insert Attendances (some verified, some pending)
INSERT INTO attendances (id, volunteer_id, activity_id, check_in_at, check_out_at, verified_by_user_id, status) VALUES 
    ('at111111-1111-1111-1111-111111111111', 'v1111111-1111-1111-1111-111111111111', 'a2222222-2222-2222-2222-222222222222', '2024-12-10 10:05:00+00', '2024-12-10 14:55:00+00', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Verified'),
    ('at222222-2222-2222-2222-222222222222', 'v2222222-2222-2222-2222-222222222222', 'a2222222-2222-2222-2222-222222222222', '2024-12-10 09:58:00+00', '2024-12-10 15:02:00+00', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb', 'Verified'),
    ('at333333-3333-3333-3333-333333333333', 'v3333333-3333-3333-3333-333333333333', 'a3333333-3333-3333-3333-333333333333', '2024-12-08 08:10:00+00', '2024-12-08 15:50:00+00', 'cccccccc-cccc-cccc-cccc-cccccccccccc', 'Verified'),
    ('at444444-4444-4444-4444-444444444444', 'v4444444-4444-4444-4444-444444444444', 'a4444444-4444-4444-4444-444444444444', '2024-12-12 07:05:00+00', '2024-12-12 13:45:00+00', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'Verified'),
    ('at555555-5555-5555-5555-555555555555', 'v5555555-5555-5555-5555-555555555555', 'a6666666-6666-6666-6666-666666666666', '2024-12-05 09:15:00+00', '2024-12-05 16:30:00+00', 'ffffffff-ffff-ffff-ffff-ffffffffffff', 'Verified'),
    ('at666666-6666-6666-6666-666666666666', 'v1111111-1111-1111-1111-111111111111', 'a1111111-1111-1111-1111-111111111111', '2024-12-15 09:00:00+00', NULL, NULL, 'Pending'),
    ('at777777-7777-7777-7777-777777777777', 'v6666666-6666-6666-6666-666666666666', 'a4444444-4444-4444-4444-444444444444', '2024-12-12 07:00:00+00', '2024-12-12 14:00:00+00', 'dddddddd-dddd-dddd-dddd-dddddddddddd', 'Verified');

-- Insert Volo Credits (based on verified attendances)
INSERT INTO volo_credits (id, volunteer_id, source_attendance_id, amount, status, granted_at, expires_at) VALUES 
    ('vc111111-1111-1111-1111-111111111111', 'v1111111-1111-1111-1111-111111111111', 'at111111-1111-1111-1111-111111111111', 48.50, 'Available', '2024-12-10 15:00:00+00', '2025-12-10 15:00:00+00'),
    ('vc222222-2222-2222-2222-222222222222', 'v2222222-2222-2222-2222-222222222222', 'at222222-2222-2222-2222-222222222222', 50.00, 'Allocated', '2024-12-10 15:05:00+00', '2025-12-10 15:05:00+00'),
    ('vc333333-3333-3333-3333-333333333333', 'v3333333-3333-3333-3333-333333333333', 'at333333-3333-3333-3333-333333333333', 77.50, 'Available', '2024-12-08 16:00:00+00', '2025-12-08 16:00:00+00'),
    ('vc444444-4444-4444-4444-444444444444', 'v4444444-4444-4444-4444-444444444444', 'at444444-4444-4444-4444-444444444444', 67.00, 'Allocated', '2024-12-12 14:00:00+00', '2025-12-12 14:00:00+00'),
    ('vc555555-5555-5555-5555-555555555555', 'v5555555-5555-5555-5555-555555555555', 'at555555-5555-5555-5555-555555555555', 73.25, 'Available', '2024-12-05 17:00:00+00', '2025-12-05 17:00:00+00'),
    ('vc666666-6666-6666-6666-666666666666', 'v6666666-6666-6666-6666-666666666666', 'at777777-7777-7777-7777-777777777777', 70.00, 'Allocated', '2024-12-12 14:15:00+00', '2025-12-12 14:15:00+00');

-- Insert Brand Messages
INSERT INTO brand_messages (id, company_id, content, image_url, active_from, active_to) VALUES 
    ('bm111111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', 'TechCorp is proud to support environmental initiatives in your community!', 'https://example.com/techcorp-green.jpg', '2024-12-01 00:00:00+00', '2025-06-01 00:00:00+00'),
    ('bm222222-2222-2222-2222-222222222222', 'c2222222-2222-2222-2222-222222222222', 'Green Energy Ltd: Powering a sustainable future together', 'https://example.com/green-energy.jpg', '2024-11-01 00:00:00+00', '2025-05-01 00:00:00+00'),
    ('bm333333-3333-3333-3333-333333333333', 'c3333333-3333-3333-3333-333333333333', 'Global Finance Bank believes in investing in communities that matter', 'https://example.com/global-finance.jpg', '2024-12-15 00:00:00+00', '2025-07-15 00:00:00+00');

-- Insert Allocations (following the 50/50 rule)
INSERT INTO allocations (id, volunteer_id, project_id, company_id, source_credit_id, amount, kind) VALUES 
    -- Bob's allocations (50% mandatory to attended project, 50% free choice)
    ('al111111-1111-1111-1111-111111111111', 'v2222222-2222-2222-2222-222222222222', 'p2222222-2222-2222-2222-222222222222', 'c1111111-1111-1111-1111-111111111111', 'vc222222-2222-2222-2222-222222222222', 25.00, 'MANDATORY_50'),
    ('al222222-2222-2222-2222-222222222222', 'v2222222-2222-2222-2222-222222222222', 'p1111111-1111-1111-1111-111111111111', 'c2222222-2222-2222-2222-222222222222', 'vc222222-2222-2222-2222-222222222222', 25.00, 'FREE_CHOICE_50'),
    -- David's allocations
    ('al333333-3333-3333-3333-333333333333', 'v4444444-4444-4444-4444-444444444444', 'p4444444-4444-4444-4444-444444444444', 'c3333333-3333-3333-3333-333333333333', 'vc444444-4444-4444-4444-444444444444', 33.50, 'MANDATORY_50'),
    ('al444444-4444-4444-4444-444444444444', 'v4444444-4444-4444-4444-444444444444', 'p7777777-7777-7777-7777-777777777777', 'c1111111-1111-1111-1111-111111111111', 'vc444444-4444-4444-4444-444444444444', 33.50, 'FREE_CHOICE_50'),
    -- Frank's allocations  
    ('al555555-5555-5555-5555-555555555555', 'v6666666-6666-6666-6666-666666666666', 'p4444444-4444-4444-4444-444444444444', 'c4444444-4444-4444-4444-444444444444', 'vc666666-6666-6666-6666-666666666666', 35.00, 'MANDATORY_50'),
    ('al666666-6666-6666-6666-666666666666', 'v6666666-6666-6666-6666-666666666666', 'p2222222-2222-2222-2222-222222222222', 'c5555555-5555-5555-5555-555555555555', 'vc666666-6666-6666-6666-666666666666', 35.00, 'FREE_CHOICE_50');

-- Insert Credit Exchanges
INSERT INTO credit_exchanges (id, allocation_id, project_id) VALUES 
    ('ce111111-1111-1111-1111-111111111111', 'al111111-1111-1111-1111-111111111111', 'p2222222-2222-2222-2222-222222222222'),
    ('ce222222-2222-2222-2222-222222222222', 'al222222-2222-2222-2222-222222222222', 'p1111111-1111-1111-1111-111111111111'),
    ('ce333333-3333-3333-3333-333333333333', 'al333333-3333-3333-3333-333333333333', 'p4444444-4444-4444-4444-444444444444'),
    ('ce444444-4444-4444-4444-444444444444', 'al444444-4444-4444-4444-444444444444', 'p7777777-7777-7777-7777-777777777777'),
    ('ce555555-5555-5555-5555-555555555555', 'al555555-5555-5555-5555-555555555555', 'p4444444-4444-4444-4444-444444444444'),
    ('ce666666-6666-6666-6666-666666666666', 'al666666-6666-6666-6666-666666666666', 'p2222222-2222-2222-2222-222222222222');

-- Insert Ledger Company NGO relationships
INSERT INTO ledger_company_ngo (id, company_id, organization_id) VALUES 
    ('lcn11111-1111-1111-1111-111111111111', 'c1111111-1111-1111-1111-111111111111', 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'),
    ('lcn22222-2222-2222-2222-222222222222', 'c2222222-2222-2222-2222-222222222222', 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb'),
    ('lcn33333-3333-3333-3333-333333333333', 'c3333333-3333-3333-3333-333333333333', 'cccccccc-cccc-cccc-cccc-cccccccccccc'),
    ('lcn44444-4444-4444-4444-444444444444', 'c4444444-4444-4444-4444-444444444444', 'dddddddd-dddd-dddd-dddd-dddddddddddd'),
    ('lcn55555-5555-5555-5555-555555555555', 'c5555555-5555-5555-5555-555555555555', 'eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee');

-- Insert sample Ledger Entries (for audit trail)
INSERT INTO ledger_entries (id, ref_type, ref_id, hash, prev_hash) VALUES 
    ('le111111-1111-1111-1111-111111111111', 'Attendance', 'at111111-1111-1111-1111-111111111111', 'abc123def456', NULL),
    ('le222222-2222-2222-2222-222222222222', 'VoloCredit', 'vc111111-1111-1111-1111-111111111111', 'def456ghi789', 'abc123def456'),
    ('le333333-3333-3333-3333-333333333333', 'Allocation', 'al111111-1111-1111-1111-111111111111', 'ghi789jkl012', 'def456ghi789'),
    ('le444444-4444-4444-4444-444444444444', 'Attendance', 'at222222-2222-2222-2222-222222222222', 'jkl012mno345', 'ghi789jkl012'),
    ('le555555-5555-5555-5555-555555555555', 'VoloCredit', 'vc222222-2222-2222-2222-222222222222', 'mno345pqr678', 'jkl012mno345');

-- Insert sample Notifications
INSERT INTO notifications (id, volunteer_id, message, read) VALUES 
    ('n1111111-1111-1111-1111-111111111111', 'v1111111-1111-1111-1111-111111111111', 'Welcome to Volo! Your profile has been created successfully.', TRUE),
    ('n2222222-2222-2222-2222-222222222222', 'v1111111-1111-1111-1111-111111111111', 'Your attendance at Adult Literacy Program has been verified. You earned 48.50 credits!', TRUE),
    ('n3333333-3333-3333-3333-333333333333', 'v2222222-2222-2222-2222-222222222222', 'Thank you for your allocation! 25.00 credits have been allocated to Urban Tree Planting.', FALSE),
    ('n4444444-4444-4444-4444-444444444444', 'v3333333-3333-3333-3333-333333333333', 'New activity available: Emergency Food Distribution in your region!', FALSE),
    ('n5555555-5555-5555-5555-555555555555', 'v4444444-4444-4444-4444-444444444444', 'Reminder: Youth Mentorship activity starts in 2 hours.', FALSE);

-- Update profile statistics based on the sample data
UPDATE profiles SET 
    total_hours = (
        SELECT COALESCE(SUM(EXTRACT(EPOCH FROM (check_out_at - check_in_at))/3600), 0)
        FROM attendances 
        WHERE volunteer_id = profiles.volunteer_id 
        AND status = 'Verified'
        AND check_out_at IS NOT NULL
    ),
    total_credits_earned = (
        SELECT COALESCE(SUM(amount), 0)
        FROM volo_credits 
        WHERE volunteer_id = profiles.volunteer_id
    ),
    total_credits_allocated = (
        SELECT COALESCE(SUM(amount), 0)
        FROM allocations 
        WHERE volunteer_id = profiles.volunteer_id
    );

-- Create some indexes for better performance on sample queries
CREATE INDEX IF NOT EXISTS idx_sample_attendances_volunteer_verified 
ON attendances(volunteer_id) WHERE status = 'Verified';

CREATE INDEX IF NOT EXISTS idx_sample_activities_status_date 
ON activities(status, starts_at);

-- Insert some additional test scenarios

-- Volunteer with no activities yet
INSERT INTO volunteers (id, name, email, age, region_id) VALUES 
    ('vnew1111-1111-1111-1111-111111111111', 'New Volunteer', 'new.volunteer@email.com', 25, '11111111-1111-1111-1111-111111111111');

-- Expired credits scenario
INSERT INTO volo_credits (id, volunteer_id, source_attendance_id, amount, status, granted_at, expires_at) VALUES 
    ('vcexp111-1111-1111-1111-111111111111', 'v1111111-1111-1111-1111-111111111111', 'at111111-1111-1111-1111-111111111111', 10.00, 'Expired', '2023-12-01 15:00:00+00', '2024-12-01 15:00:00+00');

COMMIT;