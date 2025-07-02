from typing import Optional
from contextlib import AsyncExitStack

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters

import nest_asyncio
import asyncio

nest_asyncio.apply()


async def main():
    server_params = StdioServerParameters(
        command="python",  # The command to run your server
        args=["server.py"],  # Arguments to the command
    )

    session: Optional[ClientSession] = None
    async with AsyncExitStack() as exit_stack:
        stdio_transport = await exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        session = await exit_stack.enter_async_context(ClientSession(stdio, write))

        session.initialize()

        # List available tools
        tools_result = session.list_tools()
        print("\nConnected to server with tools:")
        for tool in tools_result.tools:
            print(f"  - {tool.name}: {tool.description}")


# Run the async main function
asyncio.run(main())
