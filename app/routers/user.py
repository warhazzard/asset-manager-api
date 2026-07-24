from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session 
from app.database import get_db
from app.crud import user as crud_user
from app.models.user import User 
from app.schemas.user import UserCreate, UserResponse 


router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_new_user(user:UserCreate, db: Session = Depends(get_db)) -> User:
    existing_user = crud_user.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    
    return crud_user.register_user(db, user)
    
