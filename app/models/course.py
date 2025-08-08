"""
defines the CourseModel class for performing CRUD operations on courses 
in a MongoDB database.
"""
from bson import ObjectId
from app.core.database import db
from app.core.database import courses_collection


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
        except:
            return None  # Invalid ObjectId format
        course = await cls.collection.find_one({"_id": obj_id})
        if course:
            course["id"] = str(course["_id"])
        return course

    @classmethod
    async def get_all_courses(cls):
        """Retrieve all courses."""
        courses = []
        async for course in collection.find():
            course["_id"] = str(course["_id"])
            # courses.append(course)
            courses.append({
                "id": course["_id"],
                "title": course["title"],
                "description": course["description"],
                "category": course.get("category"),
                "instructor": course["instructor"],
                "duration": course.get("duration"),
                "created_at": course.get("created_at"),
                "updated_at": course.get("updated_at"),
            })
        return courses
