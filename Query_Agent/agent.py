from langgraph.graph import StateGraph
from langchain_groq import ChatGroq
from langchain.tools import tool
from typing import TypedDict, Any
from math_tools import plus, subtract, multiply, divide
from config import groq_api_key
import re

class GraphState(TypedDict):
    input: str
    next: str
    args: list[Any]  
    result: str      

@tool
def add_tool(x: list[int]) -> str:
    """Add two or more numbers together."""
    return str(plus(*x))

@tool
def subtract_tool(x: list[int]) -> str:
    """Subtract the second number from the first."""
    return str(subtract(*x))

@tool
def multiply_tool(x: list[int]) -> str:
    """Multiply two or more numbers together."""
    return str(multiply(*x))

@tool
def divide_tool(x: list[int]) -> str:
    """Divide the first number by the second."""
    return str(divide(*x))

def add_node(state):
    """Custom add node that works with our state."""
    args = state.get('args', [])
    if args:
        result = str(plus(*args))
        return {"result": f"The result is {result}"}
    return {"result": "No arguments provided for addition"}

def subtract_node(state):
    """Custom subtract node that works with our state."""
    args = state.get('args', [])
    if args and len(args) >= 2:
        result = str(subtract(*args))
        return {"result": f"The result is {result}"}
    return {"result": "Need at least 2 arguments for subtraction"}

def multiply_node(state):
    """Custom multiply node that works with our state."""
    args = state.get('args', [])
    if args:
        result = str(multiply(*args))
        return {"result": f"The result is {result}"}
    return {"result": "No arguments provided for multiplication"}

def divide_node(state):
    """Custom divide node that works with our state."""
    args = state.get('args', [])
    if args and len(args) >= 2:
        if args[1] == 0:
            return {"result": "Error: Cannot divide by zero"}
        result = str(divide(*args))
        return {"result": f"The result is {result}"}
    return {"result": "Need 2 arguments for division"}

def math_tool_router(state):
    prompt = state['input'].lower()
    match = re.findall(r"(\d+)\s*(plus|add|minus|subtract|multiply|times|divided by|divide)\s*(\d+)", prompt)
    
    if not match:
        return {"next": "llm"}  

    a, op, b = match[0]
    a, b = int(a), int(b)

    if "add" in op or "plus" in op:
        return {"next": "add", "args": [a, b]}
    elif "minus" in op or "subtract" in op:
        return {"next": "subtract", "args": [a, b]}
    elif "multiply" in op or "times" in op:
        return {"next": "multiply", "args": [a, b]}
    elif "divide" in op or "divided" in op:
        return {"next": "divide", "args": [a, b]}
    else:
        return {"next": "llm"}

def router(state):
    return math_tool_router(state)

def llm_node(state):
    llm = ChatGroq(
        model="llama3-8b-8192",
        groq_api_key=groq_api_key
    )
    try:
        response = llm.invoke(state['input'])
        return {"result": response.content}
    except Exception as e:
        return {"result": f"Error from LLM: {str(e)}"}

graph = StateGraph(GraphState)

graph.add_node("router", router)
graph.set_entry_point("router")

graph.add_node("llm", llm_node)
graph.add_node("add", add_node)
graph.add_node("subtract", subtract_node)
graph.add_node("multiply", multiply_node)
graph.add_node("divide", divide_node)

def route_condition(state):
    """Extract the 'next' field from state for routing."""
    return state.get("next", "llm")

graph.add_conditional_edges(
    "router",
    route_condition,
    {
        "llm": "llm",
        "add": "add",
        "subtract": "subtract",
        "multiply": "multiply",
        "divide": "divide"
    }
)

graph.set_finish_point("llm")
graph.set_finish_point("add")
graph.set_finish_point("subtract")
graph.set_finish_point("multiply")
graph.set_finish_point("divide")

app = graph.compile()

if __name__ == "__main__":
    print("🔹 Math Example:")
    try:
        result = app.invoke({"input": "What is 12 divided by 4?"})
        print(result)
    except Exception as e:
        print(f"Error: {e}")

    print("\n🔹 General Knowledge Example:")
    try:
        result = app.invoke({"input": "What is artificial intelligence?"})
        print(result)
    except Exception as e:
        print(f"Error: {e}")
        
    print("\n🔹 Additional Math Examples:")
    test_cases = [
        "What is 15 plus 25?",
        "Calculate 100 minus 37",
        "What is 8 times 9?",
        "Divide 144 by 12"
    ]
    
    for test in test_cases:
        try:
            print(f"\nInput: {test}")
            result = app.invoke({"input": test})
            print(f"Output: {result.get('result', 'No result')}")
        except Exception as e:
            print(f"Error: {e}")