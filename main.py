from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base
from app.crud import create_participant, get_participant_by_aztlan_id, update_participant
from app.schemas import ParticipantCreate, ParticipantResponse, ParticipantUpdate
import os
from uuid import uuid4
from app.logger.logger import logger

Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration: Specify which domains can access the API
origins = [
    "http://localhost:3000",  # Frontend React URL (for local development)
    "http://127.0.0.1:3000",  # Another common address for localhost
    "http://localhost:3001",  # Frontend React URL (for local development)
    "http://127.0.0.1:3001",  # Another common address for localhost
]

# Add the CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_headers=["Content-Type", "Authorization", "X-Requested-With", "Accept"],  # Allow specific headers
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Directory to store uploaded files
UPLOAD_DIR = "./uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/participants/", response_model=ParticipantResponse)
def register_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    return create_participant(db, participant)

@app.get("/participants/{participant_id}", response_model=ParticipantResponse)
def read_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = get_participant_by_aztlan_id(db, participant_id)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.patch("/participants/{participant_id}", response_model=ParticipantResponse)
def update_payment(participant_id: int, updates: ParticipantUpdate, db: Session = Depends(get_db)):
    db_participant = update_participant(db, participant_id, updates)
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return db_participant

@app.post("/participants/{aztlan_id}/upload")
def upload_payment_proof(
    aztlan_id: str,
    file: UploadFile = File(...),  # Expecting a file from the client
    db: Session = Depends(get_db),
):
    # Check if participant exists
    logger.info("so el linea 86")
    try:
        db_participant = get_participant_by_aztlan_id(db, aztlan_id)
        if not db_participant:
            logger.info("so el linea 67")
            raise HTTPException(status_code=404, detail="Participant not found")
        
        # Validate file type
        file_extension = os.path.splitext(file.filename)[1]
        if file_extension not in [".jpg", ".jpeg", ".png"]:
            raise HTTPException(status_code=400, detail="Invalid file format. Only JPG and PNG are allowed.")
        
        # Generate a unique filename
        unique_filename = f"comprobante-{aztlan_id}{file_extension}"
        file_path = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Save the file synchronously
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        # Update participant's payment proof
        file_url = f"/static/{unique_filename}"  # Public URL for the file
        updates = ParticipantUpdate(payment_proof=file_url)
        updated_participant = update_participant(db, aztlan_id, updates)
        
        return updated_participant
    
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Serve static files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory=UPLOAD_DIR), name="static")