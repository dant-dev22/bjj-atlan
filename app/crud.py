from sqlalchemy.orm import Session
from .models import Participant
from .schemas import ParticipantCreate, ParticipantUpdate
from app.logger.logger import logger
from uuid import uuid4
from datetime import datetime

def create_participant(db: Session, participant: ParticipantCreate):
    db_participant = Participant(**participant.dict())
    generated_id = uuid4()
    generated_id_str = str(generated_id)
    short_id = generated_id_str[:6]
    aztlan_id = f"{short_id}"
    
    db_participant.created_at = datetime.utcnow()

    db_participant.aztlan_id = aztlan_id
    logger.info(f"Creando participante {db_participant.aztlan_id}")

    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)

    return db_participant

def get_participant_by_aztlan_id(db: Session, aztlan_id: str):
    logger.info(f"Buscando participante con aztlan_id {aztlan_id}")
    return db.query(Participant).filter(Participant.aztlan_id == aztlan_id).first()

def update_participant(db: Session, participant_id: int, updates: ParticipantUpdate):
    logger.info(f"Actualizando participante con ID {participant_id}")
    db_participant = get_participant(db, participant_id)
    if not db_participant:
        logger.warning(f"Participante con ID {participant_id} no encontrado para actualización")
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_participant, key, value)
    if updates.payment_proof:
        db_participant.is_payment_complete = True
    db.commit()
    db.refresh(db_participant)
    return db_participant

def delete_participant(db: Session, participant_id: int):
    logger.info(f"Eliminando participante en el crud con ID {participant_id}")
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if db_participant:
        logger.info(f"Participante encontrado. Procediendo con la eliminación: ID {participant_id}")
        db.delete(db_participant)
        db.commit()
        return db_participant
    logger.warning(f"No se encontró participante con ID {participant_id} para eliminar")
    return None