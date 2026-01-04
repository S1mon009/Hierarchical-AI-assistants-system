from langchain_openai import ChatOpenAI
from src.core.config import config
from src.modules.chat.tools.web_search_tool import web_search_tool

SYSTEM_PROMPT = """
You are a main AI assistant.
You can delegate tasks to tools if needed.
If you cannot answer, say so explicitly.
"""

class MainAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            api_key=config.openrouter_api_key,
            base_url=config.openrouter_url,
            model="mistralai/devstral-2512:free",
            temperature=0.5, 
        )

        self.agent = self.llm.bind_tools([web_search_tool])

    def invoke(self, messages: list[dict]) -> dict:
        """
        messages = [
          {"role": "system", "content": "..."},
          {"role": "user", "content": "..."},
          ...
        ]
        """
        if messages[0]["role"] != "system":
            messages.insert(0, {
                "role": "system",
                "content": SYSTEM_PROMPT
            })

        return self.agent.invoke(messages)
