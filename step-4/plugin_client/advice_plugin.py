
from semantic_kernel.functions import kernel_function


class AdvicePluginClient:

    @kernel_function(
        name="give_advice",
        description="Give advice based on weather text"
    )
    def give_advice(self, weather_text: str) -> str:
        if "rain" in weather_text.lower():
            return "Carry an umbrella."
        if "cold" in weather_text.lower():
            return "Wear warm clothes."
        return "Weather looks fine."
