# Lab 05: MCP Server Build

<div align="center">

**Building Your First Model Context Protocol Server**

⭐⭐⭐ Advanced | ⏱️ 90 minutes | 📚 Module 06

</div>

---

## Learning Objectives

By the end of this lab, you will:

- [ ] Understand MCP server architecture and components
- [ ] Implement a functional MCP server with resources and tools
- [ ] Connect your server to Claude Desktop or another MCP client
- [ ] Handle requests and responses using JSON-RPC 2.0
- [ ] Apply security best practices for MCP servers

---

## Prerequisites

- Completed Labs 00-04
- Node.js 18+ installed
- Python 3.11+ installed
- Claude Desktop OR MCP Inspector installed
- Understanding of JSON-RPC protocol basics

---

## Overview

The Model Context Protocol (MCP) enables standardized communication between LLM applications and external data sources or tools. In this lab, you'll build a complete MCP server that exposes:

1. **Resources**: Data that the LLM can read (files, documents, configs)
2. **Tools**: Functions the LLM can execute (search, calculate, fetch)
3. **Prompts**: Reusable prompt templates

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP CLIENT                              │
│                   (Claude Desktop)                           │
└─────────────────────────┬───────────────────────────────────┘
                          │ JSON-RPC 2.0
                          │ (stdio or HTTP/SSE)
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCP SERVER                              │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │  Resources  │  │    Tools    │  │   Prompts   │         │
│  │             │  │             │  │             │         │
│  │ • Documents │  │ • search    │  │ • summarize │         │
│  │ • Config    │  │ • calculate │  │ • analyze   │         │
│  │ • Data      │  │ • fetch     │  │ • format    │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└─────────────────────────────────────────────────────────────┘
```

---

## Part 1: Project Setup (10 minutes)

### Step 1.1: Create Project Directory

```bash
mkdir -p ~/fwg-mcp-lab/src
cd ~/fwg-mcp-lab
```

### Step 1.2: Initialize Python Project

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Create requirements.txt
cat > requirements.txt << 'EOF'
mcp>=0.9.0
httpx>=0.25.0
python-dotenv>=1.0.0
pydantic>=2.0.0
EOF

# Install dependencies
pip install -r requirements.txt
```

### Step 1.3: Create Project Structure

```bash
mkdir -p src/{resources,tools}
touch src/__init__.py
touch src/server.py
touch src/resources/__init__.py
touch src/tools/__init__.py
```

---

## Part 2: Basic MCP Server (20 minutes)

### Step 2.1: Create the Main Server

Create `src/server.py`:

