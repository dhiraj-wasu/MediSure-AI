def decide_mode(state, extracted):

    # Update state
    for k, v in extracted.items():
        if v:
            state[k] = v

    # Mode detection
    if extracted.get("reference_previous_order"):
        state["mode"] = "REFILL"

    elif extracted.get("has_prescription"):
        state["mode"] = "PRESCRIPTION"

    elif extracted.get("is_information_query"):
        state["mode"] = "INFO"

    elif extracted.get("symptoms"):
        state["mode"] = "OTC"

    return state


def required_fields(state):

    if state["mode"] == "PRESCRIPTION":
        if not state["prescription_uploaded"]:
            return "upload_prescription"

    if state["mode"] == "OTC":
        if not state["patient_name"]:
            return "patient_name"
        if not state["age_group"]:
            return "age_group"
        if not state["quantity"]:
            return "quantity"

    return None
