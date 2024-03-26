from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from queries.websocket import ConnectionManager


router = APIRouter()


@router.websocket("/websocket/{username}")
async def websocket_endpoint(
    websocket: WebSocket,
    username: str,
    manager: ConnectionManager = Depends(),
):
    await manager.connect(websocket, username)
    try:
        while True:
            data = await websocket.receive_json()
            await manager.broadcast(data)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, username)