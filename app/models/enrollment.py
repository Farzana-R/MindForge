"""
"""

from datetime import datetime, timezone

from fastapi import HTTPException

from app.core.database import db

collection = db["enrollments"]


class EnrollmentModel:
    """Model for enrollment operations."""

    collection = collection

    @classmethod
    async def enroll_user(cls, user_id: str, course_id: str):
        """Enroll a user in a course."""
        # check if the user is already enrolled in this course
        existing_enrollment = await cls.collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )
        if existing_enrollment:
            return {"message": "Already enrolled in this course"}

        enrollment_data = {
            "user_id": user_id,
            "course_id": course_id,
            "enrolled_at": datetime.now(timezone.utc).isoformat(),
        }

        result = await cls.collection.insert_one(enrollment_data)
        enrollment_data["_id"] = str(result.inserted_id)
        return enrollment_data

    # @classmethod
    # async def enroll_user(cls, enrollment_data: dict):
    #     """Enroll a user in a course."""
    #     enrollment_data["enrolled_at"] = datetime.utcnow().isoformat()
    #     result = await cls.collection.insert_one(enrollment_data)
    #     enrollment_data["_id"] = str(result.inserted_id)
    #     return enrollment_data

    # @classmethod
    # async def create_enrollment(cls, enrollment_data: dict):
    #     """Create a new enrollment in the database."""
    #     result = await cls.collection.insert_one(enrollment_data)
    #     enrollment_data["_id"] = str(result.inserted_id)
    #     return enrollment_data

    # @classmethod
    # async def get_enrollment_by_id(cls, enrollment_id: str):
    #     """Retrieve an enrollment by its ID."""
    #     try:
    #         obj_id = ObjectId(enrollment_id)  # Convert string to ObjectId
    #     except:
    #         return None  # Invalid ObjectId format
    #     enrollment = await cls.collection.find_one({"_id": obj_id})
    #     if enrollment:
    #         enrollment["id"] = str(enrollment["_id"])
    #     return enrollment

    @classmethod
    async def get_enrollments_by_user(cls, user_id: str):
        """Retrieve all enrollments for a specific user."""
        enrollments = []
        cursor = cls.collection.find({"user_id": user_id})
        async for enrollment in cursor:
            enrollment["_id"] = str(enrollment["_id"])
            enrollments.append(enrollment)
        return enrollments

    @classmethod
    async def get_enrollments(cls, user_id: str, course_id: str):
        """Retrieve enrollment for a specific user in a specific course."""

        enrollment = await cls.collection.find_one(
            {"user_id": user_id, "course_id": course_id}
        )

        if not enrollment:
            raise HTTPException(status_code=404, detail="Enrollment not found")
        else:
            enrollment["id"] = str(enrollment["_id"])
            enrollment["user_id"] = str(enrollment["user_id"])
            enrollment["course_id"] = str(enrollment["course_id"])
        return enrollment
