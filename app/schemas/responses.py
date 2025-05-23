from pydantic import BaseModel
from typing import List, Dict

class SourceInfo(BaseModel):
    source: str
    page: int

class QueryResponse(BaseModel):
    answer: str
    sources: List[SourceInfo]
    relevant_chunks: List[Dict]

class ChunkMetadata(BaseModel):
    source: str
    page: int
    chunk_id: int
    score: float
    text: str

class MetadataResponse(BaseModel):
    metadata: List[ChunkMetadata]