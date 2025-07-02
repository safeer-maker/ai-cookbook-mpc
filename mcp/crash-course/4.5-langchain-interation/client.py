
import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

import nest_asyncio

nest_asyncio.apply()

async def get_tool_names():

    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
)

    session: Optional[ClientSession] = None 

    async with AsyncExitStack() as exit_stack:

        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await exit_stack.enter_async_context(ClientSession(stdio, write))

        await session.initialize()

        print ("Session initialized." )
        # List available tools
        tools_result = await session.list_tools()
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")

        tool_call = await session.call_tool (
            "get_state_and_qrid",
            arguments={
                "longitude": "-122.3321",
                "latitude": "47.6062"
            }
        )

        print("\nTool call result:")
        print(tool_call)

    return tool_call.content[0].text


if __name__ == "__main__":
    results = asyncio.run(get_tool_names())
    print (results)
