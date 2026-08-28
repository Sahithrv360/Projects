from openai import OpenAI
from config.config import OPENAI_API_KEY


class LLM:

    def __init__(self):
        self.client = OpenAI(
            api_key=OPENAI_API_KEY
        )

    def generate(self, messages):

        response = self.client.responses.create(
            model="gpt-5-mini",
            input=messages
        )

        return response.output_text