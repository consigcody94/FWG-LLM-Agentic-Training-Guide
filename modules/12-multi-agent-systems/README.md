<div align="center">

# Module 12: Multi-Agent Systems

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_8-green?style=for-the-badge" alt="Prerequisites"/>

*Orchestrating collaborative AI agents for complex federal workflows*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Design multi-agent architectures for complex tasks
- [ ] Implement agent communication patterns
- [ ] Build supervisor and hierarchical agent systems
- [ ] Handle agent coordination and conflict resolution
- [ ] Deploy production multi-agent systems

---

## 12.1 Multi-Agent Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                 MULTI-AGENT ARCHITECTURE PATTERNS                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PEER-TO-PEER              HIERARCHICAL           SUPERVISOR    │
│                                                                  │
│    ┌───┐   ┌───┐           ┌───────┐              ┌───────┐    │
│    │ A │◄─►│ B │           │Manager│              │ Super │    │
│    └─┬─┘   └─┬─┘           └───┬───┘              │ visor │    │
│      │       │                 │                  └───┬───┘    │
│      └───┬───┘            ┌────┴────┐            ┌────┴────┐   │
│          │                │         │            │         │   │
│       ┌──┴──┐          ┌──┴──┐   ┌──┴──┐     ┌──┴──┐   ┌──┴──┐│
│       │  C  │          │Team │   │Team │     │Agent│   │Agent││
│       └─────┘          │  A  │   │  B  │     │  1  │   │  2  ││
│                        └─────┘   └─────┘     └─────┘   └─────┘│
│                                                                  │
│  Use: Collaborative       Use: Complex         Use: Task        │
│       problem-solving          orgs            delegation       │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  PIPELINE                  VOTING/CONSENSUS      BLACKBOARD     │
│                                                                  │
│  ┌───┐   ┌───┐   ┌───┐    ┌───┐ ┌───┐ ┌───┐   ┌───────────┐   │
│  │ A │──►│ B │──►│ C │    │ A │ │ B │ │ C │   │ Blackboard│   │
│  └───┘   └───┘   └───┘    └─┬─┘ └─┬─┘ └─┬─┘   │  (Shared) │   │
│                             │     │     │      └─────┬─────┘   │
│                             └─────┼─────┘            │          │
│                                   ▼              ┌───┴───┐      │
│                              ┌────────┐          │Agents │      │
│                              │Consensus│         │R/W    │      │
│                              └────────┘          └───────┘      │
│                                                                  │
│  Use: Sequential           Use: High-stakes    Use: Complex     │
│       processing                decisions           state       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Pattern Selection Guide

| Pattern | Best For | Complexity | Coordination |
|---------|----------|------------|--------------|
| **Peer-to-Peer** | Collaborative tasks | Low | Direct messaging |
| **Hierarchical** | Large organizations | High | Chain of command |
| **Supervisor** | Task delegation | Medium | Central control |
| **Pipeline** | Sequential workflows | Low | Pass-through |
| **Voting** | Critical decisions | Medium | Aggregation |
| **Blackboard** | Complex state | High | Shared memory |

---

## 12.2 Supervisor Pattern Implementation

