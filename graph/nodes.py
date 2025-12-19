from datetime import datetime
from rag.qa import rag_answer
from tools.weather import fetch_weather, extract_city
from llm.model import get_llm


llm = get_llm()


def start_node(state):
    # Entry point node
    return {}


def weather_node(state):
    city = extract_city(state["question"])

    if not city:
        return {"answer": "Please specify a city for weather information."}
    try:
        weather_data = fetch_weather(city)
    except Exception as e:
        print("Error while fetching weather", e)
        return {"answer": f"Could not find weather forcust for {city}"}

    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""
    ROLE: You are a Weather Expert and Today's date is {today}. 
    TASK: Given the following weather data, summarize it in a short, user-friendly way. Higlight the key wether phenomenons and give your precautionary advice for the user also for the said location.
    Weather data:
    {weather_data}

    STRICTLY GIVE the outcome only don't explain or provide any justification.
    """
    
    response = llm.invoke(prompt)

    return {"answer": response.content}


def rag_node(state):
    answer, sources, chunks = rag_answer(state["question"])

    return {"answer": answer, "sources": list(set(sources)), "chunks": chunks}
