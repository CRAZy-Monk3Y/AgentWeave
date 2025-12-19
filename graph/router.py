def route_question(state):
    question = state["question"].lower()

    weather_keywords = [
        "weather",
        "temperature",
        "rain",
        "forecast",
        "climate",
        "humidity"
    ]

    if any(word in question for word in weather_keywords):
        return "weather"

    return "rag"
