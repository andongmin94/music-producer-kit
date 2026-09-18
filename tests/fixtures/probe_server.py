"""SDK subprocess fixture, deliberately not an Ableton simulator."""
from pathlib import Path
import sys
from mcp.server import MCPServer

server = MCPServer('Music kit protocol fixture')

@server.tool()
def forbidden_write(value: int) -> int:
    """Must never run during catalog discovery."""
    Path(sys.argv[1]).write_text('unexpected tool execution', encoding='utf-8')
    return value

if __name__ == '__main__':
    server.run()
