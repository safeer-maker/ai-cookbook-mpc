from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("../.env")

# Create an MCP server
mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",  # only used for SSE transport (localhost)
    port=8050,  # only used for SSE transport (set this to any port)
) 


# Add a simple calculator tool
@mcp.tool()
def add(a, b) -> int:
    """Add two numbers together.
    
    Args:
        a: The first number
        b: The second number
    """

    summ = int(a) + int(b)
    print(f"Adding {a} and {b} to get {summ}")

    return summ


# Run the server
if __name__ == "__main__":
    transport = "sse"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")
