from fastapi import Depends, HTTPException, status

from app.dependencies.auth import get_current_user


def require_role(*roles: list[str]):
    """Decorator to require a specific role for the current user."""

    async def role_checker(user=Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted for the current user role",
            )
        return user

    return role_checker
