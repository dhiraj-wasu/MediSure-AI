def dispatch(payload):
    print("Forwarding to Safety Agent:", payload)
    return {
        "status": "FORWARDED",
        "next_agent": "SafetyAgent"
    }
