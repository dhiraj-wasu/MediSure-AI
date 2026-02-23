import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen2.5:14b"   # <-- change here if needed

PROMPT = """ You are an AI Pharmacist Conversational Agent. 
Your task: 1. Identify mode: - ORDER_PRESCRIPTION_MEDICINE - ORDER_OTC_MEDICINE - REFILL_EXISTING_PRESCRIPTION - MEDICINE_INFORMATION - SYMPTOM_GUIDANCE
 2. Extract relevant structured fields. 
 3. If missing required data, set: "requires_clarification": true and provide a safe clarification question. Never diagnose. Never approve prescription. Never invent medical data. Return JSON only. """


# -------------------------
# JSON extractor
# -------------------------

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No valid JSON found in model output")


# -------------------------
# Ollama Call
# -------------------------

def call_local_llm(history: list):

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": PROMPT},
            *history
        ],
        "options": {
            "temperature": 0.0
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception("Ollama API error")

    data = response.json()

    raw_text = data["message"]["content"]

    return extract_json(raw_text)


# -------------------------
# Public Detection Function
# -------------------------

def detect_intent_llm(history: list):

    try:
        return call_local_llm(history)

    except Exception as e:
        print("⚠ LLM JSON Error:", str(e))

        return {
            "mode": None,
            "patient_name": None,
            "symptoms": None,
            "medicine_name": None,
            "dosage": None,
            "quantity": None,
            "reference_previous_order": False,
            "has_prescription": False,
            "is_information_query": False
        }
