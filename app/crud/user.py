from sqlalchemy.orm import Session
from app.models.user import User 
from app.schemas.user import UserCreate
from app.utils import get_hashed_password 


# GET: get user by email
def get_user_by_email(db:Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


# CREATE: Register a new user
def register_user(db: Session, user: UserCreate) -> User:
    hashed_pass = get_hashed_password(user.password)
    db_user = User(
        **user.model_dump(exclude={"password"}),
        hashed_password=hashed_pass,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
