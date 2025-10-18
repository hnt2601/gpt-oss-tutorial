"""
Example: Model Context Protocol (MCP)

This example demonstrates how to use MCP servers to extend
model capabilities with external tools and services.

Key Concepts:
- MCP server integration
- Remote tool execution
- Tool approval policies
"""

from pprint import pprint
from src.client import create_client, get_default_model


def mcp_github_documentation():
    """
    Example: Using MCP to access GitHub documentation
    
    Connects to a GitMCP server to search and fetch documentation
    from GitHub repositories.
    """
    client = create_client()
    
    print("=" * 60)
    print("Example: MCP - GitHub Documentation Access")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="How does tiktoken work? Search the tiktoken repository for documentation.",
        tools=[
            {
                "type": "mcp",
                "server_label": "gitmcp",
                "server_url": "https://gitmcp.io/openai/tiktoken",
                "allowed_tools": [
                    "search_tiktoken_documentation", 
                    "fetch_tiktoken_documentation"
                ],
                "require_approval": "never"
            }
        ]
    )
    
    print("\nQuery: How does tiktoken work?")
    print("\nMCP Server: gitmcp (tiktoken repo)")
    print("\n💬 Response:")
    output_text = response.output[-1].content[0].text
    pprint(output_text)
    
    print("\n" + "=" * 60)
    return response


def mcp_with_approval():
    """
    Example: MCP with approval policy
    
    Demonstrates different approval settings for MCP tools
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: MCP with Approval Policy")
    print("=" * 60)
    
    # Available approval policies:
    # - "never": Auto-approve all tool calls
    # - "always": Always require approval
    # - "auto": Approve safe operations, require approval for sensitive ones
    
    print("\nApproval Policies:")
    print("  • never: Auto-approve all calls (dev/testing)")
    print("  • always: Always require approval (production/sensitive)")
    print("  • auto: Smart approval based on operation type")
    
    response = client.responses.create(
        model=get_default_model(),
        input="Search for Python asyncio documentation",
        tools=[
            {
                "type": "mcp",
                "server_label": "docs_server",
                "server_url": "https://docs-mcp.example.com",
                "allowed_tools": ["search_docs", "get_doc_content"],
                "require_approval": "auto"  # Smart approval
            }
        ]
    )
    
    print("\n💬 Response:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def mcp_multiple_servers():
    """
    Example: Using multiple MCP servers
    
    Shows how to combine multiple MCP servers for different capabilities
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: Multiple MCP Servers")
    print("=" * 60)
    
    response = client.responses.create(
        model=get_default_model(),
        input="Compare the README files of openai/gpt-3 and anthropic/claude repositories",
        tools=[
            {
                "type": "mcp",
                "server_label": "github_mcp",
                "server_url": "https://gitmcp.io/openai/gpt-3",
                "allowed_tools": ["search_repo", "get_file"],
                "require_approval": "never"
            },
            {
                "type": "mcp",
                "server_label": "github_mcp_2",
                "server_url": "https://gitmcp.io/anthropic/claude",
                "allowed_tools": ["search_repo", "get_file"],
                "require_approval": "never"
            }
        ]
    )
    
    print("\nQuery: Compare READMEs from two repos")
    print("\n💬 Response:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def mcp_tool_filtering():
    """
    Example: MCP with specific tool filtering
    
    Demonstrates how to limit which tools the model can use
    from an MCP server.
    """
    client = create_client()
    
    print("\n" + "=" * 60)
    print("Example: MCP Tool Filtering")
    print("=" * 60)
    
    print("\nAllowed tools: ['search_only']")
    print("(Preventing write/modify operations)")
    
    response = client.responses.create(
        model=get_default_model(),
        input="Search for information about Python decorators",
        tools=[
            {
                "type": "mcp",
                "server_label": "docs_mcp",
                "server_url": "https://docs-mcp.example.com/python",
                "allowed_tools": [
                    "search_docs",  # Read-only
                    # "update_docs",  # Excluded
                    # "delete_docs",  # Excluded
                ],
                "require_approval": "never"
            }
        ]
    )
    
    print("\n💬 Response:")
    print(response.output_text)
    
    print("\n" + "=" * 60)
    return response


def main():
    """Run all MCP examples"""
    print("\n🚀 GPT-OSS MCP Examples")
    print("=" * 60)
    
    print("\nℹ️  Note: These examples require MCP servers to be available.")
    print("    Some may not work if servers are offline or require auth.\n")
    
    # Example 1: GitHub documentation
    try:
        mcp_github_documentation()
    except Exception as e:
        print(f"⚠️  Example 1 failed: {e}\n")
    
    # Example 2: Approval policies
    print("\n" + "=" * 60)
    mcp_with_approval()
    
    # Example 3: Multiple servers
    print("\n" + "=" * 60)
    mcp_multiple_servers()
    
    # Example 4: Tool filtering
    print("\n" + "=" * 60)
    mcp_tool_filtering()
    
    print("\n✅ All MCP examples completed!")


if __name__ == "__main__":
    main()

