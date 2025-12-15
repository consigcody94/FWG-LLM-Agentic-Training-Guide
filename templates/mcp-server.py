#!/usr/bin/env python3
"""
MCP Server Template for Federal Applications

This template provides a starting point for building MCP servers
that expose resources, tools, and prompts to LLM applications.

Usage:
    python mcp_server.py

Configuration:
    Set environment variables as needed for your use case.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Prompt,
    PromptMessage,
    PromptArgument,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize server
server = Server("federal-mcp-server")

# ============================================================================
# CONFIGURATION
# ============================================================================

# Add your configuration here
CONFIG = {
    "server_name": "Federal MCP Server",
    "version": "1.0.0",
    "data_path": "/path/to/data",
}

# ============================================================================
# RESOURCES
# Resources are data sources that the LLM can read
# ============================================================================

@server.list_resources()
async def list_resources() -> List[Resource]:
    """
    List all available resources.

    Modify this function to return resources specific to your use case.
    """
    return [
        Resource(
            uri="federal://example/resource1",
            name="Example Resource 1",
            description="Description of what this resource contains",
            mimeType="text/markdown"
        ),
        Resource(
            uri="federal://example/resource2",
            name="Example Resource 2",
            description="Another resource description",
            mimeType="application/json"
        ),
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    """
    Read a specific resource by URI.

    Add handlers for each resource URI pattern.
    """
    logger.info(f"Reading resource: {uri}")

    if uri == "federal://example/resource1":
        # Return markdown content
        return "# Example Resource\n\nThis is example content."

    elif uri == "federal://example/resource2":
        # Return JSON content
        return json.dumps({"key": "value", "data": [1, 2, 3]})

    else:
        raise ValueError(f"Unknown resource URI: {uri}")

# ============================================================================
# TOOLS
# Tools are functions that the LLM can invoke
# ============================================================================

@server.list_tools()
async def list_tools() -> List[Tool]:
    """
    List all available tools.

    Define tools with clear names, descriptions, and input schemas.
    """
    return [
        Tool(
            name="example_tool",
            description="""
            Brief description of what this tool does.

            Use this tool when:
            - Condition 1
            - Condition 2

            Do NOT use when:
            - Condition 3
            """,
            inputSchema={
                "type": "object",
                "properties": {
                    "required_param": {
                        "type": "string",
                        "description": "Description of this required parameter"
                    },
                    "optional_param": {
                        "type": "integer",
                        "description": "Description of optional parameter",
                        "default": 10
                    },
                    "enum_param": {
                        "type": "string",
                        "enum": ["option1", "option2", "option3"],
                        "description": "Parameter with fixed options"
                    }
                },
                "required": ["required_param"]
            }
        ),
        Tool(
            name="search_tool",
            description="Search for items matching a query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Maximum results to return",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 100
                    }
                },
                "required": ["query"]
            }
        ),
    ]

@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """
    Execute a tool call.

    Add handlers for each tool name.
    """
    logger.info(f"Calling tool: {name} with args: {arguments}")

    try:
        if name == "example_tool":
            result = await execute_example_tool(
                required_param=arguments["required_param"],
                optional_param=arguments.get("optional_param", 10),
                enum_param=arguments.get("enum_param")
            )
            return [TextContent(type="text", text=result)]

        elif name == "search_tool":
            results = await execute_search(
                query=arguments["query"],
                limit=arguments.get("limit", 10)
            )
            return [TextContent(type="text", text=json.dumps(results, indent=2))]

        else:
            return [TextContent(
                type="text",
                text=f"Error: Unknown tool '{name}'"
            )]

    except Exception as e:
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(
            type="text",
            text=f"Error executing tool: {str(e)}"
        )]

# ============================================================================
# PROMPTS
# Prompts are reusable prompt templates
# ============================================================================

@server.list_prompts()
async def list_prompts() -> List[Prompt]:
    """
    List available prompt templates.
    """
    return [
        Prompt(
            name="analysis_template",
            description="Template for performing analysis tasks",
            arguments=[
                PromptArgument(
                    name="subject",
                    description="The subject to analyze",
                    required=True
                ),
                PromptArgument(
                    name="focus_area",
                    description="Specific area to focus on",
                    required=False
                )
            ]
        ),
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str]) -> List[PromptMessage]:
    """
    Get a prompt template with arguments filled in.
    """
    if name == "analysis_template":
        subject = arguments.get("subject", "unknown")
        focus_area = arguments.get("focus_area", "general")

        return [
            PromptMessage(
                role="user",
                content=TextContent(
                    type="text",
                    text=f"""Analyze the following subject: {subject}

Focus Area: {focus_area}

Please provide:
1. Overview
2. Key findings
3. Recommendations
4. Next steps"""
                )
            )
        ]

    raise ValueError(f"Unknown prompt: {name}")

# ============================================================================
# HELPER FUNCTIONS
# Implement your business logic here
# ============================================================================

async def execute_example_tool(
    required_param: str,
    optional_param: int = 10,
    enum_param: Optional[str] = None
) -> str:
    """
    Execute the example tool logic.

    Replace with your actual implementation.
    """
    # Simulate some processing
    await asyncio.sleep(0.1)

    result = f"Processed: {required_param}"
    if enum_param:
        result += f" with option: {enum_param}"
    result += f" (limit: {optional_param})"

    return result

async def execute_search(query: str, limit: int = 10) -> List[Dict]:
    """
    Execute search logic.

    Replace with your actual search implementation.
    """
    # Simulate search results
    await asyncio.sleep(0.1)

    return [
        {"id": i, "title": f"Result {i} for '{query}'", "score": 1.0 - (i * 0.1)}
        for i in range(min(limit, 5))
    ]

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

async def main():
    """
    Run the MCP server.
    """
    logger.info(f"Starting {CONFIG['server_name']} v{CONFIG['version']}")

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
