from passlib.context import CryptContext  


# Get hashed password using bcrypt algorithm through passlib 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    """Takes plain-password and returns hashed-password through pwd_context object"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if the plain password matches the hashed version in database"""
    return pwd_context.verify(plain_password, hashed_password)


