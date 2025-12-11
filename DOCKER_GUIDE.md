# Docker Quick Reference Guide

This guide provides quick commands for working with the Volo project entirely in Docker.

## Starting the Project

```bash
# Start all services in the background
docker compose up -d

# Start all services and view logs
docker compose up

# Check service status
docker compose ps

# View logs from all services
docker compose logs

# View logs from a specific service
docker compose logs fastapi
docker compose logs postgres

# Follow logs in real-time
docker compose logs -f
docker compose logs -f fastapi
```

## Running Tests and Scripts

```bash
# Run basic API tests
docker compose exec scripts python test_basic_api.py

# Run full architecture tests
docker compose exec scripts python test_architecture.py

# Access the scripts container shell
docker compose exec scripts bash

# Inside the scripts container, you can run:
# - python test_basic_api.py
# - python test_architecture.py
# - Any other Python scripts
```

## Database Operations

```bash
# Connect to PostgreSQL
docker compose exec postgres psql -U volo_user -d volo_db

# Run a SQL query from the command line
docker compose exec postgres psql -U volo_user -d volo_db -c "SELECT COUNT(*) FROM volunteers;"

# Access database via Adminer web UI
# Open browser: http://localhost:8080
# Server: postgres, User: volo_user, Password: volo_password, Database: volo_db

# Access database via PgAdmin web UI
# Open browser: http://localhost:5050
# Email: admin@volo.com, Password: admin123
```

## Backend Development

```bash
# View backend logs
docker compose logs -f fastapi

# Restart backend (e.g., after config changes)
docker compose restart fastapi

# Access backend container shell
docker compose exec fastapi bash

# Inside the backend container, you can:
# - Run pytest (when tests are available)
# - Run python commands
# - Check installed packages: pip list
```

## Rebuilding Services

```bash
# Rebuild all services (after Dockerfile changes)
docker compose up --build

# Rebuild a specific service
docker compose up --build fastapi
docker compose up --build scripts

# Rebuild and start in detached mode
docker compose up -d --build
```

## Stopping and Cleaning Up

```bash
# Stop all services (keep volumes)
docker compose down

# Stop all services and remove volumes (WARNING: deletes data)
docker compose down -v

# Stop all services, remove volumes and images
docker compose down -v --rmi all

# Stop a specific service
docker compose stop fastapi
docker compose stop scripts

# Remove stopped containers
docker compose rm
```

## Troubleshooting

### Port Already in Use

If you get a port conflict error:

```bash
# Check what's using the ports
lsof -i :5432  # PostgreSQL
lsof -i :8000  # FastAPI
lsof -i :8080  # Adminer
lsof -i :5050  # PgAdmin

# Either stop the conflicting service or edit docker-compose.yml to use different ports
```

### Container Won't Start

```bash
# Check logs for errors
docker compose logs <service-name>

# Try rebuilding
docker compose up --build <service-name>

# Check if image built successfully
docker images | grep volo
```

### Database Connection Issues

```bash
# Check if PostgreSQL is healthy
docker compose ps
docker compose logs postgres

# Restart PostgreSQL
docker compose restart postgres

# Wait for PostgreSQL to be ready
docker compose exec postgres pg_isready -U volo_user
```

### Code Changes Not Reflecting

For the backend, hot reload is enabled via volume mounts. If changes aren't reflecting:

```bash
# Check if volume mount is working
docker compose exec fastapi ls -la /app

# Restart the service
docker compose restart fastapi
```

## Development Workflow

### Typical Development Session

```bash
# 1. Start all services
docker compose up -d

# 2. Check everything is running
docker compose ps
curl http://localhost:8000/health

# 3. Make code changes in your editor
# Changes to backend code are automatically reloaded

# 4. Run tests to verify changes
docker compose exec scripts python test_basic_api.py

# 5. View logs if needed
docker compose logs -f fastapi

# 6. When done, stop services
docker compose down
```

### Testing Changes

```bash
# 1. Make code changes

# 2. If Dockerfile changed, rebuild
docker compose up -d --build

# 3. Run tests
docker compose exec scripts python test_basic_api.py

# 4. Check API
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/volunteers/

# 5. Check database
docker compose exec postgres psql -U volo_user -d volo_db -c "SELECT COUNT(*) FROM volunteers;"
```

## Useful One-Liners

```bash
# Quick reset (stop, clean, start fresh)
docker compose down -v && docker compose up -d

# View all container resource usage
docker stats

# Clean up unused Docker resources
docker system prune -a

# Get into a bash shell in any container
docker compose exec <service-name> bash

# Run a one-off command in a service
docker compose run --rm scripts python test_basic_api.py
```

## Production Considerations

### SSL Certificate Handling

The current Dockerfiles use `--trusted-host` flags to handle SSL certificate issues in development environments. For production:

1. **Remove the trusted-host flags** from Dockerfiles
2. **Configure proper SSL certificates** in your build environment
3. **Use a private PyPI mirror** if working in a corporate network
4. **Add corporate certificate bundle** to the Docker image if needed

Example production Dockerfile (backend):
```dockerfile
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Production: Use standard pip install without --trusted-host
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-stage Builds

For smaller production images, consider multi-stage builds:

```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Environment Variables

The project uses environment variables defined in `docker-compose.yml`. To customize:

1. Copy `.env.example` to `.env`
2. Edit `.env` with your values
3. Restart services: `docker compose down && docker compose up -d`

## Next Steps

- Explore the API documentation at http://localhost:8000/docs
- Check out database schemas via Adminer at http://localhost:8080
- Run the architecture tests to validate the system
- Make code changes and see them automatically reload

## Getting Help

- View README.md for detailed project documentation
- Check docker-compose.yml for service configurations
- View Dockerfile in backend/ and scripts/ for build details
