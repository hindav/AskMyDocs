import streamlit as st
import os
import base64
from PIL import Image
from dotenv import load_dotenv
import warnings

# Suppress noisy warnings globally
try:
    from langchain_core._api import LangChainDeprecationWarning
    warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
except ImportError:
    pass

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

from document_utils import process_documents
from conversation import get_ai_response
from prompt_refiner import refine_prompt_with_llm
from analytics import generate_summary, analyze_document, display_analytics

load_dotenv()

def main():
    # Load custom icon
    try:
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons', 'ico.png')
        im = Image.open(icon_path)
    except Exception:
        im = "📚" # Fallback if file not found

    st.set_page_config(
        page_title="AskMyDocs - Dental Edition",
        page_icon=im,
        layout="wide"
    )

    # Custom CSS
    st.markdown("""
    <style>
        .stChatMessage {
            background-color: transparent !important;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            padding-bottom: 1.5rem !important;
            padding-top: 1.5rem !important;
        }
        .stChatInput textarea { border-radius: 12px !important; }
        .stButton button {
            background: linear-gradient(90deg, #4ECDC4 0%, #556270 100%);
            color: white; border-radius: 8px; width: 100%;
        }
        h1 {
            background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed" not in st.session_state:
        st.session_state.processed = False
    if "enable_refinement" not in st.session_state:
        st.session_state.enable_refinement = False
    if "summary" not in st.session_state:
        st.session_state.summary = None
    if "analytics" not in st.session_state:
        st.session_state.analytics = None

    # Auto-indexing on start
    DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    if not st.session_state.processed and os.path.exists(DATA_DIR):
        with st.spinner("📦 Loading library..."):
            status_text = process_documents(data_dir=DATA_DIR)
            if status_text:
                st.session_state.processed = True
                if "Loaded from saved index" in status_text:
                    st.session_state.summary = "🚀 Instant Load: Using pre-computed medical index (FAISS)."
                else:
                    st.session_state.summary = "✨ Successfully indexed books from the data folder."

    # Header
    st.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h1 style='font-size: 3rem;'>📖 AskMyDocs <span style='font-size: 1rem; color: gray;'>v2.9.25</span></h1>
        <p style='color: gray;'>Dental Reference Library Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ System Status")
        if st.session_state.processed:
            st.success("✅ Library Indexed")
        else:
            st.warning("⚠️ No documents indexed")

        st.divider()
        st.markdown("### � API Override (Optional)")
        api_key_input = st.text_input("Groq API Key (leave empty for local Ollama)", type="password")
        
        st.divider()
        st.markdown("### 🛠️ Options")
        st.session_state.enable_refinement = st.toggle("✨ Prompt Refinement", value=st.session_state.enable_refinement)
        
        if st.button("🔄 Force Re-index Data/"):
            with st.spinner("📑 Re-processing all documents... this may take a while."):
                status_text = process_documents(data_dir=DATA_DIR, force_reindex=True)
                if status_text:
                    st.session_state.processed = True
                    st.session_state.summary = "✅ Re-indexed all documents successfully."
                    st.rerun()

        st.divider()
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Chat Interface
    if not st.session_state.processed:
        st.info("No documents found in `data/`. Please add books to the folder.")
    else:
        tab1, tab2 = st.tabs(["💬 Consult AI", "📊 Library Insights"])
        
        with tab1:
            chat_container = st.container(height=600)
            with chat_container:
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
                        if "images" in message:
                            for img_path in message["images"]:
                                if os.path.exists(img_path):
                                    # Display image at roughly 60% width
                                    st.image(img_path, width=450)

            if prompt := st.chat_input("Ask a dental question..."):
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                with chat_container:
                    st.chat_message("user").markdown(prompt)

                    final_prompt = prompt
                    if st.session_state.enable_refinement:
                        with st.status("Refining question...", expanded=False):
                            final_prompt = refine_prompt_with_llm(prompt, api_key=api_key_input)

                    with st.chat_message("assistant"):
                        with st.spinner("Searching medical records..."):
                            result = get_ai_response(final_prompt, api_key=api_key_input)
                            
                            if result:
                                answer = result["answer"]
                                images = result["images"]
                                
                                st.markdown(answer)
                                for img_path in images:
                                    if os.path.exists(img_path):
                                        st.image(img_path, caption="Reference Image from Book", width=450)
                                
                                st.session_state.chat_history.append({
                                    "role": "assistant", 
                                    "content": answer,
                                    "images": images
                                })
        
        with tab2:
            st.markdown("### 📝 Library Summary")
            st.info(st.session_state.summary if st.session_state.summary else "No summary available.")
            if st.session_state.analytics:
                display_analytics(st.session_state.analytics)

    # Footer
    st.divider()
    st.markdown("<p style='text-align: center; color: gray;'>Built with ❤️ for Dental Professionals</p>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
