import fitz  # PyMuPDF
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

IMAGE_EXTRACT_DIR = "extracted_images"
if not os.path.exists(IMAGE_EXTRACT_DIR):
    os.makedirs(IMAGE_EXTRACT_DIR)

def extract_from_pdf(pdf_path_or_file, is_path=True):
    """Extracts text and images from a PDF using PyMuPDF."""
    documents = []
    
    if is_path:
        doc = fitz.open(pdf_path_or_file)
        filename = os.path.basename(pdf_path_or_file)
    else:
        # Handle Streamlit uploaded file (binary stream)
        file_bytes = pdf_path_or_file.read()
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        filename = getattr(pdf_path_or_file, "name", "uploaded_pdf")

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        # Check for images on the page
        image_list = page.get_images(full=True)
        images_on_page = []
        
        if image_list:
            for img_index, img in enumerate(image_list):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                # Save image
                image_filename = f"{filename}_p{page_num+1}_img{img_index+1}.{image_ext}"
                image_path = os.path.join(IMAGE_EXTRACT_DIR, image_filename)
                
                # We only save if it's large enough to be a "photo" and not a small icon
                if len(image_bytes) > 2000: # 2KB threshold
                    with open(image_path, "wb") as f:
                        f.write(image_bytes)
                    images_on_page.append(image_path)

        if text.strip() or images_on_page:
            documents.append(Document(
                page_content=text,
                metadata={
                    "source": filename,
                    "page": page_num + 1,
                    "images": images_on_page
                }
            ))
    
    doc.close()
    return documents

def get_text_from_file(uploaded_file):
    """Legacy extractor for non-PDF files."""
    try:
        if uploaded_file.type == "text/plain":
            text = uploaded_file.read().decode('utf-8')
            return [Document(page_content=text, metadata={"source": uploaded_file.name})]
        elif uploaded_file.type == "text/csv":
            text = "".join(", ".join(row) + "\n" for row in csv.reader(uploaded_file.read().decode('utf-8').splitlines()))
            return [Document(page_content=text, metadata={"source": uploaded_file.name})]
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            elements = partition(file=uploaded_file)
            text = "\n".join(map(str, elements))
            return [Document(page_content=text, metadata={"source": uploaded_file.name})]
        return []
    except Exception as e:
        st.error(f"Error reading file '{uploaded_file.name}': {e}")
        return []

def process_documents(docs=None, data_dir=None, api_key=None, force_reindex=False):
    """
    Processes documents from either uploaded files or a local directory.
    Uses saved index if available to save time.
    """
    try:
        # 1. Try to load existing vectorstore first (FAST PATH)
        if not force_reindex:
            vectorstore = get_vectorstore(force_reindex=False)
            if vectorstore:
                st.session_state.conversation = get_conversationchain(vectorstore, api_key=api_key)
                return "Loaded from saved index. No PDF processing required."

        # 2. SLOW PATH: Process documents
        all_documents = []
        
        # 1. Process from directory
        if data_dir and os.path.exists(data_dir):
            for file in os.listdir(data_dir):
                file_path = os.path.join(data_dir, file)
                if file.lower().endswith(".pdf"):
                    all_documents.extend(extract_from_pdf(file_path))
        
        # 2. Process from memory (Streamlit upload)
        if docs:
            for doc in docs:
                if doc.name.lower().endswith(".pdf"):
                    all_documents.extend(extract_from_pdf(doc, is_path=False))
                else:
                    all_documents.extend(get_text_from_file(doc))

        if not all_documents:
            st.error("No valid documents found and no saved index exists.")
            return None

        # Create Knowledge Base (Vector Store)
        all_chunks = get_chunks(all_documents)
        vectorstore = get_vectorstore(all_chunks, force_reindex=True)

        if vectorstore:
            st.session_state.conversation = get_conversationchain(vectorstore, api_key=api_key)
            full_text = "\n".join([d.page_content for d in all_documents[:100]])
            return full_text
        else:
            st.error("Failed to create knowledge base.")
            return None

    except Exception as e:
        import traceback
        st.error(f"System Error: {str(e)}")
        st.code(traceback.format_exc())
        return None
