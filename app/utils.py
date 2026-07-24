from passlib.context import CryptContext 
from datetime import datetime, timedelta, UTC
import jwt 
import os 
from dotenv import load_dotenv 


load_dotenv() 
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# Get hashed password using bcrypt algorithm through passlib 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """Takes plain-password and returns hashed-password through pwd_context object"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the plain password matches the hashed version in database"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()

    # calculate the expiration time from now 
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    # Add expiration time to the payload under the standard  "exp"except
    to_encode.update({"exp": expire})

    # Create the JWT Token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt 

    