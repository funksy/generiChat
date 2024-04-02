from typing import Annotated
from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    Depends,
    Cookie,
    status,
)
from authenticator import authenticator
from queries.websocket import ConnectionManager


router = APIRouter()


@router.websocket("/websocket/{username}")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str,
    manager: ConnectionManager = Depends(),
):
    token = websocket.cookies.get("fastapi_token")
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, username)