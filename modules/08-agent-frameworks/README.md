<div align="center">

# Module 08: Agent Frameworks

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--7-green?style=for-the-badge" alt="Prerequisites"/>

*Building intelligent agents with LangChain, LangGraph, CrewAI, and AutoGen*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand agent architectures and reasoning patterns
- [ ] Build agents using LangChain and LangGraph
- [ ] Implement multi-agent workflows with CrewAI
- [ ] Design autonomous systems with AutoGen
- [ ] Select appropriate frameworks for federal use cases

---

## Module Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    AGENT FRAMEWORK LANDSCAPE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│    ┌──────────────┐     ┌──────────────┐     ┌──────────────┐  │
│    │  LangChain   │     │  LangGraph   │     │   CrewAI     │  │
│    │              │     │              │     │              │  │
│    │  - Chains    │     │  - Graphs    │     │  - Crews     │  │
│    │  - Agents    │     │  - States    │     │  - Agents    │  │
│    │  - Tools     │     │  - Edges     │     │  - Tasks     │  │
│    │  - Memory    │     │  - Cycles    │     │  - Roles     │  │
│    └──────┬───────┘     └──────┬───────┘     └──────┬───────┘  │
│           │                    │                    │           │
│           └────────────────────┴────────────────────┘           │
│                              │                                   │
│                    ┌─────────▼─────────┐                        │
│                    │     AutoGen       │                        │
│                    │                   │                        │
│                    │  - Conversations  │                        │
│                    │  - Multi-Agent    │                        │
│                    │  - Human-in-Loop  │                        │
│                    └───────────────────┘                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8.1 Agent Architecture Fundamentals

### What is an Agent?

An agent is an LLM-powered system that can:
1. **Perceive** - Take in inputs from environment
2. **Reason** - Process information and plan actions
3. **Act** - Execute actions using tools
4. **Learn** - Adapt behavior based on feedback

```
┌─────────────────────────────────────────────────────────────────┐
│                      AGENT ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│      ┌─────────────┐                                            │
│      │   INPUT     │                                            │
│      │  (Query)    │                                            │
│      └──────┬──────┘                                            │
│             │                                                    │
│             ▼                                                    │
│      ┌─────────────────────────────────────────────┐            │
│      │              AGENT CORE                      │            │
│      │  ┌─────────────────────────────────────┐    │            │
│      │  │           LLM (Brain)               │    │            │
│      │  │  • Reasoning                        │    │            │
│      │  │  • Planning                         │    │            │
│      │  │  • Decision Making                  │    │            │
│      │  └─────────────────────────────────────┘    │            │
│      │                    │                         │            │
│      │     ┌──────────────┼──────────────┐         │            │
│      │     ▼              ▼              ▼         │            │
│      │  ┌──────┐    ┌──────────┐    ┌───────┐     │            │
│      │  │Memory│    │  Tools   │    │Prompts│     │            │
│      │  └──────┘    └──────────┘    └───────┘     │            │
│      └─────────────────────────────────────────────┘            │
│             │                                                    │
│             ▼                                                    │
│      ┌─────────────┐                                            │
│      │   OUTPUT    │                                            │
│      │ (Response)  │                                            │
│      └─────────────┘                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Reasoning Patterns

| Pattern | Description | Best For |
|---------|-------------|----------|
| **ReAct** | Reasoning + Acting interleaved | General tasks with tool use |
| **Plan-and-Execute** | Plan first, then execute | Complex multi-step tasks |
| **Reflection** | Self-critique and improvement | Quality-critical tasks |
| **Tree of Thought** | Explore multiple reasoning paths | Problem-solving |

---

## 8.2 LangChain Framework

### Installation

```bash
pip install langchain langchain-openai langchain-anthropic langchain-community
```

### Basic Agent Structure

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain import hub

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Define tools
tools = [
    Tool(
        name="Calculator",
        func=lambda x: eval(x),
        description="Useful for math calculations"
    ),
    Tool(
        name="Search",
        func=lambda x: search_function(x),
        description="Search for current information"
    )
]

# Get prompt template
prompt = hub.pull("hwchase17/react")

# Create agent
agent = create_react_agent(llm, tools, prompt)

# Create executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=10,
    early_stopping_method="generate"
)

# Run agent
result = agent_executor.invoke({
    "input": "What is 25% of the current US population?"
})
```

