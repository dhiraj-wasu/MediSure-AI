class Prescription:
    id: int
    patient_id: int
    doctor_name: str
    clinic_name: str
    issue_date: str
    status: str  # PENDING / VERIFIED / REJECTED