```python
"""
FWG MCP Server - Lab 05
A demonstration MCP server for Federal Working Group training.
"""

import asyncio
import json
from datetime import datetime
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Initialize the MCP server
server = Server("fwg-training-server")

# ============================================================================
# RESOURCES: Data sources the LLM can read
# ============================================================================

# In-memory data store for demo purposes
POLICY_DATABASE = {
    "ai-governance": {
        "title": "AI Governance Policy",
        "version": "2.0",
        "effective_date": "2025-01-01",
        "content": """
# Federal AI Governance Policy

## Purpose
This policy establishes guidelines for the responsible development and
deployment of AI systems within federal agencies.

## Key Principles
1. Transparency: AI systems must be explainable
2. Accountability: Clear ownership and oversight
3. Fairness: Bias detection and mitigation
4. Security: Robust protection of AI systems
5. Privacy: Protection of personal information

## Compliance Requirements
- All AI systems must undergo impact assessment
- High-risk AI requires human oversight
- Annual security reviews mandatory
"""
    },
    "data-classification": {
        "title": "Data Classification Guidelines",
        "version": "1.5",
        "effective_date": "2024-06-01",
        "content": """
# Data Classification Guidelines

## Classification Levels
- **PUBLIC**: No restrictions on disclosure
- **INTERNAL**: For internal use only
- **CONFIDENTIAL**: Limited distribution
- **RESTRICTED**: Strict access controls required

## AI Training Data Requirements
- CUI data prohibited for external AI training
- PII must be anonymized before AI processing
- All training data requires classification review
"""
    }
}


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List all available resources."""
    resources = []

    for policy_id, policy in POLICY_DATABASE.items():
        resources.append(
            Resource(
                uri=f"policy://{policy_id}",
                name=policy["title"],
                description=f"Federal policy document v{policy['version']}",
                mimeType="text/markdown"
            )
        )

    # Add a dynamic resource
    resources.append(
        Resource(
            uri="status://server",
            name="Server Status",
            description="Current server status and metrics",
            mimeType="application/json"
        )
    )

    return resources


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read a specific resource by URI."""

    if uri.startswith("policy://"):
        policy_id = uri.replace("policy://", "")
        if policy_id in POLICY_DATABASE:
            policy = POLICY_DATABASE[policy_id]
            return policy["content"]
        raise ValueError(f"Policy not found: {policy_id}")

    elif uri == "status://server":
        status = {
            "server_name": "fwg-training-server",
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "resources_count": len(POLICY_DATABASE),
            "tools_available": 3
        }
        return json.dumps(status, indent=2)

    raise ValueError(f"Unknown resource URI: {uri}")


# ============================================================================
# TOOLS: Functions the LLM can execute
# ============================================================================

@server.list_tools()
async def list_tools() -> list[Tool]:
    """List all available tools."""
    return [
        Tool(
            name="search_policies",
            description="Search federal policies for specific keywords or topics",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query (keywords or topic)"
                    },
                    "policy_type": {
                        "type": "string",
                        "enum": ["all", "governance", "security", "data"],
                        "description": "Type of policy to search"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="compliance_check",
            description="Check if a proposed AI use case complies with federal policies",
            inputSchema={
                "type": "object",
                "properties": {
                    "use_case": {
                        "type": "string",
                        "description": "Description of the AI use case"
                    },
                    "data_types": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Types of data involved (e.g., PII, CUI, public)"
                    },
                    "risk_level": {
                        "type": "string",
                        "enum": ["low", "medium", "high"],
                        "description": "Assessed risk level of the use case"
                    }
                },
                "required": ["use_case", "data_types"]
            }
        ),
        Tool(
            name="calculate_tokens",
            description="Estimate token count and cost for a given text",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze"
                    },
                    "model": {
                        "type": "string",
                        "enum": ["gpt-4", "gpt-4o", "claude-3-sonnet", "claude-3-opus"],
                        "description": "Target model for pricing"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute a tool with the given arguments."""

    if name == "search_policies":
        results = search_policies(
            query=arguments["query"],
            policy_type=arguments.get("policy_type", "all")
        )
        return [TextContent(type="text", text=json.dumps(results, indent=2))]

    elif name == "compliance_check":
        result = compliance_check(
            use_case=arguments["use_case"],
            data_types=arguments["data_types"],
            risk_level=arguments.get("risk_level", "medium")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    elif name == "calculate_tokens":
        result = calculate_tokens(
            text=arguments["text"],
            model=arguments.get("model", "gpt-4o")
        )
        return [TextContent(type="text", text=json.dumps(result, indent=2))]

    raise ValueError(f"Unknown tool: {name}")


# Tool implementation functions
def search_policies(query: str, policy_type: str = "all") -> dict:
    """Search policies for matching content."""
    results = []
    query_lower = query.lower()

    for policy_id, policy in POLICY_DATABASE.items():
        # Simple keyword matching (in production, use vector search)
        if query_lower in policy["content"].lower() or query_lower in policy["title"].lower():
            results.append({
                "policy_id": policy_id,
                "title": policy["title"],
                "version": policy["version"],
                "match_preview": policy["content"][:200] + "..."
            })

    return {
        "query": query,
        "policy_type": policy_type,
        "results_count": len(results),
        "results": results
    }


def compliance_check(use_case: str, data_types: list, risk_level: str = "medium") -> dict:
    """Check compliance with federal policies."""
    findings = []
    compliant = True

    # Check data type restrictions
    if "PII" in data_types or "pii" in [d.lower() for d in data_types]:
        findings.append({
            "category": "Privacy",
            "status": "WARNING",
            "message": "PII involvement requires privacy impact assessment",
            "reference": "Data Classification Guidelines, Section 2"
        })

    if "CUI" in data_types or "cui" in [d.lower() for d in data_types]:
        findings.append({
            "category": "Security",
            "status": "ALERT",
            "message": "CUI data prohibited for external AI training",
            "reference": "Data Classification Guidelines, AI Training Data Requirements"
        })
        compliant = False

    # Risk level checks
    if risk_level == "high":
        findings.append({
            "category": "Governance",
            "status": "REQUIRED",
            "message": "High-risk AI requires human oversight and approval",
            "reference": "AI Governance Policy, Compliance Requirements"
        })

    return {
        "use_case": use_case,
        "data_types": data_types,
        "risk_level": risk_level,
        "overall_compliance": compliant,
        "findings": findings,
        "recommendations": [
            "Complete AI impact assessment",
            "Document data handling procedures",
            "Establish monitoring and oversight"
        ] if findings else ["No immediate concerns identified"]
    }


def calculate_tokens(text: str, model: str = "gpt-4o") -> dict:
    """Estimate token count and cost."""
    # Simplified estimation (real implementation would use tiktoken)
    word_count = len(text.split())
    estimated_tokens = int(word_count * 1.3)  # Rough approximation

    # Pricing per 1K tokens (simplified)
    pricing = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "claude-3-sonnet": {"input": 0.003, "output": 0.015},
        "claude-3-opus": {"input": 0.015, "output": 0.075}
    }

    model_pricing = pricing.get(model, pricing["gpt-4o"])
    estimated_cost = (estimated_tokens / 1000) * model_pricing["input"]

    return {
        "text_length": len(text),
        "word_count": word_count,
        "estimated_tokens": estimated_tokens,
        "model": model,
        "estimated_input_cost": f"${estimated_cost:.4f}",
        "pricing_note": "Estimates only; actual costs may vary"
    }


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
```

