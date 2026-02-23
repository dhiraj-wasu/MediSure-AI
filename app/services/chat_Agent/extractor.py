import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b"   # or your pulled model

EXTRACTION_PROMPT = """
You are a structured medical information extraction engine.

Extract structured signals from the user's message.

Return ONLY valid JSON.

Schema:

{
  "patient_name": null,
  "symptoms": null,
  "medicine_name": null,
  "dosage": null,
  "quantity": null,
  "reference_previous_order": false,
  "has_prescription": false,
  "is_information_query": false
}

Rules:
- If field not mentioned, return null.
- Do not explain.
- Do not add extra text.
- Response must start with { and end with }.
"""

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    raise ValueError("No valid JSON found in model output")

def extract_signals(history):

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": EXTRACTION_PROMPT},
            *history
        ],
        "options": {
            "temperature": 0.0
        },
        "stream": False   # 🔥 CRITICAL FIX
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    data = response.json()

    raw_text = data["message"]["content"]

    return extract_json(raw_text)
