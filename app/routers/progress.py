from fastapi import APIRouter, Depends, HTTPException

from app.dependencies.roles import require_role
from app.models.enrollment import EnrollmentModel
from app.models.progress import ProgressModel
from app.schemas.progress import ProgressResponse, ProgressUpdate

router = APIRouter(prefix="/progress", tags=["progress"])


@router.post("/{course_id}", response_model=ProgressResponse)
async def update_course_progress(
    course_id: str,
    progress_update: ProgressUpdate,
    current_user=Depends(require_role("student")),
):
    """Update or create a user's progress in a course"""
    user_id = current_user["_id"]

    # Check if the user is enrolled in the course
    enrollment = await EnrollmentModel.get_enrollments(user_id, course_id)
    if not enrollment:
        raise HTTPException(
            status_code=403, detail="User is not enrolled in this course"
        )

    try:
        progress_data = await ProgressModel.update_progress(
            user_id=user_id, course_id=course_id, progress=progress_update.progress
        )
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

    return ProgressResponse(
        user_id=progress_data["user_id"],
        course_id=progress_data["course_id"],
        progress=progress_data["progress"],
        is_completed=progress_data.get("is_completed", False),
        created_at=progress_data["created_at"],
        updated_at=progress_data["updated_at"],
    )


@router.get("/user", response_model=list[ProgressResponse])
async def get_user_progress(
    current_user=Depends(require_role("student", "instructor", "admin"))
):
    """Retrieve all progress entries for the current user"""
    user_id = current_user["_id"]
    progress_entries = []

    cursor = ProgressModel.collection.find({"user_id": user_id})
    async for progress_data in cursor:
        progress_entries.append(
            ProgressResponse(
                user_id=progress_data["user_id"],
                course_id=progress_data["course_id"],
                progress=progress_data["progress"],
                is_completed=progress_data.get("is_completed", False),
                created_at=progress_data["created_at"],
                updated_at=progress_data["updated_at"],
            )
        )

    return progress_entries
