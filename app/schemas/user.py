"""pydantic models - validates request/response"""

from enum import Enum
from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
    """User roles in the system."""
    ADMIN = "admin"
    INSTRUCTOR = "instructor"
    STUDENT = "student"


class UserBase(BaseModel):
    """Base model for user data."""
    email: EmailStr = Field(..., description="The user's email address")
    first_name: str = Field(..., min_length=1, max_length=50,
                            description="The user's first name")
    last_name: str = Field(..., min_length=1, max_length=50,
                           description="The user's last name")
    date_of_birth: str = Field(...,
                               description="The user's date of birth in YYYY-MM-DD format")
    phone_number: str = Field(..., min_length=10, max_length=15,
                              description="The user's phone number")
    address: str = Field(..., description="The user's residential address")
    gender: str = Field(..., description="The user's gender",
                        pattern="^(male|female|other)$", examples=["male", "female", "other"])
    role: UserRole = Field(..., description="The user's role in the system")


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8, description="The user's password")


class UserOut(UserBase):
    """Model for outputting user data."""
    id: str = Field(..., description="The unique identifier for the user")
