# ⚡ Groq-Powered YouTube Summarizer (Day 2 of 30)

Bu layihə, **Groq LPU** (Language Processing Unit) texnologiyasından istifadə edərək YouTube videolarının transkriptini çıxaran və saniyələr içində detallı xülasə hazırlayan süni intellekt alətidir.

## 🚀 Xüsusiyyətlər
- **Çoxpilləli Transkript Sistemi:** 1. `YouTubeTranscriptApi` (Rəsmi/Avtomatik alt yazılar)
  2. `yt-dlp` Fallback (Daxili sub-title çəkmə sistemi)
  3. Metadata Fallback (Transkript tapılmadıqda başlıq və təsvir analizi)
- **Dil Tanıma (Custom Detection):** Azərbaycan, Türk və İngilis dillərini avtomatik tanıyır və xülasəni həmin dildə təqdim edir.
- **Sürət:** Groq-un `llama-3.3-70b-versatile` modeli ilə şimşək sürətində analiz.
- **Map-Reduce Məntiqi:** Uzun videoları hissələrə bölərək (chunking) heç bir məlumat itkisi olmadan xülasə edir.

## 🛠 Texnoloji Stack
- **Frontend:** Streamlit
- **LLM:** Groq (Llama 3.3 70B)
- **Framework:** LangChain
- **Data Extraction:** yt-dlp, YouTubeTranscriptApi

## 📦 Quraşdırılma

1. Reponu klonlayın:
   ```bash
   git clone https://github.com/nihadidriszade1/Day2VideoSummarizer.git
2. Lazımi kitabxanaları yükləyin:
   ```bash
   pip install streamlit youtube-transcript-api langchain-groq yt-dlp requests
3. Tətbiqi başladın:
   ```bash
   streamlit run app.py
