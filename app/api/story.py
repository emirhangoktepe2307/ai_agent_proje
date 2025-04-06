from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
from ..services.ai_service import AIService

router = APIRouter()
ai_service = AIService()

class StoryRequest(BaseModel):
    prompt: str
    style: Optional[str] = "creative"
    length: Optional[str] = "medium"
    language: Optional[str] = "tr"

class StoryResponse(BaseModel):
    story: str
    parts: Dict[str, str]
    evaluation: Dict[str, float]
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    audio_url: Optional[str] = None

@router.post("/generate", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        # Hikaye oluştur
        story_result = await ai_service.generate_story(
            prompt=request.prompt,
            style=request.style,
            length=request.length,
            language=request.language
        )
        
        # Görsel oluştur
        image_prompt = f"Create an illustration for this story: {story_result['story'][:200]}"
        image_url = await ai_service.generate_image(image_prompt)
        
        # Ses oluştur
        audio = await ai_service.generate_voice(story_result['story'])
        
        # Video oluştur
        video_url = await ai_service.generate_video(image_url)
        
        return StoryResponse(
            story=story_result['story'],
            parts=story_result['parts'],
            evaluation=story_result['evaluation'],
            image_url=image_url,
            video_url=video_url,
            audio_url="audio_url_placeholder"  # Gerçek implementasyonda bu URL'i döndüreceğiz
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 