### Custom Tool Creation

```python
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

class DocumentSearchInput(BaseModel):
    """Input schema for document search."""
    query: str = Field(description="Search query")
    classification: str = Field(
        description="Document classification level",
        default="UNCLASSIFIED"
    )

class FederalDocumentSearch(BaseTool):
    """Search federal documents with classification awareness."""

    name: str = "federal_document_search"
    description: str = """
    Search federal documents. Requires query and classification level.
    Classification levels: UNCLASSIFIED, CUI, CONFIDENTIAL, SECRET
    """
    args_schema: Type[BaseModel] = DocumentSearchInput

    def _run(
        self,
        query: str,
        classification: str = "UNCLASSIFIED"
    ) -> str:
        # Validate user clearance (mock)
        if not self._check_clearance(classification):
            return "Access denied: Insufficient clearance"

        # Search documents
        results = self._search_documents(query, classification)
        return results

    def _check_clearance(self, level: str) -> bool:
        # Implement actual clearance check
        return level in ["UNCLASSIFIED", "CUI"]

    def _search_documents(self, query: str, level: str) -> str:
        # Implement actual search
        return f"Results for '{query}' at {level} level"
```

### Memory Systems

```python
from langchain.memory import (
    ConversationBufferMemory,
    ConversationSummaryMemory,
    ConversationBufferWindowMemory,
    VectorStoreRetrieverMemory
)
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# Simple buffer memory
buffer_memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Window memory (last k interactions)
window_memory = ConversationBufferWindowMemory(
    k=5,
    memory_key="chat_history",
    return_messages=True
)

# Summary memory (compress old conversations)
summary_memory = ConversationSummaryMemory(
    llm=llm,
    memory_key="chat_history",
    return_messages=True
)

# Vector store memory (semantic retrieval)
embeddings = OpenAIEmbeddings()
vectorstore = Chroma(embedding_function=embeddings)

retriever_memory = VectorStoreRetrieverMemory(
    retriever=vectorstore.as_retriever(search_kwargs={"k": 5}),
    memory_key="relevant_history"
)
```

---

## 8.3 LangGraph for Stateful Agents

### Graph-Based Agent Architecture

```python
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from typing import TypedDict, Annotated, Sequence
from langchain_core.messages import BaseMessage
import operator

# Define state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], operator.add]
    next_action: str

# Create graph
workflow = StateGraph(AgentState)

# Define nodes
def agent_node(state: AgentState):
    """Main agent reasoning node."""
    messages = state["messages"]

    # Get LLM response
    response = llm.invoke(messages)

    # Determine next action
    if should_use_tool(response):
        return {
            "messages": [response],
            "next_action": "tools"
        }
    return {
        "messages": [response],
        "next_action": "end"
    }

def tool_node(state: AgentState):
    """Execute tool based on agent decision."""
    last_message = state["messages"][-1]

    # Parse tool call
    tool_call = parse_tool_call(last_message)

    # Execute tool
    result = tool_executor.invoke(tool_call)

    return {
        "messages": [ToolMessage(content=result)],
        "next_action": "agent"
    }

# Add nodes
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)

# Add edges
workflow.set_entry_point("agent")

workflow.add_conditional_edges(
    "agent",
    lambda x: x["next_action"],
    {
        "tools": "tools",
        "end": END
    }
)

workflow.add_edge("tools", "agent")

# Compile
app = workflow.compile()

# Run
result = app.invoke({
    "messages": [HumanMessage(content="Search for NIST guidelines")]
})
```

