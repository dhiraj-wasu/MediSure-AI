from fastapi import APIRouter

router = APIRouter()

@router.post("/verify/{prescription_id}")
def verify_prescription(prescription_id: int, approve: bool):
    if approve:
        return {"status": "VERIFIED"}
    return {"status": "REJECTED"}
