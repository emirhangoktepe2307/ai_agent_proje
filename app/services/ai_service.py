from typing import Optional, Dict
import os
from openai import OpenAI
from elevenlabs import generate, set_api_key
import requests
from .story_agent import StoryAgent, StoryConfig

class AIService:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        set_api_key(os.getenv("ELEVENLABS_API_KEY"))
        self.runway_api_key = os.getenv("RUNWAYML_API_KEY")
        self.story_agent = StoryAgent(model_name="gpt-4")  # veya "claude-3-opus-20240229"

    async def generate_story(self, prompt: str, style: str = "creative", length: str = "medium", language: str = "tr") -> Dict:
        """StoryAgent ile optimize edilmiş hikaye oluşturur"""
        try:
            # Hikaye konfigürasyonunu oluştur
            config = StoryConfig(
                style=style,
                length=length,
                language=language
            )
            
            # Hikayeyi bölümlere ayırarak oluştur
            story_parts = await self.story_agent.generate_complete_story(prompt, config)
            
            # Hikayeyi birleştir ve akıcılığını sağla
            final_story = await self.story_agent.refine_story(story_parts, config)
            
            # Hikayeyi değerlendir
            evaluation = self.story_agent.evaluate_story(final_story)
            
            return {
                "story": final_story,
                "parts": story_parts,
                "evaluation": evaluation
            }
        except Exception as e:
            raise Exception(f"Hikaye oluşturulurken hata oluştu: {str(e)}")

    async def generate_image(self, prompt: str) -> str:
        """DALL-E ile optimize edilmiş görsel oluşturur"""
        try:
            # Görsel oluşturma promptunu optimize et
            optimized_prompt = f"Create a detailed illustration for: {prompt}. Style: realistic, high quality, 4K"
            
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=optimized_prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            raise Exception(f"Görsel oluşturulurken hata oluştu: {str(e)}")

    async def generate_voice(self, text: str) -> bytes:
        """ElevenLabs ile optimize edilmiş ses oluşturur"""
        try:
            # Metni optimize et (uzun metinleri parçalara ayır)
            chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
            audio_chunks = []
            
            for chunk in chunks:
                audio = generate(
                    text=chunk,
                    voice="Bella",
                    model="eleven_monolingual_v1"
                )
                audio_chunks.append(audio)
            
            # Ses parçalarını birleştir (bu kısım implementasyon gerektirir)
            return audio_chunks[0]  # Şimdilik sadece ilk parçayı döndür
        except Exception as e:
            raise Exception(f"Ses oluşturulurken hata oluştu: {str(e)}")

    async def generate_video(self, image_url: str) -> str:
        """RunwayML ile optimize edilmiş video oluşturur"""
        try:
            # RunwayML API entegrasyonu burada yapılacak
            # Şimdilik örnek bir implementasyon
            return "video_url_placeholder"
        except Exception as e:
            raise Exception(f"Video oluşturulurken hata oluştu: {str(e)}") 