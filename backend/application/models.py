from sqlalchemy import Column, Integer, String, ForeignKey, VARCHAR, DATETIME
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(VARCHAR(255))
    name = Column(VARCHAR(255))
    username = Column(VARCHAR(255), unique=True, index=True, nullable=False)
    hashed_password = Column(VARCHAR(255), nullable=False)
    created_at = Column(DATETIME)
    avatar = Column(Integer, default=1)
    sent_messages = relationship("Messages", back_populates="sender", foreign_keys="[Messages.sender_id]")
    received_messages = relationship("Messages", back_populates="recipient", foreign_keys="[Messages.recipient_id]")


class Message(Base):
    __tablename__ = "messages"
    
    ## Defining relationship on username instead of user id for scaliing as user's id could change
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.id'))
    recipient_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String)
    created_at = Column(DATETIME)
    sender = relationship("Users", back_populates="sent_messages", foreign_keys=[sender_id])
    recipient = relationship("Users", back_populates="received_messages", foreign_keys=[recipient_id])