<div align="center">

# Module 13: Tool Use & Function Calling

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_4--5-green?style=for-the-badge" alt="Prerequisites"/>

*Extending LLM capabilities with external tools and APIs*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Design effective tool schemas for LLM consumption
- [ ] Implement function calling across major providers
- [ ] Build secure tool execution pipelines
- [ ] Handle tool errors and edge cases
- [ ] Create federal-compliant tool integrations

---

## 13.1 Tool Use Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    TOOL USE FLOW                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   1. User Query       2. LLM Analysis      3. Tool Selection    │
│   ┌──────────┐        ┌──────────┐         ┌──────────┐        │
│   │ "What's  │   ──►  │   LLM    │   ──►   │ weather  │        │
│   │ the      │        │ decides  │         │ tool     │        │
│   │ weather?"│        │ tool use │         │ selected │        │
│   └──────────┘        └──────────┘         └──────────┘        │
│                                                                  │
│   4. Execute Tool     5. Process Result    6. Final Response   │
│   ┌──────────┐        ┌──────────┐         ┌──────────┐        │
│   │ Call     │   ──►  │   LLM    │   ──►   │ "The     │        │
│   │ Weather  │        │ formats  │         │ weather  │        │
│   │ API      │        │ response │         │ is 72°F" │        │
│   └──────────┘        └──────────┘         └──────────┘        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Tool Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Retrieval** | Fetch information | Database queries, API calls, search |
| **Action** | Perform operations | Send email, create ticket, deploy |
| **Computation** | Calculate/analyze | Math, statistics, data transformation |
| **Integration** | Connect systems | CRM, ERP, legacy systems |

---

## 13.2 Tool Schema Design

### OpenAI Function Schema

```python
# Well-designed tool schema
get_employee_info = {
    "type": "function",
    "function": {
        "name": "get_employee_info",
        "description": "Retrieve employee information from HR system. Use this when you need to look up details about a specific federal employee.",
        "parameters": {
            "type": "object",
            "properties": {
                "employee_id": {
                    "type": "string",
                    "description": "The employee's unique identifier (format: EMP-XXXXX)",
                    "pattern": "^EMP-[0-9]{5}$"
                },
                "fields": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["name", "department", "title", "email", "hire_date"]
                    },
                    "description": "Specific fields to retrieve. Omit for all fields.",
                    "default": []
                },
                "include_sensitive": {
                    "type": "boolean",
                    "description": "Include sensitive data (requires elevated permissions)",
                    "default": False
                }
            },
            "required": ["employee_id"]
        }
    }
}

# Search tool with complex parameters
search_documents = {
    "type": "function",
    "function": {
        "name": "search_federal_documents",
        "description": "Search federal document repository. Supports full-text search with filters.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (supports boolean operators: AND, OR, NOT)"
                },
                "document_type": {
                    "type": "string",
                    "enum": ["policy", "memo", "report", "regulation", "all"],
                    "description": "Type of document to search"
                },
                "date_range": {
                    "type": "object",
                    "properties": {
                        "start": {
                            "type": "string",
                            "format": "date",
                            "description": "Start date (YYYY-MM-DD)"
                        },
                        "end": {
                            "type": "string",
                            "format": "date",
                            "description": "End date (YYYY-MM-DD)"
                        }
                    }
                },
                "classification": {
                    "type": "string",
                    "enum": ["UNCLASSIFIED", "CUI"],
                    "default": "UNCLASSIFIED"
                },
                "max_results": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 100,
                    "default": 10
                }
            },
            "required": ["query"]
        }
    }
}
```

### Anthropic Tool Schema

