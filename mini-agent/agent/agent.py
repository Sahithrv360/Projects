from llm.model import LLM


class Agent:

    def __init__(self):
        self.llm = LLM()

    def run(self, user_input):

        messages = [
            {
                "role": "system",
                "content": "You are Mini Agent, a helpful AI assistant."
            },
            {
                "role": "user",
                "content": user_input
            }
        ]

        return self.llm.generate(messages)