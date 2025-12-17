def generate_response(messages):
    for m in reversed(messages):
        if m.get("role") == "user":
            return f"Faesh engine heard: {m.get('content')}"
    return "Faesh engine is ready."
