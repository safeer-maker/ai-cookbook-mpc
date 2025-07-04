from langchain_mcp_adapters.client import MultiServerMCPClient
import nest_asyncio
import json

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv("../../../.env")  # Load environment variables from .env file

os.getenv("AIRTABLE_API_KEY","")

nest_asyncio.apply()  # Needed to run interactive python

client = MultiServerMCPClient(
    {
        # "weather": {
        #     "command": "python",
        #     "args": ["/home/safeer/Documents/devops/mcp/mcp/crash-course/4.5-langchain-interation/server.py"],
        #     "transport": "stdio",
        # },
        "weather": {
            "url": "http://localhost:4567/sse",
            "transport": "sse",
        },

    }
)

tools = await client.get_tools()
tools

llm = ChatOpenAI(
    model="gpt-4o-mini",
)

llm_with_tools = llm.bind_tools(tools)

call =  llm_with_tools.invoke ("Hi there! Can you tell me the grid for Seattle?")

for tool_call in call.additional_kwargs.get("tool_calls", []):
    print(f"Tool call: {tool_call}")

await tools[0].invoke( input= json.dumps({"latitude": "47.6062", "longitude": "-122.3321"}))