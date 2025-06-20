import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from models import EmployeeInput, ProgressUpdate, TaskStatus
from database import db
from agents import onboarding_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("🚀 Starting Smart Onboarding Assistant...")
    try:
        await db.connect()
        logger.info("✅ All services initialized")
    except Exception as e:
        logger.error(f"❌ Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("👋 Shutting down...")
    await db.disconnect()

# Create FastAPI app
app = FastAPI(
    title="Smart Onboarding Assistant",
    description="AI-powered onboarding system with LangChain, LangGraph, and FAISS",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/ping")
def ping():
    return {"status": "ok"}

@app.get("/")
async def root():
    """Health check"""
    return {
        "message": "Smart Onboarding Assistant",
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        # Test MongoDB
        await db.client.admin.command('ping')
        db_status = "healthy"
    except:
        db_status = "unhealthy"
    
    return {
        "status": "healthy" if db_status == "healthy" else "degraded",
        "services": {
            "database": db_status,
            "vector_db": "healthy" if db.vector_index else "unhealthy",
            "llm": "healthy" if onboarding_agent.llm else "unhealthy"
        },
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/onboard")
async def create_onboarding_plan(employee: EmployeeInput):
    """Create complete onboarding plan"""
    try:
        logger.info(f"Creating onboarding for {employee.name}")
        
        result = await onboarding_agent.create_onboarding_plan(employee)
        
        return {
            "success": True,
            "message": f"Onboarding plan created for {employee.name}",
            "employee": result["employee"],
            "journey": result["journey"],
            "analysis": result["analysis"]
        }
        
    except Exception as e:
        logger.error(f"Onboarding creation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/journey/{employee_id}")
async def get_onboarding_journey(employee_id: str):
    """Get onboarding journey"""
    try:
        journey = await onboarding_agent.get_journey(employee_id)
        return journey
        
    except ValueError:
        raise HTTPException(status_code=404, detail="Journey not found")
    except Exception as e:
        logger.error(f"Get journey failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/progress")
async def update_task_progress(progress: ProgressUpdate):
    """Update task progress"""
    try:
        result = await onboarding_agent.update_progress(
            progress.employee_id,
            progress.task_id,
            progress.status,
            progress.feedback
        )
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Progress update failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/search")
async def search_knowledge_base(query: str, top_k: int = 3):
    """Search knowledge base"""
    try:
        results = db.search_knowledge_base(query, top_k)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        logger.error(f"Knowledge search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/employee/{employee_id}")
async def get_employee(employee_id: str):
    """Get employee profile"""
    try:
        employee = await db.db.employees.find_one({"employee_id": employee_id})
        if not employee:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        employee.pop("_id", None)  # Remove MongoDB ObjectId
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get employee failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Example usage endpoint
@app.post("/api/v1/demo")
async def demo_onboarding():
    """Demo endpoint with sample data"""
    try:
        # Sample employee
        sample_employee = EmployeeInput(
            employee_id="DEMO001",
            name="Alice Johnson",
            email="alice@company.com",
            role="Software Engineer",
            department="Engineering",
            experience_level="Mid",
            skills=["Python", "JavaScript"]
        )
        
        # Create onboarding plan
        result = await onboarding_agent.create_onboarding_plan(sample_employee)
        
        return {
            "message": "Demo onboarding plan created!",
            "employee_id": sample_employee.employee_id,
            "tasks_created": len(result["journey"]["tasks"]),
            "estimated_duration": result["journey"]["estimated_duration"],
            "journey": result["journey"]
        }
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )