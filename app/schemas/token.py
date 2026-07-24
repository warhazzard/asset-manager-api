from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional


class Token(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    access_token: str = Field(description="JWT Access Token")
    token_type: str = Field(default="Bearer", description="Type of the token. Always 'Bearer'")


class TokenData(BaseModel):
    email: Optional[str] = None