```python
from typing import List, Dict, Any, Literal
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage
import operator
from typing import Annotated, TypedDict

# Define state
class SupervisorState(TypedDict):
    messages: Annotated[List, operator.add]
    next_agent: str
    task_complete: bool
    results: Dict[str, Any]

# Define agents
class ResearchAgent:
    """Agent specialized in research tasks."""

    def __init__(self, llm):
        self.llm = llm

    async def execute(self, state: SupervisorState) -> Dict:
        task = state['messages'][-1].content

        response = await self.llm.ainvoke([
            {"role": "system", "content": "You are a research specialist. Find relevant information for the task."},
            {"role": "user", "content": task}
        ])

        return {
            "messages": [AIMessage(content=response.content, name="researcher")],
            "results": {"research": response.content}
        }

class AnalysisAgent:
    """Agent specialized in analysis."""

    def __init__(self, llm):
        self.llm = llm

    async def execute(self, state: SupervisorState) -> Dict:
        research = state['results'].get('research', '')

        response = await self.llm.ainvoke([
            {"role": "system", "content": "You are an analyst. Analyze the research findings."},
            {"role": "user", "content": f"Analyze this research:\n{research}"}
        ])

        return {
            "messages": [AIMessage(content=response.content, name="analyst")],
            "results": {"analysis": response.content}
        }

class WriterAgent:
    """Agent specialized in writing reports."""

    def __init__(self, llm):
        self.llm = llm

    async def execute(self, state: SupervisorState) -> Dict:
        analysis = state['results'].get('analysis', '')

        response = await self.llm.ainvoke([
            {"role": "system", "content": "You are a technical writer. Create a clear report."},
            {"role": "user", "content": f"Write a report based on:\n{analysis}"}
        ])

        return {
            "messages": [AIMessage(content=response.content, name="writer")],
            "results": {"report": response.content},
            "task_complete": True
        }

# Supervisor logic
class Supervisor:
    """Orchestrates agent execution."""

    def __init__(self, llm, agents: List[str]):
        self.llm = llm
        self.agents = agents

    async def route(self, state: SupervisorState) -> Dict:
        """Determine next agent to execute."""
        if state.get('task_complete'):
            return {"next_agent": "end"}

        # Use LLM to decide routing
        messages = state['messages']
        results = state.get('results', {})

        prompt = f"""Based on the task and current progress, decide which agent should work next.

Task: {messages[0].content if messages else 'Unknown'}

Completed work:
{list(results.keys())}

Available agents: {self.agents}

Which agent should work next? Reply with just the agent name or 'done' if complete."""

        response = await self.llm.ainvoke([
            {"role": "user", "content": prompt}
        ])

        next_agent = response.content.strip().lower()

        if next_agent == 'done' or 'writer' in results:
            return {"next_agent": "end", "task_complete": True}

        return {"next_agent": next_agent}

# Build graph
def build_supervisor_graph(llm):
    # Initialize agents
    researcher = ResearchAgent(llm)
    analyst = AnalysisAgent(llm)
    writer = WriterAgent(llm)
    supervisor = Supervisor(llm, ["researcher", "analyst", "writer"])

    # Create graph
    workflow = StateGraph(SupervisorState)

    # Add nodes
    workflow.add_node("supervisor", supervisor.route)
    workflow.add_node("researcher", researcher.execute)
    workflow.add_node("analyst", analyst.execute)
    workflow.add_node("writer", writer.execute)

    # Add edges
    workflow.set_entry_point("supervisor")

    # Conditional routing from supervisor
    workflow.add_conditional_edges(
        "supervisor",
        lambda x: x["next_agent"],
        {
            "researcher": "researcher",
            "analyst": "analyst",
            "writer": "writer",
            "end": END
        }
    )

    # All agents return to supervisor
    for agent in ["researcher", "analyst", "writer"]:
        workflow.add_edge(agent, "supervisor")

    return workflow.compile()

# Usage
async def run_multi_agent_task(task: str):
    graph = build_supervisor_graph(llm)

    result = await graph.ainvoke({
        "messages": [HumanMessage(content=task)],
        "next_agent": "",
        "task_complete": False,
        "results": {}
    })

    return result
```

---

## 12.3 Hierarchical Teams

