import redis
import json

redis_client = redis.Redis(host="localhost", port=6379, decode_responses=True)

TTL = 1800  # 30 min

def default_state():
    return {
        "mode": None,
        "patient_name": None,
        "symptoms": None,
        "age_group": None,
        "medicine_name": None,
        "dosage": None,
        "quantity": None,
        "has_prescription": False,
        "prescription_uploaded": False,
        "extracted_medicines": [],
        "user_confirmed": False,
        "cart": [],
        "history": []
    }

def load_state(session_id):
    data = redis_client.get(session_id)
    return json.loads(data) if data else default_state()

def save_state(session_id, state):
    redis_client.setex(session_id, TTL, json.dumps(state))

def clear_state(session_id):
    redis_client.delete(session_id)
