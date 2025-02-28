from typing import Any
from vector_db import db_collection


def get_related_products(product_details: str, general: bool) -> str:
    # product_details: list[dict[str, str]], general: bool
    """
    Retrieves related products based on the given product details or general category queries.

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
        general (bool): A flag indicating whether the query is general (`True`) or product-specific (`False`).
    """
    print("product details:", product_details)

    print("general:", general)
    if str(general).lower() == "true":
        max_n_items = 3
    else:
        max_n_items = 1

    result = db_collection.get_matching_items(
        query_text=str(product_details), max_n_items=max_n_items
    )
    print("\nresult: ", result)
    return str(result)
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
