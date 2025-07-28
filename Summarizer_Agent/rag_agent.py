from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from config import groq_api_key
import os

def load_documents(data_dir="data"):
    """Load and split documents from a directory."""
    try:
        loader = DirectoryLoader(data_dir, glob="**/*.txt")
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        return splitter.split_documents(docs)
    except Exception as e:
        raise Exception(f"Error loading documents: {str(e)}")

def build_faiss_index():
    """Build and save FAISS vector store."""
    try:
        chunks = load_documents()
        if not chunks:
            raise ValueError("No documents loaded.")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(chunks, embeddings)
        vectorstore.save_local("vectorstore")
        return vectorstore
    except Exception as e:
        raise Exception(f"Error building FAISS index: {str(e)}")

def load_vectorstore():
    """Load existing FAISS vector store or build a new one."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    if os.path.exists("vectorstore/index.faiss"):
        return FAISS.load_local("vectorstore", embeddings, allow_dangerous_deserialization=True)
    return build_faiss_index()

def rag_agent(query: str) -> str:
    """Retrieve and generate answer using RAG."""
    try:
        vectorstore = load_vectorstore()
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        docs = retriever.invoke(query)

        if not docs:
            return "No relevant documents found."

        llm = ChatGroq(model="llama3-8b-8192", groq_api_key=groq_api_key)

        prompt = PromptTemplate.from_template("""
Use the following context to answer the question concisely and accurately:
{context}

Question: {question}

Answer:
""")

        def generate_answer(inputs):
            context = "\n\n".join([doc.page_content for doc in inputs["input_documents"]])
            question = inputs["question"]
            return llm.invoke(prompt.format(context=context, question=question)).content

        chain = RunnableLambda(generate_answer)
        result = chain.invoke({"input_documents": docs, "question": query})
        return result
    except Exception as e:
        return f"Error in RAG agent: {str(e)}"