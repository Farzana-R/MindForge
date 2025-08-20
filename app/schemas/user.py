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
    created_at: Optional[str] = Field(None)
    updated_at: Optional[str] = Field(None)


class PaginatedUsers(BaseModel):
    """Model for paginated user responses."""
    page: int
    limit: int
    total_users: int
    total_pages: int
    users: list[UserOut]


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


class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    date_of_birth: Optional[str] = Field(None)  # You can switch to date type if needed
    phone_number: Optional[str] = Field(None, min_length=8, max_length=15)
    address: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, pattern="^(male|female|other)$")
