import streamlit as st
import os
import base64
from PIL import Image
from dotenv import load_dotenv

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
        im = "🤖" # Fallback if file not found

    st.set_page_config(
        page_title="AskMyDocs",
        page_icon=im,
        layout="wide"
    )

    # Custom CSS for Modern Look (Theme Compatible)
    st.markdown("""
    <style>
        /* Chat Messages */
        .stChatMessage {
            background-color: transparent !important;
            border-bottom: 1px solid rgba(128, 128, 128, 0.2);
            padding-bottom: 1.5rem !important;
            padding-top: 1.5rem !important;
            transition: background-color 0.2s ease;
        }
        .stChatMessage:hover {
            background-color: rgba(128, 128, 128, 0.05) !important;
        }

        /* Input Field Styling */
        .stChatInput textarea {
            border-radius: 12px !important;
            padding: 12px !important;
            border: 1px solid rgba(128, 128, 128, 0.2) !important;
        }
        .stChatInput textarea:focus {
            border-color: #4ECDC4 !important;
            box-shadow: 0 0 10px rgba(78, 205, 196, 0.2) !important;
        }

        /* Buttons under Sidebar */
        .stButton button {
            background: linear-gradient(90deg, #4ECDC4 0%, #556270 100%);
            border: none;
            color: white;
            font-weight: 600;
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            width: 100%;
            transition: all 0.3s ease;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
            color: white !important;
        }

        /* Typography */
        h1 {
            background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
        }

        /* Expander Styling */
        .streamlit-expanderHeader {
            border-radius: 8px;
            background-color: rgba(128, 128, 128, 0.05);
        }
        
        /* Code Blocks */
        code {
            border-radius: 4px;
            padding: 0.2em 0.4em;
        }
    </style>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "docs" not in st.session_state:
        st.session_state.docs = []
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

    # Title placed in the header bar
    st.markdown("""
    <div style='position: fixed; top: 12px; left: 50%; transform: translateX(-50%); z-index: 999999; display: flex; align-items: center; gap: 10px; pointer-events: none;'>
        <h1 style='margin: 0; padding: 0; font-size: 2.8rem; background: -webkit-linear-gradient(45deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
            🤖 AskMyDocs
        </h1>
    </div>
    """, unsafe_allow_html=True)

    # Subtitle in main flow
    st.markdown("<h5 style='text-align: center; color: gray; margin-top: 10px;'>Chat with Your Documents</h5>", unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # Groq API Key Section
        with st.expander("🔑 Groq API Setup", expanded=not os.getenv("GROQ_API_KEY")):
            st.markdown("""
            1. Go to **[Groq Console](https://console.groq.com/keys)**.
            2. Log in and click **Create API Key**.
            3. Copy your key and paste it below.
            """)
            api_key_input = st.text_input(
                "Enter Groq API Key", 
                type="password", 
                placeholder="gsk_...",
                help="Your key is not stored permanently."
            )
            
            if not api_key_input and not os.getenv("GROQ_API_KEY"):
                st.warning("⚠️ API Key is required!")
            else:
                st.success("API Key detected!")

        st.divider()

        # Settings
        st.markdown("### 🛠️ Functionality")
        st.session_state.enable_refinement = st.toggle(
            "✨ Activate prompt refinement capability", 
            value=st.session_state.enable_refinement,
            help="Uses AI to rewrite your question for better results."
        )
        
        st.divider()

        # File Uploader
        st.markdown("### 📂 Document Upload")
        docs = st.file_uploader(
            "Upload PDF, TXT, CSV, DOCX", 
            accept_multiple_files=True, 
            type=["pdf", "txt", "csv", "docx"]
        )
        
        process_btn = st.button("🚀 Process Documents", use_container_width=True)

        if process_btn:
            if docs:
                with st.spinner("Analyzing & indexing documents..."):
                    # Reset
                    st.session_state.chat_history = []
                    st.session_state.conversation = None
                    st.session_state.summary = None
                    st.session_state.analytics = None
                    
                    # Process
                    raw_text = process_documents(docs, api_key=api_key_input)
                    st.session_state.processed = True
                    
                    # Generate Summary & Analytics
                    if raw_text:
                        st.session_state.summary = generate_summary(raw_text, api_key_input)
                        st.session_state.analytics = analyze_document(raw_text)
                    
                    st.rerun()

            else:
                st.error("Please upload files first.")

        if st.session_state.processed:
            st.success("✅ Ready!")

    # Main Interface with Tabs
    if not st.session_state.processed:
        st.info("👈 Please upload and process documents in the sidebar to start chatting.")
    else:
        tab1, tab2 = st.tabs(["💬 Chat", "📊 Document Insights"])
        
        with tab1:
            # Create a scrollable container for chat history
            # Height ensures the input bar (pinned to bottom) doesn't overlap weirdly if page is short,
            # and gives a "window" feel.
            chat_container = st.container(height=600)

            with chat_container:
                # Display Chat History
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            # Chat Input
            if prompt := st.chat_input("Ask about your documents..."):
                # Append user message to history
                st.session_state.chat_history.append({"role": "user", "content": prompt})
                
                # Display user message immediately in the container
                with chat_container:
                    st.chat_message("user").markdown(prompt)

                    # Refinement Logic
                    final_prompt = prompt
                    if st.session_state.enable_refinement:
                        with st.status("Refining question...", expanded=False) as status:
                            refined = refine_prompt_with_llm(prompt, api_key=api_key_input)
                            status.write(f"Refined to: {refined}")
                            final_prompt = refined
                            status.update(label="Question refined!", state="complete")

                    # Generate Response
                    with st.chat_message("assistant"):
                        with st.spinner("Diving deep..."):
                            response = get_ai_response(final_prompt, api_key=api_key_input)
                            
                            if response:
                                st.markdown(response)
                                st.session_state.chat_history.append({"role": "assistant", "content": response})
        
        with tab2:
            st.markdown("### 📝 AI Summary")
            if st.session_state.summary:
                st.info(st.session_state.summary)
            else:
                st.warning("No summary available yet.")
            
            st.divider()
            
            if st.session_state.analytics:
                display_analytics(st.session_state.analytics)
            else:
                st.warning("No analytics data available.")

    # Clear History setup
    # Clear History setup
    with st.sidebar:
        st.divider()
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()

    # Footer & About Section
    st.divider()
    
    # Load logo for About section
    try:
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'icons', 'ico.png')
        img_base64 = get_base64_image(icon_path)
        logo_html = f'<img src="data:image/png;base64,{img_base64}" style="vertical-align: middle; height: 40px; width: 40px; border-radius: 50%; margin-right: 10px;">'
    except:
        logo_html = "👨‍💻"

    st.markdown("### About Me")
    st.markdown(f"""
    <div style="text-align: center; padding: 25px; background: linear-gradient(145deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02)); border-radius: 15px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2 style="margin: 0; padding-bottom: 10px; color: #4ECDC4;">
            <a href="https://hindav.vercel.app/" target="_blank" style="text-decoration: none; color: inherit; cursor: pointer;">
                {logo_html} Hindav
            </a>
        </h2>
        <p style="color: #aaa; font-size: 1.0em; margin-bottom: 20px;">Solo Developer & AI Enthusiast</p>
        <div style="display: flex; justify-content: center; gap: 25px; flex-wrap: wrap;">
            <a href="https://www.linkedin.com/in/hindav/" target="_blank" style="text-decoration: none; color: #0077b5; font-weight: bold; padding: 8px 16px; background: rgba(0,119,181,0.1); border-radius: 20px; transition: all 0.3s;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" style="vertical-align: middle;"> LinkedIn
            </a>
            <a href="https://github.com/hindav" target="_blank" style="text-decoration: none; color: #ffffff; font-weight: bold; padding: 8px 16px; background: #333; border-radius: 20px; transition: all 0.3s;">
                <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" width="20" style="vertical-align: middle; filter: invert(1);"> GitHub
            </a>
            <a href="mailto:hindav.dev@gmail.com" style="text-decoration: none; color: #D44638; font-weight: bold; padding: 8px 16px; background: rgba(212,70,56,0.1); border-radius: 20px; transition: all 0.3s;">
                <img src="https://cdn-icons-png.flaticon.com/512/732/732200.png" width="20" style="vertical-align: middle;"> Email
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)



if __name__ == '__main__':
    main()
