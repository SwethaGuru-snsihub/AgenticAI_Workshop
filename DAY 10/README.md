Smart Onboarding Assistant:
An AI-powered employee onboarding system built with LangChain, LangGraph, FAISS, and MongoDB. This system creates personalized onboarding journeys using OpenAI's GPT-4o-mini and provides intelligent progress tracking.
Key Features

AI-Powered Analysis: Uses OpenAI GPT-4o-mini to analyze employee profiles and generate personalized plans
Knowledge Base Integration: Rule-based knowledge search for relevant onboarding content
Progress Tracking: Real-time monitoring of task completion and employee progress
Role-Based Customization: Different onboarding paths for different roles and experience levels
RESTful API: Complete web service with FastAPI framework
Database Integration: MongoDB for persistent data storage

Architecture Overview
System Components
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Frontend       │    │  Node.js        │    │  Python AI      │    │  MongoDB        │
│  (ReactJS+JSX)  │◄──►│  Backend        │◄──►│  Engine         │◄──►│  Database       │
│                 │    │  (Express)      │    │  (FastAPI)      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
The Node.js backend serves as the bridge between the frontend and Python-based Agentic AI system. User inputs flow from React to Node.js, which relays them to the Python endpoint. The response is routed back in reverse.
Detailed Agentic Workflow
The system includes the following specialized agents:

Profile Analysis Agent – Parses and enriches employee data
Journey Generator Agent (RAG-Enabled) – Fetches context from vector DB and generates onboarding roadmap
Progress Tracker Agent – Tracks task completion using time-series data
Sentiment Analysis Agent – Analyzes user sentiment using NLP and behavioral signals
Journey Adapter Agent – Dynamically adjusts onboarding based on performance or feedback
Notification Agent – Sends alerts, reminders, and celebrations via multichannel delivery

Python Backend Architecture
Application ──► FastAPI (web server) ──► OpenAI (gpt-4o-mini)
     │
     ▼
MongoDB (Database) / Knowledge Base

Component Overview
FastAPI Web Server

Handles HTTP requests and responses
Implements REST API endpoints
Manages request validation and error handling
Provides interactive API documentation

AI Agent System

Profile analysis and skill gap identification
Journey generation with personalized tasks
Progress tracking and completion monitoring
Fallback mechanisms for offline operation

MongoDB Database

Employee profile storage
Onboarding journey persistence
Progress tracking and analytics
Scalable document-based storage

Knowledge Base

Company policies and procedures
Role-specific onboarding guides
Best practices and templates
Rule-based content retrieval

Technology Stack
Frontend

React + JSX
Redux Toolkit, RTK Query

Backend (Node)

Express.js
Axios, dotenv

Python AI Engine

FastAPI, Python 3.8+
LangChain, LangGraph, FAISS
OpenAI GPT-4o-mini
Sentence Transformers (all-MiniLM-L6-v2)
Pydantic, python-dotenv

Databases

MongoDB Atlas (profiles, journeys)
FAISS Vector DB (knowledge embeddings)

Technology Stack Details
ComponentTechnologyVersionPurposeWeb FrameworkFastAPI0.104.1REST API serverRuntimePython3.8+Application runtimeDatabaseMongoDB4.4+Document storageDatabase DriverMotor3.3.2Async MongoDB driverAI/MLOpenAI API1.6.1Text generationData ValidationPydantic2.5.0Request/response modelsConfigurationpython-dotenv1.0.0Environment management
Prerequisites

Python 3.8 or higher
Node.js 16+
OpenAI API key
MongoDB Atlas account (or local MongoDB)
Git

Quick Start
1. Clone the Repository
bashgit clone <repository-url>
cd smart-onboarding-assistant
2. Backend Setup (Node.js)
bashcd backend
npm install
Create a .env file in backend/ with the following variables:
bashMONGODB_URL=your_mongodb_connection_string
MONGODB_DB_NAME=onboarding_assistant
PYTHON_API_URL=http://localhost:8000
PORT=3000
Start the Backend Server:
bashnpm start
The backend runs on http://localhost:3000.
3. Python AI Engine Setup
bashcd python
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
Configure Environment Variables:
bash# Copy the example environment file
cp .env.example .env
# Edit .env file and add your credentials
nano .env
Required environment variables:
bashGEMINI_API_KEY=your_openai_api_key
MONGODB_URL=your_mongodb_connection_string
MONGODB_DB_NAME=onboarding_assistant
LLM_MODEL=gpt-4o-mini
EMBEDDING_MODEL=all-MiniLM-L6-v2
DEBUG=true
Start the Python AI Engine:
bashpython main.py
The Python backend runs on http://localhost:8000.
4. Frontend Setup
bashcd frontend
npm install
Start the Frontend:
bashnpm run dev
The frontend runs on http://localhost:5173.
5. Test the System
Test with Postman

Import the Postman collection from docs/postman/
Set environment variables in Postman:

base_url: http://localhost:8000
node_base_url: http://localhost:3000


Run the test sequence

Configuration
Environment Variables
VariableDescriptionDefaultGEMINI_API_KEYOpenAI API keyRequiredMONGODB_URLMongoDB connection stringRequiredMONGODB_DB_NAMEDatabase nameonboarding_assistantLLM_MODELOpenAI modelgpt-4o-miniEMBEDDING_MODELEmbedding modelall-MiniLM-L6-v2DEBUGDebug modetrue
Model Configuration
The system uses lightweight, cost-effective models:

LLM: GPT-4o-mini (fast, affordable)
Embeddings: all-MiniLM-L6-v2 (384 dimensions, efficient)

Security

Environment variables for sensitive data
Input validation with Pydantic
MongoDB connection encryption
API rate limiting (recommended for production)

Monitoring

Health check endpoint: /health
Structured logging throughout the application
Progress tracking in database
Error handling and recovery

Troubleshooting
Common Issues

OpenAI API Errors

Check API key validity
Verify sufficient credits
Check rate limits


MongoDB Connection Issues

Verify connection string
Check network access
Ensure database exists


Import Errors

Reinstall requirements: pip install -r requirements.txt
Check Python version compatibility


Vector Database Issues

Clear FAISS index and restart
Check embedding model download


Resources
Architecture Diagram
View Architecture
Demo Video
Watch Demo
Acknowledgments

LangChain for AI orchestration
FastAPI for the web framework
FAISS for vector similarity search
MongoDB for document storage
OpenAI for language models
