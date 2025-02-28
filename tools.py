from typing import Any
from vector_db import db_collection


def get_related_products(product_details: str, no_of_products_specified: int) -> str:
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
            - If the query is general, set it to 5.
    """
    print("product details:", product_details)
    print("type product details:", type(product_details))
    # try:
    #     product_details=product_details.to_list()
    #     print("list of prd:",product_details)
    # except Exception as e:
    #     print("exception:",e)

    print("no of products:",no_of_products_specified)

    results=db_collection.get_matching_items(
                query_text=str(product_details), max_n_items=no_of_products_specified+1
            )

    print("\nresult: ", results)
    return str(results)
    # return str( {
    #         "Product": "Omega 4K OLED TV",
    #         "Category": "Smart TV",
    #         "Price": "$990",
    #         "Features": ["50\" 4K OLED display", "Dolby Vision", "AI-powered upscaling"],
    #         "Colors": ["Black", "Gray"],
    #         "Availability": "Limited stock",
    #         "Shipping Policy": {
    #             "Standard Shipping (5-7 business days)": "$22.99",
    #             "Express Shipping (2-3 business days)": "$47.99",
    #             "Free Standard Shipping on Orders Over": "$500"
    #         }
    #     })
