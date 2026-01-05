from langchain_community.tools import DuckDuckGoSearchResults

web_search_tool = DuckDuckGoSearchResults(
    output_format="list",
    max_results=5
)
