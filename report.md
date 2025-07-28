LangGraph Multi-Agent Research and Summarization System Report
Overview
This project implements a multi-agent research and summarization system using LangGraph, as specified in the assignment. The system processes user queries by routing them to appropriate agents (Web Research or RAG) and summarizing the results using an LLM. Conversational memory is included to improve responses based on past interactions.
LLM Usage

Model: LLaMA3-8b-8192 via Groq API.
Roles:
RAG Agent: Generates answers from documents retrieved from a FAISS vector store.
Summarization Agent: Refines raw results from Web or RAG agents into structured summaries.
Fallback (optional): Direct LLM query answering (not used by router but available for complex reasoning).



Agent Workflow

Router Agent: Analyzes the query for keywords ("latest", "current", "news", "happening", "today"). If present, routes to Web Research; otherwise, routes to RAG. Uses conversation history for context-aware routing.
Web Research Agent: Uses Tavily API to fetch up-to-date web results (up to 3) and extracts titles and content snippets.
RAG Agent: Retrieves relevant documents from a FAISS vector store (built from data/ directory) using HuggingFace embeddings and generates answers with LLaMA3.
Summarization Agent: Summarizes raw results from Web or RAG into a structured response using LLaMA3.

Decision-Making Process

Routing Logic: The Router Agent checks for time-sensitive keywords to decide between web search (for current information) and RAG (for knowledge-based queries). Conversation history is included to maintain context.
Conditional Edges: Implemented in LangGraph to route from router to web or rag, with both paths converging at summarize.

Graph Structure

Nodes:
router: Determines the next agent based on query keywords and history.
web: Executes web search via Tavily API.
rag: Retrieves and answers using FAISS and LLaMA3.
summarize: Synthesizes final response.


Edges:
router → web or rag (conditional based on next state).
web → summarize.
rag → summarize.


Entry Point: router.
Finish Point: summarize.

Conversational Memory

Implemented using LangChain’s ConversationBufferMemory.
Stores input-output pairs after summarization, making history available for subsequent queries.
Enhances context-aware routing and responses.

Test Queries and Results

Query: "What is LangGraph and how is it used?"
Route: RAG
Result: "LangGraph is a library built on LangChain for stateful, multi-agent applications with a graph-like structure, used for decision trees, multi-step agents, and research workflows."


Query: "Current trends in generative AI?"
Route: Web
Result: Summarized web results (e.g., advancements in multimodal models, AI ethics, scalable architectures).


Query: "Explain vector stores in LangChain"
Route: RAG
Result: "Vector stores in LangChain store document embeddings for efficient retrieval, enabling RAG applications."



Limitations

Dataset: The RAG dataset relies on a data/ directory. A larger, more diverse dataset would improve performance.
Tool Calling: The system uses LLaMA3 via Groq, but explicit tool-calling features are not utilized.

Future Improvements

Expand the RAG dataset with comprehensive AI-related documents.
Incorporate explicit tool-calling for structured LLM outputs.
Add persistence for conversational memory (e.g., save to a database).
