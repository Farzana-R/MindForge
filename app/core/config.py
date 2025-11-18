"""
This file contains the configuration settings for the application.
"""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Pydantic settings configuration for the MindForge application."""

    Project_Name: str = "MindForge"
    MONGO_URL: str
    DATABASE_NAME: str = "mindforge_db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Add these lines:
    ADMIN_EMAIL: str | None = None
    ADMIN_PASSWORD: str | None = None
    USER_PASSWORD: str | None = None

    class Config:
        """Pydantic settings configuration"""

        env_file = ".env"


settings = Settings()
