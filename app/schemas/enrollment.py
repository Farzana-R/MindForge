from datetime import datetime

from pydantic import BaseModel


class EnrollmentResponse(BaseModel):
    id: str
    user_id: str
    course_id: str
    enrolled_at: datetime
