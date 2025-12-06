from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.gemini_service import gemini_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class TranslateRequest(BaseModel):
    chapter_id: str
    content: str
    language: str = "ur"  # Urdu


class TranslateResponse(BaseModel):
    translated_content: str
    chapter_id: str
    language: str


@router.post("/", response_model=TranslateResponse)
async def translate_content(request: TranslateRequest):
    """
    Translate chapter content to Urdu
    
    Preserves:
    - Technical terms in English
    - Code blocks unchanged
    - Formatting and structure
    """
    try:
        if request.language != "ur":
            raise HTTPException(
                status_code=400,
                detail="Only Urdu (ur) translation is currently supported"
            )
        
        translated = await gemini_service.translate_to_urdu(request.content)
        
        return TranslateResponse(
            translated_content=translated,
            chapter_id=request.chapter_id,
            language=request.language
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def translate_health():
    """Health check for translation service"""
    return {"status": "healthy", "service": "translate"}
