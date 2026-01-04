import requests


class WeatherTool:
    def get_weather(self, city: str) -> dict:
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