```python
from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class AgentRole(Enum):
    MANAGER = "manager"
    LEAD = "lead"
    WORKER = "worker"

@dataclass
class Agent:
    name: str
    role: AgentRole
    specialty: str
    llm: Any
    subordinates: List['Agent'] = None

    def __post_init__(self):
        if self.subordinates is None:
            self.subordinates = []

class HierarchicalTeam:
    """Hierarchical multi-agent team structure."""

    def __init__(self):
        self.org_chart = {}

    def build_federal_compliance_team(self, llm) -> Agent:
        """Build a federal compliance review team."""

        # Worker agents
        security_analyst = Agent(
            name="security_analyst",
            role=AgentRole.WORKER,
            specialty="NIST 800-53 controls analysis",
            llm=llm
        )

        privacy_analyst = Agent(
            name="privacy_analyst",
            role=AgentRole.WORKER,
            specialty="Privacy impact assessment",
            llm=llm
        )

        policy_analyst = Agent(
            name="policy_analyst",
            role=AgentRole.WORKER,
            specialty="Federal policy interpretation",
            llm=llm
        )

        technical_writer = Agent(
            name="technical_writer",
            role=AgentRole.WORKER,
            specialty="Compliance documentation",
            llm=llm
        )

        # Team leads
        security_lead = Agent(
            name="security_lead",
            role=AgentRole.LEAD,
            specialty="Security assessment coordination",
            llm=llm,
            subordinates=[security_analyst]
        )

        compliance_lead = Agent(
            name="compliance_lead",
            role=AgentRole.LEAD,
            specialty="Compliance review coordination",
            llm=llm,
            subordinates=[privacy_analyst, policy_analyst]
        )

        documentation_lead = Agent(
            name="documentation_lead",
            role=AgentRole.LEAD,
            specialty="Documentation management",
            llm=llm,
            subordinates=[technical_writer]
        )

        # Manager
        program_manager = Agent(
            name="program_manager",
            role=AgentRole.MANAGER,
            specialty="ATO program management",
            llm=llm,
            subordinates=[security_lead, compliance_lead, documentation_lead]
        )

        return program_manager

    async def delegate_task(
        self,
        manager: Agent,
        task: str,
        context: Dict
    ) -> Dict:
        """Delegate task through hierarchy."""

        # Manager analyzes task
        analysis = await self._analyze_task(manager, task)

        # Identify required specialists
        assignments = await self._assign_to_leads(
            manager,
            analysis,
            context
        )

        # Leads delegate to workers
        results = {}
        for lead, subtask in assignments.items():
            lead_result = await self._execute_with_team(
                lead,
                subtask,
                context
            )
            results[lead.name] = lead_result

        # Manager synthesizes results
        final = await self._synthesize_results(
            manager,
            task,
            results
        )

        return final

    async def _analyze_task(self, manager: Agent, task: str) -> Dict:
        """Manager analyzes and decomposes task."""
        prompt = f"""As a {manager.specialty}, analyze this task and break it down:

Task: {task}

Identify:
1. Security analysis requirements
2. Compliance review requirements
3. Documentation requirements

Provide a structured breakdown."""

        response = await manager.llm.ainvoke([
            {"role": "user", "content": prompt}
        ])

        return {"breakdown": response.content}

    async def _execute_with_team(
        self,
        lead: Agent,
        task: str,
        context: Dict
    ) -> Dict:
        """Lead coordinates worker execution."""
        worker_results = []

        for worker in lead.subordinates:
            result = await self._worker_execute(worker, task, context)
            worker_results.append({
                "worker": worker.name,
                "result": result
            })

        # Lead reviews and consolidates
        consolidated = await self._lead_review(lead, worker_results)

        return consolidated
```

---

## 12.4 Agent Communication

### Message Protocol

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional
from enum import Enum
import uuid

class MessageType(Enum):
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"
    ACK = "acknowledgment"
    ERROR = "error"

