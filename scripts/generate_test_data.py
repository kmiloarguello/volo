#!/usr/bin/env python3
"""
Random data generator for Volo database
This script generates additional test data for the Volo volunteer system
"""

import os
import sys
import random
from datetime import datetime, timedelta
from decimal import Decimal
from faker import Faker
import uuid
import psycopg2
from psycopg2.extras import RealDictCursor

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'volo_db'),
    'user': os.getenv('DB_USER', 'volo_user'),
    'password': os.getenv('DB_PASSWORD', 'volo_password')
}

fake = Faker()
Faker.seed(42)  # For reproducible data
random.seed(42)

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        sys.exit(1)

def generate_regions(conn, count=10):
    """Generate additional regions"""
    print(f"Generating {count} regions...")
    
    regions = []
    region_names = [
        "Northern California", "Southern California", "Texas Gulf", "New York Metro",
        "Florida Keys", "Pacific Northwest", "Great Lakes", "Rocky Mountains",
        "New England", "Mid-Atlantic", "Southeast", "Southwest", "Midwest Plains",
        "Alaska Frontier", "Hawaiian Islands"
    ]
    
    with conn.cursor() as cur:
        for i in range(count):
            region_id = str(uuid.uuid4())
            name = random.choice(region_names) + f" #{i+1}" if i >= len(region_names) else region_names[i]
            
            cur.execute("""
                INSERT INTO regions (id, name) 
                VALUES (%s, %s) 
                ON CONFLICT (name) DO NOTHING
                RETURNING id
            """, (region_id, name))
            
            result = cur.fetchone()
            if result:
                regions.append(region_id)
                print(f"  Created region: {name}")
    
    conn.commit()
    return regions

def generate_organizations(conn, count=15):
    """Generate additional organizations"""
    print(f"Generating {count} organizations...")
    
    organizations = []
    org_names = [
        "Community Action Network", "Future Leaders Foundation", "Health Access Alliance",
        "Environmental Stewards", "Education Equity Initiative", "Senior Support Services",
        "Youth Empowerment Center", "Disability Rights Coalition", "Food Security Alliance",
        "Housing Justice Collective", "Mental Health Advocates", "Arts for Change",
        "Technology for Good", "Climate Action Group", "Social Justice Network"
    ]
    
    org_types = ["NGO", "NBE"]
    
    with conn.cursor() as cur:
        for i in range(count):
            org_id = str(uuid.uuid4())
            name = org_names[i] if i < len(org_names) else fake.company() + " Foundation"
            org_type = random.choice(org_types)
            
            cur.execute("""
                INSERT INTO organizations (id, type, name) 
                VALUES (%s, %s, %s)
                RETURNING id
            """, (org_id, org_type, name))
            
            organizations.append(org_id)
            print(f"  Created {org_type}: {name}")
    
    conn.commit()
    return organizations

def generate_companies(conn, count=10):
    """Generate additional companies"""
    print(f"Generating {count} companies...")
    
    companies = []
    company_types = ["Tech", "Finance", "Healthcare", "Energy", "Retail", "Manufacturing", "Consulting"]
    
    with conn.cursor() as cur:
        for i in range(count):
            company_id = str(uuid.uuid4())
            company_type = random.choice(company_types)
            name = f"{fake.company()} {company_type}"
            
            cur.execute("""
                INSERT INTO companies (id, name) 
                VALUES (%s, %s)
                RETURNING id
            """, (company_id, name))
            
            companies.append(company_id)
            print(f"  Created company: {name}")
    
    conn.commit()
    return companies

def get_existing_regions(conn):
    """Get existing region IDs"""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM regions")
        return [row[0] for row in cur.fetchall()]

