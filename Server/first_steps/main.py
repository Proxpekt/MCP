import random
from fastmcp import FastMCP

# Create a FastMCP server instance
mcp = FastMCP(name="Demo Server")

@mcp.tool()
def roll_dice(n: int = 1) -> list[int]:
    """Roll n 6-sided dice and return the results in an array."""
    return [random.randint(1, 6) for _ in range(n)]

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b

if __name__ == "__main__":
    mcp.run()
