from dataclasses import dataclass, field
from typing import List, Dict, Any
import uuid
from datetime import datetime

@dataclass
class Turn:
    role: str
    content: str
    meta: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

@dataclass
class Session:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    turns: List[Turn] = field(default_factory=list)

    def add(self, role: str, content: str, **meta):
        self.turns.append(Turn(role=role, content=content, meta=meta))

class SessionStore:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}

    def new(self) -> Session:
        s = Session()
        self.sessions[s.session_id] = s
        return s

    def get(self, session_id: str) -> Session:
        return self.sessions[session_id]

store = SessionStore()
current_session = store.new()