@dataclass
class AgentMessage:
    """Standard message format for agent communication."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType = MessageType.REQUEST
    sender: str = ""
    recipient: str = ""
    content: Any = None
    metadata: Dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    reply_to: Optional[str] = None
    priority: int = 5  # 1-10, lower is higher priority

class MessageBroker:
    """Central message broker for agent communication."""

    def __init__(self):
        self.queues: Dict[str, List[AgentMessage]] = {}
        self.subscribers: Dict[str, List[str]] = {}
        self.message_history: List[AgentMessage] = []

    def register_agent(self, agent_id: str):
        """Register an agent with the broker."""
        self.queues[agent_id] = []

    def send(self, message: AgentMessage):
        """Send a message to an agent."""
        self.message_history.append(message)

        if message.type == MessageType.BROADCAST:
            # Send to all agents
            for queue in self.queues.values():
                queue.append(message)
        else:
            # Send to specific recipient
            if message.recipient in self.queues:
                self.queues[message.recipient].append(message)

    def receive(self, agent_id: str) -> Optional[AgentMessage]:
        """Receive next message for an agent."""
        if agent_id in self.queues and self.queues[agent_id]:
            # Sort by priority
            self.queues[agent_id].sort(key=lambda m: m.priority)
            return self.queues[agent_id].pop(0)
        return None

    def subscribe(self, agent_id: str, topic: str):
        """Subscribe agent to a topic."""
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        self.subscribers[topic].append(agent_id)

    def publish(self, topic: str, message: AgentMessage):
        """Publish message to topic subscribers."""
        if topic in self.subscribers:
            for agent_id in self.subscribers[topic]:
                self.queues[agent_id].append(message)
```

### Conversation Patterns

```python
class ConversationManager:
    """Manage multi-agent conversations."""

    def __init__(self, broker: MessageBroker):
        self.broker = broker
        self.conversations: Dict[str, List[AgentMessage]] = {}

    async def request_response(
        self,
        sender: str,
        recipient: str,
        content: Any,
        timeout: float = 30.0
    ) -> AgentMessage:
        """Simple request-response pattern."""
        request = AgentMessage(
            type=MessageType.REQUEST,
            sender=sender,
            recipient=recipient,
            content=content
        )

        self.broker.send(request)

        # Wait for response
        start = datetime.utcnow()
        while (datetime.utcnow() - start).total_seconds() < timeout:
            response = self.broker.receive(sender)
            if response and response.reply_to == request.id:
                return response
            await asyncio.sleep(0.1)

        raise TimeoutError("No response received")

    async def gather_responses(
        self,
        sender: str,
        recipients: List[str],
        content: Any,
        timeout: float = 60.0
    ) -> List[AgentMessage]:
        """Gather responses from multiple agents."""
        requests = []

        # Send requests to all recipients
        for recipient in recipients:
            request = AgentMessage(
                type=MessageType.REQUEST,
                sender=sender,
                recipient=recipient,
                content=content
            )
            self.broker.send(request)
            requests.append(request)

        # Collect responses
        responses = []
        request_ids = {r.id for r in requests}
        start = datetime.utcnow()

        while len(responses) < len(recipients):
            if (datetime.utcnow() - start).total_seconds() > timeout:
                break

            response = self.broker.receive(sender)
            if response and response.reply_to in request_ids:
                responses.append(response)

            await asyncio.sleep(0.1)

        return responses

    async def consensus_vote(
        self,
        agents: List[str],
        proposal: Any,
        threshold: float = 0.66
    ) -> Tuple[bool, Dict]:
        """Conduct a consensus vote among agents."""
        responses = await self.gather_responses(
            sender="coordinator",
            recipients=agents,
            content={
                "type": "vote_request",
                "proposal": proposal
            }
        )

        votes = {}
        for response in responses:
            votes[response.sender] = response.content.get('vote', False)

        approve_count = sum(1 for v in votes.values() if v)
        approval_rate = approve_count / len(agents)

        return approval_rate >= threshold, votes
```

---

## 12.5 Conflict Resolution

```python
class ConflictResolver:
    """Resolve conflicts between agent outputs."""

    def __init__(self, llm):
        self.llm = llm

    async def resolve_by_voting(
        self,
        outputs: List[Dict],
        weights: Optional[Dict[str, float]] = None
    ) -> Dict:
        """Resolve by weighted voting."""
        if not outputs:
            return {}

        # Score each unique output
        scores = {}
        for output in outputs:
            key = str(output['content'])
            agent = output['agent']
            weight = weights.get(agent, 1.0) if weights else 1.0

            if key not in scores:
                scores[key] = {'content': output['content'], 'score': 0}
            scores[key]['score'] += weight

        # Return highest scored
        winner = max(scores.values(), key=lambda x: x['score'])
        return winner['content']

    async def resolve_by_synthesis(
        self,
        outputs: List[Dict],
        task_context: str
    ) -> str:
        """Use LLM to synthesize conflicting outputs."""
        outputs_text = "\n\n".join([
            f"Agent {o['agent']}:\n{o['content']}"
            for o in outputs
        ])

        prompt = f"""Multiple agents have provided different outputs for the same task.
