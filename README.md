# 📄 AskMyDocs

### Chat with Your Documents using AI (RAG)

Welcome to **AskMyDocs** — an AI-powered document chatbot that lets you upload documents and interact with them conversationally. Built using **Retrieval-Augmented Generation (RAG)**, this project combines modern AI retrieval, embeddings, and large language models to provide accurate answers directly from your files.

---

## ✨ Overview

AskMyDocs enables intelligent document interaction through natural language queries. Instead of manually searching through files, you can simply ask questions and get contextual answers instantly.

The system processes documents, converts them into vector embeddings, retrieves relevant content, and generates responses using advanced LLM inference.

### 🎥 Project Demo

<video src="Demo.mp4" controls width="700">
Your browser does not support the video tag.
</video>

---

## 🚀 Features

### 📂 Document Handling

* Upload multiple documents (PDF, TXT, CSV, DOCX)
* Automatic text extraction and preprocessing
* Efficient vector embedding generation

### 🤖 AI Chat System

* Conversational Q&A from your documents
* Context-aware memory retention
* Retrieval-Augmented Generation pipeline

### 🧠 Smart Enhancements

* Optional prompt refinement for better responses
* Document summarization support
* Fast inference powered by Groq LLMs

### 💻 User Interface

* Streamlit-based interactive UI
* Clean and simple workflow
* Quick document upload and querying

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

* Python 3.9+
* UV package manager (recommended)

Install UV:

```bash
pip install uv
```

---

## 🔑 Environment Setup

Create a `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

This key is required for LLM inference.

---

## 💻 Installation

### Clone Repository

```bash
git clone https://github.com/hindav/AskMyDocs.git
cd AskMyDocs
```

### Run Application

Using uv:

```bash
uv run streamlit run src/app.py
```

Or:

```bash
bash setup.sh
```

---

## ▶️ Access the App

Open in browser:

```
http://localhost:8501
```

---

## 📝 Usage

1. Upload your documents
2. System converts them to embeddings
3. Ask questions naturally
4. Receive AI-generated contextual answers

Optional:

* Enable prompt refinement for accuracy
* Use summarization for quick insights

---

## 🧰 Tech Stack

* Python
* Streamlit
* LangChain
* FAISS Vector Database
* HuggingFace Embeddings
* Groq LLM (Llama models)

---

## 🎯 Use Cases

* Research document analysis
* Study material Q&A
* Knowledge base assistant
* Business document exploration
* Personal document AI assistant

---

## 📜 License

MIT License — free to use, modify, and distribute with attribution.

---

## 👨‍💻 Maintained By

**Hindav Deshmukh**
AI • Data Engineering • Machine Learning

---

⭐ If you found this useful, consider starring the repository!
