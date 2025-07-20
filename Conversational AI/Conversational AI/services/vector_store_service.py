import os
import json
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document

def load_vector_store():
    # Load JSON data from OSM fetch
    with open("datas/koramangala_stores.json", "r", encoding="utf-8") as f:
    # with open("datas/stores_data.json", "r", encoding="utf-8") as f:
        stores = json.load(f)

    documents = []
    for store in stores:
        name = store.get("name", "Unknown")
        category = store.get("category") or store.get("type", "Unknown")
        lat = store.get("lat", "N/A")
        lon = store.get("lon", "N/A")
        location = store.get("location", "N/A")
        footfall = store.get("footfall", None)
        peak_hours = store.get("peak_hours", None)
        # Prefer lat/lon if present, else use location
        if lat != "N/A" and lon != "N/A":
            loc_str = f"located at latitude {lat} and longitude {lon}"
        else:
            loc_str = f"located at {location}"
        # Add footfall and peak_hours if available
        extra = ""
        if footfall:
            extra += f" Footfall is {footfall}."
        if peak_hours:
            extra += f" Peak hours are {peak_hours}."
        content = f"{name} is a {category} store {loc_str}.{extra}"
        documents.append(Document(page_content=content, metadata={"source": "osm", **store}))

    # Split if needed
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs = splitter.split_documents(documents)

    # Embeddings using Gemini
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Load into FAISS
    vector_store = FAISS.from_documents(docs, embeddings)

    return vector_store
