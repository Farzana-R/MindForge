from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_role
from app.models.course import CourseModel
from app.models.enrollment import EnrollmentModel
from app.schemas.enrollment import EnrollmentResponse

router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
    responses={404: {"description": "Not found"}},
)


@router.post("/{course_id}", response_model=EnrollmentResponse)
async def enroll_user_in_course(
    # user_id: str,
    course_id: str,
    current_user=Depends(require_role("student")),
):
    """Enroll a user in a course."""
    # Check if the course exists
    # TODO: replace user_id with JWT user info
    course = await CourseModel.get_course_by_id(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    user_id = current_user["_id"]

    enrollment = await EnrollmentModel.enroll_user(user_id, course_id)
    if "message" in enrollment:
        raise HTTPException(status_code=400, detail=enrollment["message"])

    return {
        "id": enrollment["_id"],
        "user_id": enrollment["user_id"],
        "course_id": enrollment["course_id"],
        "enrolled_at": enrollment["enrolled_at"],
    }


@router.get("/user/{user_id}")
async def get_user_enrollments(user_id: str):
    """Get all enrollments for a user."""
    return await EnrollmentModel.get_enrollments_by_user(user_id)
