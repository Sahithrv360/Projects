from agent.agent import Agent


def main():

    agent = Agent()

    print("==============================")
    print("        MINI AGENT v0.1")
    print("==============================")
    print("Type 'exit' to quit.\n")

    while True:

        user_input = input("You: ")

        if user_input.lower() == "exit":
            break

        response = agent.run(user_input)

        print("AI:", response)
        print()


if __name__ == "__main__":
    main()