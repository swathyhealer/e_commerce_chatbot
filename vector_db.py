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
        self.collection = self.__client__.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"}
        )

    def update_collection(self, docs: list[dict]):
        for i, doc in enumerate(docs):
            doc_str = json.dumps(doc)
            embedding = self.__emb_model__.generate_embeddings([doc_str])

            self.collection.upsert(
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
    print("Please wait for the vector database setup to complete!!!!!")

    with open(product_json_path, "r") as f:
        data = json.load(f)
    prds = data["products"]
    vec_db = ChromaVectorDB(emb_model=GeminiEmbeddingModel())
    vec_db.create_collection(collection_name=collection_name)
    vec_db.update_collection(docs=prds)
    print("completed setup!!!")
    return vec_db


db_collection = vector_db_setup(
    collection_name="sample1111", product_json_path="data/product_data.json"
)
# print("count:",db_collection.collection.count())
