import streamlit as st
from agent import app, memory
import time

# Set page configuration
st.set_page_config(
    page_title="LangGraph Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .main-header { color: #52357B; font-size: 2.5em; font-weight: bold; }
    .sub-header { color: #648DB3; font-size: 1.5em; margin-top: 20px; }
    .response-box { 
        background-color: #F5F5F5; 
        padding: 15px; 
        border-radius: 10px; 
        border: 1px solid #E0E0E0; 
        margin-top: 10px; 
    }
    .query-button { 
        background-color: #42A5F5; 
        color: white; 
        border-radius: 5px; 
        padding: 8px; 
        margin: 5px; 
    }
    .error-box { 
        background-color: #FFEBEE; 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px solid #EF5350; 
    }
    .sidebar .stButton>button { 
        width: 100%; 
        background-color: #EF5350; 
        color: white; 
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for history and controls
with st.sidebar:
    st.header("Query History")
    history = memory.load_memory_variables({})["history"]
    if history:
        with st.expander("View Past Queries"):
            for i, (input_msg, output_msg) in enumerate(zip(history[::2], history[1::2])):
                st.markdown(f"**Q{i+1}:** {input_msg.content}")
                st.markdown(f"**A{i+1}:** {output_msg.content[:100]}...")
    if st.button("Clear History", key="clear_history"):
        memory.clear()
        st.success("Conversation history cleared!")
        st.rerun()

# Main content
st.markdown('<div class="main-header">🔍 LangGraph Research Assistant</div>', unsafe_allow_html=True)
st.markdown("""
This intelligent assistant leverages a multi-agent system to answer your questions using:
- 🌐 **Web Search** for current information
- 📚 **Knowledge Base (RAG)** for predefined data
- 🧠 **LLM Summarization** for concise, structured responses
- 💬 **Conversational Memory** for context-aware answers

**Try these example queries:**
""")

# Example query buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("What is LangGraph?", key="example1", help="Ask about LangGraph"):
        st.session_state.user_input = "What is LangGraph and how is it used?"
with col2:
    if st.button("AI Trends", key="example2", help="Ask about generative AI trends"):
        st.session_state.user_input = "Current trends in generative AI?"
with col3:
    if st.button("Vector Stores", key="example3", help="Ask about vector stores"):
        st.session_state.user_input = "Explain vector stores in LangChain"

# Query input
st.markdown('<div class="sub-header">Ask Your Question</div>', unsafe_allow_html=True)
user_input = st.text_input(
    "Enter your research question:",
    value=st.session_state.get("user_input", ""),
    placeholder="e.g., What is LangGraph used for?",
    key="query_input"
)

# Process query
if user_input:
    st.markdown('<div class="sub-header">Response</div>', unsafe_allow_html=True)
    with st.spinner("🔄 Researching and summarizing..."):
        try:
            # Invoke the LangGraph app with history
            response = app.invoke({"input": user_input, "history": memory.load_memory_variables({})["history"]})
            result = response.get("result", "No result")
            st.markdown(f'<div class="response-box">{result}</div>', unsafe_allow_html=True)
            # Add copy button for response
            st.button("Copy Response", on_click=lambda: st.write_clipboard(result), key="copy_response")
        except Exception as e:
            st.markdown(f'<div class="error-box">❌ Error: {str(e)}</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
---
*Built with LangGraph, powered by LLaMA3 via Groq API. Supports web search, RAG, and conversational memory.*
""")