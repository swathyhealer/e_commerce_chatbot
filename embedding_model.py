from google import genai
from google.genai import types


class GeminiEmbeddingModel:
    def __init__(self):
        self.__client__ = genai.Client(
            api_key="AIzaSyAgRL_W_f3sh3nx3cJTj7cPj5PRXzmLDOg"
        )
        self.__config__ = types.EmbedContentConfig(output_dimensionality=10)

    def generate_embeddings(self, contents: list[str]):
        response = self.__client__.models.embed_content(
            model="text-embedding-004",
            contents=contents,
            config=self.__config__,
        )
        return response.embeddings[0].values
