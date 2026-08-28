from google import genai
from config.config import GEMINI_API_KEY


class LLM:

    def __init__(self):
        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.model = "gemini-2.5-flash"

    def generate(self, prompt):

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt
        )

        return response.text