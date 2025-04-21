from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
from .image_generator import ImageGenerator

load_dotenv()

class StoryScene(BaseModel):
    text: str = Field(description="Sahne metni")
    image_prompt: str = Field(description="Görsel oluşturma komutu")
    image_url: Optional[str] = Field(default=None, description="Oluşturulan görsel URL'si")

class Story(BaseModel):
    title: str = Field(description="Hikaye başlığı")
    scenes: List[StoryScene] = Field(description="Hikaye sahneleri")

class StoryGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-turbo-preview",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.image_generator = ImageGenerator()
        
    async def generate_story(self, prompt: str) -> Optional[Story]:
        """
        Kullanıcı prompt'una göre hikaye oluşturur
        
        Args:
            prompt (str): Kullanıcı prompt'u
            
        Returns:
            Optional[Story]: Oluşturulan hikaye
        """
        try:
            # Hikaye oluşturma şablonu
            story_template = ChatPromptTemplate.from_messages([
                ("system", """Sen bir hikaye yazarısın. Kullanıcının istediği konuda 
                ilgi çekici ve yaratıcı bir hikaye oluştur. Hikaye 3-5 sahne içermeli.
                Her sahne için ayrı bir görsel oluşturulacak, bu yüzden her sahne için
                detaylı bir görsel açıklaması da ekle."""),
                ("user", "{prompt}")
            ])
            
            # JSON çıktı parser'ı
            parser = JsonOutputParser(pydantic_object=Story)
            
            # Zincir oluştur
            chain = story_template | self.llm | parser
            
            # Hikayeyi oluştur
            story = await chain.ainvoke({"prompt": prompt})
            
            # Her sahne için görsel oluştur
            for scene in story.scenes:
                image_url = await self.image_generator.generate_image(
                    prompt=scene.image_prompt,
                    size="1024x1024",
                    quality="standard"
                )
                scene.image_url = image_url
                
            return story
            
        except Exception as e:
            print(f"Hikaye oluşturma hatası: {str(e)}")
            return None 