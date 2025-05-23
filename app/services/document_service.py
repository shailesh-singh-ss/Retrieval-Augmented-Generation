from typing import List
from fastapi import Depends
from app.db.chromadb import ChromaDBClient
from app.db.metadata import MetadataDB
from app.processing.document_loader import DocumentLoader
from app.core.embeddings import EmbeddingModel
from app.schemas.documents import DocumentMetadata
import uuid

class DocumentService:
    def __init__(self):
        self.loader = DocumentLoader()
        self.embedding_model = EmbeddingModel()
        self.chroma_db = ChromaDBClient()
        self.metadata_db = MetadataDB()

    async def process_document(self, file_bytes: bytes, filename: str) -> DocumentMetadata:
        
        # clear out ANY existing vectors
        self.chroma_db.clear_collection()

        # Load and chunk document
        chunks = self.loader.load_document(file_bytes, filename)
        
        # Generate embeddings
        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.generate_embeddings(texts)
        
        # Prepare documents for storage
        doc_id = str(uuid.uuid4())
        # assign a unique index across ALL chunks
        for idx, chunk in enumerate(chunks):
            chunk["chunk_id"] = idx
            chunk["id"]       = f"{doc_id}_{idx}"
        
        # Store in vector DB
        self.chroma_db.store_documents(chunks, embeddings)
        
        # Store metadata
        metadata = {
            "id": doc_id,
            "filename": filename,
            "chunk_count": len(chunks),
            "page_count": max(chunk["page"] for chunk in chunks) if chunks else 0
        }
        # sync call now
        self.metadata_db.insert_document(metadata)

        # return Pydantic model so .id/.filename attrs work
        return DocumentMetadata(**metadata)

    def get_all_documents(self) -> List[DocumentMetadata]:
        raw = self.metadata_db.get_all_documents()
        return [DocumentMetadata.from_orm(d) for d in raw]