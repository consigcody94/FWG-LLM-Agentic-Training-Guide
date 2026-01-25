# Lab 28.3: Multi-Agent Document Analysis System

## Overview

Build a multi-agent system that processes large documents using specialized agents working in parallel. The system will extract requirements, analyze compliance implications, and generate structured reports.

**Duration:** 120 minutes
**Difficulty:** Advanced
**Prerequisites:** Module 12 (Multi-Agent Systems), Module 28.1-28.2

## Learning Objectives

1. Implement hierarchical agent orchestration
2. Build specialized analysis agents
3. Create consensus mechanisms for verification
4. Generate structured compliance reports

## Architecture

```
                    ┌─────────────────────┐
                    │   COORDINATOR       │
                    │   AGENT             │
                    └──────────┬──────────┘
           ┌───────────────────┼───────────────────┐
           ▼                   ▼                   ▼
   ┌───────────────┐   ┌───────────────┐   ┌───────────────┐
   │   EXTRACTOR   │   │   ANALYZER    │   │   VERIFIER    │
   │   AGENT       │   │   AGENT       │   │   AGENT       │
   └───────────────┘   └───────────────┘   └───────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   SYNTHESIZER       │
                    │   AGENT             │
                    └─────────────────────┘
```

## Part 1: Base Agent Implementation (30 minutes)

### Task 1.1: Create Base Agent Class

```python
"""
Task: Implement the base agent class.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import asyncio

@dataclass
class AgentMessage:
    """Message passed between agents"""
    sender: str
    recipient: str
    content: Any
    message_type: str  # 'task', 'result', 'query', 'response'
    metadata: Dict[str, Any] = None

class BaseAgent(ABC):
    """Base class for all agents"""

    def __init__(self, name: str, llm_client=None):
        self.name = name
        self.llm = llm_client
        self.inbox: asyncio.Queue = asyncio.Queue()
        self.results: List[Any] = []

    async def send(self, recipient: "BaseAgent", content: Any, msg_type: str):
        """Send message to another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient.name,
            content=content,
            message_type=msg_type
        )
        await recipient.inbox.put(message)

    async def receive(self, timeout: float = None) -> Optional[AgentMessage]:
        """Receive message from inbox"""
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
    async def process(self, input_data: Any) -> Any:
        """Process input and return result"""
        pass

    async def run(self):
        """Main agent loop"""
        while True:
            message = await self.receive()
            if message is None:
                break
            if message.message_type == "shutdown":
                break
            result = await self.process(message.content)
            self.results.append(result)
```

### Task 1.2: Implement Extractor Agent

```python
"""
Task: Implement the requirement extraction agent.

This agent:
1. Reads document chunks
2. Extracts requirements (SHALL, MUST, REQUIRED)
3. Categorizes by type (technical, procedural, compliance)
4. Returns structured requirements
"""

@dataclass
class Requirement:
    text: str
    category: str  # 'technical', 'procedural', 'compliance', 'documentation'
    priority: str  # 'mandatory', 'recommended', 'optional'
    source_location: str
    confidence: float

class ExtractorAgent(BaseAgent):
    """Extracts requirements from document chunks"""

    REQUIREMENT_KEYWORDS = {
        'mandatory': ['shall', 'must', 'required', 'will'],
        'recommended': ['should', 'recommend', 'encouraged'],
        'optional': ['may', 'can', 'optional']
    }

    async def process(self, chunk: str) -> List[Requirement]:
        """
        Extract requirements from a document chunk.

        Steps:
        1. Split into sentences
        2. Identify requirement indicators
        3. Classify category and priority
        4. Return structured requirements
        """
        # TODO: Implement extraction logic
        pass

    def _identify_priority(self, sentence: str) -> str:
        """Identify requirement priority from keywords"""
        sentence_lower = sentence.lower()
        for priority, keywords in self.REQUIREMENT_KEYWORDS.items():
            if any(kw in sentence_lower for kw in keywords):
                return priority
        return 'unknown'

    def _categorize(self, sentence: str) -> str:
        """Categorize requirement type"""
        # TODO: Implement categorization logic
        pass
```

## Part 2: Specialized Agents (30 minutes)

### Task 2.1: Implement Analyzer Agent

