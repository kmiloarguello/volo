"""
Configuration module for the Volo application.
Loads all environment variables using pydantic-settings.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    postgres_db: str = "volo_db"
    postgres_user: str = "volo_user"
    postgres_password: str = "volo_password"
    postgres_host: str = "postgres"  # 'postgres' for Docker, 'localhost' for local dev
    postgres_port: int = 5432
    
    # Database URL (can be set directly or constructed from parts)
    database_url: Optional[str] = None
    
    # Database Connection Settings
    db_echo: bool = False
    
    # FastAPI Configuration
    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_reload: bool = True
    
    # CORS Configuration
    cors_origins: str = "*"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    def get_database_url(self) -> str:
        """
        Get the database URL. If DATABASE_URL is set, use it.
        Otherwise, construct it from individual components.
        """
        if self.database_url:
            return self.database_url
        
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )
    
    def get_cors_origins_list(self) -> List[str]:
        """
        Convert CORS_ORIGINS string to a list.
        Supports comma-separated values or "*" for all origins.
        """
        if self.cors_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.cors_origins.split(",")]


# Create a global settings instance
settings = Settings()
