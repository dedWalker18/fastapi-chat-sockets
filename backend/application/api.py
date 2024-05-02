from fastapi import HTTPException, Depends, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from application.parsers import *
from application.models import *
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
import bcrypt

SECRET_KEY = "432546565744234234436565464234"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
LIFE_UNIVERSE_EVERYTHING = 43

def get_user_by_username(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# async def verify_access_token(token: str) -> dict:
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     except JWTError:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
#     return payload

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Assuming "token" is your login endpoint

# async def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
#     try:
#         payload = await verify_access_token(token)
#         return payload.get("sub")  
#     except:
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")

def create_user(db: Session, user: UserInput):
    ps = user.password
    hashed_ps = hash_password(ps)
    db_user = Users(name=user.name, 
                    username=user.username.lower(),
                    email=user.email, 
                    hashed_password=hashed_ps, 
                    avatar=user.avatar, 
                    created_at=datetime.now(timezone(timedelta(hours=5, minutes=30))))
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user