from plugin_client.weather_client import WeatherPluginClient
from llm.openai_llm import OpenAILLM


class WeatherAgent:
    def __init__(self):
        self.llm = OpenAILLM()
        self.weather_plugin = WeatherPluginClient()

    def run(self, user_input: str) -> str:
        print("Agent started")

        # Step 1: LLM intent + entity parsing
        parsed = self.llm.parse_intent(user_input)
        intent = parsed.get("intent")
        city = parsed.get("city")

        if intent != "WEATHER":
            return "I can only help with weather-related requests."

        if not city:
            return " Please specify a city."

       # Decide if forecast is needed
        if "forecast" in user_input.lower() or "next" in user_input.lower():
            data = self.weather_plugin.get_forecast(city, days=3)
            result = f"3-Day Forecast for {city}:\n"
            for day in data["forecast_days"]:
                result += (
                    f"{day['date']}: {day['condition']}, "
                    f"{day['min_temp_c']}°C - {day['max_temp_c']}°C, "
                    f"Avg: {day['avg_temp_c']}°C\n"
                )
            return result
        else:
            data = self.weather_plugin.get_weather(city)
            return (
                f"Current Weather in {city}:\n"
                f"Temperature: {data['temperature_c']}°C\n"
                f"Feels Like: {data['feels_like_c']}°C\n"
                f"Condition: {data['condition']}\n"
                f"Humidity: {data['humidity']}%"
            )


agent = WeatherAgent()
print(agent.run("i wanted to know the Bengalore weather"))
print(agent.run("i wanted to know the North wales  weather for next 2 days"))
