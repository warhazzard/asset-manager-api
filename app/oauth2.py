from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt 

from app.utils import SECRET_KEY, ALGORITHM
from app.crud.user import get_user_by_email
from app.schemas.token import TokenData 
from app.database import get_db 


# Tell fastapi where to get token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        #  Try to decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        token_data = TokenData(email=email)
    except jwt.PyJWTError:
        raise credential_exception
        
    # Check if the email exists in database
    if not token_data.email:
        raise credential_exception

    #  Fetch the user by the email
    user = get_user_by_email(db, email=token_data.email)

    # Check if user exists in database
    if not user:
        raise credential_exception

    return user 
    

        