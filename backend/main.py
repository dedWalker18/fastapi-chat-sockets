# from fastapi import FastAPI, HTTPException, Depends, WebSocket, Request, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from sqlalchemy.orm import Session
# from application import models
# from application.parsers import *
# from application.api import *
# from application.models import *
# from application.database import SessionLocal, engine
# from datetime import timedelta
# from typing import Dict, Any, List
# import json

# app = FastAPI()

# models.Base.metadata.create_all(bind=engine)
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
#     allow_headers=["Content-Type", "Authorization"],
# )

# @app.post("/users", tags=["Users"])
# async def add_user(user: UserInput, db: Session = Depends(get_db)):
#     db_user = get_user_by_username(db, user.username)
#     if db_user:
#         raise HTTPException(status_code=400, 
#                     detail="Username Already Taken")
#     create_user(db, user)
#     return {"message": f"User {user.username} Added Successfully!!!"}

# @app.get("/users",  tags=["Users"])
# async def get_users(db: Session = Depends(get_db)):
#     result = db.query(Users).all()
#     return result

# @app.get("/users/{user_id}", tags=["Users"])
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = db.query(Users).filter(Users.id == user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, 
#                     detail="User not found")
#     return db_user

# # @app.delete("/users", tags=["Users"])
# # async def delete_user(current_user: str = Depends(get_current_user), db: Session = Depends(get_db)):
# #     db_user = db.query(Users).filter(Users.username == current_user).first()
# #     if db_user is None:
# #         raise HTTPException(status_code=404, 
# #                     detail="User not found")
# #     db.delete(db_user)
# #     db.commit()
# #     return {"message": f"User Deleted Successfully!!!"}

# @app.post("/loginuser", tags=["Login"])
# async def login(user_login : UserLogin, db: Session = Depends(get_db)):
#     un = user_login.username.lower()
#     try:
#         db_user = db.query(Users).filter(Users.username == un).first()
#         if not verify_password(user_login.password, db_user.hashed_password):
#             raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                 detail="Wrong Password")
#         else:
#             access_token = create_access_token(data={"sub": un}, 
#                             expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#         return {"token" : access_token}
#     except:
#         raise HTTPException(status_code=401,
#                             detail="User not found")

# @app.post("/send_message")
# async def send_message_via_http(message_data: Message, db: Session = Depends(get_db)):
#     sender = get_user_by_username(db, message_data.sender_username)
#     recipient = get_user_by_username(db, message_data.recipient_username)
#     message = Messages(
#         sender_id=sender.id,
#         recipient_id=recipient.id,
#         content=message_data.content,
#         created_at=datetime.now(timezone(timedelta(hours=5, minutes=30)))
#     )
#     db.add(message)
#     db.commit()
#     return {"message": "Message sent successfully"}


#     # while True:
#     #     try:
#     #         data = await websocket.receive_text()
#     #         message_data = Message.parse_raw(data)
#     #         recipient = get_user_by_username(db, message_data.recipient_username)
#     #         sender = get_user_by_username(db, message_data.sender_username)
#     #         message = Messages(
#     #             sender_id=sender.id,
#     #             recipient_id=recipient.id,
#     #             content=message_data.content,
#     #             created_at=datetime.now(timezone(timedelta(hours=5, minutes=30)))
#     #         )
#     #         db.add(message)
#     #         db.commit()
#     #         await websocket.send_text("Message sent successfully")
#     #     except WebSocketDisconnect:
#     #         break
    
# class ConnectionManager:
#     def __init__(self):
#         self.active_connections: List[WebSocket] = []

#     async def connect(self, websocket: WebSocket):
#         await websocket.accept()
#         self.active_connections.append(websocket)

#     def disconnect(self, websocket: WebSocket):
#         self.active_connections.remove(websocket)

#     async def send_personal_message(self, message: str, websocket: WebSocket):
#         await websocket.send_text(message)

#     async def broadcast(self, message: str):
#         for connection in self.active_connections:
#             await connection.send_text(message)


# manager = ConnectionManager()


# @app.websocket("/ws/broadcast")
# async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             message_data = Message.parse_raw(data)
#             sender = get_user_by_username(db, message_data.sender_username)
#             if sender:
#                 message = {
#                     "sender": sender.username,
#                     "content": message_data.content,
#                     "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30)))
#                 }
#                 await manager.broadcast(json.dumps(message))
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast("Offline")

# @app.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             message_data = Message.parse_raw(data)
#             sender = get_user_by_username(db, message_data.sender_username)
#             recipient = get_user_by_username(db, message_data.recipient_username)
#             if sender and recipient:
#                 message = {
#                     "sender": sender.username,
#                     "content": message_data.content,
#                     "created_at": datetime.now(timezone(timedelta(hours=5, minutes=30)))
#                 }
#                 await manager.send_personal_message(json.dumps(message), websocket)
#     except:
#         manager.disconnect(websocket)
#         await manager.broadcast("Offline")