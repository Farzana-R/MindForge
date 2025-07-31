"""User model for managing user data in the database."""
from app.core.database import db


COLLECTION_NAME = "users"


class UserModel:
    """User model for managing user data in the database."""
    collection = db[COLLECTION_NAME]

    @classmethod
    async def create(cls, user_data: dict) -> dict:
        """Create a new user in the database."""
        result = await cls.collection.insert_one(user_data)
        user_data["_id"] = str(result.inserted_id)
        return user_data

    @classmethod
    async def get_by_email(cls, email: str) -> dict | None:
        """Retrieve a user by email."""
        user = await cls.collection.find_one({"email": email})
        if user:
            user["_id"] = str(user["_id"])
        return user
