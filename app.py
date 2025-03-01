from agent import GeminiAgentWithRAGTool


def run_agent():

    chat_agent = GeminiAgentWithRAGTool()

    print("Customer Support AI (Type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_agent.send_msg(query)

        print("customer service specialist :", str(response))

    print(
        "\n\n\n end---------------------------------------------------------------------------"
    )
    chat_agent.get_history()


if __name__ == "__main__":
    run_agent()
