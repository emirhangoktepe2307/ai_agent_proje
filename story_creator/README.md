# AI Hikaye Oluşturucu

Bu proje, kullanıcıların girdiği promptlar doğrultusunda otomatik hikaye oluşturan bir AI sistemidir.

## Özellikler

- GPT-4/Claude ile hikaye oluşturma
- DALL·E 3 / Stable Diffusion ile görsel üretimi
- Runway Gen-2 / Pika Labs ile video üretimi
- ElevenLabs / Google TTS ile seslendirme

## Teknolojiler

- Backend: FastAPI
- Frontend: React Native
- AI Servisleri: OpenAI, ElevenLabs, RunwayML

## Kurulum

1. Python 3.9+ yükleyin
2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```
3. `.env` dosyasını oluşturun ve gerekli API anahtarlarını ekleyin
4. Uygulamayı başlatın:
```bash
uvicorn main:app --reload
```

## Proje Yapısı

```
story_creator/
├── app/
│   ├── api/
│   ├── core/
│   ├── models/
│   └── services/
├── tests/
├── requirements.txt
└── README.md
``` 