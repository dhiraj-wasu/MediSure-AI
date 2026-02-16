from fastapi import APIRouter, UploadFile, File

router = APIRouter()

@router.post("/upload")
def upload_prescription(file: UploadFile = File(...)):
    return {
        "status": "RECEIVED",
        "message": "Prescription uploaded. Processing started."
    }