def generate_volunteers(conn, region_ids, count=50):
    """Generate additional volunteers"""
    print(f"Generating {count} volunteers...")
    
    volunteers = []
    
    with conn.cursor() as cur:
        for i in range(count):
            volunteer_id = str(uuid.uuid4())
            name = fake.name()
            email = fake.unique.email()
            age = random.randint(18, 65)
            region_id = random.choice(region_ids)
            
            try:
                cur.execute("""
                    INSERT INTO volunteers (id, name, email, age, region_id) 
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (volunteer_id, name, email, age, region_id))
                
                volunteers.append(volunteer_id)
                if i % 10 == 0:
                    print(f"  Created {i+1} volunteers...")
                    
            except psycopg2.IntegrityError as e:
                conn.rollback()
                print(f"  Skipped duplicate email: {email}")
                continue
    
    conn.commit()
    print(f"  Successfully created {len(volunteers)} volunteers")
    return volunteers

def get_existing_organizations(conn):
    """Get existing organization IDs"""
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM organizations")
        return [row[0] for row in cur.fetchall()]

def generate_projects(conn, org_ids, region_ids, count=25):
    """Generate additional projects"""
    print(f"Generating {count} projects...")
    
    projects = []
    project_themes = [
        "Environmental Conservation", "Education Support", "Healthcare Access", 
        "Community Development", "Food Security", "Youth Programs", "Senior Care",
        "Disability Services", "Mental Health", "Arts & Culture", "Technology Training",
        "Housing Assistance", "Emergency Relief", "Economic Development"
    ]
    
    with conn.cursor() as cur:
        for i in range(count):
            project_id = str(uuid.uuid4())
            theme = random.choice(project_themes)
            name = f"{theme} - {fake.city()} Initiative"
            description = fake.paragraph(nb_sentences=3)
            ngo_id = random.choice(org_ids)
            region_id = random.choice(region_ids)
            
            cur.execute("""
                INSERT INTO projects (id, ngo_id, region_id, name, description) 
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (project_id, ngo_id, region_id, name, description))
            
            projects.append(project_id)
            if i % 5 == 0:
                print(f"  Created {i+1} projects...")
    
    conn.commit()
    print(f"  Successfully created {len(projects)} projects")
    return projects

def generate_activities(conn, project_ids, count=100):
    """Generate activities for projects"""
    print(f"Generating {count} activities...")
    
    activities = []
    activity_types = [
        "Community Cleanup", "Food Drive", "Educational Workshop", "Health Screening",
        "Tree Planting", "Senior Visit", "Youth Mentoring", "Fundraising Event",
        "Awareness Campaign", "Volunteer Training", "Emergency Response", "Art Workshop"
    ]
    
    statuses = ["Scheduled", "Completed", "Cancelled"]
    status_weights = [0.6, 0.35, 0.05]  # Most scheduled, some completed, few cancelled
    
    with conn.cursor() as cur:
        for i in range(count):
            activity_id = str(uuid.uuid4())
            project_id = random.choice(project_ids)
            activity_type = random.choice(activity_types)
            
            # Generate realistic dates
            base_date = datetime.now()
            days_offset = random.randint(-30, 60)  # Activities from 30 days ago to 60 days ahead
            starts_at = base_date + timedelta(days=days_offset, hours=random.randint(8, 18))
            ends_at = starts_at + timedelta(hours=random.randint(2, 8))
            
            location = f"{fake.street_address()}, {fake.city()}"
            capacity = random.randint(5, 50)
            status = random.choices(statuses, weights=status_weights)[0]
            
            # If activity is in the past, it should be completed or cancelled
            if starts_at < datetime.now():
                status = random.choices(["Completed", "Cancelled"], weights=[0.9, 0.1])[0]
            
            cur.execute("""
                INSERT INTO activities (id, project_id, starts_at, ends_at, location, capacity, status) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (activity_id, project_id, starts_at, ends_at, location, capacity, status))
            
            activities.append({
                'id': activity_id,
                'project_id': project_id,
                'starts_at': starts_at,
                'ends_at': ends_at,
                'status': status,
                'capacity': capacity
            })
            
            if i % 20 == 0:
                print(f"  Created {i+1} activities...")
    
    conn.commit()
    print(f"  Successfully created {len(activities)} activities")
    return activities

def generate_attendances(conn, volunteer_ids, activities, attendance_rate=0.3):
    """Generate attendances for activities"""
    print(f"Generating attendances with {attendance_rate*100}% participation rate...")
    
    attendances = []
    attendance_statuses = ["Pending", "Verified", "Rejected"]
    status_weights = [0.1, 0.85, 0.05]  # Most verified, few pending/rejected
    
    with conn.cursor() as cur:
        for activity in activities:
            # Determine how many volunteers attend this activity
            max_attendees = min(activity['capacity'], len(volunteer_ids))
            num_attendees = random.randint(1, int(max_attendees * attendance_rate * 2))
            
            # Select random volunteers for this activity
            activity_volunteers = random.sample(volunteer_ids, min(num_attendees, len(volunteer_ids)))
            
            for volunteer_id in activity_volunteers:
                attendance_id = str(uuid.uuid4())
                
                # Generate check-in/check-out times based on activity times
                if activity['status'] == 'Completed':
                    check_in_offset = timedelta(minutes=random.randint(-10, 30))
                    check_out_offset = timedelta(minutes=random.randint(-30, 15))
                    check_in_at = activity['starts_at'] + check_in_offset
                    check_out_at = activity['ends_at'] + check_out_offset
                    status = random.choices(attendance_statuses, weights=status_weights)[0]
                else:
                    # Future or cancelled activities
                    check_in_at = None
                    check_out_at = None
                    status = "Pending"
                
                try:
                    cur.execute("""
                        INSERT INTO attendances (id, volunteer_id, activity_id, check_in_at, check_out_at, status) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (attendance_id, volunteer_id, activity['id'], check_in_at, check_out_at, status))
                    
                    attendances.append({
                        'id': attendance_id,
                        'volunteer_id': volunteer_id,
                        'activity_id': activity['id'],
                        'status': status,
                        'check_in_at': check_in_at,
                        'check_out_at': check_out_at
                    })
                    
                except psycopg2.IntegrityError:
                    # Skip duplicates
                    conn.rollback()
                    continue
    
    conn.commit()
    print(f"  Successfully created {len(attendances)} attendances")
    return attendances