```python
"""
Task: Implement the compliance analyzer agent.

This agent:
1. Takes extracted requirements
2. Analyzes compliance implications
3. Identifies dependencies between requirements
4. Assesses implementation complexity
"""

@dataclass
class ComplianceAnalysis:
    requirement: Requirement
    implications: List[str]
    dependencies: List[str]
    complexity: str  # 'low', 'medium', 'high'
    estimated_effort: str
    risks: List[str]

class AnalyzerAgent(BaseAgent):
    """Analyzes compliance implications of requirements"""

    async def process(self, requirements: List[Requirement]) -> List[ComplianceAnalysis]:
        """
        Analyze each requirement for compliance implications.
        """
        analyses = []
        for req in requirements:
            analysis = await self._analyze_requirement(req)
            analyses.append(analysis)
        return analyses

    async def _analyze_requirement(self, req: Requirement) -> ComplianceAnalysis:
        """
        Analyze a single requirement.

        For LLM-based analysis, prompt could be:
        "Analyze this requirement for compliance:
         {req.text}

         Provide:
         1. Key implications
         2. Dependencies on other systems/processes
         3. Implementation complexity (low/medium/high)
         4. Potential risks"
        """
        # TODO: Implement analysis
        pass
```

### Task 2.2: Implement Verifier Agent

```python
"""
Task: Implement the verification agent.

This agent:
1. Cross-checks extracted requirements
2. Validates consistency
3. Identifies conflicts
4. Confirms completeness
"""

@dataclass
class VerificationResult:
    is_valid: bool
    conflicts: List[str]
    gaps: List[str]
    confidence: float
    notes: str

class VerifierAgent(BaseAgent):
    """Verifies requirement extraction and analysis"""

    async def process(
        self,
        data: Dict[str, Any]
    ) -> VerificationResult:
        """
        Verify extracted requirements and analysis.

        Input data contains:
        - original_text: Source document
        - requirements: Extracted requirements
        - analysis: Compliance analysis
        """
        original = data['original_text']
        requirements = data['requirements']
        analysis = data['analysis']

        # Check for conflicts
        conflicts = self._find_conflicts(requirements)

        # Check for gaps
        gaps = self._find_gaps(original, requirements)

        # Calculate confidence
        confidence = self._calculate_confidence(requirements, analysis)

        return VerificationResult(
            is_valid=len(conflicts) == 0 and confidence > 0.8,
            conflicts=conflicts,
            gaps=gaps,
            confidence=confidence,
            notes=""
        )

    def _find_conflicts(self, requirements: List[Requirement]) -> List[str]:
        """Find conflicting requirements"""
        # TODO: Implement conflict detection
        pass

    def _find_gaps(self, original: str, requirements: List[Requirement]) -> List[str]:
        """Find potential missing requirements"""
        # TODO: Implement gap analysis
        pass
```

## Part 3: Orchestrator (30 minutes)

### Task 3.1: Implement Coordinator

```python
"""
Task: Implement the coordinator agent.

This agent:
1. Splits document into chunks
2. Distributes work to specialized agents
3. Collects and aggregates results
4. Handles failures and retries
"""

class CoordinatorAgent(BaseAgent):
    """Coordinates multi-agent document analysis"""

    def __init__(
        self,
        name: str,
        chunk_size: int = 2000,
        llm_client=None
    ):
        super().__init__(name, llm_client)
        self.chunk_size = chunk_size

        # Child agents
        self.extractor = ExtractorAgent("extractor")
        self.analyzer = AnalyzerAgent("analyzer")
        self.verifier = VerifierAgent("verifier")
        self.synthesizer = SynthesizerAgent("synthesizer")

    async def process(self, document: str) -> Dict[str, Any]:
        """
        Process a document through the agent pipeline.

        Steps:
        1. Chunk the document
        2. Extract requirements in parallel
        3. Analyze requirements
        4. Verify results
        5. Synthesize final report
        """
        # Step 1: Chunk document
        chunks = self._chunk_document(document)

        # Step 2: Parallel extraction
        extraction_tasks = [
            self.extractor.process(chunk)
            for chunk in chunks
        ]
        all_requirements = await asyncio.gather(*extraction_tasks)
        requirements = self._merge_requirements(all_requirements)

        # Step 3: Analysis
        analysis = await self.analyzer.process(requirements)

        # Step 4: Verification
        verification = await self.verifier.process({
            'original_text': document,
            'requirements': requirements,
            'analysis': analysis
        })

        # Step 5: Synthesis
        if verification.is_valid:
            report = await self.synthesizer.process({
                'requirements': requirements,
                'analysis': analysis,
                'verification': verification
            })
        else:
            # Handle verification failure
            report = self._create_error_report(verification)

        return {
            'requirements': requirements,
            'analysis': analysis,
            'verification': verification,
            'report': report
        }

    def _chunk_document(self, document: str) -> List[str]:
        """Split document into chunks"""
        # TODO: Implement chunking with overlap
        pass

    def _merge_requirements(
        self,
        all_requirements: List[List[Requirement]]
    ) -> List[Requirement]:
        """Merge and deduplicate requirements from all chunks"""
        # TODO: Implement deduplication
        pass
```

