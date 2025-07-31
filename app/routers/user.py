"""
This code defines a FastAPI router for user management,
including a route to create a new user.
"""
from uuid import uuid4
from fastapi import APIRouter, status, HTTPException
from app.models.user import UserModel
from app.schemas.user import UserCreate, UserOut


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

# in-memory user storage for demonstration purposes
fake_users = []


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Create a new user in the system.
    """
    existing_user = await UserModel.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_data = new_func(user)
    new_user = await UserModel.create(user_data)
    return {
        "id": str(uuid4()),  # Generate a unique ID for the user
        "email": new_user["email"],
        "name": new_user.get("name", ""),
        "created_at": new_user.get("created_at", ""),
    }


def new_func(user):
    """Helper function to convert user schema to dictionary."""
    user_data = user.dict()
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
