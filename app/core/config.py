"""
This file contains the configuration settings for the application.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ Pydantic settings configuration for the MindForge application. """
    Project_Name: str = "MindForge"
    MONGO_URL: str = "mongodb://localhost:27017"
    DATABASE_NAME: str = "mindforge_db"
    
    class Config:
        """ Pydantic settings configuration """
        env_file = ".env"

settings = Settings()