---

## Part 3: Testing Your Server (20 minutes)

### Step 3.1: Install MCP Inspector

```bash
npm install -g @anthropic-ai/mcp-inspector
```

### Step 3.2: Run the Inspector

```bash
# In one terminal, start the inspector
mcp-inspector

# In another terminal, connect your server
cd ~/fwg-mcp-lab
source .venv/bin/activate
python -m src.server
```

### Step 3.3: Test Resources

In the MCP Inspector:

1. Click "List Resources"
2. Click on a resource to read it
3. Verify the policy content is returned

### Step 3.4: Test Tools

1. Click "List Tools"
2. Select "search_policies"
3. Enter test arguments:
   ```json
   {
     "query": "AI",
     "policy_type": "all"
   }
   ```
4. Verify results are returned

---

## Part 4: Connect to Claude Desktop (15 minutes)

### Step 4.1: Configure Claude Desktop

Add your server to Claude Desktop's configuration:

**macOS/Linux**: `~/.config/claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "fwg-training": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/fwg-mcp-lab",
      "env": {
        "PYTHONPATH": "/path/to/fwg-mcp-lab"
      }
    }
  }
}
```

### Step 4.2: Restart Claude Desktop

1. Quit Claude Desktop completely
2. Restart the application
3. Look for the MCP server icon in the interface

### Step 4.3: Test Integration

Ask Claude:
- "What policies are available in the FWG training server?"
- "Search policies for information about AI governance"
- "Check if using customer PII for AI training is compliant"

---

