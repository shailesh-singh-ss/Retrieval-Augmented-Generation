from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.documents import router as documents_router
from app.routes.queries import router as queries_router
from app.routes.health import router as health_router
from app.core.config import settings
from app.db.database import init_db

app = FastAPI(title=settings.app_name)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(documents_router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(queries_router, prefix="/api/v1/query", tags=["queries"])
app.include_router(health_router, prefix="/health", tags=["health"])

@app.on_event("startup")
async def on_startup():
    init_db()