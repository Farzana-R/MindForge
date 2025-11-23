"""
defines the CourseModel class for performing CRUD operations on courses
in a MongoDB database.
"""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId, errors
from bson.errors import InvalidId
from fastapi import HTTPException

from app.core.database import courses_collection, db

collection = db["courses"]


class CourseModel:
    """Model for course operations."""

    collection = courses_collection

    @classmethod
    async def create_course(cls, course_data: dict):
        """Create a new course in the database."""
        result = await cls.collection.insert_one(course_data)
        course_data["_id"] = str(result.inserted_id)
        return course_data

    @classmethod
    async def get_course_by_id(cls, course_id: str):
        """Retrieve a course by its ID."""
        try:
            obj_id = ObjectId(course_id)  # Convert string to ObjectId
        except InvalidId:
            return None  # Invalid ObjectId format
        course = await cls.collection.find_one({"_id": obj_id})
        if course:
            course["id"] = str(course["_id"])
        return course

    @classmethod
    async def get_all_courses(
        cls,
        skip: int = 0,
        limit: int = 10,
        category: Optional[str] = None,
        instructor: Optional[str] = None,
        search: Optional[str] = None,
        sort_by: Optional[str] = "created_at",
        sort_order: Optional[int] = -1,
    ):
        """Retrieve all courses with pagination, filtering, searching, and sorting."""
        query: dict = {}
        # ----------filtering-----------
        if category:
            query["category"] = category
        if instructor:
            query["instructor"] = instructor
        # ----------searching-----------
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"description": {"$regex": search, "$options": "i"}},
            ]
        # ----------sorting-----------
        valid_sort_fields = ["title", "created_at", "updated_at"]
        if sort_by not in valid_sort_fields:
            valid_fields = ", ".join(valid_sort_fields)
            raise HTTPException(
                status_code=400,
                detail=f"Invalid sort field. Valid fields are: {valid_fields}",
            )

        courses = []
        cursor = (
            cls.collection.find(query).sort(sort_by, sort_order).skip(skip).limit(limit)
        )
        async for course in cursor:
            course["_id"] = str(course["_id"])
            # courses.append(course)
            courses.append(
                {
                    "id": course["_id"],
                    "title": course["title"],
                    "description": course["description"],
                    "category": course.get("category"),
                    "instructor": course["instructor"],
                    "duration": course.get("duration"),
                    "created_at": course.get("created_at"),
                    "updated_at": course.get("updated_at"),
                }
            )
        total = await cls.collection.count_documents(query)
        return {"total": total, "data": courses}

    @classmethod
    async def update_course(cls, course_id: str, course_data: dict):
        """Update an existing course."""
        try:
            obj_id = ObjectId(course_id)
        except errors.InvalidId:
            return None  # Invalid ObjectId format
        # course_data["_id"] = obj_id
        course_data["updated_at"] = course_data.get(
            "updated_at", datetime.now(timezone.utc).isoformat()
        )
        # result = await cls.collection.replace_one({"_id": obj_id}, course_data)
        result = await cls.collection.update_one(
            {"_id": obj_id}, {"$set": course_data}  # Use $set to update fields
        )
        if result.modified_count == 0:
            return None
        updated_course = await cls.collection.find_one({"_id": obj_id})
        if updated_course:
            updated_course["_id"] = str(updated_course["_id"])
            # Convert ObjectId to string for JSON serialization
            return updated_course
        # course_data["id"] = str(obj_id)
        # return course_data

    @classmethod
    async def get_courses_by_instructor(cls, instructor_email: str):
        """Retrieve courses by instructor's email."""
        courses = []
        async for course in cls.collection.find({"instructor": instructor_email}):
            course["_id"] = str(course["_id"])
            courses.append(
                {
                    "id": course["_id"],
                    "title": course["title"],
                    "description": course["description"],
                    "category": course.get("category"),
                    "instructor": course["instructor"],
                    "duration": course.get("duration"),
                    "created_at": course.get("created_at"),
                    "updated_at": course.get("updated_at"),
                }
            )
        return courses

    @classmethod
    async def get_courses_by_category(cls, category: str):
        """Retrieve courses by category."""
        courses = []
        async for course in cls.collection.find({"category": category}):
            course["_id"] = str(course["_id"])
            courses.append(
                {
                    "id": course["_id"],
                    "title": course["title"],
                    "description": course["description"],
                    "category": course.get("category"),
                    "instructor": course["instructor"],
                    "duration": course.get("duration"),
                    "created_at": course.get("created_at"),
                    "updated_at": course.get("updated_at"),
                }
            )
        return courses

    @classmethod
    async def delete_course(cls, course_id: str):
        """Delete a course by its ID."""
        try:
            obj_id = ObjectId(course_id)
        except errors.InvalidId:
            return None
        result = await cls.collection.delete_one({"_id": obj_id})
        if result.deleted_count == 0:
            return None
        return {"detail": "Course deleted successfully"}
