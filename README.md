# Weather API

A REST API built with FastAPI that fetches real-time weather data from Visual Crossing, with Redis caching, rate limiting, and error handling.

## Features

- 🌤️ Real-time weather data from the [Visual Crossing API](https://www.visualcrossing.com/weather-api)
- ⚡ Redis caching with 12-hour expiration 
- 🛡️ Rate limiting (10 requests/minute per IP) via `slowapi`
- ❌ Error handling for invalid cities and unexpected failures
- 📄 Auto-generated API docs via FastAPI's built-in Swagger UI

## Stack

- **Python** + **FastAPI** — API framework
- **Redis** — In-memory caching
- **slowapi** — Rate limiting
- **requests** — HTTP client for Visual Crossing
- **python-dotenv** — Environment variable management

## Requirements

- Python 3.8+
- Redis running locally
- Visual Crossing API key ([visualcrossing.com](https://www.visualcrossing.com))

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/betancourt-ncs/weather-api.git
cd weather-api
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the root directory:

```
VISUAL_CROSSING_API_KEY=your_api_key_here
```

### 5. Start Redis

```bash
brew services start redis
```

### 6. Run the server

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

## Usage

### Get weather for a city

```bash
GET /weather?city={city}
```

**Example:**

```bash
curl "http://localhost:8000/weather?city=Miami"
```

**Response:**

```json
{
  "City": "Miami",
  "Temperature": 83.2,
  "Conditions": "Partially cloudy",
  "Humidity": 73.6,
  "Date": "2026-05-22",
  "Feels like": 89.5,
  "Precipitation": 0.0,
  "UV Index": 9.0,
  "Sunrise": "06:32:08",
  "Sunset": "20:03:22"
}
```

### Interactive docs

Visit `http://localhost:8000/docs` for the auto-generated Swagger UI where you can test the endpoint directly in your browser.

## Error Handling

| Status Code | Description |
|-------------|-------------|
| `200` | Successful response |
| `404` | City not found |
| `429` | Rate limit exceeded (10 requests/minute) |
| `500` | Internal server error |

## Caching

Weather data is cached in Redis using the city name as the key, with a 12-hour TTL. Subsequent requests for the same city within that window are served from cache without hitting the Visual Crossing API.

To verify a cached entry:

```bash
redis-cli get "Miami"
```
