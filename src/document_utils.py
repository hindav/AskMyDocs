from PyPDF2 import PdfReader
import csv
from unstructured.partition.auto import partition
import streamlit as st
from text_processing import get_chunks, get_vectorstore
from conversation import get_conversationchain
import os
import warnings
from langchain_core.documents import Document

# Suppress warnings
warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=r".*clean_up_tokenization_spaces.*"
)

# OpenMP fix
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

def get_text_from_file(uploaded_file):
    """Extracts text from various file formats."""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_reader = PdfReader(uploaded_file)
            text = "".join(page.extract_text() for page in pdf_reader.pages)
            if not text.strip():
                raise ValueError("PDF is empty or scanned (images only).")
            return text

        elif uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode('utf-8')
            if not text.strip():
                raise ValueError("Text file is empty.")
            return text

        elif uploaded_file.type == "text/csv":
            text = "".join(", ".join(row) + "\n" for row in csv.reader(uploaded_file.read().decode('utf-8').splitlines()))
            if not text.strip():
                raise ValueError("CSV file is empty.")
            return text

        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            elements = partition(file=uploaded_file)
            text = "\n".join(map(str, elements))
            if not text.strip():
                raise ValueError("DOCX file is empty.")
            return text

        else:
            st.error(f"Unsupported file type: {uploaded_file.type}")
            return None

    except Exception as e:
        st.error(f"Error reading file '{uploaded_file.name}': {e}")
        return None

def process_documents(docs, api_key=None):
    """
    Processes uploaded documents:
    1. Extracts text
    2. Chunks text
    3. Creates vector store
    4. Initializes chain
    Returns concatenated raw text for analytics.
    """
    try:
        full_text = ""
        all_chunks = []
        
        for doc in docs:
            # Extract text
            file_text = get_text_from_file(doc)
            if file_text:
                full_text += file_text + "\n\n"
                
                # Create chunks and add metadata
                # Note: get_chunks expects a string and returns Documents
                doc_chunks = get_chunks(file_text)
                for chunk in doc_chunks:
                    chunk.metadata['source'] = doc.name
                
                all_chunks.extend(doc_chunks)

        if not all_chunks:
            st.error("No valid text found in uploaded documents.")
            return None

        # Create Knowledge Base (Vector Store)
        vectorstore = get_vectorstore(all_chunks)

        if vectorstore:
            st.session_state.conversation = get_conversationchain(vectorstore, api_key=api_key)
            return full_text
        else:
            st.error("Failed to create knowledge base.")
            return None

    except Exception as e:
        st.error(f"System Error: {str(e)}")
        return None
