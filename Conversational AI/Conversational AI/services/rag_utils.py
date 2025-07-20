from langchain.chains import RetrievalQA
# from vector_store_service import load_vector_store
from models.gemini_model import llm
from services.vector_store_service import load_vector_store


def get_rag_chain():
    vectorstore = load_vector_store()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)
    return qa_chain
