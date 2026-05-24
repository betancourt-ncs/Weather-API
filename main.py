import requests
from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
import os
import redis
import json
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)

app = FastAPI()
redis_client = redis.Redis(host='localhost', port=6379)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

load_dotenv()
API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")

BASE_URL = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"


@app.get("/weather")
@limiter.limit("10/minute")
def get_weather(request: Request, city: str):
    try:
        cache_key = city
        cached_data = redis_client.get(cache_key)
        if cached_data:
            weather_data = json.loads(cached_data)
            return weather_data

        else:
            response = requests.get(f"{BASE_URL}{city}?key={API_KEY}")

            if response.status_code != 200:
                raise HTTPException(404, "City not found")

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

            redis_client.setex(cache_key, 43200, json.dumps(weather_info))

            return weather_info

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(500, "Internal server error")
