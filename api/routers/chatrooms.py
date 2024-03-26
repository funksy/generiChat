from fastapi import (
    APIRouter,
    Depends,
    status,
    Request,
    Response,
    HTTPException,
)
from authenticator import authenticator
from queries.chatrooms import (
    ChatroomIn,
    ChatroomOut,
    ChatroomListOut,
    ChatroomRepository,
    HttpError,
    DuplicateChatroomError,
)

router = APIRouter()


@router.post(
    "/chatrooms", response_model=ChatroomOut | HttpError, tags=["chatrooms"]
)
def create_chatroom(
    new_chatroom: ChatroomIn,
    request: Request,
    response: Response,
    repo: ChatroomRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    try:
        chatroom_owner = account_data["username"]
        new_chatroom = repo.create_chatroom(new_chatroom, chatroom_owner)
    except DuplicateChatroomError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chatroom by that name already exists",
        )
    return new_chatroom


@router.get(
    "/chatrooms/{chatroom_name}",
    response_model=ChatroomOut | None,
    tags=["chatrooms"],
)
def get_chatroom(
    chatroom_name: str,
    repo: ChatroomRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    chatroom = repo.get_chatroom(chatroom_name)
    return chatroom


@router.get("/chatrooms", response_model=ChatroomListOut, tags=["chatrooms"])
def get_chatroom_list(
    repo: ChatroomRepository = Depends(),
    account_data: dict = Depends(authenticator.get_current_account_data),
):
    return repo.get_chatroom_list()
