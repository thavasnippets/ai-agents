import os
from openai import OpenAI

import os
import json
from openai import OpenAI


class OpenAILLM:
    def __init__(self, api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def parse_intent(self, user_input: str) -> dict:
        prompt = f"""
                    You are an intent classification and entity extraction engine.

                    User input:
                    "{user_input}"

                    Rules:
                    - Identify if the intent is about weather.
                    - If weather-related, extract the city.
                    - Respond ONLY in valid JSON.

                    Response format:
                    {{
                    "intent": "WEATHER" or "UNKNOWN",
                    "city": "city name or null"
                    }}
                """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You classify intent and extract entities."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return json.loads(response.choices[0].message.content)
