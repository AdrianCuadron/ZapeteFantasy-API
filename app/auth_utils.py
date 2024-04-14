from datetime import timedelta
import crud, models, schemas
from database import get_db
from fastapi import Depends, HTTPException, Form
from datetime import datetime, timedelta, timezone
import logging
from typing import List

from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "4a25e2cebe6e650571794f94da3eb70717b9825b7a836a3bf91003679ee0b03d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 # One day

class OAuth2RefreshTokenForm:
    def __init__(
            self,
            grant_type: str = Form(..., regex="refresh_token"),
            refresh_token: str = Form(...),
    ):
        self.grant_type = grant_type
        self.refresh_token = refresh_token
        


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

def verify_password(plain_password, hashed_password):
    print(f"Verifying password: plain_password={plain_password}, hashed_password={hashed_password}", flush=True)
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db, username: str, password: str):
    user = crud.get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(username=username)
        
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user
    
async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    return current_user

def create_refresh_token(data: dict):
    expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    return create_access_token(data, expires_delta=expires)