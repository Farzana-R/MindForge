"""API endpoints to handle course-related requests."""

from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.dependencies.auth import get_current_user
from app.dependencies.roles import require_role
from app.models.course import CourseModel
from app.schemas.course import (
    CourseCreate,
    CourseOut,
    CourseUpdate,
    CourseUpdateOut,
    PaginatedCourses,
)

# from app.dependencies.auth import get_current_user


router = APIRouter(
    prefix="/courses",
    tags=["courses"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CourseOut)
async def create_course(
    course: CourseCreate, user=Depends(require_role("instructor", "admin"))
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
        "updated_at": created["updated_at"],
    }


@router.get("/{course_id}", response_model=CourseOut)
async def get_course(course_id: str, current_user=Depends(get_current_user)):
    """Retrieve a course by its ID."""
    if not course_id:
        raise HTTPException(status_code=400, detail="Course ID is required")
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    course = await CourseModel.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.get("/", response_model=PaginatedCourses)
async def list_courses(
    current_user=Depends(get_current_user),
    skip: int = Query(0, description="Number of courses to skip for pagination"),
    limit: int = Query(10, description="Number of courses to return per page"),
    category: Optional[str] = Query(None, description="Filter by course category"),
    instructor: Optional[str] = Query(None, description="Filter by instructor email"),
    search: Optional[str] = Query(
        None, description="Search courses by title or description"
    ),
    sort_by: Optional[str] = Query(
        "created_at", description="Sort courses by created_at or updated_at"
    ),
    sort_order: Optional[int] = Query(
        -1, description="Sort order: 1 for ascending, -1 for descending"
    ),
):
    """Retrieve all courses with pagination, filtering, searching, and sorting."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")

    courses = await CourseModel.get_all_courses(
        skip=skip,
        limit=limit,
        category=category,
        instructor=instructor,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )
    return courses


@router.patch("/update/{course_id}", response_model=CourseUpdateOut)
async def update_course(
    course_id: str,
    course: CourseUpdate,
    user=Depends(require_role("instructor", "admin")),
):
    """Update an existing course."""
    existing_course = await CourseModel.get_course_by_id(course_id)
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    if existing_course["instructor"] != user["email"]:
        raise HTTPException(
            status_code=403,
            detail=(
                "you are not the creator of this course."
                "so, You do not have permission to update this course"
            ),
        )

    course_data = course.model_dump(exclude_unset=True)
    course_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    updated_course = await CourseModel.update_course(course_id, course_data)
    return {
        "id": updated_course["_id"],
        "title": updated_course["title"],
        "description": updated_course["description"],
        "category": updated_course.get("category"),
        "instructor": updated_course["instructor"],
        "created_at": updated_course["created_at"],
        "updated_at": updated_course["updated_at"],
    }


@router.delete("/{course_id}", status_code=200)
async def delete_course(
    course_id: str, user=Depends(require_role("instructor", "admin"))
):
    """Delete a course by its ID.
    Only the course creator or an admin can delete it."""
    existing_course = await CourseModel.get_course_by_id(course_id)
    if not existing_course:
        raise HTTPException(status_code=404, detail="Course not found")
    is_admin = user["role"] == "admin"
    is_course_creator = existing_course["instructor"] == user["email"]

    if not (is_admin or is_course_creator):
        raise HTTPException(
            status_code=403, detail="You do not have permission to delete this course"
        )
    await CourseModel.delete_course(course_id)
    return {"detail": "Course deleted successfully"}


@router.get("/instructor/{instructor_email}", response_model=list[CourseOut])
async def get_courses_by_instructor(
    instructor_email: str, current_user=Depends(get_current_user)
):
    """Retrieve all courses taught by a specific instructor."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    courses = await CourseModel.get_courses_by_instructor(instructor_email)
    if not courses:
        raise HTTPException(
            status_code=404, detail="No courses found for this instructor"
        )
    return courses


@router.get("/category/{category}", response_model=list[CourseOut])
async def get_courses_by_category(
    category: str, current_user=Depends(get_current_user)
):
    """Retrieve all courses in a specific category."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized access")
    courses = await CourseModel.get_courses_by_category(category)
    if not courses:
        raise HTTPException(status_code=404, detail="No courses found in this category")
    return courses
