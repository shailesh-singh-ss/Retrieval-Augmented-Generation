from pydantic import BaseSettings, Field

class Settings(BaseSettings):
    app_name: str = "RAG Pipeline"
    chroma_host: str = Field(default="chromadb", env="CHROMA_HOST")
    chroma_port: int = Field(default=8000, env="CHROMA_PORT")
    gemini_api_key: str = Field(..., env="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-pro", env="GEMINI_MODEL")
    embedding_model: str = Field(default="textembedding-gecko@001", env="EMBEDDING_MODEL")
    chunk_size: int = Field(default=1000, env="CHUNK_SIZE")
    chunk_overlap: int = Field(default=200, env="CHUNK_OVERLAP")
    max_documents: int = Field(default=20, env="MAX_DOCUMENTS")
    max_pages: int = Field(default=1000, env="MAX_PAGES")
    

    
    class Config:
        env_file = ".env"


settings = Settings()