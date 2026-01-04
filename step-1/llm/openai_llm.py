import os
from openai import OpenAI


class OpenAILLM:
    def __init__(self, api_key=None, model="gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        print(self.api_key)
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found")

        self.client = OpenAI(api_key=self.api_key)
        self.model = model

    def extract_city(self, user_input: str) -> str:
        prompt = f"""
                    Extract the city name from the following user request.
                    Return ONLY the city name, nothing else.

                    User request:
                    "{user_input}"
                    """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You extract location names."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )

        return response.choices[0].message.content.strip()
