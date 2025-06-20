import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from pydantic import BaseModel

from models import Employee, OnboardingJourney, OnboardingTask, TaskPriority, TaskStatus, EmployeeInput
from database import db

logger = logging.getLogger(__name__)

class OnboardingState(BaseModel):
    employee_data: Dict[str, Any] = {}
    analysis_result: Dict[str, Any] = {}
    journey_plan: Dict[str, Any] = {}
    knowledge_context: List[Dict[str, Any]] = []
    final_result: Dict[str, Any] = {}

class SmartOnboardingAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="learnlm-2.o-flash-experimental",
            temperature=0.3,
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        self.workflow = None
        self._build_workflow()
    
    def _build_workflow(self):
        """Build LangGraph workflow for onboarding"""
        
        # Define workflow steps
        def analyze_employee(state: OnboardingState) -> Dict[str, Any]:
            """Step 1: Analyze employee profile"""
            logger.info("🔍 Analyzing employee profile...")
            
            employee_data = state.employee_data
            
            # Get relevant knowledge
            query = f"onboarding for {employee_data.get('role', '')} {employee_data.get('experience_level', '')}"
            knowledge_results = db.search_knowledge_base(query, top_k=3)
            
            # Analyze with LLM
            system_prompt = """You are an HR onboarding specialist. Analyze the employee profile and identify:
1. Key skill gaps for their role
2. Learning priorities  
3. Onboarding complexity level
4. Estimated duration

Respond in JSON format with these fields: skill_gaps, learning_priorities, complexity_level, estimated_days."""

            context = "\n".join([doc["content"] for doc in knowledge_results])
            human_prompt = f"""
Employee Profile:
- Role: {employee_data.get('role')}
- Experience: {employee_data.get('experience_level')}
- Skills: {employee_data.get('skills', [])}
- Department: {employee_data.get('department')}

Relevant Knowledge:
{context}

Provide analysis in JSON format."""

            try:
                response = self.llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt)
                ])
                logger.info(f"LLM raw response (analyze_employee): {response.content}")
                
                analysis = json.loads(response.content)
                logger.info("✅ Employee analysis completed")
                
                return {
                    "analysis_result": analysis,
                    "knowledge_context": knowledge_results
                }
                
            except Exception as e:
                logger.error(f"❌ Analysis failed: {e}")
                # Fallback analysis
                return {
                    "analysis_result": {
                        "skill_gaps": ["Git", "Company Tools"],
                        "learning_priorities": ["Team Integration", "Technical Setup"],
                        "complexity_level": "medium",
                        "estimated_days": 14
                    },
                    "knowledge_context": knowledge_results
                }
        
        def generate_journey(state: OnboardingState) -> Dict[str, Any]:
            """Step 2: Generate personalized onboarding journey"""
            logger.info("🗺️ Generating onboarding journey...")
            
            employee_data = state.employee_data
            analysis = state.analysis_result
            
            system_prompt = """You are an onboarding journey designer. Create a personalized onboarding plan with specific tasks.

Generate 5-8 tasks with:
- Clear titles and descriptions
- Priority levels (high/medium/low)
- Estimated duration in minutes
- Realistic deadlines

Respond in JSON format: {"tasks": [{"title": "", "description": "", "priority": "", "duration_minutes": 0, "deadline_days": 0}]}"""

            human_prompt = f"""
Create an onboarding journey for:
- Role: {employee_data.get('role')}
- Experience: {employee_data.get('experience_level')}
- Skill gaps: {analysis.get('skill_gaps', [])}
- Learning priorities: {analysis.get('learning_priorities', [])}
- Estimated duration: {analysis.get('estimated_days', 14)} days

Focus on practical, actionable tasks."""

            try:
                response = self.llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=human_prompt)
                ])
                
                journey_data = json.loads(response.content)
                logger.info("✅ Journey generation completed")
                
                return {"journey_plan": journey_data}
                
            except Exception as e:
                logger.error(f"❌ Journey generation failed: {e}")
                # Fallback journey
                return {
                    "journey_plan": {
                        "tasks": [
                            {
                                "title": "Complete HR Setup",
                                "description": "Fill out all required HR paperwork and setup accounts",
                                "priority": "high",
                                "duration_minutes": 120,
                                "deadline_days": 1
                            },
                            {
                                "title": "Meet Your Team",
                                "description": "Schedule intro meetings with team members",
                                "priority": "high",
                                "duration_minutes": 90,
                                "deadline_days": 2
                            },
                            {
                                "title": "Development Environment Setup",
                                "description": "Set up your development tools and environment",
                                "priority": "medium",
                                "duration_minutes": 180,
                                "deadline_days": 3
                            }
                        ]
                    }
                }
        
        def finalize_onboarding(state: OnboardingState) -> Dict[str, Any]:
            """Step 3: Finalize and structure the onboarding plan"""
            logger.info("✅ Finalizing onboarding plan...")
            
            employee_data = state.employee_data
            analysis = state.analysis_result
            journey_plan = state.journey_plan
            
            # Create structured tasks
            tasks = []
            for i, task_data in enumerate(journey_plan.get("tasks", [])):
                deadline = datetime.now() + timedelta(days=task_data.get("deadline_days", i+1))
                
                task = OnboardingTask(
                    task_id=f"{employee_data['employee_id']}_task_{i}",
                    title=task_data.get("title", f"Task {i+1}"),
                    description=task_data.get("description", "Complete this onboarding task"),
                    priority=TaskPriority(task_data.get("priority", "medium")),
                    estimated_duration=task_data.get("duration_minutes", 60),
                    deadline=deadline,
                    resources=["HR Portal", "Team Directory"]
                )
                tasks.append(task)
            
            # Create employee profile
            employee = Employee(
                employee_id=employee_data["employee_id"],
                name=employee_data["name"],
                email=employee_data["email"],
                role=employee_data["role"],
                department=employee_data["department"],
                experience_level=employee_data["experience_level"],
                skills=employee_data.get("skills", []),
                start_date=employee_data.get("start_date", datetime.now()),
                skill_gaps=analysis.get("skill_gaps", []),
                learning_path=analysis.get("learning_priorities", [])
            )
            
            # Create onboarding journey
            journey = OnboardingJourney(
                journey_id=f"journey_{employee_data['employee_id']}",
                employee_id=employee_data["employee_id"],
                tasks=tasks,
                estimated_duration=analysis.get("estimated_days", 14)
            )
            
            return {
                "final_result": {
                    "employee": employee.model_dump(),
                    "journey": journey.model_dump(),
                    "analysis": analysis
                }
            }
        
        # Build the workflow graph
        workflow = StateGraph(OnboardingState)
        
        # Add nodes
        workflow.add_node("analyze_employee", analyze_employee)
        workflow.add_node("generate_journey", generate_journey)
        workflow.add_node("finalize_onboarding", finalize_onboarding)
        
        # Add edges
        workflow.add_edge("analyze_employee", "generate_journey")
        workflow.add_edge("generate_journey", "finalize_onboarding")
        workflow.add_edge("finalize_onboarding", END)
        
        # Set entry point
        workflow.set_entry_point("analyze_employee")
        
        # Compile the workflow
        self.workflow = workflow.compile()
        logger.info("✅ LangGraph workflow built successfully")
    
    async def create_onboarding_plan(self, employee_input: EmployeeInput) -> Dict[str, Any]:
        """Create complete onboarding plan using LangGraph workflow"""
        try:
            logger.info(f"🚀 Creating onboarding plan for {employee_input.name}")
            
            # Prepare initial state
            initial_state = OnboardingState(
                employee_data=employee_input.model_dump()
            )
            
            # Run the workflow
            final_state = await self.workflow.ainvoke(initial_state.model_dump())
            
            result = final_state["final_result"]
            
            # Save to database
            await self._save_to_database(result)
            
            logger.info("✅ Onboarding plan created successfully")
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to create onboarding plan: {e}")
            raise
    
    async def update_progress(self, employee_id: str, task_id: str, status: TaskStatus, feedback: str = None) -> Dict[str, Any]:
        """Update task progress"""
        try:
            # Get current journey
            journey_data = await db.db.journeys.find_one({"employee_id": employee_id})
            if not journey_data:
                raise ValueError("Journey not found")
            
            # Update task status
            for task in journey_data["tasks"]:
                if task["task_id"] == task_id:
                    task["status"] = status.value
                    break
            
            # Calculate progress
            total_tasks = len(journey_data["tasks"])
            completed_tasks = len([t for t in journey_data["tasks"] if t["status"] == "completed"])
            progress = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
            
            journey_data["progress_percentage"] = progress
            
            # Save updated journey
            await db.db.journeys.update_one(
                {"employee_id": employee_id},
                {"$set": journey_data}
            )
            
            # Save progress event
            progress_event = {
                "employee_id": employee_id,
                "task_id": task_id,
                "status": status.value,
                "feedback": feedback,
                "timestamp": datetime.utcnow()
            }
            await db.db.progress.insert_one(progress_event)
            
            logger.info(f"✅ Progress updated: {task_id} -> {status.value}")
            
            return {
                "success": True,
                "progress_percentage": progress,
                "completed_tasks": completed_tasks,
                "total_tasks": total_tasks
            }
            
        except Exception as e:
            logger.error(f"❌ Progress update failed: {e}")
            raise
    
    async def get_journey(self, employee_id: str) -> Dict[str, Any]:
        """Get onboarding journey for employee"""
        try:
            journey = await db.db.journeys.find_one({"employee_id": employee_id})
            if not journey:
                raise ValueError("Journey not found")
            
            # Remove MongoDB ObjectId for JSON serialization
            journey.pop("_id", None)
            return journey
            
        except Exception as e:
            logger.error(f"❌ Failed to get journey: {e}")
            raise
    
    async def _save_to_database(self, result: Dict[str, Any]):
        """Save employee and journey to database"""
        try:
            employee_data = result["employee"]
            journey_data = result["journey"]
            
            # Save employee
            await db.db.employees.update_one(
                {"employee_id": employee_data["employee_id"]},
                {"$set": employee_data},
                upsert=True
            )
            
            # Save journey
            await db.db.journeys.update_one(
                {"employee_id": journey_data["employee_id"]},
                {"$set": journey_data},
                upsert=True
            )
            
            logger.info("✅ Data saved to database")
            
        except Exception as e:
            logger.error(f"❌ Database save failed: {e}")
            raise

# Global agent instance
onboarding_agent = SmartOnboardingAgent()