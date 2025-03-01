import ast
from typing import Any
from vector_db import db_collection


def get_related_products(
    product_details: str, no_of_products_specified: int, general_question: str
) -> str:
    # product_details: list[dict[str, str]], general: bool
    """
    Retrieves related products based on the given product details and no_of_products_specified.

    Args:
        product_details (List[Dict[str, Any]]): A list of dictionaries, each containing details about a product.
            Each dictionary follows the structure:
            {
                "Product": str,        # Product name
                "Category": str,       # Category of the product
                "Price": str,          # Price of the product
                "Features": List[str], # List of product features
                "Colors": List[str],   # Available colors
                "Availability": str,   # Stock status (e.g., "In stock", "Out of stock")
                "Shipping Policy": Dict[str, str]  # Shipping details
            }
        no_of_products_specified (int):
            - The number of products relevant to the user's query.
            - If the query is product-specific, set it to the number of specified products.
            - If the query is general, set it to 3.
        general_question (str):
            - A rephrased query for retrieving general product details from the vector database.
    """

    try:
        product_details = ast.literal_eval(product_details)
        results = []
        if len(product_details) == 1 and no_of_products_specified > 1:
            # complete general question
            max_n_items = no_of_products_specified
        else:
            # multiple product items related question or single product related question
            max_n_items = 1

        for single_prd in product_details:
            new_result = db_collection.get_matching_items(
                query_text=str(single_prd), max_n_items=max_n_items
            )[0]
            results.extend(new_result)
    except (SyntaxError, ValueError) as e:
        print(f"Error parsing string: {e}")
        results = db_collection.get_matching_items(
            query_text=str(product_details), max_n_items=no_of_products_specified
        )[0]

    # general_result=db_collection.get_matching_items(
    #             query_text=general_question, max_n_items=no_of_products_specified
    #         )[0]
    # print("\n\n\nprd results:",results)
    # print("\n\n\ngen results:",general_result)
    # results.extend(general_result)
    # results=list(set(results))

    return str(results)
