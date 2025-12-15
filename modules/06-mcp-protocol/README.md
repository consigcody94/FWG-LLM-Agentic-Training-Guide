<div align="center">

# Module 06: Model Context Protocol (MCP)

<img src="https://img.shields.io/badge/Duration-6_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_01,_04-orange?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Explain the MCP architecture and its role in LLM applications
- [ ] Implement MCP servers that expose resources and tools
- [ ] Integrate MCP clients into LLM-powered applications
- [ ] Configure security controls for MCP deployments
- [ ] Build custom tools for federal use cases
- [ ] Troubleshoot common MCP integration issues

---

## Table of Contents

1. [What is MCP?](#1-what-is-mcp)
2. [Protocol Architecture](#2-protocol-architecture)
3. [Server Implementation](#3-server-implementation)
4. [Client Integration](#4-client-integration)
5. [Resource Management](#5-resource-management)
6. [Tool Definition](#6-tool-definition)
7. [Security Patterns](#7-security-patterns)
8. [Federal Use Cases](#8-federal-use-cases)

---

## 1. What is MCP?

### Overview

The Model Context Protocol (MCP) is an open standard that enables seamless communication between LLM applications and external data sources, tools, and services.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MODEL CONTEXT PROTOCOL (MCP)                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PURPOSE: Standardize how LLMs access external context and capabilities      ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                         THE PROBLEM                                    │ ║
║  │                                                                         │ ║
║  │  Traditional Approach:                                                  │ ║
║  │  ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐          │ ║
║  │  │  App A  │────▶│Custom   │────▶│ Data    │     │  LLM    │          │ ║
║  │  │         │     │Adapter A│     │Source 1 │     │         │          │ ║
║  │  └─────────┘     └─────────┘     └─────────┘     └─────────┘          │ ║
║  │  ┌─────────┐     ┌─────────┐     ┌─────────┐         │               │ ║
║  │  │  App B  │────▶│Custom   │────▶│ Data    │─────────┘               │ ║
║  │  │         │     │Adapter B│     │Source 2 │                          │ ║
║  │  └─────────┘     └─────────┘     └─────────┘                          │ ║
║  │                                                                         │ ║
║  │  ❌ N × M integration problem                                          │ ║
║  │  ❌ Inconsistent interfaces                                            │ ║
║  │  ❌ Duplicated effort                                                  │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                         THE SOLUTION                                   │ ║
║  │                                                                         │ ║
║  │  MCP Approach:                                                          │ ║
║  │  ┌─────────┐                 ┌─────────────────┐     ┌─────────┐      │ ║
║  │  │  App A  │─────┐           │   MCP Server    │────▶│ Data    │      │ ║
║  │  └─────────┘     │           │                 │     │Source 1 │      │ ║
║  │  ┌─────────┐     │  ┌─────┐ │  • Resources    │     └─────────┘      │ ║
║  │  │  App B  │─────┼─▶│ MCP │▶│  • Tools        │     ┌─────────┐      │ ║
║  │  └─────────┘     │  │     │ │  • Prompts      │────▶│ Data    │      │ ║
║  │  ┌─────────┐     │  └─────┘ │                 │     │Source 2 │      │ ║
║  │  │  App C  │─────┘           └─────────────────┘     └─────────┘      │ ║
║  │  └─────────┘                                                           │ ║
║  │                                                                         │ ║
║  │  ✅ Standard protocol                                                  │ ║
║  │  ✅ Reusable servers                                                   │ ║
║  │  ✅ Consistent interface                                               │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Core Concepts

| Concept | Description | Example |
|:--------|:------------|:--------|
| **Resources** | Data sources exposed to LLMs | Files, database records, API responses |
| **Tools** | Functions the LLM can invoke | Search, calculate, send email |
| **Prompts** | Reusable prompt templates | Analysis templates, report formats |
| **Sampling** | Request LLM completions from server | Nested model calls |

### MCP vs Other Protocols

| Protocol | Purpose | Scope |
|:---------|:--------|:------|
| **MCP** | LLM ↔ Data/Tools | Context & capabilities |
| **A2A** | Agent ↔ Agent | Multi-agent coordination |
| **OpenAI Functions** | API ↔ LLM | Single provider |
| **LangChain Tools** | Framework-specific | Within LangChain |

---

## 2. Protocol Architecture

### Communication Flow

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          MCP COMMUNICATION FLOW                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                           MCP HOST (Client)                             │║
║  │           (Claude Desktop, VS Code Extension, Custom App)               │║
║  │                                                                          │║
║  │  ┌────────────────────────────────────────────────────────────────────┐ │║
║  │  │                      MCP Client Library                            │ │║
║  │  │                                                                     │ │║
║  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐             │ │║
║  │  │  │ Connection   │  │   Request    │  │  Response    │             │ │║
║  │  │  │ Manager      │  │   Handler    │  │  Parser      │             │ │║
║  │  │  └──────────────┘  └──────────────┘  └──────────────┘             │ │║
║  │  └────────────────────────────────────────────────────────────────────┘ │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                      │                                       ║
║                                      │ JSON-RPC 2.0                          ║
║                                      │ (stdio or HTTP/SSE)                   ║
║                                      ▼                                       ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                           MCP SERVER                                    │║
║  │                                                                          │║
║  │  ┌────────────────────────────────────────────────────────────────────┐ │║
║  │  │                    Request Router                                  │ │║
║  │  └────────────────────────────────────────────────────────────────────┘ │║
║  │           │                    │                    │                    │║
║  │           ▼                    ▼                    ▼                    │║
║  │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │║
║  │  │  Resources   │     │    Tools     │     │   Prompts    │            │║
║  │  │  Handler     │     │   Handler    │     │   Handler    │            │║
║  │  │              │     │              │     │              │            │║
║  │  │ list_resources│    │ list_tools   │     │ list_prompts │            │║
║  │  │ read_resource│     │ call_tool    │     │ get_prompt   │            │║
║  │  └──────────────┘     └──────────────┘     └──────────────┘            │║
║  │           │                    │                    │                    │║
║  │           ▼                    ▼                    ▼                    │║
║  │  ┌──────────────────────────────────────────────────────────────────┐  │║
║  │  │                    External Services                              │  │║
║  │  │    [Database]    [File System]    [APIs]    [Other LLMs]         │  │║
║  │  └──────────────────────────────────────────────────────────────────┘  │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Transport Mechanisms

#### stdio Transport (Recommended for Local)
```
┌──────────────┐     stdin      ┌──────────────┐
│              │ ─────────────▶ │              │
│  MCP Host    │                │  MCP Server  │
│              │ ◀───────────── │              │
└──────────────┘     stdout     └──────────────┘
```

#### HTTP/SSE Transport (For Remote)
```
┌──────────────┐   HTTP POST    ┌──────────────┐
│              │ ─────────────▶ │              │
│  MCP Client  │                │  MCP Server  │
│              │ ◀───────────── │              │
└──────────────┘   SSE Stream   └──────────────┘
```

### Message Format (JSON-RPC 2.0)

```json
// Request
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_documents",
    "arguments": {
      "query": "federal procurement regulations",
      "limit": 10
    }
  }
}

// Response
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Found 10 documents matching 'federal procurement'..."
      }
    ]
  }
}
```

---

## 3. Server Implementation

### Python Server with MCP SDK

```python
# federal_mcp_server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource
)
import asyncio
import json

# Initialize server
server = Server("federal-compliance-server")

# ============================================
# RESOURCES - Data sources for the LLM
# ============================================

@server.list_resources()
async def list_resources():
    """List available resources."""
    return [
        Resource(
            uri="federal://regulations/far",
            name="Federal Acquisition Regulation",
            description="Complete FAR documentation",
            mimeType="text/markdown"
        ),
        Resource(
            uri="federal://policies/fisma",
            name="FISMA Guidelines",
            description="Federal Information Security Management Act guidelines",
            mimeType="text/markdown"
        ),
        Resource(
            uri="federal://nist/800-53",
            name="NIST 800-53 Controls",
            description="Security and Privacy Controls catalog",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    """Read a specific resource."""
    if uri == "federal://regulations/far":
        # Load FAR content from database or file
        content = load_far_regulation()
        return TextContent(type="text", text=content)

    elif uri == "federal://nist/800-53":
        controls = load_nist_controls()
        return TextContent(
            type="text",
            text=json.dumps(controls, indent=2)
        )

    raise ValueError(f"Unknown resource: {uri}")

# ============================================
# TOOLS - Functions the LLM can invoke
# ============================================

@server.list_tools()
async def list_tools():
    """List available tools."""
    return [
        Tool(
            name="search_regulations",
            description="Search federal regulations by keyword or citation",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query or citation (e.g., 'FAR 15.303')"
                    },
                    "regulation_type": {
                        "type": "string",
                        "enum": ["FAR", "DFARS", "AGAR", "all"],
                        "default": "all"
                    },
                    "limit": {
                        "type": "integer",
                        "default": 10,
                        "maximum": 50
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="check_compliance",
            description="Check if a system meets specific NIST 800-53 controls",
            inputSchema={
                "type": "object",
                "properties": {
                    "system_description": {
                        "type": "string",
                        "description": "Description of the system to evaluate"
                    },
                    "control_family": {
                        "type": "string",
                        "description": "NIST control family (e.g., 'AC', 'AU', 'SC')"
                    },
                    "baseline": {
                        "type": "string",
                        "enum": ["low", "moderate", "high"],
                        "default": "moderate"
                    }
                },
                "required": ["system_description", "control_family"]
            }
        ),
        Tool(
            name="generate_ssp_section",
            description="Generate a System Security Plan section",
            inputSchema={
                "type": "object",
                "properties": {
                    "control_id": {
                        "type": "string",
                        "description": "NIST control ID (e.g., 'AC-2')"
                    },
                    "implementation_details": {
                        "type": "string",
                        "description": "How the control is implemented"
                    }
                },
                "required": ["control_id", "implementation_details"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    """Execute a tool call."""

    if name == "search_regulations":
        results = await search_federal_regulations(
            query=arguments["query"],
            reg_type=arguments.get("regulation_type", "all"),
            limit=arguments.get("limit", 10)
        )
        return [TextContent(
            type="text",
            text=format_search_results(results)
        )]

    elif name == "check_compliance":
        assessment = await evaluate_compliance(
            system_desc=arguments["system_description"],
            control_family=arguments["control_family"],
            baseline=arguments.get("baseline", "moderate")
        )
        return [TextContent(
            type="text",
            text=json.dumps(assessment, indent=2)
        )]

    elif name == "generate_ssp_section":
        ssp_content = await generate_ssp(
            control_id=arguments["control_id"],
            implementation=arguments["implementation_details"]
        )
        return [TextContent(
            type="text",
            text=ssp_content
        )]

    raise ValueError(f"Unknown tool: {name}")

# ============================================
# PROMPTS - Reusable prompt templates
# ============================================

@server.list_prompts()
async def list_prompts():
    """List available prompt templates."""
    return [
        {
            "name": "compliance_analysis",
            "description": "Analyze a system for federal compliance",
            "arguments": [
                {
                    "name": "system_name",
                    "description": "Name of the system",
                    "required": True
                },
                {
                    "name": "framework",
                    "description": "Compliance framework (FISMA, FedRAMP, etc.)",
                    "required": True
                }
            ]
        }
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    """Get a prompt template with arguments."""
    if name == "compliance_analysis":
        return {
            "messages": [
                {
                    "role": "user",
                    "content": {
                        "type": "text",
                        "text": f"""Analyze the {arguments['system_name']} system
for compliance with {arguments['framework']}.

Provide:
1. Applicable controls
2. Current compliance status
3. Gaps and remediation steps
4. Timeline recommendations"""
                    }
                }
            ]
        }

# ============================================
# Helper Functions
# ============================================

async def search_federal_regulations(query: str, reg_type: str, limit: int):
    """Search regulation database."""
    # Implementation would connect to regulation database
    pass

async def evaluate_compliance(system_desc: str, control_family: str, baseline: str):
    """Evaluate compliance against NIST controls."""
    # Implementation would analyze against control requirements
    pass

async def generate_ssp(control_id: str, implementation: str):
    """Generate SSP section content."""
    # Implementation would format SSP content
    pass

def format_search_results(results):
    """Format search results for display."""
    pass

def load_far_regulation():
    """Load FAR content."""
    pass

def load_nist_controls():
    """Load NIST 800-53 controls."""
    pass

# ============================================
# Main Entry Point
# ============================================

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript Server Implementation

```typescript
// federal-mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
  ListToolsRequestSchema,
  CallToolRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  {
    name: "federal-compliance-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      resources: {},
      tools: {},
    },
  }
);

// List available resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "federal://regulations/far",
        name: "Federal Acquisition Regulation",
        description: "Complete FAR documentation",
        mimeType: "text/markdown",
      },
      {
        uri: "federal://nist/800-53",
        name: "NIST 800-53 Controls",
        description: "Security and Privacy Controls",
        mimeType: "application/json",
      },
    ],
  };
});

// Read a resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "federal://regulations/far") {
    const content = await loadFARContent();
    return {
      contents: [
        {
          uri,
          mimeType: "text/markdown",
          text: content,
        },
      ],
    };
  }

  throw new Error(`Unknown resource: ${uri}`);
});

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_regulations",
        description: "Search federal regulations",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search query" },
            limit: { type: "number", default: 10 },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// Call a tool
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "search_regulations") {
    const results = await searchRegulations(args.query, args.limit || 10);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
```

---

## 4. Client Integration

### Claude Desktop Configuration

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
// %APPDATA%\Claude\claude_desktop_config.json (Windows)

{
  "mcpServers": {
    "federal-compliance": {
      "command": "python",
      "args": ["/path/to/federal_mcp_server.py"],
      "env": {
        "REGULATION_DB_PATH": "/path/to/regulations.db",
        "LOG_LEVEL": "INFO"
      }
    },
    "document-search": {
      "command": "node",
      "args": ["/path/to/doc-search-server.js"],
      "env": {
        "INDEX_PATH": "/path/to/search-index"
      }
    }
  }
}
```

### Python Client Integration

```python
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def use_mcp_server():
    # Connect to MCP server
    server_params = StdioServerParameters(
        command="python",
        args=["federal_mcp_server.py"],
        env={"LOG_LEVEL": "INFO"}
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            # Call a tool
            result = await session.call_tool(
                "search_regulations",
                arguments={"query": "FAR 15.303", "limit": 5}
            )
            print("Search results:", result.content)

            # List resources
            resources = await session.list_resources()
            print("Available resources:", [r.uri for r in resources.resources])

            # Read a resource
            resource = await session.read_resource("federal://nist/800-53")
            print("Resource content:", resource.contents[0].text[:500])

asyncio.run(use_mcp_server())
```

---

## 5. Resource Management

### Resource Types

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          MCP RESOURCE TYPES                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  TEXT RESOURCES                                                        │ ║
║  │  • Documents (markdown, plain text)                                    │ ║
║  │  • Configuration files                                                 │ ║
║  │  • Log files                                                           │ ║
║  │  • Code files                                                          │ ║
║  │  URI: file://path/to/document.md                                      │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  DATABASE RESOURCES                                                    │ ║
║  │  • SQL query results                                                   │ ║
║  │  • Record lookups                                                      │ ║
║  │  • Schema information                                                  │ ║
║  │  URI: db://database/table/record_id                                   │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  API RESOURCES                                                         │ ║
║  │  • REST endpoint responses                                             │ ║
║  │  • GraphQL query results                                               │ ║
║  │  • Webhook payloads                                                    │ ║
║  │  URI: api://service/endpoint                                          │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  BINARY RESOURCES                                                      │ ║
║  │  • Images                                                              │ ║
║  │  • PDFs (with text extraction)                                         │ ║
║  │  • Audio transcriptions                                                │ ║
║  │  URI: media://path/to/file                                            │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Resource Templates

```python
@server.list_resource_templates()
async def list_resource_templates():
    """Define parameterized resource patterns."""
    return [
        {
            "uriTemplate": "federal://controls/{control_id}",
            "name": "NIST Control Details",
            "description": "Get details for a specific NIST 800-53 control",
            "mimeType": "application/json"
        },
        {
            "uriTemplate": "federal://far/{part}/{subpart}",
            "name": "FAR Section",
            "description": "Get specific FAR section",
            "mimeType": "text/markdown"
        }
    ]
```

---

## 6. Tool Definition

### Tool Schema Best Practices

```python
# Well-defined tool with comprehensive schema
Tool(
    name="create_authorization_package",
    description="""
    Generate a FedRAMP authorization package component.

    Use this tool when:
    - Preparing for FedRAMP assessment
    - Documenting security controls
    - Creating compliance artifacts

    Do NOT use for:
    - Informal documentation
    - Non-federal compliance
    """,
    inputSchema={
        "type": "object",
        "properties": {
            "package_type": {
                "type": "string",
                "enum": [
                    "system_security_plan",
                    "security_assessment_report",
                    "plan_of_action_milestones",
                    "continuous_monitoring"
                ],
                "description": "Type of authorization document"
            },
            "system_name": {
                "type": "string",
                "minLength": 1,
                "maxLength": 100,
                "description": "Official system name"
            },
            "impact_level": {
                "type": "string",
                "enum": ["low", "moderate", "high"],
                "description": "FIPS 199 impact level"
            },
            "controls": {
                "type": "array",
                "items": {
                    "type": "string",
                    "pattern": "^[A-Z]{2}-[0-9]+$"
                },
                "description": "List of control IDs (e.g., ['AC-2', 'AU-3'])"
            },
            "include_implementation": {
                "type": "boolean",
                "default": True,
                "description": "Include implementation details"
            }
        },
        "required": ["package_type", "system_name", "impact_level"],
        "additionalProperties": False
    }
)
```

### Error Handling

```python
@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "search_regulations":
            # Validate input
            if not arguments.get("query"):
                return [TextContent(
                    type="text",
                    text="Error: 'query' parameter is required"
                )]

            # Execute with timeout
            async with asyncio.timeout(30):
                results = await search_regulations(arguments["query"])

            if not results:
                return [TextContent(
                    type="text",
                    text=f"No results found for: {arguments['query']}"
                )]

            return [TextContent(type="text", text=format_results(results))]

    except asyncio.TimeoutError:
        return [TextContent(
            type="text",
            text="Error: Search timed out. Try a more specific query."
        )]
    except ValidationError as e:
        return [TextContent(
            type="text",
            text=f"Validation error: {str(e)}"
        )]
    except Exception as e:
        # Log error for debugging
        logger.error(f"Tool execution failed: {e}")
        return [TextContent(
            type="text",
            text="An unexpected error occurred. Please try again."
        )]
```

---

## 7. Security Patterns

### Access Control

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       MCP SECURITY ARCHITECTURE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                    SECURITY LAYERS                                     │ ║
║  │                                                                         │ ║
║  │  1. TRANSPORT SECURITY                                                  │ ║
║  │     ├── stdio: Process isolation (local only)                          │ ║
║  │     └── HTTP: TLS 1.3 required for remote                              │ ║
║  │                                                                         │ ║
║  │  2. AUTHENTICATION                                                      │ ║
║  │     ├── API keys for server identification                             │ ║
║  │     ├── OAuth 2.0 for user context                                     │ ║
║  │     └── mTLS for high-security environments                            │ ║
║  │                                                                         │ ║
║  │  3. AUTHORIZATION                                                       │ ║
║  │     ├── Tool-level permissions                                         │ ║
║  │     ├── Resource access controls                                       │ ║
║  │     └── User role-based filtering                                      │ ║
║  │                                                                         │ ║
║  │  4. INPUT VALIDATION                                                    │ ║
║  │     ├── Schema validation (JSON Schema)                                │ ║
║  │     ├── Input sanitization                                             │ ║
║  │     └── Rate limiting                                                  │ ║
║  │                                                                         │ ║
║  │  5. AUDIT LOGGING                                                       │ ║
║  │     ├── All tool invocations                                           │ ║
║  │     ├── Resource access                                                │ ║
║  │     └── Error conditions                                               │ ║
║  │                                                                         │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Secure Server Implementation

```python
import logging
from functools import wraps
from typing import Callable
import hashlib
import hmac

# Configure secure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
audit_logger = logging.getLogger('audit')

# Security decorators
def require_permission(permission: str):
    """Decorator to check permissions before tool execution."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user context from request
            user_context = get_current_user_context()

            if not user_context.has_permission(permission):
                audit_logger.warning(
                    f"Permission denied: {permission} for user {user_context.user_id}"
                )
                raise PermissionError(f"Missing permission: {permission}")

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def audit_log(action: str):
    """Decorator to log all tool invocations."""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_context = get_current_user_context()

            audit_logger.info(
                f"Action: {action} | "
                f"User: {user_context.user_id} | "
                f"Args: {kwargs}"
            )

            try:
                result = await func(*args, **kwargs)
                audit_logger.info(f"Action: {action} | Status: SUCCESS")
                return result
            except Exception as e:
                audit_logger.error(f"Action: {action} | Status: FAILED | Error: {e}")
                raise
        return wrapper
    return decorator

def rate_limit(max_requests: int, window_seconds: int):
    """Decorator to rate limit tool calls."""
    call_history = {}

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user_id = get_current_user_context().user_id
            current_time = time.time()

            # Clean old entries
            if user_id in call_history:
                call_history[user_id] = [
                    t for t in call_history[user_id]
                    if current_time - t < window_seconds
                ]
            else:
                call_history[user_id] = []

            # Check limit
            if len(call_history[user_id]) >= max_requests:
                raise RateLimitError(
                    f"Rate limit exceeded: {max_requests} requests per {window_seconds}s"
                )

            call_history[user_id].append(current_time)
            return await func(*args, **kwargs)
        return wrapper
    return decorator

# Apply security to tools
@server.call_tool()
@audit_log("tool_call")
@rate_limit(max_requests=100, window_seconds=60)
async def call_tool(name: str, arguments: dict):
    if name == "access_sensitive_data":
        # Additional permission check for sensitive operations
        await verify_clearance_level("SECRET")

    # ... tool implementation
```

---

## 8. Federal Use Cases

### Document Management System

```python
# Federal document management MCP server
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_fouo_documents",
            description="Search For Official Use Only documents",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "classification": {
                        "type": "string",
                        "enum": ["UNCLASSIFIED", "FOUO", "CUI"]
                    },
                    "date_range": {
                        "type": "object",
                        "properties": {
                            "start": {"type": "string", "format": "date"},
                            "end": {"type": "string", "format": "date"}
                        }
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="extract_pii",
            description="Identify and flag PII in document content",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "pii_types": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["SSN", "DOB", "ADDRESS", "PHONE", "EMAIL"]
                        }
                    }
                },
                "required": ["document_id"]
            }
        ),
        Tool(
            name="generate_redaction_report",
            description="Generate report of required redactions for FOIA release",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "exemptions": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["b1", "b2", "b3", "b4", "b5", "b6", "b7"]
                        }
                    }
                },
                "required": ["document_id"]
            }
        )
    ]
```

### Compliance Automation

```python
# Continuous compliance monitoring MCP server
Tool(
    name="run_compliance_scan",
    description="Execute automated compliance scan against NIST/FedRAMP controls",
    inputSchema={
        "type": "object",
        "properties": {
            "target_system": {
                "type": "string",
                "description": "System identifier or IP range"
            },
            "framework": {
                "type": "string",
                "enum": ["NIST-800-53", "FedRAMP-Moderate", "FedRAMP-High", "FISMA"]
            },
            "control_families": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Specific control families to scan"
            },
            "output_format": {
                "type": "string",
                "enum": ["OSCAL", "POAM", "JSON"],
                "default": "OSCAL"
            }
        },
        "required": ["target_system", "framework"]
    }
)
```

---

## Exercises

### Exercise 6.1: Basic MCP Server
Create an MCP server that exposes federal regulation data as resources.

### Exercise 6.2: Tool Implementation
Implement a compliance-checking tool with proper input validation and error handling.

### Exercise 6.3: Client Integration
Configure Claude Desktop to use your MCP server and test interactions.

### Exercise 6.4: Security Hardening
Add authentication, authorization, and audit logging to your MCP server.

---

## Assessment

### Knowledge Check

1. What are the four core capabilities of MCP?
2. Explain the difference between resources and tools in MCP.
3. What transport mechanisms does MCP support?
4. How do you configure an MCP server in Claude Desktop?
5. What security measures should be implemented for federal MCP deployments?

### Practical Assessment

Build a complete MCP server for a federal use case, including:
- At least 3 resources
- At least 3 tools with proper schemas
- Security controls (authentication, logging)
- Client integration demonstration

---

## Next Module

➡️ [Module 07: A2A Protocol](../07-a2a-protocol/README.md)

---

<div align="center">

[⬆ Back to Top](#module-06-model-context-protocol-mcp) · [📚 Return to Curriculum](../../README.md)

</div>
