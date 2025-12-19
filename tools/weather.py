import os
import requests
import string
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def extract_city(question: str) -> str:
    words = question.lower().split()
    for i, word in enumerate(words):
        if word == "in" and i + 1 < len(words):
            city = words[i + 1]
            return city.strip(string.punctuation).capitalize()
    return ""


def fetch_weather(city: str) -> dict:
    if not city:
        raise ValueError("City name is required")

    params = {
        "q": city,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()