```python
# Claude tool definition
tools = [
    {
        "name": "query_compliance_database",
        "description": "Query the federal compliance database for control implementations and assessment results. Returns compliance status and findings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "system_id": {
                    "type": "string",
                    "description": "System identifier in the compliance database"
                },
                "control_family": {
                    "type": "string",
                    "description": "NIST control family (e.g., 'AC', 'AU', 'SC')"
                },
                "status_filter": {
                    "type": "string",
                    "enum": ["all", "compliant", "non-compliant", "partial"],
                    "description": "Filter by compliance status"
                }
            },
            "required": ["system_id"]
        }
    },
    {
        "name": "create_poam_entry",
        "description": "Create a Plan of Action and Milestones (POA&M) entry for a compliance finding. Requires approval for execution.",
        "input_schema": {
            "type": "object",
            "properties": {
                "finding_id": {
                    "type": "string",
                    "description": "ID of the compliance finding"
                },
                "remediation_plan": {
                    "type": "string",
                    "description": "Description of planned remediation actions"
                },
                "milestone_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Target completion date"
                },
                "assigned_to": {
                    "type": "string",
                    "description": "Person or team responsible"
                },
                "priority": {
                    "type": "string",
                    "enum": ["critical", "high", "medium", "low"]
                }
            },
            "required": ["finding_id", "remediation_plan", "milestone_date", "assigned_to"]
        }
    }
]
```

---

## 13.3 Implementation Patterns

### OpenAI Function Calling

```python
from openai import OpenAI
import json

client = OpenAI()

def process_with_tools(user_message: str, tools: list) -> str:
    """Process a message with tool calling."""

    messages = [{"role": "user", "content": user_message}]

    # Initial call
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    # Check if tools were called
    while response.choices[0].message.tool_calls:
        # Add assistant message
        messages.append(response.choices[0].message)

        # Process each tool call
        for tool_call in response.choices[0].message.tool_calls:
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            # Execute tool
            result = execute_tool(function_name, arguments)

            # Add tool result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Get next response
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

    return response.choices[0].message.content

def execute_tool(name: str, args: dict) -> dict:
    """Execute a tool by name with arguments."""
    tools_registry = {
        "get_employee_info": get_employee_info_impl,
        "search_federal_documents": search_documents_impl,
        "query_compliance_database": query_compliance_impl
    }

    if name not in tools_registry:
        return {"error": f"Unknown tool: {name}"}

    try:
        return tools_registry[name](**args)
    except Exception as e:
        return {"error": str(e)}
```

### Anthropic Tool Use

```python
import anthropic

client = anthropic.Anthropic()

def process_with_claude_tools(user_message: str, tools: list) -> str:
    """Process with Claude tool use."""

    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            tools=tools,
            messages=messages
        )

        # Check for tool use
        if response.stop_reason == "tool_use":
            # Process tool calls
            tool_results = []

            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })

            # Add assistant response and tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        else:
            # Final response
            for block in response.content:
                if hasattr(block, 'text'):
                    return block.text
            break

    return ""
```

### Parallel Tool Execution

```python
import asyncio
from typing import List, Dict

async def execute_tools_parallel(
    tool_calls: List[Dict]
) -> List[Dict]:
    """Execute multiple tools in parallel."""

    async def execute_single(call: Dict) -> Dict:
        name = call['name']
        args = call['arguments']

        # Async tool execution
        result = await async_execute_tool(name, args)

        return {
            "tool_call_id": call['id'],
            "result": result
        }

    # Run all tools concurrently
    results = await asyncio.gather(
        *[execute_single(call) for call in tool_calls],
        return_exceptions=True
    )

    # Handle any exceptions
    processed_results = []
    for result in results:
        if isinstance(result, Exception):
            processed_results.append({
                "error": str(result)
            })
        else:
            processed_results.append(result)

    return processed_results
```

---

## 13.4 Secure Tool Execution

### Permission Framework

```python
from enum import Enum
from typing import Set, Optional
from dataclasses import dataclass

class Permission(Enum):
    READ_PUBLIC = "read:public"
    READ_CUI = "read:cui"
    WRITE_PUBLIC = "write:public"
    WRITE_CUI = "write:cui"
    EXECUTE_SAFE = "execute:safe"
    EXECUTE_DANGEROUS = "execute:dangerous"
    ADMIN = "admin"

@dataclass
class ToolPermissions:
    """Permission requirements for a tool."""
    tool_name: str
    required_permissions: Set[Permission]
    requires_approval: bool = False
    audit_required: bool = True

class PermissionManager:
    """Manage tool permissions and access control."""

    def __init__(self):
        self.tool_permissions: Dict[str, ToolPermissions] = {}
        self.user_permissions: Dict[str, Set[Permission]] = {}

    def register_tool(
        self,
        name: str,
        permissions: Set[Permission],
        requires_approval: bool = False
    ):
        """Register a tool with its permission requirements."""
        self.tool_permissions[name] = ToolPermissions(
            tool_name=name,
            required_permissions=permissions,
            requires_approval=requires_approval
        )

    def check_permission(
        self,
        user_id: str,
        tool_name: str
    ) -> tuple[bool, Optional[str]]:
        """Check if user can execute tool."""
        if tool_name not in self.tool_permissions:
            return False, "Tool not registered"

        tool = self.tool_permissions[tool_name]
        user_perms = self.user_permissions.get(user_id, set())

        # Check if user has all required permissions
        missing = tool.required_permissions - user_perms
        if missing:
            return False, f"Missing permissions: {missing}"

        return True, None

# Usage
perm_manager = PermissionManager()

# Register tools with permissions
perm_manager.register_tool(
    "search_documents",
    {Permission.READ_PUBLIC},
    requires_approval=False
)

perm_manager.register_tool(
    "create_poam",
    {Permission.WRITE_CUI, Permission.EXECUTE_DANGEROUS},
    requires_approval=True
)
```