def generate_credits_and_allocations(conn, attendances, project_ids, company_ids):
    """Generate volo credits and allocations for verified attendances"""
    print("Generating volo credits and allocations...")
    
    verified_attendances = [att for att in attendances if att['status'] == 'Verified' and att['check_in_at'] and att['check_out_at']]
    
    with conn.cursor() as cur:
        for attendance in verified_attendances:
            # Calculate hours worked
            if attendance['check_in_at'] and attendance['check_out_at']:
                duration = attendance['check_out_at'] - attendance['check_in_at']
                hours = duration.total_seconds() / 3600
                
                # Credit rate: $10-15 per hour
                credit_rate = Decimal(str(random.uniform(10, 15)))
                credit_amount = Decimal(str(hours)) * credit_rate
                credit_amount = credit_amount.quantize(Decimal('0.01'))  # Round to 2 decimal places
                
                # Create volo credit
                credit_id = str(uuid.uuid4())
                expires_at = datetime.now() + timedelta(days=365)
                
                cur.execute("""
                    INSERT INTO volo_credits (id, volunteer_id, source_attendance_id, amount, status, expires_at) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (credit_id, attendance['volunteer_id'], attendance['id'], credit_amount, 'Available', expires_at))
                
                # Create allocations (50/50 rule)
                mandatory_amount = credit_amount / 2
                free_choice_amount = credit_amount / 2
                
                # Mandatory 50% to the attended project's project
                with conn.cursor() as cur2:
                    cur2.execute("SELECT project_id FROM activities WHERE id = %s", (attendance['activity_id'],))
                    attended_project_id = cur2.fetchone()[0]
                
                # Mandatory allocation
                allocation1_id = str(uuid.uuid4())
                company_id = random.choice(company_ids) if company_ids else None
                
                cur.execute("""
                    INSERT INTO allocations (id, volunteer_id, project_id, company_id, source_credit_id, amount, kind) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (allocation1_id, attendance['volunteer_id'], attended_project_id, company_id, credit_id, mandatory_amount, 'MANDATORY_50'))
                
                # Free choice allocation to any project in the same region
                with conn.cursor() as cur3:
                    cur3.execute("""
                        SELECT p.id FROM projects p 
                        JOIN activities a ON p.id = a.project_id 
                        WHERE a.id = %s
                    """, (attendance['activity_id'],))
                    result = cur3.fetchone()
                    if result:
                        cur3.execute("""
                            SELECT id FROM projects WHERE region_id = (
                                SELECT region_id FROM projects WHERE id = %s
                            ) ORDER BY RANDOM() LIMIT 1
                        """, (result[0],))
                        free_choice_project = cur3.fetchone()
                        if free_choice_project:
                            allocation2_id = str(uuid.uuid4())
                            company_id2 = random.choice(company_ids) if company_ids else None
                            
                            cur.execute("""
                                INSERT INTO allocations (id, volunteer_id, project_id, company_id, source_credit_id, amount, kind) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)
                            """, (allocation2_id, attendance['volunteer_id'], free_choice_project[0], company_id2, credit_id, free_choice_amount, 'FREE_CHOICE_50'))
                
                # Update credit status to allocated
                cur.execute("UPDATE volo_credits SET status = %s WHERE id = %s", ('Allocated', credit_id))
    
    conn.commit()
    print(f"  Generated credits and allocations for {len(verified_attendances)} verified attendances")

