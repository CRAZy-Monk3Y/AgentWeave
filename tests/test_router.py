from graph.router import route_question

def test_weather_route():
    state = {"question": "What is the weather in Mumbai?"}
    assert route_question(state) == "weather"

def test_rag_route():
    state = {"question": "Explain the document summary"}
    assert route_question(state) == "rag"
