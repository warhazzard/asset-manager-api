from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm 
from sqlalchemy.orm import Session
from app.database import get_db 
from app.schemas.token import Token 
from app.utils import verify_password, create_access_token 
from app.crud.user import get_user_by_email


router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=Token, status_code=status.HTTP_201_CREATED)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, user_credentials.username)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    if not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Generate JWT token for the user
    access_token = create_access_token(data={"sub": user.email})

    return {"access_token": access_token, "token_type":"Bearer"}


