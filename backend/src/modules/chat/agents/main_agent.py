from langchain_openai import ChatOpenAI
from src.core.config import config
from src.modules.chat.tools.web_search_tool import web_search_tool

SYSTEM_PROMPT = """
You are a main AI assistant.
You can delegate tasks to tools if needed.
If you cannot answer, say so explicitly.
"""

llm = ChatOpenAI(
    api_key=config.openrouter_api_key,
    base_url=config.openrouter_url,
    model="mistralai/devstral-2512:free",
    temperature=0.5,
)

llm_with_tools = llm.bind_tools([web_search_tool])

def invoke(messages: list[dict]) -> dict:
    if not messages or messages[0]["role"] != "system":
        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant with web search capabilities."
        })
        
    response = llm_with_tools.invoke(messages)
    
    messages.append(response)
    
    for tool_call in response.tool_calls:
        tool_name = tool_call["name"]
        tool_args = tool_call["args"]
        
        if tool_name == "duckduckgo_results_json":
            print("Invoking web search tool with args:", tool_args)
            tool_result = web_search_tool.invoke(tool_args)
            
            messages.append({
                "role": "tool",
                "content": str(tool_result),
                "tool_call_id": tool_call["id"]
            })
    
    final_response = llm_with_tools.invoke(messages)

    return final_response
