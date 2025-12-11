# Volo - Volunteer Credit Allocation System

A comprehensive volunteer management system with credit allocation, built with PostgreSQL, Docker, and FastAPI.

## Overview

Volo is a volunteer engagement platform that tracks volunteer activities, grants credits for verified participation, and allows volunteers to allocate credits to projects they care about. The system implements a 50/50 allocation rule where volunteers must allocate 50% of their credits to the project they worked on (mandatory) and can freely allocate the remaining 50% to any project in their region.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   PostgreSQL    │    │   FastAPI       │    │   Frontend      │
│   Database      │◄───┤   Backend       │◄───┤   (Future)      │
│   (Docker)      │    │   (Docker)      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Features

### Core Functionality

- **Volunteer Management**: Registration, profiles, and regional organization
- **Activity Tracking**: Scheduled activities with capacity management
- **Attendance System**: QR check-in/check-out with verification by NGO representatives
- **Credit System**: Automatic credit calculation based on verified attendance hours
- **Smart Allocations**: Enforced 50/50 allocation rule (mandatory + free choice)
- **Impact Dashboard**: Real-time volunteer impact visualization
- **Audit Trail**: Immutable ledger for all critical operations

### Business Rules

1. **Credit Earning**: Credits are only granted for verified attendances with both check-in and check-out
2. **50/50 Allocation Rule**:
   - 50% must go to the project the volunteer worked on (MANDATORY_50)
   - 50% can be freely allocated to any project in the same region (FREE_CHOICE_50)
3. **Brand Integration**: Company branding shown during allocation process
4. **Regional Constraints**: Free choice allocations restricted to volunteer's region

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git (for cloning the repository)

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Volo

# Copy environment variables template
cp .env.example .env

# (Optional) Edit .env to customize configuration
nano .env

# Make sure Docker is running
docker --version
docker-compose --version
```

> **Note**: All configuration is managed through the `.env` file. See [ENV_CONFIG.md](ENV_CONFIG.md) for detailed documentation on all available environment variables.

### 2. Start the Services

```bash
# Start all services (database, API, and Adminer)
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Verify Setup

```bash
# Check database is ready
docker-compose logs postgres

# Check API is running
curl http://localhost:8000/health

# Access Adminer (Database GUI)
# Open: http://localhost:8080
# Login with credentials from .env file (default):
# - System: PostgreSQL
# - Server: postgres
# - Username: volo_user (from POSTGRES_USER)
# - Password: volo_password (from POSTGRES_PASSWORD)
# - Database: volo_db (from POSTGRES_DB)
```

### 4. Generate Additional Test Data (Optional)

```bash
# Install Python dependencies for data generator
pip install faker psycopg2-binary

# Run data generator
python scripts/generate_test_data.py
```

## Configuration

All application settings are managed through environment variables defined in the `.env` file at the project root.

### Environment Variables

The project uses a comprehensive set of environment variables for all configuration:

- **Database**: PostgreSQL connection settings (host, port, user, password, database name)
- **PgAdmin**: Admin interface credentials and port
- **Adminer**: Database management tool port
- **FastAPI**: Server host, port, and reload settings
- **CORS**: Allowed origins for cross-origin requests
- **Logging**: Database query logging settings

For a complete reference of all available environment variables and their usage, see [ENV_CONFIG.md](ENV_CONFIG.md).

### Quick Configuration Changes

To customize your setup:

1. Edit the `.env` file:
   ```bash
   nano .env
   ```

2. Modify the desired values (e.g., change ports, passwords)

3. Restart the services:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

### Security Notes

- The `.env` file is gitignored and should never be committed
- For production, use strong passwords and restrict CORS origins
- See [ENV_CONFIG.md](ENV_CONFIG.md) for security best practices

## API Documentation

### Base URL

```
http://localhost:8000
```

### Interactive API Docs

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Volunteers

- `POST /api/v1/volunteers/` - Create volunteer
- `GET /api/v1/volunteers/` - List volunteers (with pagination)
- `GET /api/v1/volunteers/{id}` - Get volunteer details
- `GET /api/v1/volunteers/{id}/dashboard` - Get volunteer impact dashboard
- `PUT /api/v1/volunteers/{id}` - Update volunteer
- `DELETE /api/v1/volunteers/{id}` - Delete volunteer

#### Activities

- `POST /api/v1/activities/` - Create activity
- `GET /api/v1/activities/` - List activities (with filters)
- `GET /api/v1/activities/{id}` - Get activity details
- `GET /api/v1/activities/{id}/summary` - Get activity summary with stats
- `PUT /api/v1/activities/{id}` - Update activity

#### Attendances

- `POST /api/v1/attendances/` - Create attendance record
- `GET /api/v1/attendances/` - List attendances (with filters)
- `POST /api/v1/attendances/{id}/check-in` - Volunteer check-in
- `POST /api/v1/attendances/{id}/check-out` - Volunteer check-out
- `POST /api/v1/attendances/{id}/verify` - Verify attendance (NGO action)

#### Allocations

- `POST /api/v1/allocations/` - Create allocation
- `GET /api/v1/allocations/` - List allocations
- `GET /api/v1/allocations/volunteer/{id}/summary` - Get allocation summary

## Database Schema

### Core Entities

#### Volunteers & Profiles

- **volunteers**: Basic volunteer information
- **profiles**: Computed statistics (hours, credits earned/allocated)
- **regions**: Geographic organization

#### Activities & Organizations

- **organizations**: NGOs and NBEs hosting projects
- **projects**: Volunteer opportunities hosted by organizations
- **activities**: Specific volunteer sessions with schedules
- **attendances**: Individual volunteer participation records

