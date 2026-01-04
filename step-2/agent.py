from tools.weather_wttr import WeatherTool
from llm.openai_llm import OpenAILLM


class WeatherAgent:
    def __init__(self):
        self.llm = OpenAILLM()
        self.weather_tool = WeatherTool()

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

        # Step 2: Tool invocation
        data = self.weather_tool.get_weather(city)

        # Step 3: Reason & respond
        current = data["current_condition"][0]
        temp = current["temp_C"]
        desc = current["weatherDesc"][0]["value"]
        feels = current["FeelsLikeC"]

        return (
            f"Weather in {city}\n"
            f"Temperature: {temp}°C\n"
            f"Feels Like: {feels}°C\n"
            f"Condition: {desc}"
        )


agent = WeatherAgent()

print(agent.run("i wanted to know the Bengalore weather"))