def update_volunteer_profiles(conn):
    """Update volunteer profiles with computed statistics"""
    print("Updating volunteer profiles...")
    
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE profiles SET 
                total_hours = COALESCE((
                    SELECT SUM(EXTRACT(EPOCH FROM (check_out_at - check_in_at))/3600)
                    FROM attendances 
                    WHERE volunteer_id = profiles.volunteer_id 
                    AND status = 'Verified'
                    AND check_out_at IS NOT NULL
                ), 0),
                total_credits_earned = COALESCE((
                    SELECT SUM(amount)
                    FROM volo_credits 
                    WHERE volunteer_id = profiles.volunteer_id
                ), 0),
                total_credits_allocated = COALESCE((
                    SELECT SUM(amount)
                    FROM allocations 
                    WHERE volunteer_id = profiles.volunteer_id
                ), 0)
        """)
    
    conn.commit()
    print("  Updated all volunteer profiles")

def generate_notifications(conn, volunteer_ids, count=200):
    """Generate notifications for volunteers"""
    print(f"Generating {count} notifications...")
    
    notification_templates = [
        "Welcome to Volo! Your volunteer journey begins now.",
        "New activity available in your region: {activity}",
        "Your attendance has been verified. You earned {credits} credits!",
        "Thank you for your allocation to {project}!",
        "Reminder: {activity} starts in 2 hours.",
        "Your volunteer profile has been updated.",
        "New project launched: {project}. Sign up today!",
        "Credits expiring soon. Make sure to allocate them.",
        "Monthly volunteer impact report is now available.",
        "Community appreciation: Thank you for your service!"
    ]
    
    with conn.cursor() as cur:
        for i in range(count):
            notification_id = str(uuid.uuid4())
            volunteer_id = random.choice(volunteer_ids)
            template = random.choice(notification_templates)
            
            # Customize message with fake data
            message = template.format(
                activity=fake.catch_phrase(),
                credits=f"{random.randint(10, 100):.2f}",
                project=fake.bs().title()
            )
            
            read_status = random.choices([True, False], weights=[0.7, 0.3])[0]  # 70% read
            created_at = fake.date_time_between(start_date='-30d', end_date='now')
            
            cur.execute("""
                INSERT INTO notifications (id, volunteer_id, message, read, created_at) 
                VALUES (%s, %s, %s, %s, %s)
            """, (notification_id, volunteer_id, message, read_status, created_at))
    
    conn.commit()
    print(f"  Generated {count} notifications")

def main():
    """Main function to generate all test data"""
    print("Starting Volo database population...")
    print("=" * 50)
    
    conn = get_db_connection()
    
    try:
        # Generate base data
        new_regions = generate_regions(conn, 5)
        new_organizations = generate_organizations(conn, 10)
        new_companies = generate_companies(conn, 8)
        
        # Get all existing data
        region_ids = get_existing_regions(conn)
        org_ids = get_existing_organizations(conn)
        
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM companies")
            company_ids = [row[0] for row in cur.fetchall()]
        
        # Generate volunteers and their activities
        volunteer_ids = generate_volunteers(conn, region_ids, 50)
        project_ids = generate_projects(conn, org_ids, region_ids, 30)
        activities = generate_activities(conn, project_ids, 150)
        attendances = generate_attendances(conn, volunteer_ids, activities, attendance_rate=0.4)
        
        # Generate credits and allocations
        generate_credits_and_allocations(conn, attendances, project_ids, company_ids)
        
        # Update computed fields
        update_volunteer_profiles(conn)
        
        # Generate notifications
        all_volunteer_ids = volunteer_ids.copy()
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM volunteers")
            existing_volunteers = [row[0] for row in cur.fetchall()]
            all_volunteer_ids.extend([v for v in existing_volunteers if v not in all_volunteer_ids])
        
        generate_notifications(conn, all_volunteer_ids, 300)
        
        print("=" * 50)
        print("✅ Database population completed successfully!")
        print(f"📊 Summary:")
        print(f"   - Regions: {len(region_ids)} total")
        print(f"   - Organizations: {len(org_ids)} total") 
        print(f"   - Companies: {len(company_ids)} total")
        print(f"   - Volunteers: {len(all_volunteer_ids)} total")
        print(f"   - Projects: {len(project_ids)} total")
        print(f"   - Activities: {len(activities)} total")
        print(f"   - Attendances: {len(attendances)} total")
        
    except Exception as e:
        print(f"❌ Error during data generation: {e}")
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()