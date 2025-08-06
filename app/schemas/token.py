from pydantic import BaseModel


class Token(BaseModel):
    """Schema for the token response."""
    access_token: str
    token_type: str = "bearer"