### Cyclic Workflows

```
┌─────────────────────────────────────────────────────────────────┐
│                    LANGGRAPH WORKFLOW                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                     ┌──────────────┐                            │
│                     │    START     │                            │
│                     └──────┬───────┘                            │
│                            │                                     │
│                            ▼                                     │
│                     ┌──────────────┐                            │
│              ┌──────│    AGENT     │◄─────────┐                 │
│              │      └──────┬───────┘          │                 │
│              │             │                   │                 │
│              │      ┌──────┴──────┐           │                 │
│              │      │  Decision   │           │                 │
│              │      └──────┬──────┘           │                 │
│              │             │                   │                 │
│              │    ┌────────┴────────┐         │                 │
│              │    │                  │         │                 │
│              ▼    ▼                  ▼         │                 │
│        ┌──────────┐           ┌──────────┐    │                 │
│        │  TOOLS   │           │   END    │    │                 │
│        └────┬─────┘           └──────────┘    │                 │
│             │                                  │                 │
│             └──────────────────────────────────┘                │
│                      (Loop back)                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Human-in-the-Loop

```python
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import StateGraph

# Add checkpointing for human intervention
memory = SqliteSaver.from_conn_string(":memory:")

def human_review_node(state: AgentState):
    """Pause for human review."""
    return {
        "messages": state["messages"],
        "requires_approval": True
    }

# Build graph with review step
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("human_review", human_review_node)
workflow.add_node("execute", execute_node)

# Add conditional edge for sensitive actions
workflow.add_conditional_edges(
    "agent",
    lambda x: "review" if x.get("sensitive") else "execute",
    {
        "review": "human_review",
        "execute": "execute"
    }
)

# Compile with checkpointing
app = workflow.compile(checkpointer=memory, interrupt_before=["human_review"])

# Run until human review needed
config = {"configurable": {"thread_id": "1"}}
for event in app.stream({"messages": [user_input]}, config):
    if event.get("requires_approval"):
        # Get human approval
        approval = get_human_approval()
        if approval:
            # Continue execution
            app.update_state(config, {"approved": True})
```

---

## 8.4 CrewAI Multi-Agent Framework

### Installation

```bash
pip install crewai crewai-tools
```

### Defining Agents and Tasks

```python
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Initialize LLM
llm = ChatOpenAI(model="gpt-4", temperature=0.7)

# Define specialized agents
security_analyst = Agent(
    role="Security Analyst",
    goal="Analyze documents for security implications and compliance issues",
    backstory="""You are an experienced federal security analyst
    with expertise in FISMA, FedRAMP, and NIST frameworks. You
    identify potential security risks and compliance gaps.""",
    llm=llm,
    verbose=True,
    allow_delegation=True
)

