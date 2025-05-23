from typing import List, Dict
import os
import PyPDF2
from io import BytesIO
from app.processing.chunking import DocumentChunker
from app.core.config import settings

class DocumentLoader:
    def __init__(self):
        self.chunker = DocumentChunker()

    def load_pdf(self, file_bytes: bytes, filename: str) -> List[Dict]:
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            
            if len(pdf_reader.pages) > settings.max_pages:
                raise ValueError(f"Document exceeds maximum page limit of {settings.max_pages}")
            
            chunks = []
            for page_num, page in enumerate(pdf_reader.pages, start=1):
                text = page.extract_text()
                if text.strip():
                    page_chunks = self.chunker.chunk_document(text, filename)
                    for chunk in page_chunks:
                        chunk["page"] = page_num
                    chunks.extend(page_chunks)
            
            return chunks
        except Exception as e:
            raise Exception(f"Failed to load PDF: {str(e)}")

    def load_text(self, file_bytes: bytes, filename: str) -> List[Dict]:
        try:
            text = file_bytes.decode("utf-8")
            chunks = self.chunker.chunk_document(text, filename)
            for chunk in chunks:
                chunk["page"] = 1
            return chunks
        except Exception as e:
            raise Exception(f"Failed to load text file: {str(e)}")

    def load_document(self, file_bytes: bytes, filename: str) -> List[Dict]:
        if filename.lower().endswith('.pdf'):
            return self.load_pdf(file_bytes, filename)
        else:
            return self.load_text(file_bytes, filename)