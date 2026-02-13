# 📄 AskMyDocs
### Chat with Your Documents

Welcome to the **Document Chatbot with Retrieval Augmented Generation (RAG)** repository! This project enables interactive document retrieval using cutting-edge AI techniques. By integrating the RAG methodology with a Streamlit-powered interface, it allows seamless querying across multiple document formats.

---

## 📚 Table of Contents

- [✨ Overview](#-overview)
- [🗂️ File Structure](#️-file-structure)
- [🚀 Features](#-features)
- [📋 Requirements](#-requirements)
- [💻 Installation](#-installation)

---
 
 ## ✨ Overview
 
 This chatbot leverages the RAG framework to enhance information retrieval from documents using natural language queries. It combines retrieval-based and generative AI capabilities for a smooth querying experience, making it ideal for dynamic, knowledge-intensive tasks.
 
 The user-friendly Streamlit interface simplifies interaction, ensuring accessibility for users across various domains.
 
 **Maintained by:** [Hindav](https://www.linkedin.com/in/hindav/)
 
 https://github.com/user-attachments/assets/6f549fe3-5594-4cb2-9e90-d51720fcffbc
 
 ---

## 🗂️ File Structure

```
.
├── icons/                    # Icons for UI (bot, user)
│   ├── bot-icon.png
│   └── user-icon.png
├── src/                      # Source code for the app
│   ├── app.py                # Main application logic
│   ├── conversation.py       # Chat handling and AI chain integration
│   ├── document_utils.py     # Document processing and summarization logic
│   ├── htmlTemplates.py      # HTML and CSS templates for UI
│   ├── prompt_refiner.py     # Logic for refining prompts with LLM
│   └── text_processing.py    # Text splitting and vector store generation
├── test/                     # Test files for the app (PDF, TXT)
│   ├── test.pdf
│   └── test.txt
├── .env                      # Store your API keys and sensitive data
├── .gitignore                # Git ignore rules
├── LICENSE                   # Project License
├── README.md                 # Project documentation and setup guide
├── directory_tree.py         # Script for visualizing the directory tree (optional)
├── pyproject.toml            # Project dependencies and configuration
├── setup.sh                  # Setup script for environment and dependencies
└── uv.lock                   # UV lock file for environment management

```

---

## 🚀 Features

- **Multi-File Upload**: Process and query multiple documents in formats like PDF, TXT, CSV, and DOCX.
- **AI-Powered Chat**: Ask natural language questions, and the bot retrieves accurate answers from document content.
- **Document Summarization**: Summarizes content for better context understanding.
- **Prompt Refinement**: Refines user questions for more precise responses. You can **enable or disable** this feature via the toggle.
- **Memory Retention**: Tracks conversation history for maintaining context.
- **Interactive UI**: A Streamlit-powered interface for intuitive interactions.
- **Fast Inference**: Powered by **Groq** for near-instant AI responses.

---

## 📋 Requirements

Ensure the following tools are installed:

- **Python 3.9+**: Managed automatically.
- **UV**: For fast dependency management.
   ```bash
   pip install uv
   ```
- **Dependencies**: Installed via `uv sync`.

### Environment Variables

Create a `.env` file in the root directory and add your Groq API key:

```plaintext
GROQ_API_KEY=gsk_your_groq_api_key_here
```

> **Note**: You can get your generic API key from the [Groq Console](https://console.groq.com/keys).

---

## 💻 Installation

Follow these steps to set up your environment:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hindav/ChatDoc.git
   cd ChatDoc
   ```

2. **Setup & Run**
   You can use `uv` directly to run the app, which handles virtual environments automatically:
   ```bash
   uv run streamlit run src/app.py
   ```
   
   Or use the setup script:
   ```bash
   bash setup.sh
   ```

3. **Access the UI**
   Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 📝 Usage

- **Input**: Upload multiple documents for analysis.
- **VectorStore Creation**: Converts documents into vector stores using FAISS and HuggingFace embeddings (local).
- **Text Generation**: Leverages **Llama 3.3 70B** via Groq for high-quality responses.
- **Prompt Refinement**: Toggle to refine queries using AI.


---

## 🙌 Acknowledgments

We extend our gratitude to the following tools and libraries that make this project possible:

- [Streamlit](https://streamlit.io/): For powering the intuitive user interface.
- [Groq](https://groq.com/): For ultra-fast AI inference.
- [Hugging Face](https://huggingface.co/): For embeddings (`all-MiniLM-L6-v2`) and transformers.
- [UV](https://pypi.org/project/uv/): For streamlined environment and dependency management.
- [FAISS](https://github.com/facebookresearch/faiss): For efficient similarity search and clustering.
- [LangChain](https://langchain.com/): For chaining multiple AI models into a cohesive workflow.

---

## 📜 License

This repository is licensed under the [MIT License](https://opensource.org/licenses/MIT). You are free to use, modify, and distribute the code, provided you include the original copyright notice and license.
