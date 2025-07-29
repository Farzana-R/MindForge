"""
This code defines a FastAPI router for user management,
including a route to create a new user.
"""
from uuid import uuid4
from fastapi import APIRouter, status
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
    new_user = {
        "id": str(uuid4()),
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
    }
    fake_users.append(new_user)
    return new_user