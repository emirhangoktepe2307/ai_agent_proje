from openai import OpenAI
import os
from dotenv import load_dotenv
from typing import List, Optional
import requests
from PIL import Image
import io

load_dotenv()

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    async def generate_image(self, prompt: str, size: str = "1024x1024", quality: str = "standard") -> Optional[str]:
        """
        DALL-E 3 kullanarak görsel üretir
        
        Args:
            prompt (str): Görsel oluşturma komutu
            size (str): Görsel boyutu (1024x1024, 1792x1024, 1024x1792)
            quality (str): Görsel kalitesi (standard, hd)
            
        Returns:
            Optional[str]: Oluşturulan görselin URL'si
        """
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=size,
                quality=quality,
                n=1,
            )
            
            return response.data[0].url
        except Exception as e:
            print(f"Görsel oluşturma hatası: {str(e)}")
            return None
            
    async def download_image(self, url: str) -> Optional[bytes]:
        """
        URL'den görseli indirir
        
        Args:
            url (str): Görsel URL'si
            
        Returns:
            Optional[bytes]: İndirilen görselin binary verisi
        """
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"Görsel indirme hatası: {str(e)}")
            return None
            
    def validate_image(self, image_data: bytes) -> bool:
        """
        Görselin geçerliliğini kontrol eder
        
        Args:
            image_data (bytes): Görsel binary verisi
            
        Returns:
            bool: Görsel geçerli mi?
        """
        try:
            image = Image.open(io.BytesIO(image_data))
            return image.size[0] >= 1024 and image.size[1] >= 1024
        except Exception as e:
            print(f"Görsel doğrulama hatası: {str(e)}")
            return False 