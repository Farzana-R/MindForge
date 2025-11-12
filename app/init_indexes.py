"""
It creates necessary indexes on the users collection,
to ensure efficient querying.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, TEXT


MONGO_URL = "mongodb://mongo:27017"
DB_NAME = "mindforge_db"


async def create_indexes():
    """
    Create necessary indexes for the MongoDB collections.
    This function is called during the application startup.
    """
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]

    print("Creating indexes...")

    # ------- Indexes for users collection -------

    # Create unique index on email field in users collection
    await db["users"].create_index([("email", ASCENDING)], unique=True)
    # Create single field index on role field in users collection
    await db["users"].create_index([("role", ASCENDING)])
    # Create compound index on first_name and last_name fields in users collection
    await db["users"].create_index([("first_name", 1), ("last_name", 1)])
    # Create text index on address field in users collection for full-text search
    await db["users"].create_index([("address", "text")])

    # ------- Indexes for courses collection -------
    await db["courses"].create_index([("title", "text"), ("description", "text"), ("category", "text")])
    await db["courses"].create_index([("instructor", ASCENDING)])
    await db["courses"].create_index([("created_at", ASCENDING)])
    await db["courses"].create_index([("category", ASCENDING)])

    print("Indexes created successfully.")

    client.close()

if __name__ == "__main__":
    asyncio.run(create_indexes())
