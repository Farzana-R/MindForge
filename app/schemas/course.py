"""Defines Pydantic models for course data validation and serialization.
"""
from typing import Optional
from pydantic import BaseModel, Field


class CourseBase(BaseModel):
    """Base model for course data."""
    title: str = Field(..., min_length=1, max_length=100,
                       description="The course title")
    description: str = Field(..., min_length=10, max_length=500,
                             description="A brief description of the course")
    # instructor_id: str = Field(..., description="The ID of the instructor teaching the course")
    category: Optional[str] = Field(description="The category of the course")
    # duration: Optional[int] = Field(None, ge=0, description="Duration of the course in hours")


class CourseCreate(CourseBase):
    """Model for creating a new course."""
    pass


class CourseOut(CourseBase):
    """Model for outputting course data."""
    id: str = Field(..., description="The unique identifier for the course")
    instructor: str = Field(..., description="The name of the instructor")
    created_at: Optional[str] = Field(...,
                            description="The date and time when the course was created")
    updated_at: Optional[str] = Field(...,
                            description="The date and time when the course was last updated")
    

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=500)
    category: Optional[str] = Field(None, description="The category of the course")

class CourseUpdateOut(CourseUpdate):
    id: str = Field(..., description="The unique identifier for the course")
    instructor: str = Field(..., description="The name of the instructor")
    created_at: Optional[str] = Field(...,
                            description="The date and time when the course was created")
    updated_at: Optional[str] = Field(...,
                            description="The date and time when the course was last updated")
    
class PaginatedCourses(BaseModel):
    """Model for paginated course results."""
    total: int = Field(..., description="Total number of courses")
    data: list[CourseOut] = Field(..., description="List of courses in the current page")
