import secrets
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://ayrtonstormix-eng.github.io"],
    allow_methods=["*"],
    allow_headers=["*"],
)

ADMIN_EMAIL = "ayrtonstormix@gmail.com"

users_by_token = {}   # jeton -> pseudo
connections = {}      # pseudo -> connexion de chat ouverte

videos = [
    {
        "id": "v1",
        "user": "@truapps",
        "description": "Vidéo de test",
        "hls_url": "https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8",
    }
]


class LoginIn(BaseModel):
    email: str


class InteractIn(BaseModel):
    video_id: str
    interaction: str


def check_token(authorization: Optional[str]) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Non connecté")
    username = users_by_token.get(authorization[7:])
    if not username:
        raise HTTPException(status_code=401, detail="Session invalide")
    return username


@app.get("/")
def home():
    return {"statut": "Le serveur Truapps fonctionne"}


@app.post("/api/login")
def login(data: LoginIn):
    email = data.email.strip().lower()
    if "@" not in email:
        raise HTTPException(status_code=400, detail="E-mail invalide")
    username = email.split("@")[0]
    token = secrets.token_urlsafe(32)
    users_by_token[token] = username
    return {
        "token": token,
        "username": username,
        "subscribed": email == ADMIN_EMAIL.lower(),
    }


@app.get("/api/feed")
def feed(authorization: Optional[str] = Header(None)):
    check_token(authorization)
    return videos


@app.post("/api/recommendations/interact")
def interact(data: InteractIn, authorization: Optional[str] = Header(None)):
    check_token(authorization)
    return {"ok": True}


@app.websocket("/ws/chat")
async def chat(ws: WebSocket):
    await ws.accept()
    username = None
    try:
        auth = await ws.receive_json()
        username = users_by_token.get(auth.get("token"))
        if not username:
            await ws.close()
            return
        connections[username] = ws
        while True:
            data = await ws.receive_json()
            if data.get("type") != "message":
                continue
            receiver = data.get("receiver", "").lstrip("@")
            text = data.get("message", "")
            await ws.send_json({"sender": "@" + username, "message": text, "mine": True})
            target = connections.get(receiver)
            if target:
                await target.send_json({"sender": "@" + username, "message": text, "mine": False})
    except WebSocketDisconnect:
        pass
    finally:
        if username and connections.get(username) is ws:
            del connections[username]
