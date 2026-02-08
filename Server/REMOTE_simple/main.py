from fastmcp import FastMCP
import random
import json

mcp = FastMCP(name="Simple Calculator Server")

@mcp.tool
def add(a: int, b: int) -> int:
    """
    Returns the sum of two integers.
    
    Parameters
    ----------
    a : int
        The first integer.
    b : int
        The second integer.
    
    Returns
    -------
    int
        The sum of a and b.
    """
    return a + b

@mcp.tool
def random_number(min_val: int = 0, max_val: int = 100) -> int:
    """
    Returns a random integer between min_val and max_val (inclusive).
    
    Parameters
    ----------
    min_val : int, default=0
        The minimum value of the range.
    max_val : int, default=100
        The maximum value of the range.
    
    Returns
    -------
    int
        A random integer in the range [min_val, max_val].
    """
    return random.randint(min_val, max_val)

@mcp.resource("info://server")
def server_info() -> str:
    info = {
        "name": "Simple Calculator Server",
        "description": "A simple calculator server.",
        "version": "1.0.0",
        "author": "Proxpekt",
        "tools": ["add", "random_number"],
    }
    
    return json.dumps(info, indent=2)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000, host="0.0.0.0")