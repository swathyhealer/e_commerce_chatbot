import chromadb
import json
import time
from embedding_model import GeminiEmbeddingModel


class ChromaVectorDB:
    def __init__(self, emb_model):
        self.__client__ = chromadb.PersistentClient(path="./chroma_db")
        self.__emb_model__ = emb_model
        self.collection = None

    def create_collection(self, collection_name):
        self.collection = self.__client__.get_or_create_collection(name=collection_name)

    def update_collection(self, docs: list[dict]):
        for i, doc in enumerate(docs):
            doc_str = json.dumps(doc)
            embedding = self.__emb_model__.generate_embeddings([doc_str])

            self.collection.add(
                ids=[str(i)], embeddings=[embedding], documents=[doc_str]
            )
            time.sleep(1)  # to avoid the quota error
        print("updated collection")

    def get_matching_items(self, query_text, max_n_items):
        query_embedding = self.__emb_model__.generate_embeddings([query_text])

        query_result = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=max_n_items,
            # where={"metadata_field": "is_equal_to_this"},
            # where_document={"$contains":"search_string"}
        )
        doc_strs = query_result.get("documents", [])
        return doc_strs


def vector_db_setup(collection_name, product_json_path):
    print("vector db setup initiated!!!!!")

    with open(product_json_path, "r") as f:
        data = json.load(f)
    prds = data["products"]
    vec_db = ChromaVectorDB(emb_model=GeminiEmbeddingModel())
    vec_db.create_collection(collection_name=collection_name)
    # vec_db.update_collection(docs=prds)
    return vec_db


db_collection = vector_db_setup(
    collection_name="sample2", product_json_path="data/product_data.json"
)
# d= {

#             "Category": "Smart TV",
#             "Features":["4k display"],
#             "Colours":["gray"]
#         }
# print(db_collection.get_matching_items(query_text="Can you show me some LG 4K Smart TV with 4k display",max_n_items=2))
# result = vec_db.get_matching_items(
#     str(
#         {
#             "Product": "UltraPhone X",
#             # "Category": "Mobile",
#             # "Price": "$799",
#             # "Features": ["6.5\" OLED display", "128GB storage", "12MP camera"],
#             # # "Colors": ["Black", "Silver", "Blue"],
#             # # "Availability": "In stock",
#             # # "Shipping Policy": {
#             # #     "Standard Shipping (3-5 business days)": "$4.99",
#             # #     "Express Shipping (1-2 business days)": "$12.99",
#             # #     "Free Standard Shipping on Orders Over": "$50"}
#         }
#     ),
#     max_n_items=2,
# )
# print(result)
