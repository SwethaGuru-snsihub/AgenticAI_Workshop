import streamlit as st
from agent import app

st.set_page_config(page_title="Math & General Query Agent", layout="centered", page_icon="🧮")

st.title("🧮 Math & General Query Agent")
st.markdown("""
- Math: "What is 15 plus 25?" or "Divide 144 by 12"
- General: "What is the capital of France?" or "Explain artificial intelligence"
""")

st.subheader("Enter Your Query")
user_input = st.text_input("Type your question here:", placeholder="e.g., What is 8 times 9? or What is photosynthesis?")

if user_input:
    with st.spinner("Processing your query..."):
        try:
            result = app.invoke({"input": user_input})
            output = result.get("result", "No result returned")
            st.subheader("Result")
            st.success(output)
        except Exception as e:
            st.error(f"Error: {str(e)}")

st.subheader("Example Queries")
st.markdown("""
Try these examples:
- **Math**: "What is 100 minus 37?" → "The result is 63"
- **Math**: "What is 8 times 9?" → "The result is 72"
- **Math**: "Divide 10 by 0" → "Error: Cannot divide by zero"
- **General**: "What is artificial intelligence?" → A detailed LLM response
""")

st.markdown("---")
st.markdown("Built with LangGraph and Groq API | © 2025")

# Add a button to clear the chat
if st.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()