policy_researcher = Agent(
    role="Policy Researcher",
    goal="Research and summarize relevant federal policies and regulations",
    backstory="""You are a policy expert with deep knowledge of
    federal regulations, OMB memoranda, and agency guidelines.
    You provide accurate policy context.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

report_writer = Agent(
    role="Report Writer",
    goal="Synthesize findings into clear, actionable reports",
    backstory="""You are a technical writer specialized in federal
    documentation. You create clear, compliant reports that meet
    federal writing standards.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Define tasks
security_review_task = Task(
    description="""
    Review the provided system documentation and identify:
    1. Security control gaps
    2. Compliance issues with NIST 800-53
    3. Risk areas requiring attention

    System: {system_name}
    Documentation: {documentation}
    """,
    agent=security_analyst,
    expected_output="Security findings with severity ratings"
)

policy_research_task = Task(
    description="""
    Research applicable federal policies for:
    1. The system type identified
    2. The data classification level
    3. Any recent policy updates

    Context from security review: {security_findings}
    """,
    agent=policy_researcher,
    expected_output="Relevant policy citations and requirements"
)

report_task = Task(
    description="""
    Create a comprehensive compliance report including:
    1. Executive summary
    2. Security findings
    3. Policy requirements
    4. Recommendations
    5. Remediation timeline

    Security Findings: {security_findings}
    Policy Context: {policy_research}
    """,
    agent=report_writer,
    expected_output="Formatted compliance report"
)

# Create crew
compliance_crew = Crew(
    agents=[security_analyst, policy_researcher, report_writer],
    tasks=[security_review_task, policy_research_task, report_task],
    process=Process.sequential,  # or Process.hierarchical
    verbose=True
)

# Run crew
result = compliance_crew.kickoff(inputs={
    "system_name": "Federal Case Management System",
    "documentation": document_content
})
```

### Hierarchical Process

```python
from crewai import Crew, Process

# Manager agent oversees other agents
manager = Agent(
    role="Project Manager",
    goal="Coordinate team efforts and ensure quality deliverables",
    backstory="Senior project manager with federal experience",
    llm=llm,
    allow_delegation=True
)

# Hierarchical crew
hierarchical_crew = Crew(
    agents=[manager, security_analyst, policy_researcher, report_writer],
    tasks=[complex_task],
    process=Process.hierarchical,
    manager_agent=manager,
    verbose=True
)
```

---

## 8.5 AutoGen Conversational Agents

### Installation

```bash
pip install pyautogen
```

### Two-Agent Conversation

```python
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Configure LLM
config_list = [
    {
        "model": "gpt-4",
        "api_key": os.environ["OPENAI_API_KEY"]
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0
}

# Create assistant agent
assistant = AssistantAgent(
    name="Federal_Analyst",
    system_message="""You are a federal systems analyst.
    You help analyze IT systems for compliance and security.
    You provide detailed, actionable recommendations.""",
    llm_config=llm_config
)

# Create user proxy (can execute code)
user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="TERMINATE",  # NEVER, ALWAYS, TERMINATE
    max_consecutive_auto_reply=10,
    code_execution_config={
        "work_dir": "workspace",
        "use_docker": False  # Set True for sandboxed execution
    }
)

# Start conversation
user_proxy.initiate_chat(
    assistant,
    message="Analyze this system architecture for FedRAMP compliance"
)
```

### Group Chat

```python
from autogen import GroupChat, GroupChatManager

# Create multiple specialized agents
security_agent = AssistantAgent(
    name="Security_Expert",
    system_message="You are a cybersecurity expert...",
    llm_config=llm_config
)

compliance_agent = AssistantAgent(
    name="Compliance_Expert",
    system_message="You are a federal compliance expert...",
    llm_config=llm_config
)

architect_agent = AssistantAgent(
    name="Solution_Architect",
    system_message="You are a cloud solution architect...",
    llm_config=llm_config
)

# Create group chat
group_chat = GroupChat(
    agents=[user_proxy, security_agent, compliance_agent, architect_agent],
    messages=[],
    max_round=20
)

# Create manager
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

# Start group discussion
user_proxy.initiate_chat(
    manager,
    message="Design a FedRAMP High compliant architecture for our agency"
)
```

---

## 8.6 Framework Comparison

| Feature | LangChain | LangGraph | CrewAI | AutoGen |
|---------|-----------|-----------|--------|---------|
| **Architecture** | Chain-based | Graph-based | Role-based | Conversation-based |
| **State Management** | Memory classes | Explicit state | Task context | Chat history |
| **Multi-Agent** | Limited | Native | Native | Native |
| **Human-in-Loop** | Custom | Built-in | Limited | Built-in |
| **Code Execution** | Via tools | Via tools | Limited | Native sandbox |
| **Complexity** | Medium | High | Low | Medium |
| **Federal Suitability** | High | High | Medium | Medium |

### When to Use Each

```
┌─────────────────────────────────────────────────────────────────┐
│                  FRAMEWORK SELECTION GUIDE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  USE CASE                          RECOMMENDED FRAMEWORK         │
│  ─────────────────────────────────────────────────────────      │
│                                                                  │
│  Simple tool-using agent          → LangChain                   │
│                                                                  │
│  Complex workflows with cycles    → LangGraph                   │
│                                                                  │
│  Role-based collaboration         → CrewAI                      │
│                                                                  │
│  Conversational multi-agent       → AutoGen                     │
│                                                                  │
│  Federal compliance workflows     → LangGraph + Human-in-Loop   │
│                                                                  │
│  Research/Analysis teams          → CrewAI                      │
│                                                                  │
│  Code generation/execution        → AutoGen                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 8.7 Federal Implementation Patterns

### Audit-Compliant Agent

```python
import logging
from datetime import datetime
import json

class AuditedAgent:
    """Agent wrapper with comprehensive audit logging."""

    def __init__(self, agent, audit_logger):
        self.agent = agent
        self.audit_logger = audit_logger

    def invoke(self, input_data: dict, user_context: dict) -> dict:
        # Generate trace ID
        trace_id = str(uuid.uuid4())

        # Log invocation start
        self.audit_logger.log({
            "event": "agent_invocation_start",
            "trace_id": trace_id,
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_context.get("user_id"),
            "clearance": user_context.get("clearance"),
            "input_hash": self._hash_input(input_data)
        })

        try:
            # Execute agent
            result = self.agent.invoke(input_data)

            # Log success
            self.audit_logger.log({
                "event": "agent_invocation_complete",
                "trace_id": trace_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "success",
                "tools_used": self._extract_tools(result),
                "output_hash": self._hash_input(result)
            })

            return result

        except Exception as e:
            # Log failure
            self.audit_logger.log({
                "event": "agent_invocation_error",
                "trace_id": trace_id,
                "timestamp": datetime.utcnow().isoformat(),
                "status": "error",
                "error_type": type(e).__name__,
                "error_message": str(e)
            })
            raise
```

### Clearance-Aware Tool Access

```python
from enum import Enum
from typing import List

class ClearanceLevel(Enum):
    UNCLASSIFIED = 0
    CUI = 1
    CONFIDENTIAL = 2
    SECRET = 3
    TOP_SECRET = 4

class ClearanceAwareToolkit:
    """Toolkit that filters tools based on user clearance."""

    def __init__(self, tools: List[Tool]):
        self.tools = tools

    def get_tools_for_user(self, user_clearance: ClearanceLevel) -> List[Tool]:
        """Return only tools the user has clearance to use."""
        return [
            tool for tool in self.tools
            if self._check_tool_access(tool, user_clearance)
        ]

    def _check_tool_access(
        self,
        tool: Tool,
        clearance: ClearanceLevel
    ) -> bool:
        tool_level = getattr(tool, 'required_clearance', ClearanceLevel.UNCLASSIFIED)
        return clearance.value >= tool_level.value
```

---

## Hands-On Lab

### Lab 8.1: Build a Federal Research Agent

Create a multi-tool agent that can:
1. Search federal regulations
2. Query agency databases
3. Generate compliance reports

**Requirements:**
- Use LangGraph for workflow control
- Implement human approval for sensitive operations
- Add comprehensive audit logging
- Handle CUI appropriately

**Starter Code:** See `labs/08-agent-frameworks/federal-research-agent/`

---

## Knowledge Check

1. What distinguishes LangGraph from LangChain for agent development?
2. How does CrewAI's role-based approach benefit federal workflows?
3. What are the key considerations for human-in-the-loop in federal agents?
4. How should tool access be controlled based on user clearance?

---

## Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- NIST SP 800-53 AI Controls Mapping

---

<div align="center">

[← Module 07: A2A Protocol](../07-a2a-protocol/README.md) | [Home](../../README.md) | [Module 09: Coding Assistants →](../09-coding-assistants/README.md)

</div>
