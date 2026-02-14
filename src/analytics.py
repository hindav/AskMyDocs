
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from collections import Counter
import nltk
from nltk.corpus import stopwords
import re

# Download required NLTK data (if not already present, though we ran commands for this earlier)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')

def generate_summary(text, api_key):
    """Generates a summary using the LLM via Groq."""
    if not text:
        return "No text available to summarize."
    
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import SystemMessage, HumanMessage
    
    try:
        llm = ChatOpenAI(
            model="llama-3.3-70b-versatile",
            temperature=0.3,
            base_url="https://api.groq.com/openai/v1",
            api_key=api_key
        )
        
        # Truncate text if too long (approx 10k chars for safety, though model handles more)
        truncated_text = text[:15000]
        
        messages = [
            SystemMessage(content="You are a helpful assistant that summarizes documents concisely."),
            HumanMessage(content=f"Please provide a concise summary of the following text:\n\n{truncated_text}")
        ]
        
        response = llm.invoke(messages)
        return response.content
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def analyze_document(text):
    """Generates analytics for the document."""
    
    # 1. Word Count & Token Estimation
    words = nltk.word_tokenize(text)
    word_count = len(words)
    estimated_reading_time = round(word_count / 200) # Average reading speed 200 wpm
    
    # 2. Most Common Words (excluding stopwords)
    stop_words = set(stopwords.words('english'))
    # Add common document words to ignore
    stop_words.update(['page', 'document', 'fig', 'figure', 'table', 'et', 'al'])
    
    filtered_words = [
        word.lower() for word in words 
        if word.isalnum() and word.lower() not in stop_words and len(word) > 2
    ]
    
    word_freq = Counter(filtered_words)
    common_words = word_freq.most_common(10)
    
    return {
        "word_count": word_count,
        "reading_time": estimated_reading_time,
        "common_words": common_words,
        "raw_text_for_cloud": " ".join(filtered_words)
    }

def display_analytics(analytics_data):
    """Displays the analytics in Streamlit."""
    
    st.markdown("### 📊 Document Analytics")
    
    # Metrics in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Words", f"{analytics_data['word_count']:,}")
    with col2:
        st.metric("Est. Reading Time", f"{analytics_data['reading_time']} min")
    
    # Word Cloud
    st.markdown("#### Word Cloud")
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='#1e1e1e',  # Dark background to match theme
        colormap='viridis',
        max_words=100
    ).generate(analytics_data['raw_text_for_cloud'])
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    # Set plot background to transparent
    fig.patch.set_alpha(0) 
    st.pyplot(fig)
    
    # Top Words Bar Chart
    st.markdown("#### Top Keywords")
    common_words = analytics_data['common_words']
    if common_words:
        df = {"Word": [w[0] for w in common_words], "Count": [w[1] for w in common_words]}
        fig_bar = px.bar(
            df, 
            x='Word', 
            y='Count', 
            text_auto=True,
            color='Count',
            color_continuous_scale='Teal'
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            showlegend=False
        )
        st.plotly_chart(fig_bar, use_container_width=True)
