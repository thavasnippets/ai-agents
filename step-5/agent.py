from plugin_client.advice_plugin import AdvicePluginClient
from plugin_client.weather_plugin import WeatherPluginClient
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import semantic_kernel as sk
import os
import json
import asyncio
from openai import OpenAI

HISTORY_FILE = "weather_history.json"


class WeatherAgent:
    def __init__(self, openai_api_key: str = None):
        self.kernel = sk.Kernel()

        if openai_api_key is None:
            openai_api_key = os.getenv("OPENAI_API_KEY")

        self.client = OpenAI(api_key=openai_api_key)

        # LLM Service
        self.llm_service = OpenAIChatCompletion(
            service_id="openai",
            # api_key=openai_api_key,
            ai_model_id='gpt-4o-mini'
        )
        # Add OpenAI LLM service
        self.kernel.add_service(self.llm_service)

        # Register SK plugins (skills)
        self.kernel.add_plugin(WeatherPluginClient(), plugin_name="weather")
        self.kernel.add_plugin(AdvicePluginClient(), plugin_name="advice")
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                self.history = json.load(f)
        else:
            self.history = []

    def _save_history(self, user_input: str, response: str, city: str):
        entry = {"user_input": user_input, "response": response, 'city': city}
        self.history.append(entry)
        with open(HISTORY_FILE, "w") as f:
            json.dump(self.history, f, indent=2)

    def _get_last_city(self):
        for entry in reversed(self.history):
            if entry.get("city"):
                return entry["city"]
        return None

    def plan_weather_request(self, user_input: str) -> dict:

        prompt = f"""
            You are an assistant that extracts structured JSON from user requests.
            User request: "{user_input}"

            Return ONLY a valid JSON object with these keys:
            - "function": either "get_current_weather" or "get_forecast"
            - "city": the city name
            - "days": number of days for forecast (default 3 if not specified)

            EXAMPLE OUTPUT:
            {{"function":"get_forecast","city":"Seattle","days":3}}

            IMPORTANT: Do not include any explanation or text outside the JSON.
            """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        text = response.choices[0].message.content
        print(text)
        try:
            return json.loads(text)
        except:

            return {"function": "get_current_weather", "city": None, "days": 3}

    async def run(self, user_input: str) -> dict:
        """Execute the weather agent for a user query."""
        plan = self.plan_weather_request(user_input)
        func_name = plan.get("function")
        city = plan.get("city")
        days = plan.get("days", 3)

        if not city:
            city = self._get_last_city()
            if not city:
                response_text = "City not detected — please specify a city."
                self._save_history(user_input, response_text, city=city)
                return {"city": None, "function_called": func_name, "result": response_text}

        # Call weather function
        if func_name == "get_current_weather":
            weather_result = await self.kernel.invoke(
                self.kernel.plugins["weather"]["current_weather"],
                city=city
            )
        else:
            weather_result = await self.kernel.invoke(
                self.kernel.plugins["weather"]["forecast"],
                city=city,
                days=days
            )

        # Call advice plugin
        advice_result = await self.kernel.invoke(
            self.kernel.plugins["advice"]["give_advice"],
            weather_text=weather_result
        )

        return {
            "city": city,
            "function_called": func_name,
            "weather": weather_result.value,
            "advice": advice_result.value
        }


async def main():
    agent = WeatherAgent()

    response1 = await agent.run("I want to know the New york  weather")
    print(response1)

    response3 = await agent.run("I want to know the weather for next 2 days")
    print(response3)

    response2 = await agent.run("I want to know the North Wales weather for next 2 days")
    print(response2)


if __name__ == "__main__":
    asyncio.run(main())
