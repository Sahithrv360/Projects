from google import genai
from config.config import GEMINI_API_KEY


class LLM:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = "gemini-3.6-flash"

    def generate(self, prompt):

        interaction = self.client.interactions.create(
            model=self.model,
            input=prompt
        )

        return interaction.output_text