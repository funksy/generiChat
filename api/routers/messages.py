from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    Response,
    HTTPException,
)
from authenticator import authenticator
from queries.messages import (
    MessageIn,
    MessageOut,
    MessageListOut,
    MessageRepository,
    HttpError,
    InvalidChatRoomError,
)

router = APIRouter()

@router.post(
    "/chatrooms/{chatroom_name}/messages",
    response_model=MessageOut,
    tags=["messages"]
)
def create_message(
    new_message: MessageIn,
    request: Request,
    response: Response,
    repo: MessageRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    try:
        creator = account_data["username"]
        new_message = repo.create_message(new_message, creator)
    except InvalidChatRoomError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chatroom name"
        )
    return new_message

@router.get(
    "/chatrooms/{chatroom_name}/messages",
    response_model=MessageListOut,
    tags=["messages"]
)
def get_chatroom_messages(
    chatroom_name: str,
    request: Request,
    response: Response,
    repo: MessageRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    try:
        messages = repo.get_chatroom_messages(chatroom_name)
    except InvalidChatRoomError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid chatroom name"
        )
    return messages