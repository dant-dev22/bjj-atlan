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

class ParticipantCreate(ParticipantBase):
    pass

class ParticipantUpdate(BaseModel):
    payment_proof: Optional[str] = None

class ParticipantResponse(ParticipantBase):
    id: int
    payment_proof: Optional[str] = None
    is_payment_complete: bool

    class Config:
        orm_mode = True

class PaymentBase(BaseModel):
    aztlan_id: str
    payment_proof: Optional[str] = None
    is_payment_complete: bool

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True