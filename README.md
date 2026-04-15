📄 DocChat — Sənədlərimlə Danış

DocChat is a high-performance, privacy-focused PDF RAG (Retrieval-Augmented Generation) chatbot. It allows you to upload multiple PDF documents and chat with them using a combination of local vector embeddings and the powerful LLaMA 3.3 model via Groq API.

Streamlit · Python · Groq · FAISS · LangChain

✨ Features

🔐 Privacy First
All embeddings are generated locally using all-MiniLM-L6-v2, ensuring your documents never leave your system.

⚡ Fast AI Responses
Powered by LLaMA 3.3 70B via Groq Cloud API for near-instant answers.

📚 Multi-PDF Chat
Upload multiple PDF files and chat with all of them at once.

🧠 RAG Architecture
Combines retrieval + generation for accurate and context-aware responses.

🌍 Multilingual Support
Optimized for Azerbaijani and English queries.

🎨 Modern UI
Clean dark-themed Streamlit interface with smooth chat experience.

🚀 Getting Started

Prerequisites
- Python 3.9+
- Groq API Key (https://console.groq.com)

Installation

1. Clone repository:
git clone https://github.com/YOUR_USERNAME/docchat.git
cd docchat

2. Create virtual environment:
python -m venv .venv

Windows:
.venv\Scripts\activate

macOS/Linux:
source .venv/bin/activate

3. Install dependencies:
pip install -r requirements.txt

4. Run app:
streamlit run app.py

🛠️ How It Works

1. PDF Text Extraction
Uses PyPDF2 to extract text from uploaded PDFs.

2. Chunking
Splits text into small chunks using RecursiveCharacterTextSplitter.

3. Embeddings
Creates local embeddings using all-MiniLM-L6-v2 model.

4. Vector Database
Stores embeddings in FAISS index.

5. Retrieval
Finds most relevant chunks using similarity search.

6. RAG Pipeline
Sends retrieved context + user question to Groq LLaMA 3.3 model.

🎨 UI Features

- Dark modern theme
- Chat-style interface
- Glassmorphism design
- Smooth Streamlit UX

🔐 Security

- API keys stored only in session state
- No permanent storage of sensitive data
- Fully local embedding generation

📦 Use Cases

- Study assistant
- Research paper analyzer
- Legal document Q&A
- Personal knowledge chatbot

📄 License

This project is licensed under the MIT License.

💡 Future Improvements

- Multi-user support
- Chat history saving
- DOCX/TXT support
- Hybrid search (BM25 + FAISS)
- Streaming responses