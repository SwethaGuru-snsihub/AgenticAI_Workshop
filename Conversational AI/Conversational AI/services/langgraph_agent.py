from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langgraph.graph import Graph
from dotenv import load_dotenv
import os
from services.stores import fetch_and_store

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize embeddings and LLM
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GOOGLE_API_KEY)

# Load FAISS vector store
vector_store_path = "faiss_index"
vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True) if os.path.exists(vector_store_path) else None

# Prompt template for generating structured report
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""Based on the following context, generate a JSON report about clothing store competitors in Koramangala, Bangalore, including store name, address, footfall trends, peak hours, and source URL. If data is missing, note it as 'Unknown'. Provide recommendations for business owners, marketing teams, real estate analysts, and investors.

Context: {context}

Question: {question}

Respond ONLY with valid JSON. Do not include any explanation, markdown, or extra text.

Output format:
{
  "competitors": [
    {
      "store_name": "string",
      "address": "string",
      "footfall_trends": "string",
      "peak_hours": "string",
      "source_url": "string"
    }
  ],
  "recommendations": {
    "business_owners": "string",
    "marketing_teams": "string",
    "real_estate_analysts": "string",
    "investors": "string"
  }
}
"""
)

def retrieve_context(question: str, k: int = 3):
    """Retrieve relevant documents from FAISS."""
    if not vector_store:
        return ""
    question_embedding = embeddings.embed_query(question)
    docs = vector_store.similarity_search_by_vector(question_embedding, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context

def generate_answer(state: dict):
    """Generate structured report using LLM and retrieved context."""
    question = state["question"]
    context = retrieve_context(question)
    if not context:  # Fallback to live search
        documents = fetch_and_store(question, api="tavily")
        context = "\n\n".join([f"Store: {doc['store_name']}\nAddress: {doc['address']}\nContent: {doc['content']}" for doc in documents])
    prompt = prompt_template.format(context=context, question=question)
    answer = llm.invoke(prompt).content
    return {"report": answer}

def create_graph():
    """Create LangGraph workflow."""
    graph = Graph()
    graph.add_node("generate_answer", generate_answer)
    graph.set_entry_point("generate_answer")
    graph.set_finish_point("generate_answer")
    return graph.compile()

if __name__ == "__main__":
    graph = create_graph()
    result = graph.invoke({"question": "Clothing store competitors in Koramangala, Bangalore"})
    print(result["report"])