"""Database connection setup for MongoDB using Motor"""
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings


client = AsyncIOMotorClient(settings.MONGO_URL)

db = client[settings.DATABASE_NAME]

courses_collection = db["courses"]
