"""User model for managing user data in the database.
its a data layer (to interact with DB)
Handles DB insert/query logic using Motor"""

from bson import ObjectId
from fastapi import HTTPException, status
from pymongo import ASCENDING

from app.core.database import db

COLLECTION_NAME = "users"


class UserModel:
    """User model for managing user data in the database.
    mongo DB collection reference"""

    collection = db[COLLECTION_NAME]

    @classmethod
    async def create(cls, user_data: dict) -> dict:
        """Create a new user in the database.
        Adds _id (MongoDB ObjectId) to the user_data and returns it"""
        result = await cls.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    @classmethod
    async def get_by_email(cls, email: str) -> dict | None:
        """Retrieve a user by email.
        Converts Mongo's _id to string so it’s JSON serializable"""
        user = await cls.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user

    @classmethod
    async def get_by_id(cls, user_id: str) -> dict | None:
        """Retrieve a user by ID."""
        if not ObjectId.is_valid(user_id):
            return None
        user = await cls.collection.find_one({"_id": ObjectId(user_id)})
        return cls._format_user(user)

    @classmethod
    async def list_users(
        cls, query: dict, limit: int = 10, page: int = 1
    ) -> list[dict]:
        """List users with pagination and filtering."""
        skip = (page - 1) * limit
        cursor = (
            cls.collection.find(query)
            .sort("created_at", ASCENDING)
            .skip(skip)
            .limit(limit)
        )
        users = []
        async for user in cursor:
            users.append(cls._format_user(user))
        return users

    @classmethod
    async def count_users(cls, query: dict) -> int:
        """Count users matching the query."""
        return await cls.collection.count_documents(query)

    @classmethod
    async def update_user(cls, user_id: str, update_data: dict) -> dict | None:
        """Update user data by ID."""
        if not ObjectId.is_valid(user_id):
            return None
        result = await cls.collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": update_data}
        )
        if result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found or no changes made",
            )
            # return None
        return await cls.get_by_id(user_id)

    @classmethod
    async def delete_user(cls, user_id: str) -> bool:
        """Delete a user by ID."""
        if not ObjectId.is_valid(user_id):
            return False
        result = await cls.collection.delete_one({"_id": ObjectId(user_id)})
        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        return result.deleted_count > 0

    @staticmethod
    def _format_user(user: dict | None) -> dict | None:
        """convert Mongo user document to JSON serializable dict"""
        if not user:
            return None
        user["id"] = str(user["_id"])  # Convert ObjectId to string
        user.pop("password", None)  # Remove password if it exists
        return user
