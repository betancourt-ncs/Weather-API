import requests
from fastapi import FastAPI
from dotenv import load_dotenv
import os

app = FastAPI()

load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


@app.get("/weather")
def get_weather(city: str):
    response = requests.get(f"{BASE_URL}{city}?key={API_KEY}")
    data = response.json()

    city_name = data["resolvedAddress"]
    temperature = data["days"][0]["temp"]
    conditions = data["days"][0]["conditions"]
    humidity = data["days"][0]["humidity"]
    date = data["days"][0]["datetime"]
    feels_like = data["days"][0]["feelslike"]
    precipitation = data["days"][0]["precip"]
    uv_index = data["days"][0]["uvindex"]
    sunrise = data["days"][0]["sunrise"]
    sunset = data["days"][0]["sunset"]

    weather_info = {
        "City": city_name,
        "Temperature": temperature,
        "Conditions": conditions,
        "Humidity": humidity,
        "Date": date,
        "Feels like": feels_like,
        "Precipitation": precipitation,
        "UV Index": uv_index,
        "Sunrise": sunrise,
        "Sunset": sunset
    }

    return weather_info
