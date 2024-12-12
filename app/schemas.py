from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class ParticipantBase(BaseModel):
    name: str
    birth_date: date
    weight: float
    academy: str
    height: float
    category: str
    aztlan_id: Optional[str] = None
    email: Optional[str]  # Nuevo campo

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantUpdate(BaseModel):
    payment_proof: Optional[str] = None

class ParticipantResponse(ParticipantBase):
    id: int
    payment_proof: Optional[str] = None
    created_at: Optional[datetime]  # Nuevo campo

    class Config:
        orm_mode = True