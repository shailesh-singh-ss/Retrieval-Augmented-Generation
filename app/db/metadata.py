from typing import List, Optional
from sqlmodel import select
from app.db.database import get_db
from app.db.models import DocumentModel

class MetadataDB:
    def insert_document(self, metadata: dict) -> DocumentModel:
        with get_db() as db:
            doc = DocumentModel(**metadata)
            db.add(doc)
            db.commit()
            db.refresh(doc)
            return doc

    def get_all_documents(self) -> List[DocumentModel]:
        with get_db() as db:
            result = db.exec(
                select(DocumentModel).order_by(DocumentModel.created_at.desc())
            )
            return result.all()

    def get_document_by_id(self, doc_id: str) -> Optional[DocumentModel]:
        with get_db() as db:
            return db.get(DocumentModel, doc_id)