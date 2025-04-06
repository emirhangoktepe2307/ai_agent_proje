from typing import List, Dict, Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import asyncio
from pydantic import BaseModel

class StoryConfig(BaseModel):
    style: str = "creative"
    length: str = "medium"
    target_length: Optional[int] = None
    language: str = "tr"

class StoryAgent:
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.llm = self._initialize_llm()
        self.output_parser = StrOutputParser()
        
    def _initialize_llm(self):
        """LLM modelini başlatır"""
        if self.model_name.startswith("gpt"):
            return ChatOpenAI(
                model=self.model_name,
                temperature=0.7,
                max_tokens=1000
            )
        elif self.model_name.startswith("claude"):
            return ChatAnthropic(
                model=self.model_name,
                temperature=0.7,
                max_tokens=1000
            )
        else:
            raise ValueError(f"Desteklenmeyen model: {self.model_name}")

    def _create_story_prompt(self, section: str, config: StoryConfig) -> ChatPromptTemplate:
        """Hikaye bölümü için optimize edilmiş prompt şablonu oluşturur"""
        length_guide = {
            "short": "150-200 kelime",
            "medium": "300-400 kelime",
            "long": "500-600 kelime"
        }
        
        style_guide = {
            "creative": "yaratıcı ve özgün",
            "dramatic": "dramatik ve duygusal",
            "humorous": "komik ve eğlenceli",
            "educational": "eğitici ve bilgilendirici"
        }
        
        return ChatPromptTemplate.from_messages([
            ("system", f"""Sen bir {style_guide[config.style]} hikaye yazarısın.
            Hikayenin {section} bölümünü yazıyorsun.
            Hikaye {config.language} dilinde olmalı.
            Bölüm yaklaşık {length_guide[config.length]} uzunluğunda olmalı.
            Önceki bölümlerle tutarlı ol ve karakter gelişimini sürdür.
            Hikaye akıcı ve etkileyici olmalı."""),
            ("user", "{prompt}")
        ])

    async def generate_story_section(self, prompt: str, section: str, config: StoryConfig, previous_sections: List[str] = None) -> str:
        """Hikayenin belirli bir bölümünü optimize edilmiş şekilde oluşturur"""
        story_prompt = self._create_story_prompt(section, config)
        
        # Önceki bölümleri context olarak ekle
        context = "\n".join(previous_sections) if previous_sections else ""
        
        chain = (
            {"prompt": RunnablePassthrough(), "section": lambda x: section, "context": lambda x: context}
            | story_prompt
            | self.llm
            | self.output_parser
        )
        
        return await chain.ainvoke(prompt)

    async def generate_complete_story(self, prompt: str, config: StoryConfig) -> Dict[str, str]:
        """Tam bir hikaye oluşturur (giriş, gelişme, sonuç)"""
        sections = ["giriş", "gelişme", "sonuç"]
        story_parts = {}
        previous_sections = []

        # Paralel işlem için görevleri oluştur
        tasks = []
        for section in sections:
            task = self.generate_story_section(
                prompt=prompt,
                section=section,
                config=config,
                previous_sections=previous_sections
            )
            tasks.append(task)
            previous_sections.append(None)  # Placeholder for parallel execution

        # Paralel olarak çalıştır
        results = await asyncio.gather(*tasks)
        
        # Sonuçları düzenle
        for section, result in zip(sections, results):
            story_parts[section] = result
            previous_sections[sections.index(section)] = result

        return story_parts

    async def refine_story(self, story_parts: Dict[str, str], config: StoryConfig) -> str:
        """Hikaye bölümlerini birleştirir ve akıcılığını sağlar"""
        refinement_prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Hikayenin bölümlerini birleştir ve akıcı bir bütün haline getir.
            Hikaye {config.language} dilinde olmalı ve {config.style} tarzında yazılmalı.
            Gerektiğinde geçiş cümleleri ekle ve tutarlılığı sağla.
            Karakterlerin gelişimini ve hikaye akışını kontrol et."""),
            ("user", "{story_parts}")
        ])

        chain = (
            {"story_parts": lambda x: "\n\n".join([f"{k.upper()}:\n{v}" for k, v in x.items()])}
            | refinement_prompt
            | self.llm
            | self.output_parser
        )

        return await chain.ainvoke(story_parts)

    def evaluate_story(self, story: str) -> Dict[str, float]:
        """Hikayenin kalitesini değerlendirir"""
        # Bu fonksiyon şimdilik basit bir değerlendirme yapıyor
        # İleride daha gelişmiş metrikler eklenebilir
        word_count = len(story.split())
        sentence_count = len(story.split('.'))
        
        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_sentence_length": word_count / sentence_count if sentence_count > 0 else 0
        } 