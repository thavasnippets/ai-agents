from tools.weather_wttr import WeatherTool
from llm.llm_mock import SimpleLLM


class WeatherAgent:
    def __init__(self, llm: SimpleLLM, weather_tool: WeatherTool):
        self.llm = llm
        self.weather_tool = weather_tool

    def run(self, user_input: str) -> str:
        print(" Agent started")

        # Step 1: Intent check
        if "weather" not in user_input.lower():
            return "I handle only weather-related queries."

        # Step 2: LLM parsing
        city = self.llm.extract_city(user_input)
        print(f"LLM extracted city: {city}")

        # Step 3: Tool invocation
        data = self.weather_tool.get_weather(city)

        # Step 4: Reason & respond
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


llm = SimpleLLM()
weather_tool = WeatherTool()
agent = WeatherAgent(llm, weather_tool)

print(agent.run("Can you tell me the weather forecast in San Francisco"))
