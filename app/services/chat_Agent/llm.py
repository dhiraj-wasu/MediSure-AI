
from google import genai
import json
import requests

client = genai.Client(api_key="AIzaSyBf_h93DNKzBvt4NIWKxl6D0jPIKejWc0E")
LLM_PROVIDER = "LOCAL"      # "LOCAL" or "GEMINI"

NGROK_URL = "https://unphotographed-describable-vernetta.ngrok-free.dev"

GEMINI_MODEL = "gemini-3-flash-preview"






# PROMPT = """ You are an intent classification engine for a pharmacy chatbot.

# Your job:
# 1.Classify the user's message into ONE of the following intents ONLY:
# NEW_PRESCRIPTION  
# REFILL_EXISTING_PRESCRIPTION  
# ORDER_NON_PRESCRIPTION_MEDICINE  
# GENERAL_QUERY  
# 2.you need to find for whom the medication is for (dad, mom, self, etc).
# 3.
# CRITICAL RULES:
# - You do NOT approve prescriptions
# - You do NOT confirm orders
# - You ONLY explain, collect confirmation, and guide user through the process.

# INTENTS Rules:
# - If the user talks about uploading, adding, or having a new doctor's prescription → NEW_PRESCRIPTION
# - If the user refers to reordering, same as last time, refill, dad/mom medicine again → REFILL_EXISTING_PRESCRIPTION
# - If the user asks for OTC medicines (crocin, paracetamol, cough syrup) → ORDER_NON_PRESCRIPTION_MEDICINE
# - If none apply → GENERAL_QUERY

# Respond ONLY in valid JSON.
# Do NOT add explanations.
# expecting a response in the following format:
# {
#   "recipient": "dad",
#   "intent": "REFILL_EXISTING_PRESCRIPTION",
#   "confidence": 0.91
# }
# """

PROMPT = """
You are an AI Pharmacist Conversational Agent.

Your task:
1. Identify mode:
   - ORDER_PRESCRIPTION_MEDICINE
   - ORDER_OTC_MEDICINE
   - REFILL_EXISTING_PRESCRIPTION
   - MEDICINE_INFORMATION
   - SYMPTOM_GUIDANCE

2. Extract relevant structured fields.

3. If missing required data, set:
   "requires_clarification": true
   and provide a safe clarification question.

Never diagnose.
Never approve prescription.
Never invent medical data.

Return JSON only.
"""

import json
import re

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No valid JSON found in model output")


def call_local_llm(history: list):

    payload = {
        "messages": [
            {"role": "system", "content": PROMPT},
            *history
        ]
    }

    response = requests.post(
        f"{NGROK_URL}/v1/chat/completions",
        json=payload,
        timeout=60
    )

    data = response.json()

    raw_text = data["choices"][0]["message"]["content"]

    # 🔥 Convert string JSON → dict
    return extract_json(raw_text)



def call_gemini_llm(history: list) -> str:

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=[PROMPT, *history],
    )

    return response.text

def detect_intent_llm(history: list):

    try:

        if LLM_PROVIDER == "LOCAL":
            raw_text = call_local_llm(history)

        elif LLM_PROVIDER == "GEMINI":
            raw_text = call_gemini_llm(history)

        else:
            raise ValueError("Invalid LLM_PROVIDER")

        return json.loads(raw_text)

    except Exception as e:

        print("⚠ LLM / JSON Error:", str(e))

        return {
            "intent": "CLARIFICATION",
            "medicine": None,
            "dosage": None,
            "quantity": None,
            "clarification_question": "Could you please clarify your request?"
        }
