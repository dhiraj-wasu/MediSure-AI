import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:14b"

def generate_question(context, missing_field):

    prompt = f"""
You are a caring and professional pharmacist speaking to a patient.

Missing information: {missing_field}
Patient name: {context.get('patient_name')}
Symptoms: {context.get('symptoms')}

Ask for the missing information in a warm, natural, human way.
Keep it short.
Do not sound robotic.
"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": prompt}
        ],
        "options": {
            "temperature": 0.4
        },
        "stream": False
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=120
    )

    if response.status_code != 200:
        raise Exception(f"Ollama error: {response.text}")

    data = response.json()

    return data["message"]["content"]
