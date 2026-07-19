from pydantic import BaseModel, Field, ConfigDict, EmailStr
from app.models.user import UserRole 


class UserBase(BaseModel):
    firstname: str = Field(min_length=1, max_length=50, description="First name of the user")
    lastname: str = Field(min_length=1, max_length=50, description="Last name of the user")
    email: EmailStr = Field(
        description="email of the user",
        json_schema_extra={
            "example":"user@example.com"
        }
    )
    role: UserRole = Field(default=UserRole.EMPLOYEE, description="Role of the user")


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=60, description="Password of the user")


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(description="ID of the user")
    is_active: bool = Field(description="Boolean indicating if user is active or not")