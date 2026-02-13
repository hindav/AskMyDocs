from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_openai import ChatOpenAI
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
    ("system", "You are an AI assistant that answers questions based on the provided context. When asked, use your general knowledge to respond if the context does not have the necessary information. For greetings or unrelated queries, respond appropriately without relying solely on the context."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    ("system", "Here is the context from the documents (if available):"),
    ("user", "{context}"),
    ("system", "Based on the context and your general knowledge, provide the most relevant and complete answer to the user's query.")
])

def get_conversationchain(vectorstore, api_key=None):
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        st.error("GROQ_API_KEY not found. Please provide it in the sidebar settings or .env file.")
        return None

    try:
        # Use Groq API (OpenAI-compatible)
        llm = ChatOpenAI(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        retriever = vectorstore.as_retriever()

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
            # Format the chat history properly
            formatted_history = format_chat_history(st.session_state.chat_history)
            
            # Prepare the input for the chain
            chain_input = {
                "chat_history": formatted_history,
                "input": question
            }

            # Invoke the chain
            response = st.session_state.conversation.invoke(chain_input)
            
            # Extract the answer from the response
            answer = response.get('answer', None)
            context = response.get('context', [])

            # Source Citations
            sources_text = ""
            if context:
                sources_text += "\n\n---\n**📚 Sources:**"
                unique_sources = set()
                for doc in context:
                    source = doc.metadata.get('source', 'Unknown Document')
                    unique_sources.add(os.path.basename(source))
                
                for src in unique_sources:
                    sources_text += f"\n- `{src}`"

            # If no answer, fall back to general response
            if not answer or answer.strip() == "":
                fallback_llm = ChatOpenAI(
                    temperature=0.7,
                    base_url="https://api.groq.com/openai/v1",
                    api_key=api_key or os.getenv("GROQ_API_KEY"),
                    model="llama-3.3-70b-versatile"
                )
                answer = fallback_llm.invoke([HumanMessage(content=question)]).content.strip()

            return answer + sources_text

        except Exception as e:
            st.error(f"Error processing question: {str(e)}")
            return None
    else:
        st.error("Please process documents first before asking questions.")
        return None
