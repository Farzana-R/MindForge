"""User schema definitions for the application.
This module defines the data models for user-related operations."""

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
    full_name: str = Field(..., min_length=3, max_length=50, description="The user's full name")
    role: UserRole = Field(..., description="The user's role in the system")


class UserCreate(UserBase):
    """Model for creating a new user."""
    password: str = Field(..., min_length=8, description="The user's password")

class UserOut(UserBase):
    """Model for outputting user data."""
    id: str = Field(..., description="The unique identifier for the user")