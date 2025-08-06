"""User model for managing user data in the database.
its a data layer (to interact with DB)
Handles DB insert/query logic using Motor"""
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
