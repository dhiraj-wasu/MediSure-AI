from fastapi import APIRouter, UploadFile, File
from app.services.redis_state import load_state, save_state
from app.services.prescription import extract_from_pdf

router = APIRouter()

@router.post("/upload/{session_id}")
async def upload_prescription(session_id: str, file: UploadFile = File(...)):

    state = load_state(session_id)

    path = f"temp_{file.filename}"
    with open(path, "wb") as f:
        f.write(await file.read())

    text = extract_from_pdf(path)

    state["prescription_uploaded"] = True
    state["extracted_medicines"] = text

    save_state(session_id, state)

    return {"message": "Prescription received. Please confirm extracted details."}
