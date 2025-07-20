import logging
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from services.langgraph_agent import create_graph
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
graph = create_graph()

class QueryInput(BaseModel):
    question: str

@app.post("/ask")
async def ask(input: QueryInput):
    if "clothing" not in input.question.lower() or "koramangala" not in input.question.lower():
        raise HTTPException(status_code=400, detail="Query must relate to clothing stores in Koramangala, Bangalore.")
    try:
        logger.info(f"Received question: {input.question}")
        try:
            logger.info("Invoking graph...")
            result = graph.invoke({"question": input.question})
            logger.info(f"graph.invoke result: {result}")
        except Exception as invoke_exc:
            logger.error(f"Exception during graph.invoke: {invoke_exc}")
            raise HTTPException(status_code=500, detail=f"Error during graph.invoke: {str(invoke_exc)}")
        output = result.get("report", "")
        logger.info(f"Raw LLM output: {output}")
        # Remove markdown code block markers if present
        output = re.sub(r"```json|```", "", output).strip()
        # Extract JSON object
        match = re.search(r"\{[\s\S]*\}", output)
        logger.info(f"Matched JSON: {match.group() if match else 'No match'}")
        try:
            if match:
                report = json.loads(match.group())
                return {"result": report}
            else:
                logger.error(f"No JSON found in LLM output. Raw output: {output}")
                raise ValueError(f"No JSON found in LLM output. Raw output: {output}")
        except Exception as parse_exc:
            logger.error(f"Error parsing JSON: {parse_exc} | Raw output: {output}")
            raise HTTPException(status_code=500, detail=f"Error parsing JSON: {str(parse_exc)} | Raw output: {output}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating report: {str(e)}")