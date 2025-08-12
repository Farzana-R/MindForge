"""pydantic models - validates request/response"""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class UserBase(BaseModel):
    """Base model for user data."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: Optional[str] = Field(..., min_length=1, max_length=50)
    date_of_birth: str = Field(...,
                               description="The user's date of birth in YYYY-MM-DD format")
    phone_number: str = Field(..., min_length=10, max_length=15)
    address: Optional[str]
    gender: str = Field(
        ...,
        pattern="^(male|female|other)$",
        examples=["male", "female", "other"]
    )
    role: UserRole = Field(..., description="The user's role in the system")


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8)


class UserOut(UserBase):
    """Model for outputting user data."""
    id: str = Field(..., description="The unique identifier for the user")
    created_at: str
    updated_at: str


class UserSignup(BaseModel):
    """Schema for self-signup (role defaults to student)."""
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: Optional[str] = Field(..., min_length=1, max_length=50)
    date_of_birth: str
    phone_number: str = Field(..., min_length=10, max_length=15)
    address: Optional[str] = Field(min_length=1, max_length=250)
    gender: str = Field(
        ...,
        pattern="^(male|female|other)$",
        examples=["male", "female", "other"]
    )
    password: str = Field(..., min_length=8)
