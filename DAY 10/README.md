# Smart Onboarding Assistant - Python backend
An AI-powered employee onboarding system built with **LangChain**, **LangGraph**, **FAISS**, and **MongoDB**. This system creates personalized onboarding journeys using OpenAI's GPT-4o-mini and provides intelligent progress tracking.
## Technology Stack
- **Backend**: FastAPI, Python 3.8+
- **Database**: MongoDB Atlas
- **Vector Store**: FAISS
- **AI/ML**: LangChain, LangGraph, OpenAI GPT-4o-mini
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Data Models**: Pydantic
## Prerequisites
- Python 3.8 or higher
- OpenAI API key
- MongoDB Atlas account (or local MongoDB)
- Git
## Quick Start - Python
### 1. Clone the Repository
```bash
git clone <repository-url>
cd python
```
### 2. Set Up Environment
```bash
# Create virtual environment
python -m venv venv
# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```
### 3. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env
# Edit .env file and add your credentials
nano .env
```
Required environment variables:
- `GEMINI_API_KEY`: Your OpenAI API key
- `MONGODB_URL`: Your MongoDB connection string
- `MONGODB_DB_NAME`: Database name
### 4. Test the System
```bash
# Start the application
python main.py

Setup Instructions
1. Clone the Repository
git clone <your-repo-url>
cd <repo-folder>
2. Backend Setup
cd backend
npm install
Create a .env file in backend/ with the values above.
Start the Backend Server
npm start
The backend runs on http://localhost:3000.

3. Frontend Setup
cd ../frontend
npm install
Start the Frontend
npm run dev
The frontend runs on http://localhost:5173.
```
### Test with Postman
1. Import the Postman collection from `docs/postman/`
2. Set environment variables in Postman:
   - `base_url`: http://localhost:8000
3. Run the test sequence
```
## Configuration
### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | OpenAI API key | Required |
| `MONGODB_URL` | MongoDB connection string | Required |
| `MONGODB_DB_NAME` | Database name | `onboarding_assistant` |
| `LLM_MODEL` | OpenAI model | `gpt-4o-mini` |
| `EMBEDDING_MODEL` | Embedding model | `all-MiniLM-L6-v2` |
| `DEBUG` | Debug mode | `true` |

### Model Configuration
The system uses lightweight, cost-effective models:
- **LLM**: GPT-4o-mini (fast, affordable)
- **Embeddings**: all-MiniLM-L6-v2 (384 dimensions, efficient)
## Security
- Environment variables for sensitive data
- Input validation with Pydantic
- MongoDB connection encryption
- API rate limiting (recommended for production)
## Monitoring
- Health check endpoint: `/health`
- Structured logging throughout the application
- Progress tracking in database
- Error handling and recovery
### Common Issues
1. **OpenAI API Errors**
   - Check API key validity
   - Verify sufficient credits
   - Check rate limits
2. **MongoDB Connection Issues**
   - Verify connection string
   - Check network access
   - Ensure database exists
3. **Import Errors**
   - Reinstall requirements: `pip install -r requirements.txt`
   - Check Python version compatibility
4. **Vector Database Issues**
   - Clear FAISS index and restart
   - Check embedding model download
## Acknowledgments
- [LangChain](https://langchain.com/) for AI orchestration
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [FAISS](https://faiss.ai/) for vector similarity search
- [MongoDB](https://mongodb.com/) for document storage
- [OpenAI](https://openai.com/) for language models
---

## System Components
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Frontend       │    │  Node.js        │    │  Python AI      │    │  MongoDB        │
│  (ReactJS+JSX)  │◄──►│  Backend        │◄──►│  Engine         │◄──►│  Database       │
│                 │    │  (Express)      │    │  (FastAPI)      │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘

The Node.js backend serves as the bridge between the frontend and Python-based Agentic AI system. User inputs flow from React to Node.js, which relays them to the Python endpoint. The response is routed back in reverse.

## Detailed Agentic Workflow
The system includes the following specialized agents:

Profile Analysis Agent – Parses and enriches employee data
Journey Generator Agent (RAG-Enabled) – Fetches context from vector DB and generates onboarding roadmap
Progress Tracker Agent – Tracks task completion using time-series data
Sentiment Analysis Agent – Analyzes user sentiment using NLP and behavioral signals
Journey Adapter Agent – Dynamically adjusts onboarding based on performance or feedback
Notification Agent – Sends alerts, reminders, and celebrations via multichannel delivery


## Link to access Architecture
https://drive.google.com/file/d/1OHwHMQiDIi00jwvFYrsvO4P-rmUe597H/view?usp=sharing

## Demo video link
https://drive.google.com/file/d/1PDY9xBh4jAdAXRzZgLbOF8nG9lav8iBr/view?usp=drive_link
