# 📚 Multi-Document Chatbot — LLM + RAG

A production-ready conversational AI application that lets you upload multiple PDF documents and ask natural language questions across all of them simultaneously. Built with **LangChain**, **Mistral AI**, **FAISS**, and **Streamlit**.

---

## ✨ Features

- 📄 **Multi-PDF ingestion** — upload and process multiple PDFs at once
- 🔍 **Semantic search** — FAISS vector database with sentence-transformer embeddings for accurate retrieval
- 🧠 **Context-aware answers** — Mistral LLM answers only from your documents, not hallucinated knowledge
- ✂️ **Optimized chunking** — 500-character chunks with 50-character overlap for precise retrieval
- 💬 **Persistent chat history** — session-based memory keeps context across the conversation
- 🌐 **Interactive UI** — clean Streamlit web interface with multi-user session support

---

## Architecture

```
User uploads PDFs
       │
       ▼
 PDF Text Extraction (PyPDF2)
       │
       ▼
 Text Chunking (LangChain TextSplitter)
 chunk_size=500 | overlap=50
       │
       ▼
 Embeddings (sentence-transformers)
       │
       ▼
 Vector Store (FAISS)
       │
       ▼
 Semantic Retrieval on user query
       │
       ▼
 RAG Chain (LangChain + Mistral LLM)
       │
       ▼
 Context-aware Answer → Streamlit UI
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| UI | Streamlit |
| LLM | Mistral AI (`langchain_mistralai`) |
| Orchestration | LangChain (core, community, text_splitters) |
| Embeddings | sentence-transformers (HuggingFace) |
| Vector Store | FAISS (faiss-cpu) |
| PDF Parsing | PyPDF2 |
| Language | Python 3.10+ |

---

## 📁 Project Structure

```
multiDocChatbot/
│
├── app/
│   └── app.py              # Main Streamlit app — UI, session management, RAG chain
│
├── .gitignore
├── requirements.txt        # All Python dependencies
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/Efraym2fero/multiDocChatbot.git
cd multiDocChatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Mistral API key

Create a `.env` file in the root directory:

```env
MISTRAL_API_KEY=your_mistral_api_key_here
```
---

## Running the App

```bash
streamlit run app/app.py
```

---

## How to Use

1. **Upload PDFs** — use the sidebar file uploader to add one or more PDF files
2. **Process documents** — click **"Process"** to extract text, chunk it, embed it, and build the FAISS index
3. **Ask questions** — type any question in the chat input; the app retrieves relevant chunks and generates an answer
4. **Continue the conversation** — the chat history is preserved across turns so you can ask follow-up questions

---

## 🔧 Configuration

You can tune the following parameters inside `app/app.py`:

| Parameter | Default | Description |
|---|---|---|
| `chunk_size` | `500` | Characters per text chunk |
| `chunk_overlap` | `50` | Overlap between adjacent chunks |
| Embedding model | `sentence-transformers` | HuggingFace embedding model |
| LLM | `mistral-small-latest` | Mistral model used for generation |
| `k` (retrieval) | `4` | Number of chunks retrieved per query |

---

## 📦 Dependencies

```
streamlit
langchain
langchain_mistralai
langchain_text_splitters
langchain_core
langchain_community
sentence-transformers
faiss-cpu
PyPDF2
```

Install all at once:

```bash
pip install -r requirements.txt
```

---

## How RAG Works in This Project

1. **Ingestion**: PDFs are parsed with `PyPDF2` and split into overlapping chunks using `LangChain RecursiveCharacterTextSplitter`
2. **Embedding**: Each chunk is converted to a dense vector using `sentence-transformers`
3. **Indexing**: Vectors are stored in a `FAISS` index for fast similarity search
4. **Retrieval**: At query time, the user's question is embedded and the top-k most similar chunks are retrieved
5. **Generation**: Retrieved chunks are injected as context into the Mistral LLM prompt, which generates a grounded answer

This ensures answers are always based on the uploaded documents — not the model's parametric knowledge.

---

## Author

**Efraym Emad Hanna Naseaf** — AI & ML Engineer

- GitHub: [@Efraym2fero](https://github.com/Efraym2fero)
- LinkedIn: [efarym-emad-495707199](https://www.linkedin.com/in/efarym-emad-495707199)

---
