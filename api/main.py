import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from authenticator import authenticator
from routers import accounts, chatrooms, messages, websocket


app = FastAPI()
app.include_router(authenticator.router)
app.include_router(accounts.router)
app.include_router(chatrooms.router)
app.include_router(messages.router)
app.include_router(websocket.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_HOST")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
