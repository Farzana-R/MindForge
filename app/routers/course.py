"""API endpoints to handle course-related requests."""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies.roles import require_role
from app.schemas.course import CourseCreate, CourseOut
from app.models.course import CourseModel
# from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CourseOut)
async def create_course(
    course: CourseCreate,
    user=Depends(require_role("instructor", "admin"))
):
    """Create a new course."""
    course_data = course.model_dump()
    course_data["instructor"] = user["email"]
    now = datetime.now(timezone.utc).isoformat()
    course_data["created_at"] = now
    course_data["updated_at"] = now
    created = await CourseModel.create_course(course_data)
    return {
        "id": created["_id"],
        "title": created["title"],
        "description": created["description"],
        "category": created.get("category"),
        "instructor": created["instructor"],
        "created_at": created["created_at"],
        "updated_at": created["updated_at"]
    }

@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: str):
    """Retrieve a course by its ID."""
    course = await CourseModel.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.get("/", response_model=list[CourseOut])
async def list_courses():
    """Retrieve all courses."""
    courses = await CourseModel.get_all_courses()
    return courses
