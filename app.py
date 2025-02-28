# from embedding_model import GeminiEmbeddingModel
# from agent import chat_agent
# from vector_db import db_collection
# Run the CLI chatbot
from agent import GeminiAgentWithRAGTool


def run_agent():

    chat_agent = GeminiAgentWithRAGTool()
    # embedding_model=GeminiEmbeddingModel()
    # res=embedding_model.generate_embeddings(['why is the sky blue?'])
    # print("res")
    # print(res)
    # print(res.embeddings[0].values)
    # print(res.keys())
    # print(res.get('embedding', None))
    # print(res[0].values)
    # return res
    # qa_chain = create_retrieval_agent()
    print("Customer Support AI (Type 'exit' to quit)")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            print("Goodbye!")
            break
        response = chat_agent.send_msg(query)
        # response = qa_chain.run(query)
        print("customer service specialist :", response)


if __name__ == "__main__":
    run_agent()
