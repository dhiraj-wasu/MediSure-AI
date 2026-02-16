from fastapi import FastAPI
from app.routes import chat, prescription, admin

app = FastAPI(title="MediSure_AI")

app.include_router(chat.router, prefix="/chat")
app.include_router(prescription.router, prefix="/prescription")
app.include_router(admin.router, prefix="/admin")



