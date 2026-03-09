import streamlit as st
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import nltk
import warnings

# Suppress noisy LangChain deprecation warnings
from langchain_core._api import LangChainDeprecationWarning
warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
# Suppress HuggingFace Hub unauthenticated warning
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

# Ensure NLTK data is downloaded for cloud environments
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

VECTOR_STORE_PATH = "faiss_index"

def get_chunks(documents):
    """
    Chunks a list of Document objects while preserving metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

def get_vectorstore(chunks=None, force_reindex=False):
    try:
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 1. Try to load existing index if not forcing re-index
        if not force_reindex and os.path.exists(VECTOR_STORE_PATH):
            return FAISS.load_local(VECTOR_STORE_PATH, embeddings, allow_dangerous_deserialization=True)
            
        # 2. Create new index if chunks are provided
        if chunks:
            vectorstore = FAISS.from_documents(chunks, embeddings)
            # Save for future use
            vectorstore.save_local(VECTOR_STORE_PATH)
            return vectorstore
        
        return None
    except Exception as e:
        st.error(f"Error handling vector store: {str(e)}")
        return None
