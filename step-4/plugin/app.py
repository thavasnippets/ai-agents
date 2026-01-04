from fastapi import FastAPI, Query
import requests

app = FastAPI(title="Weather Plugin with Forecast")

# Current weather


@app.get("/weather")
def get_weather(city: str = Query(..., description="City name")):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=5, verify=False)
    response.raise_for_status()
    current = response.json()["current_condition"][0]

    return {
        "city": city,
        "temperature_c": current["temp_C"],
        "feels_like_c": current["FeelsLikeC"],
        "condition": current["weatherDesc"][0]["value"],
        "humidity": current["humidity"]
    }

# Forecast for multiple days


@app.get("/forecast")
def get_forecast(city: str = Query(..., description="City name"),
                 days: int = Query(3, description="Number of forecast days")):
    url = f"https://wttr.in/{city}?format=j1"
    response = requests.get(url, timeout=5, verify=False)
    response.raise_for_status()
    data = response.json()
    forecast_data = []

    for i, day in enumerate(data["weather"][:days]):
        forecast_data.append({
            "date": day["date"],
            "max_temp_c": day["maxtempC"],
            "min_temp_c": day["mintempC"],
            "avg_temp_c": day["avgtempC"],
            # around mid-day
            "condition": day["hourly"][4]["weatherDesc"][0]["value"],
        })

    return {
        "city": city,
        "forecast_days": forecast_data
    }
