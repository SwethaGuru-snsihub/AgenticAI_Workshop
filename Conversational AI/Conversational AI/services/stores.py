import os
import sys
import requests
from dotenv import load_dotenv
import json
import re

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

try:
    import serpapi
except ImportError:
    serpapi = None

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize clients
tavily_client = TavilyClient(api_key=TAVILY_API_KEY) if TAVILY_API_KEY and TavilyClient else None
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)

# Text splitter for chunking content
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def fetch_tavily_data(query: str, max_results: int = 5):
    """Fetch search results from Tavily API."""
    if not tavily_client:
        print("Tavily API key or package not provided. Skipping Tavily.")
        return []
    try:
        response = tavily_client.search(query, max_results=max_results, search_depth="advanced")
        documents = [
            {
                "store_name": result.get("title", "Unknown Store"),
                "address": result.get("url", "").split("/")[-1] or "Unknown Address",
                "content": result.get("content", ""),
                "url": result.get("url", ""),
                "footfall_trends": "Unknown",  # Tavily may not provide this directly
                "peak_hours": "Unknown"
            }
            for result in response.get("results", [])
        ]
        return documents
    except Exception as e:
        print(f"Tavily API error: {e}")
        return []

def fetch_serpapi_data(query: str, max_results: int = 5):
    """Fetch search results from SerpApi using HTTP requests."""
    if not SERPAPI_API_KEY:
        print("SerpApi key not provided. Skipping SerpApi.")
        return []
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": max_results,
            "engine": "google",
            "location": "Koramangala, Bangalore, Karnataka, India"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()
        documents = [
            {
                "store_name": result.get("title", "Unknown Store"),
                "address": result.get("address", "Unknown Address"),
                "content": result.get("snippet", ""),
                "url": result.get("link", ""),
                "footfall_trends": "Unknown",
                "peak_hours": "Unknown"
            }
            for result in results.get("organic_results", [])
        ]
        return documents
    except Exception as e:
        print(f"SerpApi error: {e}")
        return []

def index_data(documents: list, vector_store_path: str = "faiss_index"):
    """Index documents into a FAISS vector store."""
    if not documents:
        print("No documents to index.")
        return None
    # Create text for embedding
    texts = []
    for doc in documents:
        text = f"Store: {doc['store_name']}\nAddress: {doc['address']}\nContent: {doc['content']}\nURL: {doc['url']}"
        chunks = text_splitter.split_text(text)
        texts.extend(chunks)
    # Create or load FAISS vector store
    if os.path.exists(vector_store_path):
        vector_store = FAISS.load_local(vector_store_path, embeddings, allow_dangerous_deserialization=True)
        vector_store.add_texts(texts)
    else:
        vector_store = FAISS.from_texts(texts, embeddings)
    # Save vector store
    vector_store.save_local(vector_store_path)
    return vector_store

def fetch_and_store(query: str, api: str = "tavily"):
    """Fetch data from specified API and store in FAISS."""
    if api == "tavily":
        documents = fetch_tavily_data(query)
    elif api == "serpapi":
        documents = fetch_serpapi_data(query)
    else:
        raise ValueError("Unsupported API. Use 'tavily' or 'serpapi'.")
    if documents:
        vector_store = index_data(documents)
        print(f"Indexed {len(documents)} documents for query: {query}")
    else:
        print(f"No results found for query: {query}")
    return documents

if __name__ == "__main__":
    # Default query for clothing store competitors
    default_query = "clothing store competitors footfall trends peak hours Koramangala Bangalore"
    query = sys.argv[1] if len(sys.argv) > 1 else default_query
    fetch_and_store(query, api="serpapi")  # Prefer SerpApi for location-specific data