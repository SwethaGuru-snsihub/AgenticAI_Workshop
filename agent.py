from langgraph.graph import StateGraph
from typing import TypedDict
from config import groq_api_key
from web_research_agent import web_research_agent
from rag_agent import rag_agent
from summarizer_agent import summarize_agent
from langchain_groq import ChatGroq
from langchain.memory import ConversationBufferMemory
import re

# Initialize memory
memory = ConversationBufferMemory(return_messages=True)

# 1. Define State Schema
class GraphState(TypedDict):
    input: str
    next: str
    raw_result: str
    result: str
    history: str  # Added to store conversation history

# 2. Router Agent
def router(state):
    prompt = state["input"].lower()
    # Include conversation history in routing decision
    history = memory.load_memory_variables({})["history"]
    full_prompt = f"{history}\nCurrent query: {prompt}"
    
    if any(word in prompt for word in ["latest", "current", "news", "happening", "today"]):
        return {"next": "web", "history": history}
    return {"next": "rag", "history": history}

# 3. Web Research Agent Node
def web_node(state):
    query = state["input"]
    raw = web_research_agent(query)
    return {"raw_result": raw, "next": "summarize", "history": state["history"]}

# 4. RAG Agent Node
def rag_node(state):
    query = state["input"]
    raw = rag_agent(query)
    return {"raw_result": raw, "next": "summarize", "history": state["history"]}

# 5. Summarization Agent Node
def summarize_node(state):
    raw = state.get("raw_result", "")
    summary = summarize_agent(raw)
    # Save conversation to memory
    memory.save_context({"input": state["input"]}, {"output": summary})
    return {"result": summary, "history": state["history"]}

# 6. LLM Fallback (optional, not triggered by router)
def llm_node(state):
    llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)
    try:
        response = llm.invoke(state["input"])
        # Save to memory
        memory.save_context({"input": state["input"]}, {"output": response.content})
        return {"result": response.content, "history": state["history"]}
    except Exception as e:
        return {"result": f"Error from LLM: {str(e)}", "history": state["history"]}

# 7. Build LangGraph
graph = StateGraph(GraphState)

graph.set_entry_point("router")
graph.add_node("router", router)
graph.add_node("web", web_node)
graph.add_node("rag", rag_node)
graph.add_node("summarize", summarize_node)

graph.add_conditional_edges(
    "router",
    lambda state: state.get("next", "rag"),  # default to rag
    {
        "web": "web",
        "rag": "rag",
    }
)

graph.add_edge("web", "summarize")
graph.add_edge("rag", "summarize")

graph.set_finish_point("summarize")

app = graph.compile()

# 8. Test Cases
if __name__ == "__main__":
    test_inputs = [
        "What is LangGraph and how is it used?",
        "Current trends in generative AI?",
        "Explain vector stores in LangChain",
    ]

    for query in test_inputs:
        print(f"\n🔹 Input: {query}")
        try:
            result = app.invoke({"input": query, "history": memory.load_memory_variables({})["history"]})
            print(f"✅ Output:\n{result.get('result', 'No result')}")
        except Exception as e:
            print(f"❌ Error: {e}")