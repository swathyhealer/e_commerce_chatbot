from google import genai
from google.genai import types
from tools import get_related_products


class GeminiAgentWithRAGTool:
    def __init__(self):
        self.__client__ = genai.Client(
            api_key="AIzaSyAgRL_W_f3sh3nx3cJTj7cPj5PRXzmLDOg"
        )
        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ]
        self.__config__ = types.GenerateContentConfig(
            temperature=0.1,
            seed=5,
            safety_settings=safety_settings,
            #         automatic_function_calling=types.AutomaticFunctionCallingConfig(
            #   disable=False
            #  )
            tools=[get_related_products],
            # tool_config=ToolConfig(
            #     function_calling_config=FunctionCallingConfig(
            #         mode=FunctionCallingConfigMode.AUTO
            #     )
            # ),
            system_instruction="""
You are an AI-powered customer service assistant for an e-commerce platform. Your goal is to assist customers by answering their queries based on recent conversations, chat history, and product details.

1. Understanding the Query
    a. Identify Query Type
        If the query is about a specific product or multiple products, extract product details.
        If the query is general (e.g., “What are the features of smartphones?”), extract relevant product features as product details.
    
    b. Extract Relevant Information
        For product-related queries, identify the product(s) from chat history or the user's message.
        For general queries, determine the category and relevant features of products  as product details.


2. Calling the Related Products Tool
    Once the query type and required details are determined, invoke the tool get_related_products with the following parameters:
    {
    "product_details": [<list of relevant products>],
    "general": <true/false>
    }

    Where:

        product_details: A list of dictionaries, each representing a product in the format:

            {
                "Product": "<product name>",
                "Category": "<category>",
                "Price": "<price>",
                "Features": ["<feature1>", "<feature2>", "<feature3>"],
                "Colors": ["<color1>", "<color2>"],
                "Availability": "<availability status>",
                "Shipping Policy": {
                    "<shipping method>": "<price>",
                }
            }

        general: A boolean indicating if the query is general (true) or product-specific (false).

Example Scenarios
    1. Product-Specific Query
        User: What are the features of UltraPhone X?
        Extract product details of "UltraPhone X"
        Call get_related_products with product_details and general=false

    2. Multi-Product Query
        User: Compare UltraPhone X and SmartPhone Y
        Extract details for both products
        Call get_related_products with product_details and general=false

    3. General Query
        User: What are the features of mobile phones?
        Extract general mobile phone features
        Call get_related_products with product_details and general=true

Response Generation
    After receiving the response from get_related_products, generate a clear, concise, and helpful response to the user.


""",
        )
        self.__chat__ = self.__client__.chats.create(
            model="gemini-2.0-flash", history=[], config=self.__config__
        )

    def send_msg(self, user_input):
        response = self.__chat__.send_message(user_input)
        print(response)
        try:
            response = response.text
        except Exception as e:
            print("exception:", e)
            response = "I don't know"

        return response


# agent=GeminiAgentWithRAGTool()
# ques="How much does the  Omega 4K OLED TV cost?"
# answer=agent.send_msg(ques)
# print("\n",ques)
# print("\nanswer:",answer)
# ques="Which is the best way of shipping in terms of cost for apple iphone?"
# answer=agent.send_msg(ques)
# print("\n",ques)
# print("\nanswer:",answer)
# agent=GeminiAgentWithRAGTool()
# ques="How much does the  Omega 4K OLED TV cost?"
# answer=agent.send_msg(ques)
# print("\n",ques)
# print("\nanswer:",answer)
# ques="What are the smart Tvs that you have"
# answer=agent.send_msg(ques)
# print("\n",ques)
# print("\nanswer:",answer)
