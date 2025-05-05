from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, FileResponse
from fastapi import Request
from pydantic import BaseModel
from typing import Optional
from ai_services.story_generator import StoryGenerator, Story
import os
from pathlib import Path

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

# Statik dosyaları ve şablonları yapılandır
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class StoryRequest(BaseModel):
    prompt: str

class StoryResponse(BaseModel):
    title: str
    scenes: list[dict]

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/presentation")
async def presentation():
    return FileResponse('docs/presentation.md')

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

@app.get("/demo")
async def demo():
    """Demo endpoint'i - örnek bir hikaye oluşturur"""
    try:
        generator = StoryGenerator()
        story = await generator.generate_story("Uzayda geçen kısa bir macera hikayesi")
        
        if not story:
            raise HTTPException(status_code=500, detail="Demo hikayesi oluşturulamadı")
            
        return StoryResponse(
            title=story.title,
            scenes=[{"text": scene.text, "image_url": scene.image_url} for scene in story.scenes]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 