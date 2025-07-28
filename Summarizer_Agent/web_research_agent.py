from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_research_agent(query: str) -> str:
    try:
        response = client.search(query=query, max_results=3)
        results = response.get("results", [])
        if not results:
            return "No relevant web data found."

        summary = "\n".join([f"- {r['title']}: {r['content'][:200]}..." for r in results])
        return f"🔍 Web Results for: '{query}'\n\n{summary}"
    except Exception as e:
        return f"Error in web research: {str(e)}"
