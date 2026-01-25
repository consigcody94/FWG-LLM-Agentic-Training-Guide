"""
Multi-Agent Orchestration Patterns - Reference Implementation

This module provides production-ready patterns for orchestrating
multiple AI agents, including hierarchical, consensus, pipeline,
debate, and swarm patterns.

Part of Module 28: Antigravity - Advanced Agent Techniques
"""

from typing import Any, Callable, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from enum import Enum
import asyncio
import uuid
import json


class MessageType(Enum):
    """Types of messages between agents."""
    TASK = "task"
    RESULT = "result"
    QUERY = "query"
    RESPONSE = "response"
    VOTE = "vote"
    DEBATE = "debate"
    SHUTDOWN = "shutdown"


class AgentRole(Enum):
    """Common agent roles in orchestration patterns."""
    COORDINATOR = "coordinator"
    WORKER = "worker"
    VALIDATOR = "validator"
    SYNTHESIZER = "synthesizer"
    CRITIC = "critic"
    ADVOCATE = "advocate"


@dataclass
class AgentMessage:
    """Message passed between agents."""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    recipient: str = ""
    content: Any = None
    message_type: MessageType = MessageType.TASK
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "sender": self.sender,
            "recipient": self.recipient,
            "content": self.content,
            "message_type": self.message_type.value,
            "metadata": self.metadata,
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class AgentResult:
    """Result from an agent's processing."""
    agent_id: str
    content: Any
    confidence: float = 1.0
    reasoning: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Abstract base class for all agents.

    Provides common functionality for message passing,
    task processing, and lifecycle management.
    """

    def __init__(
        self,
        name: str,
        role: AgentRole = AgentRole.WORKER,
        process_fn: Callable = None
    ):
        self.name = name
        self.role = role
        self.process_fn = process_fn
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.results: List[AgentResult] = []
        self.is_running = False

    async def send(
        self,
        recipient: "BaseAgent",
        content: Any,
        msg_type: MessageType = MessageType.TASK
    ) -> str:
        """Send message to another agent."""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient.name,
            content=content,
            message_type=msg_type
        )
        await recipient.inbox.put(message)
        return message.id

    async def receive(
        self,
        timeout: float = None
    ) -> Optional[AgentMessage]:
        """Receive message from inbox."""
        try:
            if timeout:
                return await asyncio.wait_for(
                    self.inbox.get(),
                    timeout=timeout
                )
            return await self.inbox.get()
        except asyncio.TimeoutError:
            return None

    @abstractmethod
    async def process(self, input_data: Any) -> AgentResult:
        """Process input and return result."""
        pass

    async def run(self):
        """Main agent loop."""
        self.is_running = True

        while self.is_running:
            message = await self.receive(timeout=1.0)

            if message is None:
                continue

            if message.message_type == MessageType.SHUTDOWN:
                break

            result = await self.process(message.content)
            result.metadata["message_id"] = message.id
            self.results.append(result)

        self.is_running = False

    async def stop(self):
        """Stop the agent."""
        self.is_running = False
        await self.inbox.put(
            AgentMessage(message_type=MessageType.SHUTDOWN)
        )


class WorkerAgent(BaseAgent):
    """
    Generic worker agent that processes tasks.

    Can be customized with a process function for
    specific task types.
    """

    def __init__(
        self,
        name: str,
        process_fn: Callable = None
    ):
        super().__init__(name, AgentRole.WORKER, process_fn)

    async def process(self, input_data: Any) -> AgentResult:
        """Process input using the configured function."""
        if self.process_fn:
            result = await self._call_process_fn(input_data)
        else:
            result = input_data  # Pass through

        return AgentResult(
            agent_id=self.name,
            content=result,
            confidence=1.0
        )

    async def _call_process_fn(self, input_data: Any) -> Any:
        """Call process function, handling sync/async."""
        if asyncio.iscoroutinefunction(self.process_fn):
            return await self.process_fn(input_data)
        return self.process_fn(input_data)


class HierarchicalOrchestrator:
    """
    Hierarchical orchestration pattern.

    A coordinator agent distributes tasks to worker agents
    and aggregates their results. Supports nested hierarchies.

    Architecture:
        Coordinator
           ├── Worker 1
           ├── Worker 2
           └── Worker 3
    """

    def __init__(
        self,
        name: str,
        aggregator_fn: Callable = None
    ):
        self.name = name
        self.workers: Dict[str, BaseAgent] = {}
        self.aggregator_fn = aggregator_fn or self._default_aggregator

    def add_worker(self, agent: BaseAgent):
        """Add a worker agent."""
        self.workers[agent.name] = agent

    def _default_aggregator(
        self,
        results: List[AgentResult]
    ) -> Any:
        """Default aggregation - combine all results."""
        return {
            r.agent_id: r.content for r in results
        }

    async def execute(
        self,
        task: Any,
        parallel: bool = True
    ) -> Dict[str, Any]:
        """
        Execute task across workers.

        Args:
            task: Task to distribute
            parallel: Run workers in parallel or sequentially

        Returns:
            Aggregated results
        """
        if parallel:
            results = await self._execute_parallel(task)
        else:
            results = await self._execute_sequential(task)

        aggregated = self.aggregator_fn(results)

        return {
            "results": results,
            "aggregated": aggregated,
            "worker_count": len(self.workers)
        }

    async def _execute_parallel(
        self,
        task: Any
    ) -> List[AgentResult]:
        """Execute task on all workers in parallel."""
        tasks = [
            worker.process(task)
            for worker in self.workers.values()
        ]
        return await asyncio.gather(*tasks)

    async def _execute_sequential(
        self,
        task: Any
    ) -> List[AgentResult]:
        """Execute task on workers sequentially."""
        results = []
        for worker in self.workers.values():
            result = await worker.process(task)
            results.append(result)
        return results


class ConsensusMechanism:
    """
    Consensus-based decision making.

    Multiple agents vote on outcomes, with configurable
    consensus thresholds and voting strategies.
    """

    def __init__(
        self,
        required_agreement: float = 0.66,
        voting_rounds: int = 1
    ):
        self.required_agreement = required_agreement
        self.voting_rounds = voting_rounds
        self.voters: List[BaseAgent] = []

    def add_voter(self, agent: BaseAgent):
        """Add a voting agent."""
        self.voters.append(agent)

    async def vote(
        self,
        proposal: Any,
        options: List[str] = None
    ) -> Dict[str, Any]:
        """
        Conduct a vote on a proposal.

        Args:
            proposal: The item being voted on
            options: Optional list of valid vote options

        Returns:
            Vote results including consensus status
        """
        options = options or ["approve", "reject"]

        for round_num in range(self.voting_rounds):
            votes = []

            for voter in self.voters:
                result = await voter.process({
                    "type": "vote",
                    "proposal": proposal,
                    "options": options,
                    "round": round_num
                })
                votes.append({
                    "voter": voter.name,
                    "vote": result.content,
                    "confidence": result.confidence,
                    "reasoning": result.reasoning
                })

            # Count votes
            vote_counts = {}
            for vote in votes:
                v = vote["vote"]
                vote_counts[v] = vote_counts.get(v, 0) + 1

            # Check for consensus
            total = len(votes)
            for option, count in vote_counts.items():
                if count / total >= self.required_agreement:
                    return {
                        "consensus": True,
                        "decision": option,
                        "agreement": count / total,
                        "votes": votes,
                        "rounds_needed": round_num + 1
                    }

        # No consensus reached
        return {
            "consensus": False,
            "decision": None,
            "vote_counts": vote_counts,
            "votes": votes,
            "rounds_needed": self.voting_rounds
        }


class PipelineOrchestrator:
    """
    Pipeline orchestration pattern.

    Agents process data sequentially, each transforming
    the output of the previous stage.

    Architecture:
        Input → Agent 1 → Agent 2 → Agent 3 → Output
    """

    def __init__(self, name: str):
        self.name = name
        self.stages: List[BaseAgent] = []

    def add_stage(self, agent: BaseAgent):
        """Add a stage to the pipeline."""
        self.stages.append(agent)

    async def execute(
        self,
        input_data: Any,
        collect_intermediate: bool = False
    ) -> Dict[str, Any]:
        """
        Execute pipeline on input data.

        Args:
            input_data: Initial input
            collect_intermediate: Store intermediate results

        Returns:
            Final output and optional intermediate results
        """
        current = input_data
        intermediate = []

        for stage in self.stages:
            result = await stage.process(current)

            if collect_intermediate:
                intermediate.append({
                    "stage": stage.name,
                    "input": current,
                    "output": result.content
                })

            current = result.content

        return {
            "output": current,
            "intermediate": intermediate if collect_intermediate else None,
            "stages_count": len(self.stages)
        }


class DebateOrchestrator:
    """
    Debate pattern for adversarial reasoning.

    Agents argue different positions on a topic,
    with a judge synthesizing the final conclusion.

    Architecture:
        Advocate 1 ←→ Advocate 2
              ↓
            Judge
    """

    def __init__(
        self,
        judge: BaseAgent,
        max_rounds: int = 3
    ):
        self.judge = judge
        self.max_rounds = max_rounds
        self.advocates: List[BaseAgent] = []

    def add_advocate(self, agent: BaseAgent):
        """Add an advocate agent."""
        self.advocates.append(agent)

    async def debate(
        self,
        topic: str,
        positions: List[str] = None
    ) -> Dict[str, Any]:
        """
        Conduct a debate on a topic.

        Args:
            topic: Topic to debate
            positions: Optional assigned positions

        Returns:
            Debate transcript and final judgment
        """
        transcript = []

        # Assign positions if provided
        if positions:
            for i, agent in enumerate(self.advocates):
                agent.position = positions[i] if i < len(positions) else None

        # Conduct debate rounds
        for round_num in range(self.max_rounds):
            round_arguments = []

            for advocate in self.advocates:
                # Get previous arguments for context
                context = {
                    "topic": topic,
                    "round": round_num,
                    "previous_arguments": transcript,
                    "position": getattr(advocate, 'position', None)
                }

                result = await advocate.process(context)

                argument = {
                    "advocate": advocate.name,
                    "round": round_num,
                    "argument": result.content,
                    "confidence": result.confidence
                }
                round_arguments.append(argument)

            transcript.extend(round_arguments)

        # Judge makes final decision
        judgment = await self.judge.process({
            "topic": topic,
            "transcript": transcript
        })

        return {
            "topic": topic,
            "transcript": transcript,
            "judgment": judgment.content,
            "judge_confidence": judgment.confidence,
            "rounds_conducted": self.max_rounds
        }


class SwarmOrchestrator:
    """
    Swarm intelligence pattern.

    Large numbers of simple agents work together
    emergently, sharing information through a
    shared state space.

    Architecture:
        ┌─────────────────────────┐
        │    Shared State Space   │
        └─────────────────────────┘
           ↑   ↑   ↑   ↑   ↑   ↑
           │   │   │   │   │   │
           A   A   A   A   A   A  (Agents)
    """

    def __init__(
        self,
        name: str,
        shared_state: Dict[str, Any] = None
    ):
        self.name = name
        self.agents: List[BaseAgent] = []
        self.shared_state = shared_state or {}
        self.state_lock = asyncio.Lock()

    def add_agent(self, agent: BaseAgent):
        """Add an agent to the swarm."""
        self.agents.append(agent)

    async def read_state(self, key: str = None) -> Any:
        """Read from shared state."""
        async with self.state_lock:
            if key:
                return self.shared_state.get(key)
            return self.shared_state.copy()

    async def write_state(self, key: str, value: Any):
        """Write to shared state."""
        async with self.state_lock:
            self.shared_state[key] = value

    async def update_state(self, updates: Dict[str, Any]):
        """Update multiple state keys."""
        async with self.state_lock:
            self.shared_state.update(updates)

    async def execute(
        self,
        task: Any,
        iterations: int = 10,
        convergence_fn: Callable = None
    ) -> Dict[str, Any]:
        """
        Execute swarm on a task.

        Args:
            task: Task for swarm to process
            iterations: Maximum iterations
            convergence_fn: Function to check convergence

        Returns:
            Final shared state and execution metrics
        """
        # Initialize state with task
        await self.write_state("task", task)
        await self.write_state("iteration", 0)

        for iteration in range(iterations):
            await self.write_state("iteration", iteration)

            # All agents process in parallel
            tasks = []
            for agent in self.agents:
                state = await self.read_state()
                tasks.append(agent.process(state))

            results = await asyncio.gather(*tasks)

            # Aggregate updates
            for result in results:
                if isinstance(result.content, dict):
                    await self.update_state(result.content)

            # Check convergence
            if convergence_fn:
                state = await self.read_state()
                if convergence_fn(state):
                    break

        final_state = await self.read_state()

        return {
            "final_state": final_state,
            "iterations": iteration + 1,
            "agent_count": len(self.agents)
        }


class TaskRouter:
    """
    Routes tasks to appropriate agents based on type.

    Supports dynamic routing rules and load balancing.
    """

    def __init__(self):
        self.routes: Dict[str, List[BaseAgent]] = {}
        self.default_agents: List[BaseAgent] = []

    def register_route(
        self,
        task_type: str,
        agent: BaseAgent
    ):
        """Register an agent for a task type."""
        if task_type not in self.routes:
            self.routes[task_type] = []
        self.routes[task_type].append(agent)

    def set_default(self, agent: BaseAgent):
        """Set default agent for unmatched tasks."""
        self.default_agents.append(agent)

    def get_agents(self, task_type: str) -> List[BaseAgent]:
        """Get agents for a task type."""
        if task_type in self.routes:
            return self.routes[task_type]
        return self.default_agents

    async def route(
        self,
        task: Any,
        task_type: str
    ) -> List[AgentResult]:
        """
        Route task to appropriate agents.

        Returns results from all matched agents.
        """
        agents = self.get_agents(task_type)

        if not agents:
            raise ValueError(f"No agents for task type: {task_type}")

        tasks = [agent.process(task) for agent in agents]
        return await asyncio.gather(*tasks)


# Example usage
if __name__ == "__main__":
    async def demo():
        # Create worker agents
        def extract_requirements(text):
            # Simple extraction demo
            requirements = []
            for line in text.split('.'):
                if 'shall' in line.lower() or 'must' in line.lower():
                    requirements.append(line.strip())
            return requirements

        def analyze_compliance(requirements):
            # Simple analysis demo
            return {
                "total": len(requirements),
                "mandatory": sum(
                    1 for r in requirements
                    if 'must' in r.lower()
                ),
                "requirements": requirements
            }

        extractor = WorkerAgent("extractor", extract_requirements)
        analyzer = WorkerAgent("analyzer", analyze_compliance)

        # Test pipeline pattern
        print("=== Pipeline Pattern ===")
        pipeline = PipelineOrchestrator("doc-pipeline")
        pipeline.add_stage(extractor)
        pipeline.add_stage(analyzer)

        test_doc = """
        All agencies shall maintain an AI inventory.
        Systems must be tested before deployment.
        Documentation should be updated regularly.
        Compliance reports must be submitted annually.
        """

        result = await pipeline.execute(test_doc, collect_intermediate=True)
        print(f"Output: {result['output']}")

        # Test hierarchical pattern
        print("\n=== Hierarchical Pattern ===")
        orchestrator = HierarchicalOrchestrator("coordinator")

        worker1 = WorkerAgent("worker1", lambda x: f"W1: {len(x)} chars")
        worker2 = WorkerAgent("worker2", lambda x: f"W2: {x.count('.')} sentences")

        orchestrator.add_worker(worker1)
        orchestrator.add_worker(worker2)

        result = await orchestrator.execute(test_doc)
        print(f"Aggregated: {result['aggregated']}")

        print("\nDemo complete!")

    asyncio.run(demo())
