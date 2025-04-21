from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .api import story
from pydantic import BaseModel
from typing import Optional
from ai_services.story_generator import StoryGenerator, Story

app = FastAPI(
    title="AI Hikaye Oluşturucu",
    description="Kullanıcı promptlarına göre hikaye oluşturan AI sistemi",
    version="1.0.0"
)

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API router'larını ekle
app.include_router(story.router, prefix="/api/story", tags=["story"])

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    title: str
    scenes: list[dict]

@app.post("/generate-story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    try:
        generator = StoryGenerator()
        story = await generator.generate_story(request.prompt)
        
        if not story:
            raise HTTPException(status_code=500, detail="Hikaye oluşturulamadı")
            
        return StoryResponse(
            title=story.title,
            scenes=[{"text": scene.text, "image_url": scene.image_url} for scene in story.scenes]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "AI Hikaye Oluşturucu API'sine Hoş Geldiniz"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 