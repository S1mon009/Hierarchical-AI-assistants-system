from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchResults

@tool
def web_search_tool(question: str) -> str:
    """Search the web for information related to the question."""
    search_tool = DuckDuckGoSearchResults(
        output_format="list",
        max_results=5
    )
    return search_tool.invoke(question)
