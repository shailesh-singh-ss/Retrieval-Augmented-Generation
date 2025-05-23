import numpy as np
if not hasattr(np, 'float_'):
    np.float_ = np.float64
if not hasattr(np, 'int_'):
    np.int_ = np.int64
if not hasattr(np, 'uint'):
    np.uint = np.uint64

import chromadb
from chromadb.config import Settings
from app.core.config import settings

class ChromaDBClient:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection_name = "document_chunks"
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def store_documents(self, chunks, embeddings):
        documents = [chunk["text"] for chunk in chunks]
        metadatas = [
            {"source": chunk["source"], "page": chunk["page"], "chunk_id": chunk["chunk_id"]}
            for chunk in chunks
        ]
        ids = [chunk["id"] for chunk in chunks]

        return self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve_documents(self, query_embedding, n_results: int = 5):
        limit = n_results

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"]
        )

        docs, mds, scores = (
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )

        # zip, sort by score ascending, then take top‐K
        sorted_hits = sorted(
            zip(docs, mds, scores),
            key=lambda x: x[2]
        )[:limit]

        return [
            {
                "text": doc,
                "source": md["source"],
                "page": md["page"],
                "chunk_id": md["chunk_id"],
                "score": score
            }
            for doc, md, score in sorted_hits
        ]
    
    def clear_collection(self):
        """
        Delete all vectors (and their metadata) from the 'document_chunks' collection.
        """
        # If you omit both `ids` and `where`, ChromaDB will delete everything.
        self.client.delete_collection(name=self.collection_name)
        
        # 2) recreate it
        self.collection = self.client.get_or_create_collection(
            name=self.collection_name,
            metadata={"hnsw:space": "cosine"}
        )