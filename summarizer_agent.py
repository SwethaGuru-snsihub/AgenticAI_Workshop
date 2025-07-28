from langchain_groq import ChatGroq
from config import groq_api_key

# Uses llama3 model to summarize input content
def summarize_agent(raw_text: str) -> str:
    prompt = f"""Summarize the following content in a clear, structured format:
    
    {raw_text}
    
    Summary:"""

    try:
        llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error in summarizer: {str(e)}"
