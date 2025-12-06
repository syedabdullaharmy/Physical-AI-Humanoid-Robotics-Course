from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.services.rag_service import rag_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    query: str
    selected_text: Optional[str] = None
    module: Optional[str] = None
    chapter: Optional[str] = None
    chat_history: Optional[List[ChatMessage]] = None


class ChatResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]]
    confidence: str
    retrieved_chunks: int


@router.post("/query", response_model=ChatResponse)
async def chat_query(request: ChatRequest):
    """
    Main chat endpoint for RAG queries.
    Note: This is a public education tool, so no user authentication is currently enforced.
    """
    - General questions about the textbook
    - Text selection-based queries
    - Context-aware responses based on current module/chapter
    """
    try:
        # Prepare user context
        user_context = {}
        if request.module:
            user_context["module"] = request.module
        if request.chapter:
            user_context["chapter"] = request.chapter
        
        # If selected text is provided, enhance the query
        query = request.query
        if request.selected_text:
            query = f"Based on this text: '{request.selected_text}'\n\nQuestion: {request.query}"
        
        # Convert chat history
        chat_history = None
        if request.chat_history:
            chat_history = [
                {"role": msg.role, "content": msg.content}
                for msg in request.chat_history
            ]
        
        # Execute RAG query
        result = await rag_service.query(
            user_query=query,
            user_context=user_context if user_context else None,
            chat_history=chat_history
        )
        
        return ChatResponse(**result)
    
    except Exception as e:
        logger.error(f"Chat query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def chat_health():
    """Health check for chat service"""
    return {"status": "healthy", "service": "chat"}