Synthesize these into a single, coherent response.

Task: {task_context}

Agent Outputs:
{outputs_text}

Synthesized Response:"""

        response = await self.llm.ainvoke([
            {"role": "user", "content": prompt}
        ])

        return response.content

    async def resolve_by_authority(
        self,
        outputs: List[Dict],
        authority_ranking: List[str]
    ) -> Dict:
        """Defer to highest authority agent."""
        for authority in authority_ranking:
            for output in outputs:
                if output['agent'] == authority:
                    return output['content']

        # Fallback to first output
        return outputs[0]['content'] if outputs else {}

    async def detect_conflicts(
        self,
        outputs: List[Dict]
    ) -> List[Dict]:
        """Detect conflicts between agent outputs."""
        conflicts = []

        for i, output1 in enumerate(outputs):
            for output2 in outputs[i+1:]:
                similarity = self._calculate_similarity(
                    output1['content'],
                    output2['content']
                )

                if similarity < 0.7:  # Threshold for conflict
                    conflicts.append({
                        'agents': [output1['agent'], output2['agent']],
                        'similarity': similarity,
                        'outputs': [output1['content'], output2['content']]
                    })

        return conflicts
```

---

## 12.6 Federal Compliance Workflow

```python
class FederalComplianceWorkflow:
    """Multi-agent workflow for federal compliance review."""

    def __init__(self, llm):
        self.llm = llm
        self.broker = MessageBroker()
        self.agents = self._initialize_agents()

    def _initialize_agents(self) -> Dict:
        """Initialize specialized compliance agents."""
        return {
            'intake': IntakeAgent(self.llm),
            'fisma': FISMAAgent(self.llm),
            'fedramp': FedRAMPAgent(self.llm),
            'privacy': PrivacyAgent(self.llm),
            'reviewer': HumanReviewAgent()
        }

    async def process_system_package(
        self,
        system_info: Dict
    ) -> Dict:
        """Process a system authorization package."""

        # Phase 1: Intake and categorization
        categorization = await self.agents['intake'].categorize(system_info)

        # Phase 2: Parallel compliance checks
        checks = await asyncio.gather(
            self.agents['fisma'].assess(system_info, categorization),
            self.agents['fedramp'].assess(system_info, categorization),
            self.agents['privacy'].assess(system_info, categorization)
        )

        # Phase 3: Conflict resolution
        resolver = ConflictResolver(self.llm)
        conflicts = await resolver.detect_conflicts([
            {'agent': 'fisma', 'content': checks[0]},
            {'agent': 'fedramp', 'content': checks[1]},
            {'agent': 'privacy', 'content': checks[2]}
        ])

        if conflicts:
            # Resolve conflicts
            resolved = await resolver.resolve_by_synthesis(
                [{'agent': name, 'content': check}
                 for name, check in zip(['fisma', 'fedramp', 'privacy'], checks)],
                f"Compliance assessment for {system_info['name']}"
            )
        else:
            resolved = self._merge_assessments(checks)

        # Phase 4: Human review for critical decisions
        if self._requires_human_review(resolved):
            resolved = await self.agents['reviewer'].review(resolved)

        # Phase 5: Generate final report
        report = await self._generate_report(system_info, resolved)

        return {
            'system': system_info['name'],
            'categorization': categorization,
            'assessments': checks,
            'conflicts_resolved': len(conflicts),
            'report': report
        }
```

---

## Hands-On Lab

### Lab 12.1: Build Federal Review Team

Create a multi-agent system for security authorization:
1. Implement supervisor pattern with specialized agents
2. Add human-in-the-loop for critical decisions
3. Handle conflicts between agent assessments
4. Generate consolidated compliance reports

---

## Knowledge Check

1. When should you use hierarchical vs peer-to-peer agent patterns?
2. How do you handle conflicting outputs from multiple agents?
3. What role does human-in-the-loop play in federal multi-agent systems?
4. How should agent communication be audited?

---

<div align="center">

[← Module 11: Fine-Tuning](../11-fine-tuning/README.md) | [Home](../../README.md) | [Module 13: Tool Use →](../13-tool-use-functions/README.md)

</div>
