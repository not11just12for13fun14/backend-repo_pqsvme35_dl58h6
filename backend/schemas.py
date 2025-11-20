from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from datetime import datetime

# This project uses Mongo in this environment. We'll scaffold models that mirror the user's desired SQL models
# so we can progress the UX and server contracts.

class User(BaseModel):
    id: Optional[str]
    email: str
    name: Optional[str]
    image: Optional[str]
    elo: int = 1200
    country: Optional[str]
    flags: Optional[List[str]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Wallet(BaseModel):
    userId: str
    soft_balance: int = 1000
    hard_balance: int = 0
    hold_soft: int = 0
    hold_hard: int = 0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Match(BaseModel):
    id: Optional[str]
    whiteId: str
    blackId: str
    status: Literal['pending','active','ended','aborted'] = 'pending'
    pot_amount: int
    base_stake: int
    raise_count: int = 0
    turn_color: Literal['white','black'] = 'white'
    raise_token_holder: Literal['white','black'] = 'white'
    time_control: str # e.g., "3+2"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime]

class Raise(BaseModel):
    id: Optional[str]
    matchId: str
    proposerId: str
    amount_delta: int
    pot_after: int
    accepted: Optional[bool]
    responderId: Optional[str]
    refusal_loss_player_id: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime]

class Move(BaseModel):
    id: Optional[str]
    matchId: str
    ply: int
    san: str
    fen_after: str
    clock_white_ms: int
    clock_black_ms: int
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Transaction(BaseModel):
    id: Optional[str]
    userId: str
    matchId: Optional[str]
    type: Literal['escrow_hold','escrow_release','payout','topup']
    currency: Literal['VC','HC'] = 'VC'
    amount: int
    idempotency_key: Optional[str]
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ModerationFlag(BaseModel):
    id: Optional[str]
    matchId: Optional[str]
    userId: Optional[str]
    reason: str
    status: Literal['open','reviewing','closed'] = 'open'
    created_at: datetime = Field(default_factory=datetime.utcnow)
