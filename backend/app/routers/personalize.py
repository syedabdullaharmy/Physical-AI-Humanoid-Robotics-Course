from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class PersonalizeRequest(BaseModel):
    chapter_id: str
    content: str
    user_profile: Dict[str, Any]


class PersonalizeResponse(BaseModel):
    personalized_content: str
    chapter_id: str


@router.post("/", response_model=PersonalizeResponse)
async def personalize_content(request: PersonalizeRequest):
    """
    Personalize chapter content based on user profile
    
    Adapts content based on:
    - Software background
    - Hardware background
    - Hardware setup choice
    - Learning goals
    """
    try:
        personalized = await gemini_service.personalize_content(
            content=request.content,
            user_profile=request.user_profile
        )
        
        return PersonalizeResponse(
            personalized_content=personalized,
            chapter_id=request.chapter_id
        )
    
    except Exception as e:
        logger.error(f"Personalization failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def personalize_health():
    """Health check for personalization service"""
    return {"status": "healthy", "service": "personalize"}
