from sqlalchemy.orm import Session
from .models import Participant
from .schemas import ParticipantCreate, ParticipantUpdate

def create_participant(db: Session, participant: ParticipantCreate):
    db_participant = Participant(**participant.dict())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant

def get_participant(db: Session, participant_id: int):
    return db.query(Participant).filter(Participant.id == participant_id).first()

def update_participant(db: Session, participant_id: int, updates: ParticipantUpdate):
    db_participant = get_participant(db, participant_id)
    if not db_participant:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_participant, key, value)
    if updates.payment_proof:
        db_participant.is_payment_complete = True
    db.commit()
    db.refresh(db_participant)
    return db_participant