"""
API endpoints to handle requests
"""
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status, HTTPException
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserOut
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
    user_data["role"] = user_data.get("role", "student")  # Default to student if not specified
    user_data["created_at"] = datetime.now(timezone.utc).isoformat()
    user_data["updated_at"] = datetime.now(timezone.utc).isoformat()
    return user_data


@router.get("/", response_model=list[UserOut])
async def list_users():
    """
    Retrieve all users in the system.
    """
    users = []
    async for user in UserModel.collection.find():
        user["_id"] = str(user["_id"])  # Convert ObjectId to string
        users.append({
            "id": user["_id"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "date_of_birth": user["date_of_birth"],
            "phone_number": user["phone_number"],
            "address": user["address"],
            "role": user["role"],
            "gender": user["gender"],
        })
    return users

@router.get("/user/profile")
async def profile(user=Depends(get_current_user)):
    """Retrieve the profile of the current user."""
    return {"email": user["email"], "role": user["role"]}


@router.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(admin_required)):
    """Admin dashboard to view all users."""
    return {"msg": "Welcome to the admin dashboard", "user": current_user}
