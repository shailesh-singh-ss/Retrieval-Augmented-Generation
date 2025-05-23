from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List
import os
from app.schemas.documents import DocumentUploadResponse
from app.services.document_service import DocumentService
from app.core.config import settings

router = APIRouter()

@router.post(
    "/upload",
    response_model=List[DocumentUploadResponse],
    summary="Upload one or more documents (max {{settings.max_documents}})"
)
async def upload_documents(
    files: List[UploadFile] = File(..., description="Up to {max} files".format(max=settings.max_documents)),
    service: DocumentService = Depends()
) -> List[DocumentUploadResponse]:
    # 1) enforce max number of uploads
    if len(files) > settings.max_documents:
        raise HTTPException(
            status_code=400,
            detail=f"Can upload at most {settings.max_documents} documents at once."
        )

    responses: List[DocumentUploadResponse] = []

    for file in files:
        # basic validations
        if not file.filename:
            raise HTTPException(status_code=400, detail="One of the files has no filename")
        contents = await file.read()

        # enforce per‐file size limit
        if len(contents) > 100 * 1024 * 1024:
            raise HTTPException(status_code=413, detail=f"File {file.filename} too large")

        # process the document (this will raise if pages > settings.max_pages)
        metadata = await service.process_document(contents, file.filename)

        responses.append(DocumentUploadResponse(
            message="Document processed successfully",
            document_id=metadata.id,
            filename=metadata.filename,
            chunk_count=metadata.chunk_count
        ))

    return responses