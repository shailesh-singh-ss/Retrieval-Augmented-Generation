from fastapi import Depends
from app.db.chromadb import ChromaDBClient
from app.core.embeddings import EmbeddingModel
from app.core.llm import GeminiLLM
from typing import Dict
from typing import List, Dict

# will hold the last retrieved chunks
latest_relevant_chunks: List[Dict] = []

class QueryService:
    def __init__(self):
        self.embedding_model = EmbeddingModel()
        self.chroma_db = ChromaDBClient()
        self.llm = GeminiLLM()

    async def process_query(self, query: str) -> Dict:
        # Generate query embedding
        query_embedding = self.embedding_model.generate_embeddings([query])[0]
        
        # Retrieve relevant documents
        retrieved_docs = self.chroma_db.retrieve_documents(query_embedding)
        
        # -- store for metadata endpoint --
        latest_relevant_chunks.clear()
        latest_relevant_chunks.extend(retrieved_docs)

        # Generate response
        context = [doc["text"] for doc in retrieved_docs]
        answer = self.llm.generate_response(query, context)
        
        # Prepare sources
        sources = [
            {
                "source": doc["source"],
                "page": doc["page"]
            }
            for doc in retrieved_docs
        ]
        
        return {
            "answer": answer,
            "sources": sources,
            "relevant_chunks": retrieved_docs
        }