### Input Validation

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List
import re

class DocumentSearchInput(BaseModel):
    """Validated input for document search tool."""

    query: str = Field(..., min_length=1, max_length=500)
    document_type: str = Field(default="all")
    classification: str = Field(default="UNCLASSIFIED")
    max_results: int = Field(default=10, ge=1, le=100)

    @validator('query')
    def sanitize_query(cls, v):
        # Remove potential injection patterns
        v = re.sub(r'[;\'"\\]', '', v)
        return v.strip()

    @validator('document_type')
    def validate_doc_type(cls, v):
        allowed = ["policy", "memo", "report", "regulation", "all"]
        if v not in allowed:
            raise ValueError(f"Invalid document type. Must be one of: {allowed}")
        return v

    @validator('classification')
    def validate_classification(cls, v):
        allowed = ["UNCLASSIFIED", "CUI"]
        if v not in allowed:
            raise ValueError(f"Invalid classification. Must be one of: {allowed}")
        return v

class SecureToolExecutor:
    """Execute tools with security controls."""

    def __init__(self, perm_manager: PermissionManager):
        self.perm_manager = perm_manager
        self.validators = {
            "search_documents": DocumentSearchInput,
            # Add more validators
        }

    async def execute(
        self,
        tool_name: str,
        arguments: dict,
        user_id: str,
        context: dict
    ) -> dict:
        # 1. Check permissions
        allowed, reason = self.perm_manager.check_permission(user_id, tool_name)
        if not allowed:
            return {"error": f"Permission denied: {reason}"}

        # 2. Validate input
        if tool_name in self.validators:
            try:
                validated = self.validators[tool_name](**arguments)
                arguments = validated.dict()
            except Exception as e:
                return {"error": f"Invalid input: {str(e)}"}

        # 3. Check if approval needed
        tool_perms = self.perm_manager.tool_permissions.get(tool_name)
        if tool_perms and tool_perms.requires_approval:
            approval = await self._get_approval(tool_name, arguments, user_id)
            if not approval:
                return {"error": "Tool execution requires approval"}

        # 4. Execute with audit logging
        try:
            result = await self._execute_tool(tool_name, arguments)
            await self._audit_log(tool_name, arguments, result, user_id, "success")
            return result
        except Exception as e:
            await self._audit_log(tool_name, arguments, str(e), user_id, "error")
            return {"error": str(e)}
```

---

## 13.5 Error Handling

```python
from typing import Union
from enum import Enum

class ToolErrorType(Enum):
    VALIDATION_ERROR = "validation_error"
    PERMISSION_DENIED = "permission_denied"
    NOT_FOUND = "not_found"
    RATE_LIMITED = "rate_limited"
    TIMEOUT = "timeout"
    INTERNAL_ERROR = "internal_error"

class ToolError(Exception):
    """Custom exception for tool errors."""

    def __init__(
        self,
        error_type: ToolErrorType,
        message: str,
        details: dict = None,
        recoverable: bool = True
    ):
        self.error_type = error_type
        self.message = message
        self.details = details or {}
        self.recoverable = recoverable
        super().__init__(message)

    def to_dict(self) -> dict:
        return {
            "error_type": self.error_type.value,
            "message": self.message,
            "details": self.details,
            "recoverable": self.recoverable
        }

