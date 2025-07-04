from langchain_mcp_adapters.client import MultiServerMCPClient
import nest_asyncio

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

