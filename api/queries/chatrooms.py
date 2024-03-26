from pydantic import BaseModel
from typing import List
from .client import Queries


class ChatroomIn(BaseModel):
    chatroom_name: str


class ChatroomOut(ChatroomIn):
    id: str
    owner: str


class ChatroomListOut(BaseModel):
    chatrooms: List[ChatroomOut]


class HttpError(BaseModel):
    detail: str


class DuplicateChatroomError(ValueError):
    pass


class ChatroomRepository(Queries):
    COLLECTION = "chatrooms"

    def create_chatroom(self, new_chatroom: ChatroomIn, chatroom_owner: str) -> ChatroomOut:
        new_chatroom = new_chatroom.dict()
        new_chatroom["owner"] = chatroom_owner
        new_chatroom["chatroom_name"] = new_chatroom["chatroom_name"].lower()
        if self.collection.find_one(
            {"chatroom_name": new_chatroom["chatroom_name"]}
        ):
            raise DuplicateChatroomError
        self.collection.insert_one(new_chatroom)
        new_chatroom["id"] = str(new_chatroom["_id"])
        del new_chatroom["_id"]
        return ChatroomOut(**new_chatroom)

    def get_chatroom(self, chatroom_name: str) -> ChatroomOut | None:
        chatroom = self.collection.find_one(
            {"chatroom_name": chatroom_name.lower()}
        )
        if not chatroom:
            return None
        chatroom["id"] = str(chatroom["_id"])
        del chatroom["_id"]
        return ChatroomOut(**chatroom)

    def get_chatroom_list(self) -> ChatroomListOut:
        chatrooms = []
        db_cursor = self.collection.find()
        for chatroom in db_cursor:
            chatroom["id"] = str(chatroom["_id"])
            del chatroom["_id"]
            chatrooms.append(ChatroomOut(**chatroom))
        return ChatroomListOut(chatrooms=chatrooms)
