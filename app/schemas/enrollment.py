from pydantic import BaseModel
from datetime import datetime


class EnrollmentResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    enrolled_at: datetime