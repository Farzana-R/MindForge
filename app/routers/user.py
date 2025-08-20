"""
API endpoints to handle requests
"""
from datetime import datetime, timezone
import re
from typing import Optional
from bson import ObjectId
from fastapi import APIRouter, Depends, Query, status, HTTPException
from app.models.user import UserModel
from app.schemas.user import PaginatedUsers, ProfileUpdate, UserCreate, UserOut
from app.utils.auth import hash_password
from app.dependencies.auth import admin_required, get_current_user


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# in-memory user storage for demonstration purposes
fake_users = []


@router.post("/admin/create-user", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_as_admin(
    user: UserCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Admin endpoint to create any type of user (student, instructor, admin).
    """
    # ensure the current user is an admin
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can create users.",
        )
    existing_user = await UserModel.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_data = new_func(user)
    new_user = await UserModel.create(user_data)
    return {
        "id": new_user["_id"],
        "email": new_user["email"],
        "first_name": new_user["first_name"],
        "last_name": new_user["last_name"],
        "date_of_birth": new_user["date_of_birth"],
        "phone_number": new_user["phone_number"],
        "address": new_user["address"],
        "gender": new_user["gender"],
        "role": new_user["role"],
        "created_at": new_user["created_at"],
        "updated_at": new_user.get("updated_at", None),
    }


def new_func(user):
    """Helper function to convert user schema to dictionary."""
    user_data = user.model_dump()
    user_data["password"] = hash_password(user.password)
    # Default to student if not specified
    user_data["role"] = user_data.get("role", "student")
    user_data["created_at"] = datetime.now(timezone.utc).isoformat()
    user_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    return user_data


@router.get("/", response_model=PaginatedUsers)
async def list_users(
    page: int = Query(1, ge=1, description="Page number (starting from 1)"),
    limit: int = Query(
        10, ge=1, le=100, description="Number of users per page"),
    role: Optional[str] = Query(None, description="Filter by role"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    # email: Optional[str] = Query(None, description="Filter by exact email"),
    search: Optional[str] = Query(None, description="Search in name, email"),
    current_user: dict = Depends(get_current_user)
):
    """
    Retrieve all users in the system.
    """
    # ✅ Role-based access control
    if current_user["role"].lower() != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only admins can list all users."
        )

    # Build dynamic filter
    query = {}
    if role:
        query["role"] = role
    if gender:
        query["gender"] = gender
    # if email:
    #     query["email"] = email

    # Partial search (case-insensitive)
    if search:
        search_regex = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [
            {"first_name": search_regex},
            {"last_name": search_regex},
            {"email": search_regex},
        ]
    users = await UserModel.list_users(query=query, limit=limit, page=page)
    total_users = await UserModel.count_users(query = query)
    total_pages = (total_users + limit - 1) // limit
    return {
        "page": page,
        "limit": limit,
        "total_users": total_users,
        "total_pages": total_pages,
        "users": users
    }


@router.get("/user/profile")
async def profile(user=Depends(get_current_user)):
    """Retrieve the profile of the current user."""
    user_data = dict(user)  # Make a copy so we don't modify the original
    user_data.pop("_id", None)
    user_data.pop("password", None)
    return user_data


@router.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(admin_required)):
    """Admin dashboard to view all users."""
    user_copy = current_user.copy()  # Avoid mutating the original dict
    user_copy.pop("password", None)  # Remove password if it exists
    return {"msg": "Welcome to the admin dashboard", "user": user_copy}


@router.get("/users/{user_id}", dependencies=[Depends(admin_required)])
async def get_user_by_id(user_id: str):
    """Get user details by ID (admin only)."""
    # validate ObjectId format
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    user = await UserModel.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user["_id"] = str(user["_id"])  # Convert ObjectId to string
    user.pop("password", None)
    user.pop("_id", None)  # Remove _id if not needed in response
    return user


@router.patch("/user/update-profile")
async def update_profile(
    profile_update: ProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Partially update the current user's profile with validation.
    Only provided fields will be updated, others remain unchanged.
    """
    # convert pydantic model to dict
    update_data = profile_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields provided for update"
        )
    await UserModel.update_user(
        str(current_user["_id"]),
        update_data
    )
    updated_user = await UserModel.get_by_id(str(current_user["_id"]))
    if updated_user:
        updated_user.pop("_id", None)  # Remove _id if not needed in response
        updated_user.pop("password", None)
        return updated_user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
    )


@router.delete("/admin/delete-user/{user_id}")
async def delete_user(
    user_id: str,
    current_user: dict = Depends(admin_required)
):
    """Delete a user by ID (admin only)."""
    # validate ObjectId format
    if not ObjectId.is_valid(user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    # prevent admin from deleting themselves
    if str(current_user["_id"]) == user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins cannot delete themselves"
        )
    await UserModel.delete_user(user_id)
    return {"msg": "User deleted successfully"}
