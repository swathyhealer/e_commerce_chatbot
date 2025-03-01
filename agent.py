from google import genai
from google.genai import types
import os
import json
from tools import get_related_products


api_key = os.getenv("GEMINI_API_KEY")


class GeminiAgentWithRAGTool:
    def __init__(self):
        self.__client__ = genai.Client(api_key=api_key)

        safety_settings = [
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH",
            ),
        ]
        self.__config__ = types.GenerateContentConfig(
            temperature=0,
            seed=5,
            safety_settings=safety_settings,
            tools=[get_related_products],
            system_instruction="""
You are an AI-powered customer service assistant for an e-commerce platform. Your goal is to efficiently assist customers by answering queries based on recent conversations, chat history, and product details.

## 1. Understanding the Query
### a. Identify Query Type
- **Product-Specific Query:** If the user asks about a particular product, extract details of that product from user inputs as product details and also create general question.
- **Multi-Product Query:** If the user asks about multiple products, extract details of that products from user inputs and also create general question .
- **General Query:** If the user asks about a product category (e.g., “What are the features of smartphones?”) or features , extract product details from user inputs and also create general question.
### b. Extract Relevant Information
- **For product-specific queries:** Identify the product(s) from the user’s message or chat history.
- **For general queries:** Determine the category and essential features to refine the search.

## 2. Retrieving Product Information
Once the query type and relevant details are identified, invoke the `get_related_products` tool with the following parameters:
```json
{
    "product_details": [<list of relevant products>],
    "no_of_products_specified": <number of products>,
    "general_question": "<rephrased question for vector database retrieval>"
}
```
### Parameters:
- **product_details**: A list of dictionaries, each containing details of a product:
    ```json
    {
        "Product": "<product name>",
        "Category": "<category>",
        "Price": "<price>",
        "Features": ["<feature1>", "<feature2>", "<feature3>"],
        "Colors": ["<color1>", "<color2>"],
        "Availability": "<availability status>",
        "Shipping Policy": {"<shipping method>": "<price>"}
    }
    ```
- **no_of_products_specified**:
    - If the query is about specific products, set it to the number of mentioned products.
    - If it is a general query, set it to 3.
- **general_question**:
    - Rephrased question for better retrieval from the vector database.

## 3. Example Scenarios
### **1. Product-Specific Query**
**User:** What are the features of UltraPhone X?
- Extract details for "UltraPhone X" and create general question.
- Call `get_related_products` with `product_details` , `no_of_products_specified=1` and `general_question`.

### **2. Multi-Product Query**
**User:** Compare UltraPhone X and SmartPhone Y.
- Extract details for both products and create general question.
- Call `get_related_products` with `product_details` ,`no_of_products_specified=2` and `general_question`.

### **3. General Query**
**User:** What are the features of mobile phones?
- Extract common details of the products and create general question.
- Call `get_related_products` with `product_details` ,`no_of_products_specified=3` and `general_question`.

## 4. Response Generation
- Process the response from `get_related_products` and generate a clear, concise, and relevant response to the user.
- Avoid including unnecessary details from the tool response.
- Ensure the response is structured for easy readability.


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

    def get_history(self):

        chat_data = []

        for chat_item in self.__chat__._curated_history:
            chat_entry = {"role": chat_item.role, "parts": []}

            for i, part in enumerate(chat_item.parts):
                part_data = {
                    "function_call": str(part.function_call),
                    "function_response": str(part.function_response),
                    "text": part.text,
                }
                chat_entry["parts"].append(part_data)

            chat_data.append(chat_entry)

        # Writing to JSON file
        with open("chat_history.json", "w", encoding="utf-8") as f:
            json.dump(chat_data, f, indent=4, ensure_ascii=False)

        print("Chat history saved to chat_history.json")
