import requests


class WeatherPluginClient:
    def __init__(self, base_url="http://localhost:3333"):
        self.base_url = base_url

    def get_weather(self, city: str):
        r = requests.get(f"{self.base_url}/weather", params={"city": city})
        r.raise_for_status()
        return r.json()

    def get_forecast(self, city: str, days: int = 3):
        r = requests.get(f"{self.base_url}/forecast",
                         params={"city": city, "days": days})
        r.raise_for_status()
        return r.json()
