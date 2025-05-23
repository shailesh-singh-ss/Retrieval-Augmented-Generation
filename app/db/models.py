from datetime import datetime
from sqlmodel import SQLModel, Field

class DocumentModel(SQLModel, table=True):
    id:       str     = Field(primary_key=True, index=True)
    filename: str
    chunk_count: int
    page_count:  int
    created_at: datetime = Field(default_factory=datetime.utcnow)