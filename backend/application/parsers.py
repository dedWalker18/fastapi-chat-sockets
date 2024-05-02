from pydantic import BaseModel
from datetime import datetime

class UserInput(BaseModel):
    name: str
    username: str
    email: str
    password: str
    avatar: int
    
class UserOutput(UserInput):
    created_at: datetime

class UserLogin(BaseModel):
    username: str
    password: str

class Message(BaseModel):
    recipient_username: str
    sender_username: str
    content: str