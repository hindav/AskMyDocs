from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

load_dotenv()

def refine_prompt_with_llm(question, api_key=None):
    if not api_key:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            return question  # Fallback if no key
            
    try:
        llm = ChatOpenAI(
            model="google/gemini-2.0-flash-exp:free", # Using free model for refinement if possible, or Groq
            # Actually, let's stick to Groq for consistency and speed if provided
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key,
            temperature=0.3
        )
        
        # Override model if using Groq base URL (Groq doesn't host Gemini)
        if "groq.com" in llm.base_url:
            llm.model_name = "llama-3.3-70b-versatile"

        messages = [
            SystemMessage(content="You are an expert at refining user questions for RAG systems. Rewrite the following question to be more specific, self-contained, and optimized for vector search. Return ONLY the refined question, no explanations."),
            HumanMessage(content=question)
        ]
        
        response = llm.invoke(messages)
        return response.content.strip()
    except Exception as e:
        # st.error(f"Error refining prompt: {e}") # Don't error UI for this, just return original
        return question