## Part 5: Add Security Features (15 minutes)

### Step 5.1: Input Validation

Add to your server:

```python
from pydantic import BaseModel, validator, Field
from typing import Optional, List

class SearchPoliciesInput(BaseModel):
    query: str = Field(..., min_length=1, max_length=500)
    policy_type: str = Field(default="all", pattern="^(all|governance|security|data)$")

    @validator('query')
    def sanitize_query(cls, v):
        # Remove potentially dangerous characters
        return v.replace('<', '').replace('>', '').replace('&', '')

class ComplianceCheckInput(BaseModel):
    use_case: str = Field(..., min_length=10, max_length=2000)
    data_types: List[str] = Field(..., min_items=1, max_items=10)
    risk_level: Optional[str] = Field(default="medium", pattern="^(low|medium|high)$")
```

### Step 5.2: Rate Limiting

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str = "default") -> bool:
        now = datetime.now()
        window_start = now - self.window

        # Clean old requests
        self.requests[client_id] = [
            ts for ts in self.requests[client_id]
            if ts > window_start
        ]

        if len(self.requests[client_id]) >= self.max_requests:
            return False

        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter()
```

### Step 5.3: Audit Logging

```python
import logging
from functools import wraps

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('mcp_audit.log'),
        logging.StreamHandler()
    ]
)

audit_logger = logging.getLogger('mcp.audit')

def audit_log(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        audit_logger.info(f"Tool called: {func.__name__}, Args: {kwargs}")
        try:
            result = await func(*args, **kwargs)
            audit_logger.info(f"Tool completed: {func.__name__}, Success")
            return result
        except Exception as e:
            audit_logger.error(f"Tool failed: {func.__name__}, Error: {e}")
            raise
    return wrapper
```

---

## Exercises

### Exercise 1: Add a New Resource

Add a new resource that exposes a "training schedule" or "compliance checklist".

### Exercise 2: Create a Custom Tool

Add a tool that generates a compliance report in a structured format.

### Exercise 3: Add Prompts

Implement the `list_prompts` and `get_prompt` handlers to provide reusable prompt templates.

---

## Challenge: Advanced Features

### Challenge A: Database Integration
Connect your MCP server to a SQLite database instead of in-memory storage.

### Challenge B: External API Integration
Add a tool that fetches real-time data from an external API.

### Challenge C: Multi-user Support
Implement session management to support multiple concurrent users.

---

## Knowledge Check

1. **What is the difference between Resources and Tools in MCP?**

2. **Why is input validation important for MCP tools?**

3. **How does the JSON-RPC 2.0 protocol facilitate MCP communication?**

4. **What security considerations apply to MCP servers in federal environments?**

---

## Self-Assessment Rubric

| Criteria | Meets Expectations |
|----------|-------------------|
| Server starts without errors | ✅ |
| Resources are listed and readable | ✅ |
| All three tools work correctly | ✅ |
| Claude Desktop integration works | ✅ |
| Input validation implemented | ✅ |
| Audit logging enabled | ✅ |

---

## Troubleshooting

### Server Won't Start

```bash
# Check for syntax errors
python -m py_compile src/server.py

# Check dependencies
pip list | grep mcp
```

### Claude Desktop Can't Connect

1. Verify the path in configuration is correct
2. Check Claude Desktop logs for errors
3. Ensure Python is in your PATH
4. Try running the server manually first

### Tools Return Errors

```python
# Add debugging
import traceback

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        # ... tool logic ...
    except Exception as e:
        traceback.print_exc()
        raise
```

---

## Next Steps

**Next Lab:** [Lab 06: A2A Agent Card →](../06-a2a-agent-card/README.md)

---

## Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Python SDK Documentation](https://modelcontextprotocol.io/docs)
- [Claude Desktop MCP Guide](https://claude.ai/docs/mcp)

---

<div align="center">

**Lab 05 Complete!** 🎉

</div>
