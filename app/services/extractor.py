import requests
import json
import re

LLM_URL = "http://localhost:8001/v1/chat/completions"

EXTRACTION_PROMPT = """
Extract structured signals from the message.

Return JSON only:

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
"""

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group())
    return {}

def extract_signals(history):

    payload = {
        "messages": [
            {"role": "system", "content": EXTRACTION_PROMPT},
            *history
        ]
    }

    response = requests.post(LLM_URL, json=payload)
    data = response.json()

    raw = data["choices"][0]["message"]["content"]
    return extract_json(raw)
