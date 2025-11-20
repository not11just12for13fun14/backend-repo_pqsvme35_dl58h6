from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# Minimal backend that exposes a few endpoints to unblock frontend integration
# In this environment, Mongo is available, but to move fast we only provide stubs
# matching the contracts. Real implementation would be in NestJS + Prisma as per spec.

app = FastAPI(title="StakeChess API (stub)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Wallet(BaseModel):
    soft_balance: int

FAKE_WALLET_DB = {"me": Wallet(soft_balance=1000)}

class QueueJoinRequest(BaseModel):
    stake: int
    time_control: str

@app.get("/test")
async def test():
    return {"ok": True, "time": datetime.utcnow().isoformat()}

@app.get("/me/wallet")
async def get_wallet():
    return FAKE_WALLET_DB["me"]

@app.post("/queue/join")
async def queue_join(req: QueueJoinRequest):
    # pretend to match instantly
    return {"matched": True, "matchId": "demo-1", "stake": req.stake, "time_control": req.time_control}

class MoveRequest(BaseModel):
    san: str

@app.post("/matches/{match_id}/move")
async def play_move(match_id: str, body: MoveRequest):
    return {"ok": True, "matchId": match_id, "san": body.san}

class RaiseRequest(BaseModel):
    multiplier: int # 25, 50, 100

@app.post("/matches/{match_id}/raise")
async def raise_offer(match_id: str, body: RaiseRequest):
    return {"offerId": "r1", "multiplier": body.multiplier}

class RaiseRespondRequest(BaseModel):
    accept: bool

@app.post("/matches/{match_id}/raise/{raise_id}/respond")
async def raise_respond(match_id: str, raise_id: str, body: RaiseRespondRequest):
    return {"resolved": True, "accept": body.accept}

@app.get("/matches/{match_id}")
async def get_match(match_id: str):
    return {"id": match_id, "status": "active"}

@app.get("/leaderboard")
async def leaderboard():
    return {"entries": []}

@app.get("/profile/{handle}")
async def profile(handle: str):
    return {"handle": handle, "elo": 1200}
