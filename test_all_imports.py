import sys
import os

print("--- Testing Imports ---")

try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    print("✅ langchain_text_splitters.RecursiveCharacterTextSplitter: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_text_splitters.RecursiveCharacterTextSplitter: FAILED ({e})")

try:
    from langchain_community.vectorstores import FAISS
    print("✅ langchain_community.vectorstores.FAISS: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_community.vectorstores.FAISS: FAILED ({e})")

try:
    from langchain_community.embeddings import HuggingFaceEmbeddings
    print("✅ langchain_community.embeddings.HuggingFaceEmbeddings: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_community.embeddings.HuggingFaceEmbeddings: FAILED ({e})")
    try:
        from langchain_huggingface import HuggingFaceEmbeddings
        print("✅ langchain_huggingface.HuggingFaceEmbeddings: SUCCESS (Migration required)")
    except ImportError as e2:
        print(f"❌ langchain_huggingface.HuggingFaceEmbeddings: FAILED ({e2})")

try:
    from langchain_core.documents import Document
    print("✅ langchain_core.documents.Document: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_core.documents.Document: FAILED ({e})")

try:
    from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
    print("✅ langchain_classic.chains (history_aware/retrieval): SUCCESS")
except ImportError as e:
    print(f"❌ langchain_classic.chains (history_aware/retrieval): FAILED ({e})")

try:
    from langchain_classic.chains.combine_documents import create_stuff_documents_chain
    print("✅ langchain_classic.chains.combine_documents: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_classic.chains.combine_documents: FAILED ({e})")

try:
    from langchain_openai import ChatOpenAI
    print("✅ langchain_openai.ChatOpenAI: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_openai.ChatOpenAI: FAILED ({e})")

try:
    from langchain_ollama import ChatOllama
    print("✅ langchain_ollama.ChatOllama: SUCCESS")
except ImportError as e:
    print(f"❌ langchain_ollama.ChatOllama: FAILED ({e})")

print("--- End of Testing ---")
