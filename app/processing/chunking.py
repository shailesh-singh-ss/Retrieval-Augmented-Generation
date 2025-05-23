from typing import List, Dict
import re
from app.core.config import settings

class DocumentChunker:
    def __init__(self):
        self.chunk_size = settings.chunk_size
        self.chunk_overlap = settings.chunk_overlap

    def chunk_document(self, text: str, source: str) -> List[Dict]:
        try:
            # Split by paragraphs first
            paragraphs = re.split(r'\n\s*\n', text)
            chunks = []
            current_chunk = ""
            
            for para in paragraphs:
                if len(current_chunk) + len(para) <= self.chunk_size:
                    current_chunk += para + "\n\n"
                else:
                    if current_chunk:
                        chunks.append(current_chunk.strip())
                    
                    # Handle overlap
                    if self.chunk_overlap > 0 and chunks:
                        last_chunk = chunks[-1]
                        overlap_start = max(0, len(last_chunk) - self.chunk_overlap)
                        current_chunk = last_chunk[overlap_start:] + "\n\n" + para
                    else:
                        current_chunk = para + "\n\n"
            
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            
            # Prepare chunks with metadata
            chunk_objects = []
            for i, chunk in enumerate(chunks):
                chunk_objects.append({
                    "text": chunk,
                    "source": source,
                    "page": 1,  # Will be updated by document loader
                    "chunk_id": i
                })
                
            return chunk_objects
        except Exception as e:
            raise Exception(f"Failed to chunk document: {str(e)}")