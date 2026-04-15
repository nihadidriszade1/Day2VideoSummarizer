import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
import yt_dlp
import requests
import xml.etree.ElementTree as ET

# Page config
st.set_page_config(page_title="Groq-Powered Summarizer", page_icon="⚡")
st.header("Groq ilə Şimşək Sürətində Video Xülasə ⚡")

# API Key
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")
    st.info("Groq Cloud-dan pulsuz API key ala bilərsiniz.")


# ---------- LANGUAGE DETECTION ----------
def detect_language(text):
    text_sample = text[:1000].lower()

    turkish_markers = ["ç", "ş", "ğ", "ı", "ö", "ü", "çok", "bir", "ve", "mi", "de", "bu"]
    azerbaijani_markers = ["ə", "ğ", "ı", "ö", "ş", "ç", "azərbaycan", "edir", "olur", "ilə", "də"]

    tr_score = sum(1 for w in turkish_markers if w in text_sample)
    az_score = sum(1 for w in azerbaijani_markers if w in text_sample)

    if tr_score == 0 and az_score == 0:
        return "en"

    if az_score > tr_score:
        return "az"
    else:
        return "tr"


# ---------- PRIMARY TRANSCRIPT ----------
def get_transcript_primary(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)

        try:
            transcript = transcript_list.find_transcript(['tr'])
        except:
            transcript = transcript_list.find_transcript(['en'])

        if transcript.language_code != "en":
            transcript = transcript.translate('en')

        data = transcript.fetch()
        return " ".join([item.text for item in data])

    except:
        return None


# ---------- FALLBACK TRANSCRIPT ----------
def get_transcript_fallback(url):
    try:
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['en', 'tr'],
            'skip_download': True,
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            subtitles = info.get("subtitles") or info.get("automatic_captions")

            if not subtitles:
                return None

            lang = 'en' if 'en' in subtitles else list(subtitles.keys())[0]
            sub_url = subtitles[lang][0]['url']

            res = requests.get(sub_url)

            root = ET.fromstring(res.text)
            texts = [elem.text for elem in root.iter("text") if elem.text]

            return " ".join(texts)

    except:
        return None


# ---------- METADATA FALLBACK ----------
def get_video_metadata(url):
    try:
        ydl_opts = {'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            title = info.get("title", "")
            description = info.get("description", "")

            return f"Title: {title}\n\nDescription: {description}"

    except:
        return None


# ---------- MAIN TRANSCRIPT HANDLER ----------
def get_youtube_transcript(video_url):
    try:
        if "v=" in video_url:
            video_id = video_url.split("v=")[1].split("&")[0]
        else:
            video_id = video_url.split("/")[-1]

        text = get_transcript_primary(video_id)

        if not text:
            st.warning("Fallback işləyir")
            text = get_transcript_fallback(video_url)

        if not text:
            st.warning("Transcript yoxdur → metadata istifadə olunur 🔄")
            text = get_video_metadata(video_url)

        if not text:
            st.error("Heç bir data tapılmadı ❌")
            return None

        return text

    except Exception as e:
        st.error(f"Xəta: {e}")
        return None


# ---------- GROQ SUMMARY ----------
def summarize_with_groq(text, api_key):

    lang = detect_language(text)

    if lang == "az":
        instruction = """
Aşağıdakı mətni Azərbaycan dilində DETAİLLİ şəkildə xülasə et.

Qaydalar:
- Qısa yox, orta uzunluqda yaz
- Ən az 5-8 cümlə olsun
- Əsas mövzunu geniş izah et
- Skelet yox, izahlı mətn yaz
"""

    elif lang == "tr":
        instruction = """
Aşağıdaki metni Türkçe olarak DETAYLI şekilde özetle.

Kurallar:
- Kısa değil, orta uzunlukta yaz
- En az 5-8 cümle olsun
- Konuyu açıklayıcı şekilde anlat
"""

    else:
        instruction = """
Summarize the following text in DETAILED English.

Rules:
- Not too short
- 5-8+ sentences
- Explain the content clearly
"""

    llm = ChatGroq(
        temperature=0,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=300
    )

    chunks = splitter.split_text(text)

    prompt = PromptTemplate.from_template(
        instruction + "\n\nText:\n{text}"
    )

    chain = prompt | llm | StrOutputParser()

    summaries = []

    for chunk in chunks:
        summaries.append(chain.invoke({"text": chunk}))

    final_text = " ".join(summaries)

    return chain.invoke({"text": final_text})

    lang = detect_language(text)

    if lang == "az":
        instruction = """
Aşağıdakı mətni Azərbaycan dilində qısa və aydın xülasə et.
• Sadə və başa düşülən yaz
• Əsas fikirləri çıxar
"""

    elif lang == "tr":
        instruction = """
Aşağıdaki metni Türkçe olarak kısa ve net özetle.
• Basit ve anlaşılır yaz
• Ana fikirleri çıkar
"""

    else:
        instruction = """
Summarize the following text in clear and simple English.
• Keep it short
• Extract main ideas
"""

    llm = ChatGroq(
        temperature=0,
        groq_api_key=api_key,
        model_name="llama-3.3-70b-versatile"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=4000,
        chunk_overlap=300
    )

    chunks = splitter.split_text(text)

    prompt = PromptTemplate.from_template(
        instruction + "\n\nText:\n{text}"
    )

    chain = prompt | llm | StrOutputParser()

    summaries = []

    for chunk in chunks:
        summaries.append(chain.invoke({"text": chunk}))

    final_text = " ".join(summaries)

    return chain.invoke({"text": final_text})


# ---------- UI ----------
url = st.text_input("YouTube Video Linki:")

if st.button("Xülasəni Hazırla"):
    if not groq_api_key:
        st.warning("Zəhmət olmasa Groq API Key daxil edin!")
    elif url:
        with st.spinner("Processing... ⚡"):
            transcript_text = get_youtube_transcript(url)

            if transcript_text:
                summary = summarize_with_groq(transcript_text, groq_api_key)

                st.subheader("Nəticə:")
                st.success(summary)