class RobustToolExecutor:
    """Tool executor with comprehensive error handling."""

    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    async def execute_with_retry(
        self,
        tool_name: str,
        arguments: dict
    ) -> Union[dict, ToolError]:
        """Execute tool with retry logic."""

        last_error = None

        for attempt in range(self.max_retries):
            try:
                result = await self._execute(tool_name, arguments)
                return result

            except ToolError as e:
                last_error = e

                if not e.recoverable:
                    # Don't retry non-recoverable errors
                    break

                if e.error_type == ToolErrorType.RATE_LIMITED:
                    # Exponential backoff
                    await asyncio.sleep(2 ** attempt)

                elif e.error_type == ToolErrorType.TIMEOUT:
                    # Increase timeout and retry
                    continue

                else:
                    break

            except Exception as e:
                last_error = ToolError(
                    ToolErrorType.INTERNAL_ERROR,
                    str(e),
                    recoverable=False
                )
                break

        return last_error

    def format_error_for_llm(self, error: ToolError) -> str:
        """Format error message for LLM to understand and handle."""

        error_messages = {
            ToolErrorType.VALIDATION_ERROR: f"Invalid input: {error.message}. Please check the parameters and try again.",
            ToolErrorType.PERMISSION_DENIED: f"Access denied: {error.message}. The user doesn't have permission for this operation.",
            ToolErrorType.NOT_FOUND: f"Not found: {error.message}. The requested resource doesn't exist.",
            ToolErrorType.RATE_LIMITED: "Rate limit exceeded. Please wait before trying again.",
            ToolErrorType.TIMEOUT: "Operation timed out. The service may be slow or unavailable.",
            ToolErrorType.INTERNAL_ERROR: f"Internal error: {error.message}. Please try a different approach."
        }

        return error_messages.get(
            error.error_type,
            f"Error: {error.message}"
        )
```

---

## 13.6 Federal Tool Examples

```python
# Example federal tools

def query_regulations(
    agency: str,
    cfr_title: int = None,
    keyword: str = None
) -> dict:
    """Query federal regulations from regulations.gov."""
    # Implementation would call regulations.gov API
    pass

def check_system_authorization(
    system_id: str,
    check_type: str = "ato_status"
) -> dict:
    """Check system authorization status in agency ATO database."""
    pass

def submit_security_finding(
    system_id: str,
    control_id: str,
    finding_type: str,
    description: str,
    severity: str
) -> dict:
    """Submit a security finding to the vulnerability management system."""
    pass

def query_nist_controls(
    control_id: str = None,
    family: str = None,
    baseline: str = "moderate"
) -> dict:
    """Query NIST 800-53 controls database."""
    pass

# Tool definitions for federal use
federal_tools = [
    {
        "type": "function",
        "function": {
            "name": "query_nist_controls",
            "description": "Query NIST 800-53 security controls. Use to look up control requirements, implementation guidance, and assessment procedures.",
            "parameters": {
                "type": "object",
                "properties": {
                    "control_id": {
                        "type": "string",
                        "description": "Specific control ID (e.g., 'AC-2', 'AU-6')"
                    },
                    "family": {
                        "type": "string",
                        "enum": ["AC", "AU", "AT", "CM", "CP", "IA", "IR", "MA", "MP", "PE", "PL", "PS", "RA", "SA", "SC", "SI"],
                        "description": "Control family code"
                    },
                    "baseline": {
                        "type": "string",
                        "enum": ["low", "moderate", "high"],
                        "default": "moderate",
                        "description": "Impact baseline"
                    }
                }
            }
        }
    }
]
```

---

## Hands-On Lab

### Lab 13.1: Build Federal Compliance Tool Suite

Create a tool suite for compliance workflows:
1. Design tools for querying compliance databases
2. Implement secure tool execution with permissions
3. Build error handling and retry logic
4. Create audit logging for all tool usage

---

## Knowledge Check

1. What makes a good tool description for LLM consumption?
2. How should sensitive operations be protected in tool execution?
3. What error information should be returned to the LLM?
4. How do you handle tool calls that require human approval?

---

<div align="center">

[← Module 12: Multi-Agent Systems](../12-multi-agent-systems/README.md) | [Home](../../README.md) | [Module 14: Memory & Context →](../14-memory-context/README.md)

</div>
