<div align="center">

# Module 07: Agent-to-Agent (A2A) Protocol

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_06-orange?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Explain the A2A protocol architecture and its purpose
- [ ] Create Agent Cards that describe agent capabilities
- [ ] Implement A2A-compliant servers using JSON-RPC
- [ ] Design task state machines for complex workflows
- [ ] Configure multi-agent routing and orchestration
- [ ] Build production-ready A2A deployments for federal use

---

## Table of Contents

1. [What is A2A?](#1-what-is-a2a)
2. [Agent Cards](#2-agent-cards)
3. [JSON-RPC Transport](#3-json-rpc-transport)
4. [Task State Machine](#4-task-state-machine)
5. [SSE Streaming](#5-sse-streaming)
6. [Discovery Mechanisms](#6-discovery-mechanisms)
7. [Multi-Agent Routing](#7-multi-agent-routing)
8. [Federal Implementation Patterns](#8-federal-implementation-patterns)

---

## 1. What is A2A?

### Overview

The Agent-to-Agent (A2A) Protocol is an open standard that enables AI agents to discover, communicate, and collaborate with each other in a standardized way.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      AGENT-TO-AGENT (A2A) PROTOCOL                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PURPOSE: Enable AI agents to discover and collaborate without              ║
║           tight coupling or proprietary integrations                         ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                      A2A ECOSYSTEM                                     │ ║
║  │                                                                         │ ║
║  │    ┌─────────────┐       ┌─────────────┐       ┌─────────────┐        │ ║
║  │    │   Agent A   │◀─────▶│   Agent B   │◀─────▶│   Agent C   │        │ ║
║  │    │             │       │             │       │             │        │ ║
║  │    │ • Research  │       │ • Analysis  │       │ • Reporting │        │ ║
║  │    │ • Discovery │       │ • Synthesis │       │ • Delivery  │        │ ║
║  │    └─────────────┘       └─────────────┘       └─────────────┘        │ ║
║  │           │                     │                     │                │ ║
║  │           └─────────────────────┼─────────────────────┘                │ ║
║  │                                 │                                       │ ║
║  │                                 ▼                                       │ ║
║  │                    ┌───────────────────────┐                           │ ║
║  │                    │    A2A Protocol       │                           │ ║
║  │                    │                       │                           │ ║
║  │                    │  • Agent Cards        │                           │ ║
║  │                    │  • JSON-RPC 2.0       │                           │ ║
║  │                    │  • Task State Machine │                           │ ║
║  │                    │  • SSE Streaming      │                           │ ║
║  │                    └───────────────────────┘                           │ ║
║  │                                                                         │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  KEY BENEFITS:                                                               ║
║  ✅ Interoperability - Agents from different vendors can collaborate        ║
║  ✅ Discovery - Agents can find and understand each other's capabilities    ║
║  ✅ Standardization - Common task lifecycle and communication patterns      ║
║  ✅ Streaming - Real-time progress updates via SSE                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### A2A vs MCP Comparison

| Aspect | A2A Protocol | MCP |
|:-------|:-------------|:----|
| **Primary Purpose** | Agent-to-Agent communication | LLM-to-Data/Tools |
| **Participants** | AI Agents (peers) | Host + Server |
| **Discovery** | Agent Cards | Configuration |
| **Task Model** | State machine lifecycle | Request/Response |
| **Streaming** | SSE built-in | Optional |
| **Use Case** | Multi-agent orchestration | Context augmentation |

### Core Concepts

| Concept | Description |
|:--------|:------------|
| **Agent** | An AI-powered service with defined capabilities |
| **Agent Card** | JSON metadata describing agent capabilities |
| **Task** | Unit of work with lifecycle (submitted → completed) |
| **Message** | Communication payload between agents |
| **Skill** | A specific capability an agent can perform |
| **Artifact** | Output produced by task execution |

---

## 2. Agent Cards

### Agent Card Structure

```json
{
  "name": "Federal Compliance Agent",
  "description": "Specialized agent for federal regulatory compliance analysis",
  "url": "https://compliance.agency.gov/a2a",
  "version": "1.0.0",
  "protocolVersion": "0.3.0",

  "capabilities": {
    "streaming": true,
    "pushNotifications": false,
    "stateTransitionHistory": true
  },

  "skills": [
    {
      "id": "compliance-assessment",
      "name": "Compliance Assessment",
      "description": "Evaluate systems against NIST, FedRAMP, and FISMA requirements",
      "tags": ["compliance", "security", "assessment", "federal"],
      "examples": [
        "Assess this system against FedRAMP Moderate baseline",
        "Identify gaps in NIST 800-53 control implementation",
        "Generate a compliance report for FISMA audit"
      ]
    },
    {
      "id": "policy-analysis",
      "name": "Policy Analysis",
      "description": "Analyze federal policies, regulations, and guidance documents",
      "tags": ["policy", "analysis", "regulations"],
      "examples": [
        "Summarize the key requirements of EO 14110",
        "Compare FAR and DFARS procurement requirements"
      ]
    },
    {
      "id": "documentation-generation",
      "name": "Documentation Generation",
      "description": "Generate compliance documentation artifacts",
      "tags": ["documentation", "SSP", "POAM", "templates"],
      "examples": [
        "Generate SSP section for AC-2 control",
        "Create POA&M entry for identified vulnerability"
      ]
    }
  ],

  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],

  "authentication": {
    "schemes": ["oauth2", "apiKey"],
    "credentials": null
  },

  "provider": {
    "organization": "Federal Agency",
    "url": "https://agency.gov"
  }
}
```

### Agent Card Location

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      AGENT CARD DISCOVERY                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Standard Location: /.well-known/agent.json                                  ║
║                                                                              ║
║  Example:                                                                    ║
║  https://compliance.agency.gov/.well-known/agent.json                       ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                                                                         │ ║
║  │  GET /.well-known/agent.json HTTP/1.1                                  │ ║
║  │  Host: compliance.agency.gov                                           │ ║
║  │                                                                         │ ║
║  │  HTTP/1.1 200 OK                                                       │ ║
║  │  Content-Type: application/json                                        │ ║
║  │                                                                         │ ║
║  │  {                                                                      │ ║
║  │    "name": "Federal Compliance Agent",                                 │ ║
║  │    "url": "https://compliance.agency.gov/a2a",                         │ ║
║  │    "skills": [...]                                                     │ ║
║  │  }                                                                      │ ║
║  │                                                                         │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Skill Definition Best Practices

```python
# Define skills with clear, actionable descriptions
skills = [
    {
        "id": "vulnerability-scan",
        "name": "Vulnerability Scanning",
        "description": """
        Perform automated vulnerability scanning and analysis.

        Input requirements:
        - Target system identifier or IP range
        - Scan type (full, quick, compliance-focused)
        - Output format preference

        Output includes:
        - Vulnerability list with CVE references
        - Risk ratings (CVSS scores)
        - Remediation recommendations
        """,
        "tags": ["security", "vulnerability", "scanning", "risk"],
        "examples": [
            "Scan the production servers for critical vulnerabilities",
            "Run a compliance-focused scan against STIG requirements",
            "Generate vulnerability report for quarterly review"
        ],
        # Input/output mode constraints
        "inputModes": ["text", "file"],
        "outputModes": ["text", "file", "data"]
    }
]
```

---

## 3. JSON-RPC Transport

### Message Format

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      A2A JSON-RPC MESSAGE FORMAT                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  REQUEST                                                                     ║
║  ────────────────────────────────────────────────────────────────────────   ║
║  {                                                                           ║
║    "jsonrpc": "2.0",                                                        ║
║    "id": "unique-request-id",                                               ║
║    "method": "message/send",                                                ║
║    "params": {                                                              ║
║      "message": {                                                           ║
║        "role": "user",                                                      ║
║        "parts": [                                                           ║
║          {                                                                  ║
║            "type": "text",                                                  ║
║            "text": "Analyze system X for FedRAMP compliance"               ║
║          }                                                                  ║
║        ]                                                                    ║
║      }                                                                      ║
║    }                                                                        ║
║  }                                                                           ║
║                                                                              ║
║  RESPONSE (Success)                                                          ║
║  ────────────────────────────────────────────────────────────────────────   ║
║  {                                                                           ║
║    "jsonrpc": "2.0",                                                        ║
║    "id": "unique-request-id",                                               ║
║    "result": {                                                              ║
║      "task": {                                                              ║
║        "id": "task-12345",                                                  ║
║        "state": "completed",                                                ║
║        "artifacts": [                                                       ║
║          {                                                                  ║
║            "type": "text",                                                  ║
║            "text": "Analysis complete. 15 controls assessed..."            ║
║          }                                                                  ║
║        ]                                                                    ║
║      }                                                                      ║
║    }                                                                        ║
║  }                                                                           ║
║                                                                              ║
║  RESPONSE (Error)                                                            ║
║  ────────────────────────────────────────────────────────────────────────   ║
║  {                                                                           ║
║    "jsonrpc": "2.0",                                                        ║
║    "id": "unique-request-id",                                               ║
║    "error": {                                                               ║
║      "code": -32600,                                                        ║
║      "message": "Invalid request",                                          ║
║      "data": { "details": "Missing required parameter" }                    ║
║    }                                                                        ║
║  }                                                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Supported Methods

| Method | Description | Response Type |
|:-------|:------------|:--------------|
| `message/send` | Send message, wait for complete response | Task with artifacts |
| `message/stream` | Send message, stream response events | SSE stream |
| `tasks/get` | Get task status by ID | Task object |
| `tasks/cancel` | Cancel a running task | Cancellation result |
| `tasks/pushNotification/set` | Configure push notifications | Confirmation |

### Server Implementation (Python)

```python
# a2a_server.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import asyncio
import uuid
import json

app = FastAPI()

# Task storage
tasks: Dict[str, Dict] = {}

# ============================================
# Agent Card Endpoint
# ============================================

@app.get("/.well-known/agent.json")
async def get_agent_card():
    return {
        "name": "Federal Analysis Agent",
        "description": "Performs federal compliance and policy analysis",
        "url": "http://localhost:8000/a2a",
        "version": "1.0.0",
        "protocolVersion": "0.3.0",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True
        },
        "skills": [
            {
                "id": "compliance-check",
                "name": "Compliance Check",
                "description": "Check systems against federal compliance frameworks",
                "tags": ["compliance", "federal", "security"],
                "examples": ["Check FedRAMP compliance for System X"]
            }
        ],
        "provider": {
            "organization": "Federal Agency"
        }
    }

# ============================================
# JSON-RPC Endpoint
# ============================================

class JsonRpcRequest(BaseModel):
    jsonrpc: str = "2.0"
    id: str
    method: str
    params: Optional[Dict[str, Any]] = None

@app.post("/a2a")
async def handle_jsonrpc(request: JsonRpcRequest):
    """Handle JSON-RPC 2.0 requests."""

    if request.method == "message/send":
        return await handle_message_send(request)

    elif request.method == "tasks/get":
        return await handle_task_get(request)

    elif request.method == "tasks/cancel":
        return await handle_task_cancel(request)

    else:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32601,
                "message": f"Method not found: {request.method}"
            }
        }

async def handle_message_send(request: JsonRpcRequest):
    """Process a message and return task result."""

    # Extract message from params
    message = request.params.get("message", {})
    message_parts = message.get("parts", [])

    # Get text content
    text_content = ""
    for part in message_parts:
        if part.get("type") == "text":
            text_content += part.get("text", "")

    # Create task
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "id": task_id,
        "state": "submitted",
        "input": text_content,
        "artifacts": [],
        "history": [
            {"state": "submitted", "timestamp": get_timestamp()}
        ]
    }

    # Process task (in real implementation, this would be async)
    try:
        tasks[task_id]["state"] = "working"
        tasks[task_id]["history"].append({
            "state": "working",
            "timestamp": get_timestamp()
        })

        # Execute task logic
        result = await process_compliance_request(text_content)

        # Complete task
        tasks[task_id]["state"] = "completed"
        tasks[task_id]["artifacts"] = [
            {"type": "text", "text": result}
        ]
        tasks[task_id]["history"].append({
            "state": "completed",
            "timestamp": get_timestamp()
        })

    except Exception as e:
        tasks[task_id]["state"] = "failed"
        tasks[task_id]["error"] = str(e)
        tasks[task_id]["history"].append({
            "state": "failed",
            "timestamp": get_timestamp()
        })

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {
            "task": tasks[task_id]
        }
    }

async def handle_task_get(request: JsonRpcRequest):
    """Get task by ID."""
    task_id = request.params.get("taskId")

    if task_id not in tasks:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": f"Task not found: {task_id}"
            }
        }

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {
            "task": tasks[task_id]
        }
    }

async def handle_task_cancel(request: JsonRpcRequest):
    """Cancel a running task."""
    task_id = request.params.get("taskId")

    if task_id not in tasks:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": f"Task not found: {task_id}"
            }
        }

    task = tasks[task_id]
    if task["state"] in ["completed", "failed", "canceled"]:
        return {
            "jsonrpc": "2.0",
            "id": request.id,
            "error": {
                "code": -32000,
                "message": f"Cannot cancel task in state: {task['state']}"
            }
        }

    task["state"] = "canceled"
    task["history"].append({
        "state": "canceled",
        "timestamp": get_timestamp()
    })

    return {
        "jsonrpc": "2.0",
        "id": request.id,
        "result": {
            "task": task
        }
    }

# ============================================
# Streaming Endpoint
# ============================================

@app.post("/a2a/stream")
async def handle_stream(request: JsonRpcRequest):
    """Handle streaming requests with SSE."""

    async def generate_events():
        task_id = str(uuid.uuid4())

        # Send task created event
        yield f"event: task_created\ndata: {json.dumps({'taskId': task_id})}\n\n"

        # Send progress events
        for i in range(5):
            await asyncio.sleep(0.5)
            yield f"event: progress\ndata: {json.dumps({'progress': (i+1)*20})}\n\n"

        # Send completion
        result = {
            "taskId": task_id,
            "state": "completed",
            "artifacts": [
                {"type": "text", "text": "Analysis complete"}
            ]
        }
        yield f"event: task_completed\ndata: {json.dumps(result)}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive"
        }
    )

# ============================================
# Helper Functions
# ============================================

async def process_compliance_request(text: str) -> str:
    """Process a compliance analysis request."""
    # Simulate processing
    await asyncio.sleep(1)

    return f"""
## Compliance Analysis Results

**Input:** {text[:100]}...

### Findings:
1. Control AC-2 (Account Management): Partially Implemented
2. Control AU-3 (Audit Content): Fully Implemented
3. Control SC-7 (Boundary Protection): Needs Attention

### Recommendations:
- Implement automated account review process
- Enable additional audit event categories
- Review firewall rule sets quarterly

**Overall Status:** 78% Compliant
"""

def get_timestamp():
    from datetime import datetime
    return datetime.utcnow().isoformat() + "Z"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 4. Task State Machine

### State Diagram

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          A2A TASK STATE MACHINE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                              ┌─────────────┐                                 ║
║                              │   START     │                                 ║
║                              └──────┬──────┘                                 ║
║                                     │                                        ║
║                                     ▼                                        ║
║                             ┌──────────────┐                                 ║
║                             │  SUBMITTED   │                                 ║
║                             └──────┬───────┘                                 ║
║                                    │                                         ║
║              ┌─────────────────────┼─────────────────────┐                  ║
║              │                     │                     │                  ║
║              ▼                     ▼                     ▼                  ║
║       ┌──────────┐          ┌──────────┐          ┌──────────┐             ║
║       │ CANCELED │          │  WORKING │          │  FAILED  │             ║
║       └──────────┘          └────┬─────┘          └──────────┘             ║
║                                  │                      ▲                   ║
║              ┌───────────────────┼──────────────────────┤                   ║
║              │                   │                      │                   ║
║              ▼                   ▼                      │                   ║
║       ┌──────────┐     ┌────────────────┐              │                   ║
║       │ CANCELED │     │INPUT_REQUIRED  │──────────────┘                   ║
║       └──────────┘     └───────┬────────┘                                   ║
║                                │                                            ║
║                                │ User provides input                        ║
║                                ▼                                            ║
║                         ┌──────────┐                                        ║
║                         │  WORKING │                                        ║
║                         └────┬─────┘                                        ║
║                              │                                              ║
║              ┌───────────────┼───────────────┐                              ║
║              │               │               │                              ║
║              ▼               ▼               ▼                              ║
║       ┌──────────┐    ┌──────────┐    ┌──────────┐                         ║
║       │ CANCELED │    │COMPLETED │    │  FAILED  │                         ║
║       └──────────┘    └──────────┘    └──────────┘                         ║
║                              │                                              ║
║                              ▼                                              ║
║                        ┌──────────┐                                         ║
║                        │   END    │                                         ║
║                        └──────────┘                                         ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### State Definitions

| State | Description | Valid Transitions |
|:------|:------------|:------------------|
| `submitted` | Task received, not yet started | working, canceled, failed |
| `working` | Task actively processing | completed, failed, canceled, input_required |
| `input_required` | Task needs additional user input | working, canceled |
| `completed` | Task finished successfully | (terminal) |
| `failed` | Task encountered error | (terminal) |
| `canceled` | Task was canceled | (terminal) |

### State Transition Implementation

```python
from enum import Enum
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime

class TaskState(Enum):
    SUBMITTED = "submitted"
    WORKING = "working"
    INPUT_REQUIRED = "input_required"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"

# Valid state transitions
VALID_TRANSITIONS = {
    TaskState.SUBMITTED: [TaskState.WORKING, TaskState.CANCELED, TaskState.FAILED],
    TaskState.WORKING: [TaskState.COMPLETED, TaskState.FAILED, TaskState.CANCELED, TaskState.INPUT_REQUIRED],
    TaskState.INPUT_REQUIRED: [TaskState.WORKING, TaskState.CANCELED],
    TaskState.COMPLETED: [],  # Terminal state
    TaskState.FAILED: [],      # Terminal state
    TaskState.CANCELED: [],    # Terminal state
}

@dataclass
class StateTransition:
    from_state: TaskState
    to_state: TaskState
    timestamp: datetime
    reason: Optional[str] = None

@dataclass
class Task:
    id: str
    state: TaskState = TaskState.SUBMITTED
    artifacts: List[dict] = field(default_factory=list)
    history: List[StateTransition] = field(default_factory=list)
    error: Optional[str] = None

    def __post_init__(self):
        # Record initial state
        self.history.append(StateTransition(
            from_state=None,
            to_state=TaskState.SUBMITTED,
            timestamp=datetime.utcnow()
        ))

    def transition_to(self, new_state: TaskState, reason: Optional[str] = None):
        """Transition to a new state with validation."""
        if new_state not in VALID_TRANSITIONS.get(self.state, []):
            raise InvalidStateTransition(
                f"Cannot transition from {self.state.value} to {new_state.value}"
            )

        self.history.append(StateTransition(
            from_state=self.state,
            to_state=new_state,
            timestamp=datetime.utcnow(),
            reason=reason
        ))
        self.state = new_state

    def is_terminal(self) -> bool:
        """Check if task is in a terminal state."""
        return self.state in [
            TaskState.COMPLETED,
            TaskState.FAILED,
            TaskState.CANCELED
        ]

class InvalidStateTransition(Exception):
    pass
```

---

## 5. SSE Streaming

### SSE Event Format

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          SSE STREAMING FORMAT                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Server-Sent Events (SSE) provide real-time updates during task execution   ║
║                                                                              ║
║  EVENT TYPES:                                                                ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  1. task_created                                                             ║
║     event: task_created                                                      ║
║     data: {"taskId": "abc-123", "state": "submitted"}                       ║
║                                                                              ║
║  2. task_state_changed                                                       ║
║     event: task_state_changed                                                ║
║     data: {"taskId": "abc-123", "state": "working", "progress": 25}         ║
║                                                                              ║
║  3. artifact_created                                                         ║
║     event: artifact_created                                                  ║
║     data: {"taskId": "abc-123", "artifact": {"type": "text", "text": "..."}}║
║                                                                              ║
║  4. task_completed                                                           ║
║     event: task_completed                                                    ║
║     data: {"taskId": "abc-123", "state": "completed", "artifacts": [...]}   ║
║                                                                              ║
║  5. task_failed                                                              ║
║     event: task_failed                                                       ║
║     data: {"taskId": "abc-123", "state": "failed", "error": "..."}          ║
║                                                                              ║
║  6. message                                                                  ║
║     event: message                                                           ║
║     data: {"role": "assistant", "parts": [{"type": "text", "text": "..."}]} ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Client-Side SSE Handling

```python
import httpx
import json

async def stream_task(url: str, message: str):
    """Stream task execution with SSE."""

    request_body = {
        "jsonrpc": "2.0",
        "id": "stream-1",
        "method": "message/stream",
        "params": {
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": message}]
            }
        }
    }

    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            f"{url}/a2a/stream",
            json=request_body,
            headers={"Accept": "text/event-stream"}
        ) as response:

            async for line in response.aiter_lines():
                if line.startswith("event:"):
                    event_type = line[6:].strip()
                elif line.startswith("data:"):
                    data = json.loads(line[5:])
                    yield event_type, data
                elif line == "":
                    # End of event
                    pass

# Usage
async def main():
    async for event_type, data in stream_task(
        "http://localhost:8000",
        "Analyze system compliance"
    ):
        if event_type == "task_created":
            print(f"Task started: {data['taskId']}")
        elif event_type == "task_state_changed":
            print(f"Progress: {data.get('progress', 0)}%")
        elif event_type == "artifact_created":
            print(f"Artifact: {data['artifact']['text'][:100]}...")
        elif event_type == "task_completed":
            print(f"Completed: {data['artifacts']}")
```

---

## 6. Discovery Mechanisms

### Registry-Based Discovery

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       AGENT DISCOVERY PATTERNS                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PATTERN 1: DIRECT URL DISCOVERY                                            ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  Client knows agent URL → Fetches /.well-known/agent.json                   ║
║                                                                              ║
║  ┌─────────┐     GET /.well-known/agent.json      ┌─────────┐              ║
║  │ Client  │ ────────────────────────────────────▶│ Agent   │              ║
║  └─────────┘     ◀──────────────────────────────── └─────────┘              ║
║                        Agent Card JSON                                       ║
║                                                                              ║
║  PATTERN 2: REGISTRY DISCOVERY                                              ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  Centralized registry maintains catalog of available agents                 ║
║                                                                              ║
║  ┌─────────┐  1. Query agents     ┌──────────┐                             ║
║  │ Client  │ ───────────────────▶ │ Registry │                             ║
║  └─────────┘                      └──────────┘                             ║
║       │         2. Return list           │                                  ║
║       │    ◀────────────────────────────┘                                  ║
║       │                                                                      ║
║       │    3. Connect to agent                                              ║
║       ▼         ┌─────────┐                                                 ║
║  ┌─────────┐   │ Agent A │                                                 ║
║  │  Agent  │◀──┤ Agent B │                                                 ║
║  │ Cards   │   │ Agent C │                                                 ║
║  └─────────┘   └─────────┘                                                 ║
║                                                                              ║
║  PATTERN 3: DNS-BASED DISCOVERY                                             ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  _a2a._tcp.agency.gov SRV record → Agent endpoint                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Agent Catalog Implementation

```python
from typing import List, Optional, Dict
from dataclasses import dataclass
import httpx
import asyncio

@dataclass
class AgentInfo:
    name: str
    url: str
    skills: List[str]
    tags: List[str]
    card: dict

class AgentCatalog:
    """Maintain a catalog of available A2A agents."""

    def __init__(self):
        self.agents: Dict[str, AgentInfo] = {}

    async def register(self, agent_url: str) -> AgentInfo:
        """Register an agent by fetching its card."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{agent_url}/.well-known/agent.json"
            )
            response.raise_for_status()
            card = response.json()

        agent = AgentInfo(
            name=card["name"],
            url=card["url"],
            skills=[s["id"] for s in card.get("skills", [])],
            tags=self._extract_tags(card.get("skills", [])),
            card=card
        )

        self.agents[agent.url] = agent
        return agent

    def find_by_skill(self, skill_id: str) -> List[AgentInfo]:
        """Find agents with a specific skill."""
        return [
            agent for agent in self.agents.values()
            if skill_id in agent.skills
        ]

    def find_by_tag(self, tag: str) -> List[AgentInfo]:
        """Find agents by tag."""
        return [
            agent for agent in self.agents.values()
            if tag.lower() in [t.lower() for t in agent.tags]
        ]

    def _extract_tags(self, skills: List[dict]) -> List[str]:
        """Extract all unique tags from skills."""
        tags = set()
        for skill in skills:
            tags.update(skill.get("tags", []))
        return list(tags)

# Usage
catalog = AgentCatalog()

async def setup_catalog():
    # Register known agents
    await catalog.register("http://compliance.agency.gov")
    await catalog.register("http://analysis.agency.gov")
    await catalog.register("http://reporting.agency.gov")

    # Find agents for compliance tasks
    compliance_agents = catalog.find_by_tag("compliance")
    print(f"Found {len(compliance_agents)} compliance agents")
```

---

## 7. Multi-Agent Routing

### Routing Strategies

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      MULTI-AGENT ROUTING STRATEGIES                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  STRATEGY 1: SKILL-BASED ROUTING                                            ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  Route tasks to agents based on skill match                                  ║
║                                                                              ║
║       Task: "Analyze compliance"                                             ║
║              │                                                               ║
║              ▼                                                               ║
║       ┌────────────┐                                                        ║
║       │   Router   │ ─── Match skill: "compliance-analysis"                 ║
║       └────────────┘                                                        ║
║              │                                                               ║
║              ▼                                                               ║
║       ┌────────────┐                                                        ║
║       │ Compliance │ ─── Agent with matching skill                          ║
║       │   Agent    │                                                        ║
║       └────────────┘                                                        ║
║                                                                              ║
║  STRATEGY 2: LOAD-BALANCED ROUTING                                          ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  Distribute tasks across equivalent agents                                   ║
║                                                                              ║
║       Task                                                                   ║
║        │                                                                     ║
║        ▼                                                                     ║
║  ┌────────────┐     ┌─────────┐  ┌─────────┐  ┌─────────┐                  ║
║  │   Router   │────▶│Agent 1  │  │Agent 2  │  │Agent 3  │                  ║
║  │ (Round-    │     │ (busy)  │  │(selected)│ │(healthy)│                  ║
║  │  Robin)    │     └─────────┘  └─────────┘  └─────────┘                  ║
║  └────────────┘                       ▲                                     ║
║                                       │                                     ║
║                               Least loaded agent                            ║
║                                                                              ║
║  STRATEGY 3: CAPABILITY-SCORED ROUTING                                      ║
║  ────────────────────────────────────────────────────────────────────────   ║
║                                                                              ║
║  Score agents by capability match, select highest scorer                    ║
║                                                                              ║
║       Task: "Generate SSP for FedRAMP High"                                 ║
║              │                                                               ║
║              ▼                                                               ║
║       ┌────────────┐                                                        ║
║       │   Scorer   │                                                        ║
║       └────────────┘                                                        ║
║              │                                                               ║
║       ┌──────┴──────────────────┐                                          ║
║       │                         │                                          ║
║       ▼                         ▼                                          ║
║  Agent A: 0.85            Agent B: 0.92  ← Selected                        ║
║  (SSP, FedRAMP-Mod)       (SSP, FedRAMP-High)                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Router Implementation

```python
from abc import ABC, abstractmethod
from typing import List, Optional
import random

class Router(ABC):
    """Base class for agent routing strategies."""

    @abstractmethod
    async def select_agent(
        self,
        task: str,
        agents: List[AgentInfo]
    ) -> Optional[AgentInfo]:
        pass

class SkillBasedRouter(Router):
    """Route based on skill matching."""

    async def select_agent(
        self,
        task: str,
        agents: List[AgentInfo]
    ) -> Optional[AgentInfo]:
        # Extract required skill from task (simplified)
        required_skill = self._extract_skill(task)

        # Find agents with matching skill
        matching = [
            agent for agent in agents
            if required_skill in agent.skills
        ]

        if not matching:
            return None

        # Return first match (or could score them)
        return matching[0]

    def _extract_skill(self, task: str) -> str:
        # Simple keyword matching (real impl would use NLP)
        if "compliance" in task.lower():
            return "compliance-assessment"
        elif "document" in task.lower():
            return "documentation-generation"
        return "general"

class LoadBalancedRouter(Router):
    """Route based on agent load."""

    def __init__(self):
        self.call_counts: Dict[str, int] = {}

    async def select_agent(
        self,
        task: str,
        agents: List[AgentInfo]
    ) -> Optional[AgentInfo]:
        if not agents:
            return None

        # Initialize counts
        for agent in agents:
            if agent.url not in self.call_counts:
                self.call_counts[agent.url] = 0

        # Select least loaded
        sorted_agents = sorted(
            agents,
            key=lambda a: self.call_counts[a.url]
        )

        selected = sorted_agents[0]
        self.call_counts[selected.url] += 1
        return selected

class ScoringRouter(Router):
    """Route based on capability scoring."""

    async def select_agent(
        self,
        task: str,
        agents: List[AgentInfo]
    ) -> Optional[AgentInfo]:
        if not agents:
            return None

        scores = []
        for agent in agents:
            score = self._score_agent(task, agent)
            scores.append((agent, score))

        # Sort by score descending
        scores.sort(key=lambda x: x[1], reverse=True)

        return scores[0][0] if scores[0][1] > 0 else None

    def _score_agent(self, task: str, agent: AgentInfo) -> float:
        """Score an agent's suitability for a task."""
        score = 0.0
        task_lower = task.lower()

        # Score based on tag matches
        for tag in agent.tags:
            if tag.lower() in task_lower:
                score += 0.2

        # Score based on skill descriptions
        for skill in agent.card.get("skills", []):
            description = skill.get("description", "").lower()
            # Simple word overlap scoring
            task_words = set(task_lower.split())
            desc_words = set(description.split())
            overlap = len(task_words & desc_words)
            score += overlap * 0.05

        return min(score, 1.0)
```

---

## 8. Federal Implementation Patterns

### Secure Federal A2A Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FEDERAL A2A DEPLOYMENT ARCHITECTURE                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                     AGENCY BOUNDARY                                    │ ║
║  │                                                                         │ ║
║  │  ┌──────────────┐                    ┌──────────────────────────────┐  │ ║
║  │  │   WAF/CDN    │                    │    AGENT GATEWAY             │  │ ║
║  │  │              │                    │                               │  │ ║
║  │  │ • DDoS prot. │                    │ • Authentication             │  │ ║
║  │  │ • TLS term.  │───────────────────▶│ • Authorization              │  │ ║
║  │  │ • Rate limit │                    │ • Audit logging              │  │ ║
║  │  └──────────────┘                    │ • Request validation         │  │ ║
║  │                                      └──────────────────────────────┘  │ ║
║  │                                                   │                     │ ║
║  │                          ┌────────────────────────┼────────────────┐   │ ║
║  │                          │                        │                │   │ ║
║  │                          ▼                        ▼                ▼   │ ║
║  │                   ┌────────────┐          ┌────────────┐   ┌──────────┐│ ║
║  │                   │ Compliance │          │ Analysis   │   │ Report   ││ ║
║  │                   │   Agent    │          │   Agent    │   │  Agent   ││ ║
║  │                   │            │          │            │   │          ││ ║
║  │                   │ FedRAMP    │          │ Policy     │   │ Document ││ ║
║  │                   │ FISMA      │          │ Regulation │   │ Generate ││ ║
║  │                   │ NIST       │          │ Analysis   │   │          ││ ║
║  │                   └────────────┘          └────────────┘   └──────────┘│ ║
║  │                          │                        │                │   │ ║
║  │                          └────────────────────────┼────────────────┘   │ ║
║  │                                                   │                     │ ║
║  │                                                   ▼                     │ ║
║  │                                      ┌──────────────────────┐          │ ║
║  │                                      │   SHARED SERVICES    │          │ ║
║  │                                      │                       │          │ ║
║  │                                      │ • Ollama (Local LLM) │          │ ║
║  │                                      │ • Vector Database    │          │ ║
║  │                                      │ • Document Store     │          │ ║
║  │                                      │ • Audit Database     │          │ ║
║  │                                      └──────────────────────┘          │ ║
║  │                                                                         │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Authentication & Authorization

```python
# Federal A2A authentication middleware
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from typing import Optional

security = HTTPBearer()

class FederalAuthMiddleware:
    """Authenticate and authorize A2A requests."""

    def __init__(
        self,
        jwt_secret: str,
        required_scopes: List[str] = None
    ):
        self.jwt_secret = jwt_secret
        self.required_scopes = required_scopes or []

    async def __call__(
        self,
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(security)
    ):
        try:
            # Verify JWT token
            payload = jwt.decode(
                credentials.credentials,
                self.jwt_secret,
                algorithms=["HS256"]
            )

            # Check required scopes
            token_scopes = payload.get("scopes", [])
            for scope in self.required_scopes:
                if scope not in token_scopes:
                    raise HTTPException(
                        status_code=403,
                        detail=f"Missing required scope: {scope}"
                    )

            # Add user context to request
            request.state.user_id = payload.get("sub")
            request.state.scopes = token_scopes
            request.state.clearance = payload.get("clearance", "UNCLASSIFIED")

        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")

# Usage
@app.post("/a2a")
async def handle_request(
    request: Request,
    auth: dict = Depends(FederalAuthMiddleware(
        jwt_secret=JWT_SECRET,
        required_scopes=["a2a:access"]
    ))
):
    # Request is authenticated and authorized
    pass
```

---

## Exercises

### Exercise 7.1: Agent Card Creation
Design and implement an Agent Card for a federal use case.

### Exercise 7.2: A2A Server
Build a complete A2A server with task management and streaming support.

### Exercise 7.3: Multi-Agent Routing
Implement a router that selects agents based on task requirements.

### Exercise 7.4: Secure Deployment
Deploy an A2A agent with authentication, authorization, and audit logging.

---

## Assessment

### Knowledge Check

1. What are the core components of the A2A protocol?
2. Explain the task state machine and valid state transitions.
3. How does SSE streaming work in A2A?
4. Compare skill-based and load-balanced routing strategies.
5. What security measures are essential for federal A2A deployments?

### Practical Assessment

Build a multi-agent system with:
- At least 2 specialized agents with Agent Cards
- A router that selects agents based on task type
- SSE streaming for real-time updates
- Authentication and audit logging

---

## Next Module

➡️ [Module 08: Agent Frameworks](../08-agent-frameworks/README.md)

---

<div align="center">

[⬆ Back to Top](#module-07-agent-to-agent-a2a-protocol) · [📚 Return to Curriculum](../../README.md)

</div>
