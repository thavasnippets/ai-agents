import re


class SimpleLLM():
    def extract_city(self, user_input: str) -> str:
        """
        Simulates LLM reasoning for city extraction
        """
        patterns = [
            r"weather in ([a-zA-Z\s]+)",
            r"forecast for ([a-zA-Z\s]+)",
            r"temperature in ([a-zA-Z\s]+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                return match.group(1).strip().title()

        # fallback: last word(s)
        tokens = user_input.split()
        return tokens[-1].title()
