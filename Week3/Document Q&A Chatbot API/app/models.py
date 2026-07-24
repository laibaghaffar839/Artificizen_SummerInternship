from pydantic import BaseModel
from typing import List


class ChatRequest(BaseModel):
    session_id: str
    query: str


class Source(BaseModel):
    source: str
    chunk_index: int


class ChatResponse(BaseModel):
    answer: str
    sources: List[Source]