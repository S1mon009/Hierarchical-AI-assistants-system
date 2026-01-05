from langchain_openai import ChatOpenAI
from src.core.config import config
from src.modules.chat.tools.web_search_tool import web_search_tool
from src.modules.chat.tools.google_calendar_tool import google_calendar_tools

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
    verbose=True,
)

llm_with_tools = llm.bind_tools([web_search_tool] + google_calendar_tools)

# Create a dict of tools for easy lookup
tools_dict = {tool.name: tool for tool in [web_search_tool] + google_calendar_tools}

def invoke(messages: list[dict]) -> dict:
    if not messages or messages[0]["role"] != "system":
        messages.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant with web search and Google Calendar management capabilities. You can create, search, update, move, and delete calendar events."
        })
        
    while True:
        response = llm_with_tools.invoke(messages)
        messages.append(response)
        
        if not response.tool_calls:
            break
        
        for tool_call in response.tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            
            if tool_name in tools_dict:
                print(f"Invoking {tool_name} with args:", tool_args)
                tool_result = tools_dict[tool_name].invoke(tool_args)
                print(f"Tool result for {tool_name}:", tool_result)
                
                messages.append({
                    "role": "tool",
                    "content": str(tool_result),
                    "tool_call_id": tool_call["id"]
                })
    
    print("Final response:", response)
    return response
