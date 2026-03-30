"""MCP server entry point."""

from mcp_parigp import mcp


def main() -> int:
    """Run the MCP server."""
    mcp.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
