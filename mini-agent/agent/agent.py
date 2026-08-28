from llm.model import LLM


class Agent:

    def __init__(self):
        self.llm = LLM()

    def run(self, user_input):

        prompt = f"""
You are Mini Agent, a helpful AI assistant.

User:
{user_input}
"""

        return self.llm.generate(prompt)