#### Credits & Allocations

- **volo_credits**: Credits earned from verified attendances
- **allocations**: Credit allocations to projects (50/50 rule)
- **credit_exchanges**: Many-to-many relationship between allocations and projects

#### Branding & Audit

- **companies**: Funding companies providing branding
- **brand_messages**: Marketing messages shown during allocation
- **ledger_entries**: Immutable audit trail
- **notifications**: User notifications

### Database Views

- **impact_dashboard**: Volunteer impact summary
- **activity_summary**: Activity participation statistics

## Sample API Usage

### 1. Create a Volunteer

```bash
curl -X POST "http://localhost:8000/api/v1/volunteers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane.doe@example.com",
    "age": 28,
    "region_id": "11111111-1111-1111-1111-111111111111"
  }'
```

### 2. Register for an Activity

```bash
curl -X POST "http://localhost:8000/api/v1/attendances/" \
  -H "Content-Type: application/json" \
  -d '{
    "volunteer_id": "{volunteer_id}",
    "activity_id": "{activity_id}"
  }'
```

### 3. Check-in to Activity

```bash
curl -X POST "http://localhost:8000/api/v1/attendances/{attendance_id}/check-in"
```

### 4. Check-out from Activity

```bash
curl -X POST "http://localhost:8000/api/v1/attendances/{attendance_id}/check-out"
```

### 5. Verify Attendance (NGO Action)

```bash
curl -X POST "http://localhost:8000/api/v1/attendances/{attendance_id}/verify" \
  -H "Content-Type: application/json" \
  -d '{
    "verified_by_user_id": "{ngo_user_id}"
  }'
```

### 6. View Volunteer Dashboard

```bash
curl "http://localhost:8000/api/v1/volunteers/{volunteer_id}/dashboard"
```

## SQL Commands for Direct Database Access

### Connect to Database

```bash
# Using Docker
docker-compose exec postgres psql -U volo_user -d volo_db

# Or using local psql
psql postgresql://volo_user:volo_password@localhost:5432/volo_db
```

### Useful Queries

#### View All Volunteers with Their Stats

```sql
SELECT * FROM impact_dashboard ORDER BY total_credits_earned DESC;
```

#### Check Activity Participation

```sql
SELECT * FROM activity_summary ORDER BY verified_attendances DESC;
```

#### Find Available Credits

```sql
SELECT v.name, vc.amount, vc.granted_at, vc.expires_at
FROM volo_credits vc
JOIN volunteers v ON vc.volunteer_id = v.id
WHERE vc.status = 'Available';
```

#### Allocation Summary by Project

```sql
SELECT p.name,
       COUNT(a.id) as total_allocations,
       SUM(a.amount) as total_amount
FROM projects p
JOIN allocations a ON p.id = a.project_id
GROUP BY p.id, p.name
ORDER BY total_amount DESC;
```

## Development

### Project Structure

```
Volo/
├── docker-compose.yml          # Docker orchestration
├── database/
│   └── init/                   # Database initialization scripts
│       ├── 01_schema.sql      # Schema definition
│       └── 02_sample_data.sql # Sample data
├── backend/
│   ├── Dockerfile             # FastAPI container
│   ├── requirements.txt       # Python dependencies
│   ├── main.py               # FastAPI application
│   ├── database/
│   │   ├── connection.py     # Database connection
│   │   └── models.py         # SQLAlchemy models
│   ├── schemas.py            # Pydantic schemas
│   └── routers/              # API route handlers
│       ├── volunteers.py
│       ├── activities.py
│       ├── attendances.py
│       └── allocations.py
├── scripts/
│   └── generate_test_data.py  # Random data generator
└── README.md                  # This file
```

### Running in Development Mode

#### Database Only

```bash
# Start only PostgreSQL and Adminer
docker-compose up postgres adminer
```

#### Local FastAPI Development

```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Set environment variables
export DATABASE_URL="postgresql://volo_user:volo_password@localhost:5432/volo_db"

# Run FastAPI with auto-reload
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing

#### Run Tests (When Available)

```bash
cd backend
pytest
```

#### Manual Testing with curl

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test volunteers endpoint
curl http://localhost:8000/api/v1/volunteers/
```

## Production Considerations

### Security

- [ ] Add authentication and authorization
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/TLS
- [ ] Implement rate limiting
- [ ] Add input validation and sanitization

### Performance

- [ ] Add database connection pooling
- [ ] Implement caching (Redis)
- [ ] Add database indexes for frequent queries
- [ ] Set up monitoring and logging

### Scalability

- [ ] Use managed database service
- [ ] Implement horizontal scaling
- [ ] Add load balancing
- [ ] Set up CI/CD pipeline

## Troubleshooting

### Common Issues

#### Database Connection Errors

```bash
# Check if PostgreSQL is running
docker-compose logs postgres

# Restart database service
docker-compose restart postgres
```

#### API Not Responding

```bash
# Check FastAPI logs
docker-compose logs fastapi

# Rebuild and restart API
docker-compose up --build fastapi
```

#### Port Conflicts

```bash
# Check what's running on ports
lsof -i :5432  # PostgreSQL
lsof -i :8000  # FastAPI
lsof -i :8080  # Adminer

# Stop conflicting services or change ports in docker-compose.yml
```

### Reset Everything

```bash
# Stop all services and remove volumes
docker-compose down -v

# Remove images (optional)
docker-compose down --rmi all

# Start fresh
docker-compose up -d
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests (when testing is set up)
5. Submit a pull request

## License

[Add your license information here]

## Support

For questions or support, please open an issue in the repository.
