# Environment Variable Configuration

This document describes the environment variable centralization implemented in the Volo project.

## Overview

All sensitive and configurable values have been centralized into a `.env` file at the root of the project. This improves security, maintainability, and makes configuration management easier across different environments (development, staging, production).

## Files Created/Modified

### Created Files

1. **`.env`** - Contains all environment variables with default development values
   - **Note**: This file is gitignored and should not be committed to version control
   - Each developer/deployment should have their own `.env` file

2. **`.env.example`** - Template file showing all required environment variables
   - This file is committed to version control
   - Use this as a starting point: `cp .env.example .env`

3. **`backend/config.py`** - Configuration module using pydantic-settings
   - Loads all environment variables from `.env` file
   - Provides type-safe access to configuration values
   - Includes helper methods for complex configurations

4. **`scripts/test_env_config.py`** - Test script to validate configuration loading

### Modified Files

1. **`docker-compose.yml`**
   - Updated to read environment variables from `.env` file
   - All hardcoded values replaced with variable references
   - Uses `env_file` directive to load `.env` for each service

2. **`backend/database/connection.py`**
   - Updated to use the new `config` module
   - Removed hardcoded database URL fallback
   - Database echo setting now configurable via `DB_ECHO`

3. **`backend/main.py`**
   - Updated to use configuration for CORS origins
   - FastAPI server settings (host, port, reload) now configurable
   - Imported and uses the `settings` object from `config` module

## Environment Variables Reference

### Database Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `POSTGRES_DB` | PostgreSQL database name | `volo_db` |
| `POSTGRES_USER` | PostgreSQL username | `volo_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `volo_password` |
| `POSTGRES_HOST` | PostgreSQL host (for FastAPI) | `postgres` |
| `POSTGRES_PORT` | PostgreSQL port | `5432` |
| `PGDATA` | PostgreSQL data directory | `/var/lib/postgresql/data/pgdata` |
| `DATABASE_URL` | Full database connection URL | Constructed from above values |
| `DB_ECHO` | Enable SQLAlchemy query logging | `true` |

### PgAdmin Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `PGADMIN_DEFAULT_EMAIL` | PgAdmin login email | `admin@volo.com` |
| `PGADMIN_DEFAULT_PASSWORD` | PgAdmin login password | `admin123` |
| `PGADMIN_PORT` | PgAdmin external port | `5050` |

### Adminer Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `ADMINER_PORT` | Adminer external port | `8080` |

### FastAPI Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `FASTAPI_HOST` | FastAPI server host | `0.0.0.0` |
| `FASTAPI_PORT` | FastAPI server port | `8000` |
| `FASTAPI_RELOAD` | Enable auto-reload on code changes | `true` |

### CORS Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `CORS_ORIGINS` | Allowed CORS origins (comma-separated or `*`) | `*` |

### Python Configuration

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `PYTHONPATH` | Python module search path | `/app` |

## Usage

### Development Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your local configuration:
   ```bash
   nano .env  # or your preferred editor
   ```

3. Start the application:
   ```bash
   docker compose up -d
   ```

### Production Deployment

For production, ensure you:

1. Create a `.env` file with production values
2. Use strong, unique passwords
3. Restrict `CORS_ORIGINS` to your actual frontend domains
4. Set `DB_ECHO=false` to reduce logging
5. Set `FASTAPI_RELOAD=false` for better performance
6. Secure the `.env` file with appropriate permissions:
   ```bash
   chmod 600 .env
   ```

### Accessing Configuration in Code

```python
from config import settings

# Get database URL
db_url = settings.get_database_url()

# Get CORS origins as a list
cors_origins = settings.get_cors_origins_list()

# Access individual settings
port = settings.fastapi_port
db_echo = settings.db_echo
```

## Security Best Practices

1. **Never commit `.env` to version control** - It's already in `.gitignore`
2. **Always commit `.env.example`** - So others know what variables are needed
3. **Use strong passwords** - Especially for production environments
4. **Rotate credentials regularly** - Especially database and admin passwords
5. **Limit CORS origins** - In production, don't use `*`
6. **Secure the `.env` file** - Use proper file permissions (600 or 400)

## Testing

To validate the configuration is loaded correctly:

```bash
# Run the configuration test script
python3 scripts/test_env_config.py
```

## Troubleshooting

### Issue: Application can't connect to database

**Solution**: Check that `POSTGRES_HOST` is set to `postgres` (the Docker service name) when running in Docker, or `localhost` when running locally.

### Issue: CORS errors in browser

**Solution**: Update `CORS_ORIGINS` in `.env` to include your frontend URL:
```
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### Issue: Configuration not loading

**Solution**: Ensure the `.env` file exists in the project root and has the correct format (KEY=value, no spaces around =).

## Migration from Hardcoded Values

All previously hardcoded values have been successfully migrated:

- ✅ Database credentials (user, password, database name)
- ✅ Database connection URL
- ✅ PgAdmin credentials
- ✅ All service ports (PostgreSQL, FastAPI, Adminer, PgAdmin)
- ✅ CORS settings
- ✅ FastAPI server configuration
- ✅ Python path configuration
- ✅ Database logging settings

No hardcoded sensitive values remain in the codebase.
