"""Utility functions for authentication,
including password hashing and JWT token creation."""

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
