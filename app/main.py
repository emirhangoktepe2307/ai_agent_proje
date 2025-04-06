from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import story

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

@app.get("/")
async def root():
    return {"message": "AI Hikaye Oluşturucu API'sine Hoş Geldiniz"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 