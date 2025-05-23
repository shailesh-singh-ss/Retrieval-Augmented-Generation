from fastapi import APIRouter, HTTPException, Depends
from app.schemas.queries import QueryRequest
from app.schemas.responses import MetadataResponse, ChunkMetadata, QueryResponse
from app.services.query_service import QueryService, latest_relevant_chunks


router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def process_query(request: QueryRequest, 
                       service: QueryService = Depends()):
    try:
        response = await service.process_query(request.query)
        return {
            "answer": response["answer"],
            "sources": response["sources"],
            "relevant_chunks": response["relevant_chunks"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metadata", response_model=MetadataResponse)
async def get_query_metadata():
    try:
        
        hits = latest_relevant_chunks

        # 3) map to ChunkMetadata
        metadata = [
            ChunkMetadata(
                source=hit["source"],
                page=hit["page"],
                chunk_id=hit["chunk_id"],
                score=hit["score"],
                text=hit["text"]
            )
            for hit in hits
        ]
        return MetadataResponse(metadata=metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))