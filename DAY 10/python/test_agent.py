from dotenv import load_dotenv
import os

# Always load the .env from the current file's directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

from agents import onboarding_agent
from models import EmployeeInput
from database import db  

import asyncio

async def test_agent():
    await db.connect()  # <-- Initialize DB and embedding model

    employee = EmployeeInput(
        employee_id="EMPTEST",
        name="Agent Test",
        email="agent@test.com",
        role="QA Engineer",
        department="QA",
        experience_level="Mid",
        skills=["Testing", "Automation"]
    )
    result = await onboarding_agent.create_onboarding_plan(employee)
    print(result)

    await db.disconnect()  # <-- Clean up

asyncio.run(test_agent())