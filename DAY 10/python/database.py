import os
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any
import json

logger = logging.getLogger(__name__)

class DatabaseService:
    def __init__(self):
        self.client = None
        self.db = None
        self.embedding_model = None
        self.vector_index = None
        self.documents = []
        
    async def connect(self):
        """Connect to MongoDB and initialize FAISS"""
        try:
            # MongoDB connection
            mongodb_url = os.getenv("MONGODB_URL")
            db_name = os.getenv("MONGODB_DB_NAME")
            
            self.client = AsyncIOMotorClient(mongodb_url)
            self.db = self.client[db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info("✅ Connected to MongoDB")
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Embedding model loaded")
            
            # Initialize knowledge base
            await self._initialize_vector_db()
            
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    async def _initialize_vector_db(self):
        """Initialize FAISS vector database with knowledge base"""
        try:
            # Load knowledge base documents
            knowledge_docs = [
                {
                    "id": "policy_1",
                    "content": "Company remote work policy: All employees can work remotely 3 days per week. Core hours are 10 AM to 4 PM in your local timezone.",
                    "type": "policy"
                },
                {
                    "id": "guide_1", 
                    "content": "Software Engineer onboarding: Set up development environment, complete Git training, join team meetings, complete first code review.",
                    "type": "onboarding_guide"
                },
                {
                    "id": "guide_2",
                    "content": "New employee checklist: Complete HR paperwork, set up email and Slack, meet your manager, complete security training.",
                    "type": "onboarding_guide"
                },
                {
                    "id": "guide_3",
                    "content": "Data Scientist onboarding: Set up Python environment, access data platforms, complete data privacy training, meet data team.",
                    "type": "onboarding_guide"
                }
            ]
            
            # Create embeddings
            texts = [doc["content"] for doc in knowledge_docs]
            embeddings = self.embedding_model.encode(texts)
            
            # Initialize FAISS index
            dimension = embeddings.shape[1]
            self.vector_index = faiss.IndexFlatIP(dimension)  # Inner Product for similarity
            
            # Normalize embeddings for cosine similarity
            faiss.normalize_L2(embeddings)
            self.vector_index.add(embeddings.astype('float32'))
            
            self.documents = knowledge_docs
            logger.info(f"✅ Vector database initialized with {len(knowledge_docs)} documents")
            
        except Exception as e:
            logger.error(f"❌ Vector DB initialization failed: {e}")
            raise
    
    def search_knowledge_base(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search knowledge base using vector similarity"""
        try:
            # Encode query
            query_embedding = self.embedding_model.encode([query])
            faiss.normalize_L2(query_embedding)
            
            # Search
            scores, indices = self.vector_index.search(query_embedding.astype('float32'), top_k)
            
            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
                if idx != -1:  # Valid result
                    doc = self.documents[idx].copy()
                    doc["similarity_score"] = float(score)
                    results.append(doc)
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Knowledge base search failed: {e}")
            return []
    
    async def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("✅ Disconnected from MongoDB")

# Global instance
db = DatabaseService()