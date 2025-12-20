from datetime import datetime
import streamlit as st
from rag.vectorstore import load_vectorstore
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
    kb_id = st.session_state.get("current_kb")

    if not kb_id:
        return {"answer": "Please upload or select a knowledge base first."}

    vectorstore = load_vectorstore(kb_id)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

    docs = retriever.invoke(state["question"])
    context = "\n\n".join(d.page_content for d in docs)

    prompt = f"""
Answer the question using only the context below.

Context:
{context}

Question:
{state["question"]}
"""

    try:
        response = llm.invoke(prompt)
        answer = response.content
    except Exception:
        answer = "I can’t help with that request due to safety guidelines."

    return {
        "answer": answer,
        "chunks": [d.page_content for d in docs],
        "sources": list({d.metadata.get("source") for d in docs}),
    }
