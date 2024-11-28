from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import engine, SessionLocal
from .models import Base
from .crud import create_participant, get_participant, update_participant
from .schemas import ParticipantCreate, ParticipantResponse, ParticipantUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/participants/", response_model=ParticipantResponse)
def register_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    return create_participant(db, participant)

@app.get("/participants/{participant_id}", response_model=ParticipantResponse)
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = get_participant(db, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.patch("/participants/{participant_id}", response_model=ParticipantResponse)
def update_payment(participant_id: int, updates: ParticipantUpdate, db: Session = Depends(get_db)):
    db_participant = update_participant(db, participant_id, updates)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant