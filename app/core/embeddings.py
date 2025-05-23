from typing import List
import google.generativeai as genai
from app.core.config import settings

class EmbeddingModel:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = settings.embedding_model

    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        try:
            result = genai.embed_content(
                model=self.model,
                content=texts,
                task_type="RETRIEVAL_DOCUMENT"
            )
            return result['embedding']
        except Exception as e:
            raise Exception(f"Failed to generate embeddings: {str(e)}")