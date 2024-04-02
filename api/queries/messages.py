from fastapi import Depends
from pydantic import BaseModel
from typing import List
from datetime import datetime
from .client import Queries
from .chatrooms import ChatroomRepository


class MessageIn(BaseModel):
    chatroom: str
    content: str


class MessageOut(MessageIn):
    id: str
    username: str
    timestamp: datetime


class MessageListOut(BaseModel):
    messages: List[MessageOut]


class HttpError(BaseModel):
    detail: str


class InvalidChatRoomError(ValueError):
    pass


class MessageRepository(Queries):
    COLLECTION = "messages"

    def __init__(self, chatroom_repo: ChatroomRepository = Depends()):
        self.chatroom_repo = chatroom_repo

    def create_message(
        self, new_message: MessageIn, username: str
    ) -> MessageOut:
        new_message = new_message.dict()
        if not self.chatroom_repo.get_chatroom(new_message["chatroom"]):
            raise InvalidChatRoomError
        new_message["username"] = username
        new_message["timestamp"] = datetime.now()
        self.collection.insert_one(new_message)
        new_message["id"] = str(new_message["_id"])
        del new_message["_id"]
        return MessageOut(**new_message)

    def get_chatroom_messages(self, chatroom_name: str) -> MessageListOut:
        if not self.chatroom_repo.get_chatroom(chatroom_name):
            raise InvalidChatRoomError
        messages = []
        db_cursor = self.collection.find()
        for message in db_cursor:
            if message["chatroom"] == chatroom_name:
                message["id"] = str(message["_id"])
                del message["_id"]
                messages.append(MessageOut(**message))
        return MessageListOut(messages=messages)
