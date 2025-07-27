# LangGraph Multi-Agent Research and Summarization System

This project implements a multi-agent system using **LangGraph** that can:

- 🌐 Perform live web research using Tavily
- 📚 Retrieve answers from a knowledge base using FAISS (RAG)
- ✨ Summarize all responses using a Groq LLM

---

## Agents and Their Roles

| Agent              | Role                                                                |
|------------------- |---------------------------------------------------------------------|
| Router Agent       | Decides where to send the query (web search or RAG)                 |
| Web Research Agent | Uses Tavily to get real-time web content                            |
| RAG Agent          | Searches local documents using FAISS and OpenAI embeddings          |
| Summarizer Agent   | Uses LLM to summarize and structure the final response              |

---

## Architecture

- Uses **LangGraph** to create a modular flow
- Automatically routes queries to the correct agent
- All responses are summarized for clarity

---

## Example Queries

Try asking:

- “What is LangGraph used for?”
- “Current trends in AI?”
- “Explain vector stores in LangChain.”

---

## How to Run

### 1. Setup Environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
# OR
source venv/bin/activate  # On macOS/Linux
```
### 2. Install Dependencies

```bash
pip install -r requirements.txt
```
### 3. Add .env File
Create a .env file in the root directory and add:
```bash
GROQ_API_KEY=your_groq_key_here
TAVILY_API_KEY=your_tavily_key_here
```
### 4. Add Your Knowledge Base
Place a .txt file inside the data/ folder, for example:
```bash
data/sample.txt
```
### 5. Run the App
```bash
streamlit run app.py
```
