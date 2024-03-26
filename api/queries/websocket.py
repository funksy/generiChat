from fastapi import WebSocket, Depends
from typing import List
from pydantic import BaseModel
from .chatrooms import ChatroomRepository
from .messages import MessageRepository


class User(BaseModel):
    username: str
    current_room: str


class ConnectionManager:
    def __init__(
        self,
        message_repo: MessageRepository = Depends(),
        chat_repo: ChatroomRepository = Depends()
    ):
        self.message_repo = message_repo
        self.chat_repo = chat_repo

    active_connections: List[dict] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        user = User(username=username, current_room="main")
        connection = {
            "websocket": websocket,
            "user": user,
        }
        self.active_connections.append(connection)

        await self.direct_message(websocket, f'Welcome, {username}')
        await self.broadcast(websocket, f'{username} connected')

    async def disconnect(self, websocket: WebSocket, username: str):
        for connection in self.active_connections:
            if connection["websocket"] == websocket:
                self.active_connections.remove(connection)
        
        await self.broadcast(websocket, f'{username} disconnected')
    
    async def broadcast(self, websocket: WebSocket, content: str):
        for connection in self.active_connections:
            if connection["websocket"] == websocket:
                continue
            await connection["websocket"].send_json({"test": content})
    
    async def direct_message(self, websocket: WebSocket, content: str):
        await websocket.send_json({"test": content})