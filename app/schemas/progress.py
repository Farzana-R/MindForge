from datetime import datetime

from pydantic import BaseModel, Field


class ProgressUpdate(BaseModel):
    progress: int = Field(..., ge=0, le=100)


class ProgressResponse(BaseModel):
    user_id: str
    course_id: str
    progress: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime
