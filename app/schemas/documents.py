from pydantic import BaseModel
from typing import List

class DocumentMetadata(BaseModel):
    id: str
    filename: str
    chunk_count: int
    page_count: int

    class Config:
        orm_mode = True

class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    filename: str
    chunk_count: int