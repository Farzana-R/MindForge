from datetime import datetime, timezone

from app.core.database import db

collection = db["progress"]


class ProgressModel:
    collection = collection

    @classmethod
    async def update_progress(cls, user_id: str, course_id: str, progress: dict):
        """Update or create a user's progress in a course"""
        if progress < 0 or progress > 100:
            raise ValueError("progress must be between 0 and 100")
        existing_progress = await cls.collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )
        if existing_progress:
            # Update existing progress
            updated_data = {
                "progress": progress,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            await cls.collection.update_one(
                {"_id": existing_progress["_id"]}, {"$set": updated_data}
            )
            existing_progress.update(updated_data)
            existing_progress["id"] = str(existing_progress["_id"])
            return existing_progress
        else:
            # Create new progress entry
            progress_data = {
                "user_id": user_id,
                "course_id": course_id,
                "progress": progress,
                "is_completed": progress == 100,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            result = await cls.collection.insert_one(progress_data)
            progress_data["_id"] = str(result.inserted_id)
            return progress_data

    @classmethod
    async def get_progress(cls, user_id: str, course_id: str):
        """Retrieve a user's progress in a course"""
        progress = await cls.collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )
        if progress:
            progress["id"] = str(progress["_id"])
        return progress
