from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from registration_apis import database

from registration_apis.models import User
from .config import (
    ALGORITHM,
    SECRET_KEY
)

from jose import jwt,JWTError
from pydantic import ValidationError
from registration_apis.schemas import Token, TokenData,UserBase
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT"
)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        db = database.SessionLocal()
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenData(**payload)
        
        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        user: Union[dict[str, Any], None] = db.query(User).filter(User.email == token_data.sub).first()
        user_Details = {
            'id' : user.id,
            "email": user.email,
            'role': user.role,
            'first_name': user.first_name,
            'last_name':  user.last_name,
            'phone_number':  user.phone_number,
        }
        
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Could not find user",
            )
        
        return user_Details
    except(jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )