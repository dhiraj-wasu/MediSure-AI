import requests

LLM_URL = "http://localhost:11434"


def generate_question(context, missing_field):

    prompt = f"""
We need to ask the user for: {missing_field}.
Patient name: {context.get('patient_name')}
Symptom: {context.get('symptoms')}

Generate a warm, human, pharmacist-style question.
Keep it short.
"""

    payload = {
        "messages": [
            {"role": "system", "content": prompt}
        ]
    }

    response = requests.post(LLM_URL, json=payload)
    return response.json()["choices"][0]["message"]["content"]
