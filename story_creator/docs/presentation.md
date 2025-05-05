# AI Hikaye Oluşturucu - Proje Sunumu

## Proje Amacı
- Yapay zeka destekli hikaye ve görsel üretim sistemi
- Kullanıcıların promptlarına göre özgün içerik oluşturma
- Çoklu AI servislerinin entegrasyonu

## Kullanılan Teknolojiler
- Backend: FastAPI (Python)
- AI Servisleri:
  - GPT-4 (Hikaye oluşturma)
  - DALL-E 3 (Görsel üretimi)
  - LangChain (AI servisleri entegrasyonu)

## Proje Yapısı
```
story_creator/
├── app/              # API ve uygulama katmanı
├── ai_services/      # AI servisleri
├── tests/           # Test dosyaları
└── docs/            # Dokümantasyon
```

## Temel Özellikler
1. Hikaye Oluşturma
   - GPT-4 ile özgün hikaye üretimi
   - Sahne bazlı hikaye yapısı
   - Dinamik prompt işleme

2. Görsel Üretimi
   - DALL-E 3 entegrasyonu
   - Her sahne için özel görsel
   - Görsel kalite kontrolü

3. API Entegrasyonu
   - RESTful API tasarımı
   - Asenkron işlem yönetimi
   - Hata yönetimi ve loglama

## Teknik Detaylar
- Python 3.9+
- FastAPI framework
- OpenAI API entegrasyonu
- Asenkron programlama
- Pydantic modelleri

## API Kullanımı
```python
# Hikaye oluşturma isteği
POST /generate-story
{
    "prompt": "Uzayda geçen bir macera hikayesi"
}

# Yanıt
{
    "title": "Galaktik Macera",
    "scenes": [
        {
            "text": "Uzay gemisi yeni bir gezegene yaklaşıyor...",
            "image_url": "https://..."
        }
    ]
}
```

## Kurulum
1. Python 3.9+ yükleyin
2. Gerekli paketleri yükleyin:
   ```bash
   pip install -r requirements.txt
   ```
3. .env dosyasını oluşturun
4. Uygulamayı başlatın:
   ```bash
   uvicorn app.main:app --reload
   ```

## Gelecek Geliştirmeler
- Seslendirme entegrasyonu
- Video üretimi
- Kullanıcı arayüzü
- Çoklu dil desteği

## Sonuç
- Başarılı AI servisleri entegrasyonu
- Ölçeklenebilir mimari
- Modern API tasarımı
- Genişletilebilir yapı 