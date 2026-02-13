# 📄 AskMyDocs

### Chat with Your Documents using AI (RAG)

Welcome to **AskMyDocs** — an AI-powered document chatbot built with **Retrieval-Augmented Generation (RAG)**. This project enables you to upload multiple documents and interact with them conversationally using natural language.

It combines modern AI retrieval techniques with fast LLM inference and a clean Streamlit interface to deliver accurate, context-aware answers from your documents.

---

## ✨ Overview

**AskMyDocs** allows users to:

* Upload documents in multiple formats
* Extract meaningful information instantly
* Ask questions conversationally
* Generate summaries and contextual answers

The project integrates document retrieval, embeddings, vector databases, and large language models to create a seamless document-chat experience.

---

## 🚀 Features

### 📂 Document Handling

* Multi-file upload support (PDF, TXT, CSV, DOCX)
* Automatic text extraction and preprocessing
* Intelligent document chunking

### 🤖 AI-Powered Chat

* Natural language Q&A from documents
* Context-aware conversation memory
* Retrieval-Augmented Generation (RAG) pipeline

### 🧠 Smart Enhancements

* Prompt refinement toggle for better queries
* Document summarization capability
* Fast inference powered by Groq LLMs

### 💻 User Interface

* Streamlit-based interactive UI
* Simple, responsive experience
* Easy document management

---

## 🗂️ Project Structure

```
.
├── icons/
│   └── ico.png
├── src/
│   ├── analytics.py
│   ├── app.py
│   ├── conversation.py
│   ├── document_utils.py
│   ├── prompt_refiner.py
│   └── text_processing.py
├── README.md
├── pyproject.toml
├── setup.sh
└── uv.lock
```

---

## 📋 Requirements

* Python **3.9+**
* `uv` package manager (recommended)

Install uv if needed:

```bash
pip install uv
```

---

## 🔑 Environment Setup

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_api_key_here
```

This key is required for AI inference.

---

## 💻 Installation & Setup

### 1️⃣ Clone Repository

```bash
git clone https://github.com/hindav/ChatDoc.git
cd ChatDoc
```

### 2️⃣ Run Application

Using uv:

```bash
uv run streamlit run src/app.py
```

Or:

```bash
bash setup.sh
```

---

## ▶️ Running the App

After starting:

```
http://localhost:8501
```

Open this in your browser to access the interface.

---

## 📝 Usage Guide

1. Upload one or more documents
2. System converts them into embeddings
3. Ask questions naturally
4. Get contextual AI-generated responses

Optional:

* Enable prompt refinement for better accuracy
* Use summarization for quick document insights

---

## 🧰 Tech Stack

* Streamlit — Frontend UI
* LangChain — AI orchestration
* FAISS — Vector similarity search
* HuggingFace Embeddings — Text embeddings
* Groq LLM (Llama 3.3 70B) — Fast AI inference
* Python — Core backend

---

## 🎯 Use Cases

* Research document analysis
* Study material querying
* Knowledge base assistants
* Business document exploration
* Personal document organization

---

## 📜 License

This project is licensed under the **MIT License**.
You are free to use, modify, and distribute it with proper attribution.

---

## 👨‍💻 Maintained By

**Hindav Deshmukh**
AI • Data Engineering • ML Systems

---

⭐ If you find this useful, consider starring the repository!
