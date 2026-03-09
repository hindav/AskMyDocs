# 📄 AskMyDocs

### Chat with Your Documents using AI (RAG)

Welcome to **AskMyDocs** — an AI-powered document chatbot that allows you to upload documents and interact with them conversationally. Built using **Retrieval-Augmented Generation (RAG)**, it combines document retrieval, embeddings, and large language models to deliver contextual answers directly from your files.

---

## 🎥 Project Demo

[![Watch Demo](https://img.youtube.com/vi/sYKnJxIQ0pE/0.jpg)](https://youtu.be/sYKnJxIQ0pE)

👉 Click the image above to watch the full demo video.

---

## ✨ Overview

AskMyDocs simplifies document analysis using AI:

* Upload multiple files
* Ask questions naturally
* Receive contextual AI-generated answers
* Quickly extract insights without manual searching

This project demonstrates how modern AI pipelines can transform document interaction and knowledge retrieval.

---

## 🚀 Features

### 📂 Document Processing

* Supports PDF, TXT, CSV, DOCX files
* Automatic text extraction
* Efficient document chunking and embedding

### 🤖 AI Chatbot

* Conversational Q&A from documents
* Context-aware responses
* Retrieval-Augmented Generation pipeline

### 🧠 Smart Enhancements

* Optional prompt refinement
* Document summarization
* Fast inference powered by Groq LLM

### 💻 User Interface

* Streamlit interactive dashboard
* Simple upload & chat workflow
* Clean, responsive design

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
* UV package manager recommended

Install uv:

```
pip install uv
```

---

## 🔑 Environment Setup

Create `.env` file in root:

```
GROQ_API_KEY=your_api_key_here
```

Required for AI inference.

---

## 💻 Installation

### Clone Repository

```
git clone https://github.com/hindav/AskMyDocs.git
cd AskMyDocs
```

### Run Application

Using uv:

```
uv run streamlit run src/app.py
```

Or:

```
bash setup.sh
```

---

## ▶️ Access the App

Open browser:

```
http://localhost:8501
```

---

## 📝 Usage

1. Upload documents
2. System converts them into embeddings
3. Ask questions naturally
4. Get contextual AI responses

Optional:

* Enable prompt refinement
* Generate document summaries

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

## 👨‍💻 Maintained By

**Hindav Deshmukh**
AI • Data Engineering • Machine Learning

GitHub: https://github.com/hindav
LinkedIn: https://www.linkedin.com/in/hindav/

---

## 📜 License

MIT License — free to use, modify, and distribute with attribution.

---

⭐ If you find this project useful, consider starring the repository!
