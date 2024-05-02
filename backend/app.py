from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect, status
from fastapi.security import OAuth2PasswordBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi_jwt import jwt
from jwt import PyJWTError
from application.models import User, Message  # Import models from application.models
from application.database import SessionLocal  # Import session from application.database
from typing import Any
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

router = APIRouter()


class User(BaseModel):
    username: str = Field(..., min_length=3)
    email: EmailStr
    password: str = Field(..., min_length=8)
    hashed_password: str


class Message(BaseModel):
    sender: int  # Change type from ObjectId to int (assuming user ID)
    recipient: int  # Change type from ObjectId to int (assuming user ID)
    content: str
    timestamp: datetime


async def get_user_by_email(email: str, session: Session = Depends(SessionLocal)):
    user = session.query(User).filter_by(email=email).first()
    return user


async def authenticate_user(username: str, password: str, session: Session = Depends(SessionLocal)):
    user = await get_user_by_email(username, session)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire.timestamp()})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(SessionLocal)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token")
        user = await get_user_by_email(email, session)  # Retrieve user from database
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        return user  # Return the retrieved user object
    except PyJWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not decode access token")


async def save_message(message: Message, session: Session = Depends(SessionLocal)):
    session.add(message)
    session.commit()


async def get_messages(recipient: int, session: Session = Depends(SessionLocal)):
    return session.query(Message).filter_by(recipient=recipient).all()


connected_users = {}

@router.websocket("/ws/{username}")
async def websocket_endpoint(websocket: WebSocket, username: str, session: Session = Depends(SessionLocal)):
    current_user = await get_current_user(websocket.token, session)
    connected_users[current_user.id] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            message = Message(sender=current_user.id, recipient=int(data), content=data)
            await save_message(message, session)

            for user_id, user_ws in connected_users.items():
                if user_id != current_user.id:
                    try:
                        await user_ws.send_text(data)
                    except WebSocketDisconnect:
                        del connected_users[user_id]
    except WebSocketDisconnect:
        del connected_users[current_user.id]


@router.post("/register")
async def register(user: User, session: Session = Depends(SessionLocal)):
    existing_user = await get_user_by_email(user.email, session)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    user.hashed_password = pwd_context.hash(user.password)
    session.add(user)
    session.commit()
    return {"message": "User created successfully"}


@router.post("/login")
async def login(token_data: HTTPAuthorizationCredentials = Depends(oauth2_scheme), session: Session = Depends(SessionLocal)):
    user = await authenticate_user(token_data.username, token_data.password, session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}