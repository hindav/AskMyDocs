from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
import streamlit as st
from dotenv import load_dotenv
import os
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

load_dotenv()

# Updated Prompts
prompt_search_query = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("user", "Given the above conversation, generate a search query to look up information relevant to the conversation.")
])

prompt_get_answer = ChatPromptTemplate.from_messages([
    ("system", """You are a professional medical/dental AI assistant preparing students for exams. 
    Follow these specific length requirements:
    1. If the user asks for a 'Short Note' or 'Short Answer': Provide a comprehensive, structured answer roughly equivalent to 1 full page (approx 500-600 words). Use headings, bullet points, and clinical significance.
    2. If the user asks for a 'Long Note' or 'Long Answer': Provide an exhaustive, detailed answer equivalent to 3 full pages (approx 1500-1800 words). Include classification, etiology, pathophysiology, clinical features, histopathology, diagnosis, and management in depth.
    3. For all other queries: Be concise but thorough.
    
    Answer ONLY based on the provided context if possible. If the context is insufficient, state that first, then use your knowledge base."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("system", "Context from books:"),
    ("user", "{context}"),
])

def get_conversationchain(vectorstore, api_key=None):
    # Try to get API key from: 1. Argument, 2. Env Var, 3. Streamlit Secrets (for Cloud)
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        try:
            if "GROQ_API_KEY" in st.secrets:
                api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            # secrets.toml doesn't exist or isn't accessible
            pass

    try:
        if api_key:
            llm = ChatOpenAI(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                base_url="https://api.groq.com/openai/v1",
                api_key=api_key
            )
        else:
            # Check if we are running locally (Ollama only works locally)
            try:
                llm = ChatOllama(
                    model="llama3.2",
                    temperature=0.2,
                )
            except Exception:
                st.error("⚠️ **Ollama not found.** If you are running this online, you MUST provide a Groq API Key in the sidebar.")
                return None
        
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        # Create history-aware retriever
        retriever_chain = create_history_aware_retriever(llm, retriever, prompt_search_query)

        # Create document chain
        document_chain = create_stuff_documents_chain(llm, prompt_get_answer)

        # Create retrieval chain
        retrieval_chain = create_retrieval_chain(retriever_chain, document_chain)

        return retrieval_chain
    except Exception as e:
        st.error(f"Error creating conversation chain: {str(e)}")
        return None

def format_chat_history(chat_history):
    formatted_messages = []
    for message in chat_history:
        if message["role"] == "user":
            formatted_messages.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            formatted_messages.append(AIMessage(content=message["content"]))
    return formatted_messages

def get_ai_response(question, api_key=None):
    if st.session_state.conversation:
        try:
            formatted_history = format_chat_history(st.session_state.chat_history)
            
            chain_input = {
                "chat_history": formatted_history,
                "input": question
            }

            response = st.session_state.conversation.invoke(chain_input)
            
            answer = response.get('answer', "")
            context = response.get('context', [])

            # Image extraction from context
            found_images = []
            sources_text = ""
            if context:
                sources_text += "\n\n---\n**📚 Sources:**"
                unique_sources = set()
                for doc in context:
                    src_name = os.path.basename(doc.metadata.get('source', 'Unknown'))
                    page_num = doc.metadata.get('page', '?')
                    unique_sources.add(f"{src_name} (Page {page_num})")
                    
                    # Collect images
                    page_images = doc.metadata.get('images', [])
                    for img in page_images:
                        if img not in found_images:
                            found_images.append(img)
                
                for src in unique_sources:
                    sources_text += f"\n- `{src}`"

            return {
                "answer": answer + sources_text,
                "images": found_images
            }

        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
            return None
    else:
        st.error("Please process documents first.")
        return None
