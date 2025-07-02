import json
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

import nest_asyncio

nest_asyncio.apply()


server_params = StdioServerParameters(
    command="python",  # The command to run your server
    args=["server.py"],  # Arguments to the command
)

session: Optional[ClientSession] = None
exit_stack = AsyncExitStack()


stdio_transport =  exit_stack.enter_async_context(stdio_client(server_params))
stdio, write = stdio_transport
session =  exit_stack.enter_async_context(ClientSession(stdio, write))

session.initialize()

# List available tools
tools_result =  session.list_tools()
print("\nConnected to server with tools:")
for tool in tools_result.tools:
    print(f"  - {tool.name}: {tool.description}")


exit_stack.aclose()
