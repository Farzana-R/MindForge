"""
This file contains the configuration settings for the application.
"""
from pydantic import BaseSettings


class Settings(BaseSettings):
    Project_Name: str = "MindForge"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "mindforge_db"

    class Config:
        env_file = ".env"

settings = Settings()
