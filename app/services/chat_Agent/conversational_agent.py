
from app.services.chat_Agent.extractor import extract_signals
from app.services.chat_Agent.decision_engine import decide_mode, required_fields
from app.services.chat_Agent.expression import generate_question

class ConversationalAgent:

    def run(self, state, user_message):

        state["history"].append({
            "role": "user",
            "content": user_message
        })

        extracted = extract_signals(state["history"])
        print("Extracted signals:", extracted)

        state = decide_mode(state, extracted)
        print("Updated state:", state)

        missing = required_fields(state)
        print("Missing field:", missing)
        
        if missing:
            question = generate_question(state, missing)
            return question, state, None

        # If prescription uploaded and confirmed
        if state["mode"] == "PRESCRIPTION" and state["prescription_uploaded"]:
            return (
                "Thank you 👍 I’ve sent your prescription for pharmacist verification. "
                "You can proceed to checkout, and we’ll notify you once approved.",
                state,
                {"intent": "FORWARD_TO_SAFETY", "data": state}
            )

        return "How can I help you further?", state, None
