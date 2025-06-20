from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from enum import Enum

class ExperienceLevel(str, Enum):
    JUNIOR = "Junior"
    MID = "Mid"
    SENIOR = "Senior"

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

# Input Models
class EmployeeInput(BaseModel):
    employee_id: str
    name: str
    email: str
    role: str
    department: str
    experience_level: ExperienceLevel
    skills: List[str] = []
    start_date: datetime = Field(default_factory=datetime.now)

# Core Models
class Employee(BaseModel):
    employee_id: str
    name: str
    email: str
    role: str
    department: str
    experience_level: ExperienceLevel
    skills: List[str]
    start_date: datetime
    skill_gaps: List[str] = []
    learning_path: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class OnboardingTask(BaseModel):
    task_id: str
    title: str
    description: str
    priority: TaskPriority
    estimated_duration: int  # minutes
    status: TaskStatus = TaskStatus.PENDING
    deadline: datetime
    resources: List[str] = []

class OnboardingJourney(BaseModel):
    journey_id: str
    employee_id: str
    tasks: List[OnboardingTask]
    estimated_duration: int  # days
    progress_percentage: float = 0.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class ProgressUpdate(BaseModel):
    employee_id: str
    task_id: str
    status: TaskStatus
    feedback: Optional[str] = None