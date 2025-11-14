"""Authentication and User Management Router"""

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.models.user import UserModel
from app.schemas.token import Token
from app.schemas.user import UserOut, UserSignup
from app.utils.auth import create_access_token, hash_password, verify_password

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)


@router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticate a user and return an access token.

    Args:
        form_data (OAuth2PasswordRequestForm):
        The form data containing email and password.
    """
    user = await UserModel.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["email"]},
        expires_delta=None,  # Use default expiration from settings
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSignup):
    """Register a new user."""
    existing_user = await UserModel.get_by_email(user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_data = user.model_dump()
    user_data["password"] = hash_password(user.password)
    user_data["role"] = "student"  # Default role for new users
    user_data["created_at"] = datetime.now(timezone.utc).isoformat()
    user_data["updated_at"] = datetime.now(timezone.utc).isoformat()

    new_user = await UserModel.create(user_data)
    return {
        "id": new_user["_id"],
        "email": new_user["email"],
        "role": new_user["role"],
        "created_at": new_user["created_at"],
        "updated_at": new_user.get("updated_at", None),
        "first_name": new_user.get("first_name", None),
        "last_name": new_user.get("last_name", None),
        "date_of_birth": new_user.get("date_of_birth", None),
        "phone_number": new_user.get("phone_number", None),
        "address": new_user.get("address", None),
        "gender": new_user["gender"],
    }