### Task 3.2: Implement Synthesizer

```python
"""
Task: Implement the report synthesizer agent.
"""

@dataclass
class ComplianceReport:
    title: str
    summary: str
    total_requirements: int
    by_category: Dict[str, int]
    by_priority: Dict[str, int]
    high_risk_items: List[str]
    recommendations: List[str]
    checklist: List[Dict[str, Any]]

class SynthesizerAgent(BaseAgent):
    """Synthesizes final compliance report"""

    async def process(self, data: Dict[str, Any]) -> ComplianceReport:
        """
        Generate structured compliance report.
        """
        requirements = data['requirements']
        analysis = data['analysis']

        # Aggregate statistics
        by_category = self._count_by_category(requirements)
        by_priority = self._count_by_priority(requirements)

        # Identify high-risk items
        high_risk = self._identify_high_risk(analysis)

        # Generate recommendations
        recommendations = self._generate_recommendations(analysis)

        # Create checklist
        checklist = self._create_checklist(requirements, analysis)

        return ComplianceReport(
            title="Document Compliance Analysis Report",
            summary=self._generate_summary(requirements, analysis),
            total_requirements=len(requirements),
            by_category=by_category,
            by_priority=by_priority,
            high_risk_items=high_risk,
            recommendations=recommendations,
            checklist=checklist
        )
```

## Part 4: Integration (30 minutes)

### Task 4.1: Complete System Test

```python
"""
Integration test with sample federal document.
"""

SAMPLE_DOCUMENT = """
FEDERAL AI GOVERNANCE POLICY

Section 1: Requirements

1.1 All agencies SHALL maintain an inventory of AI systems used in
decision-making processes. The inventory MUST be updated quarterly.

1.2 Agencies MUST conduct impact assessments for AI systems that
affect individual rights. These assessments SHALL include analysis
of potential bias and discrimination.

1.3 High-risk AI systems REQUIRE human oversight mechanisms. Agencies
SHOULD implement automated monitoring where feasible.

1.4 Documentation of AI system training data is REQUIRED. Agencies
MAY use standardized templates for documentation.

1.5 Public notice MUST be provided when AI systems are used in
rights-impacting decisions. Notice SHOULD be provided in plain language.

Section 2: Compliance

2.1 Agencies SHALL designate an AI Accountability Official responsible
for compliance monitoring.

2.2 Annual compliance reports MUST be submitted to OMB. Reports SHALL
include metrics on AI system performance and incident reports.

2.3 Non-compliance MAY result in suspension of AI system deployment
pending remediation.
"""

async def main():
    # Initialize coordinator
    coordinator = CoordinatorAgent("coordinator", chunk_size=500)

    # Process document
    print("Processing document...")
    result = await coordinator.process(SAMPLE_DOCUMENT)

    # Display results
    print("\n" + "="*60)
    print("ANALYSIS RESULTS")
    print("="*60)

    print(f"\nTotal Requirements Found: {len(result['requirements'])}")

    print("\nBy Priority:")
    for req in result['requirements']:
        print(f"  [{req.priority.upper()}] {req.text[:60]}...")

    print("\nVerification:")
    v = result['verification']
    print(f"  Valid: {v.is_valid}")
    print(f"  Confidence: {v.confidence:.1%}")
    if v.conflicts:
        print(f"  Conflicts: {v.conflicts}")
    if v.gaps:
        print(f"  Gaps: {v.gaps}")

    print("\nReport Summary:")
    print(result['report'].summary)

    print("\nChecklist:")
    for item in result['report'].checklist[:5]:
        status = "[ ]" if not item.get('completed') else "[x]"
        print(f"  {status} {item['requirement'][:50]}...")

if __name__ == "__main__":
    asyncio.run(main())
```

## Deliverables

1. Complete multi-agent system implementation
2. Test results with sample document
3. Generated compliance report

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Agents communicate correctly | 20 |
| Requirements extracted accurately | 20 |
| Analysis identifies key implications | 20 |
| Verification catches issues | 15 |
| Report is well-structured | 15 |
| Code quality | 10 |
| **Total** | **100** |

## Extension Challenges

1. Add parallel verification with multiple verifier agents
2. Implement debate pattern for conflict resolution
3. Add support for document comparison (diff two versions)
4. Create visualization of requirement dependencies
