import hashlib
from typing import Any

def generate_id(text: str) -> str:
    """Generate a unique ID for a text chunk"""
    return hashlib.md5(text.encode()).hexdigest()

def validate_document_size(content: bytes, max_size: int) -> bool:
    """Validate document size doesn't exceed maximum"""
    return len(content) <= max_size