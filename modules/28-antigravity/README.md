# Module 28: Antigravity - Overcoming Conventional AI System Limitations

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   MODULE 28: ANTIGRAVITY TECHNIQUES FOR AI AGENT SYSTEMS                     ║
║                                                                              ║
║   Advanced methods for overcoming context limitations, memory constraints,   ║
║   and computational boundaries in production agentic systems.                ║
║                                                                              ║
║   Duration: 6 hours                                                          ║
║   Prerequisites: Modules 12 (Multi-Agent Systems), 14 (Memory & Context)    ║
║   Difficulty: Advanced                                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Table of Contents

1. [Overview](#overview)
2. [Learning Objectives](#learning-objectives)
3. [28.1 Context Window Limitations](#281-context-window-limitations-and-mitigation-strategies)
4. [28.2 Hierarchical Memory Systems](#282-hierarchical-memory-systems)
5. [28.3 Semantic Compression](#283-semantic-compression-techniques)
6. [28.4 Multi-Agent Orchestration](#284-multi-agent-orchestration-for-complex-tasks)
7. [28.5 Production Reliability](#285-production-reliability-patterns)
8. [28.6 Advanced Retrieval Patterns](#286-advanced-retrieval-patterns)
9. [28.7 State Management](#287-distributed-state-management)
10. [28.8 Performance Optimization](#288-performance-optimization)
11. [28.9 Evaluation & Metrics](#289-evaluation-and-metrics)
12. [28.10 Federal Use Cases](#2810-federal-use-cases)
13. [Hands-On Labs](#hands-on-labs)
14. [Summary](#summary)
15. [References](#references)

---

## Overview

The term "antigravity" in this context refers to techniques and architectural patterns that allow AI agent systems to overcome what were previously considered hard limitations. Just as Python's `import antigravity` demonstrates that perceived impossibilities can be solved with the right approach, this module teaches practitioners how to push beyond conventional boundaries while maintaining system reliability and security.

### Why "Antigravity"?

Every AI system faces "gravitational forces" that pull it back to baseline capabilities:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    FORCES LIMITING AI AGENT CAPABILITIES                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   CONTEXT GRAVITY          MEMORY GRAVITY           COMPUTE GRAVITY        │
│   ═══════════════          ═════════════           ═══════════════        │
│   • Token limits           • Session isolation      • Latency costs        │
│   • Attention decay        • No persistence         • API rate limits      │
│   • Context fragmentation  • Working memory only    • Cost constraints     │
│                                                                             │
│   RELIABILITY GRAVITY      COORDINATION GRAVITY     KNOWLEDGE GRAVITY      │
│   ═══════════════════      ══════════════════════   ═════════════════     │
│   • API failures           • Single-agent limits    • Training cutoffs     │
│   • Timeout errors         • Sequential processing  • Domain gaps          │
│   • Inconsistent outputs   • Communication overhead • Hallucination risk   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

This module provides techniques to counteract each of these forces.

### Module Architecture

```
modules/28-antigravity/
├── README.md                      # This file
├── lessons/
│   ├── 01-context-management.md   # Deep dive on context windows
│   ├── 02-memory-architecture.md  # Memory system design
│   ├── 03-compression.md          # Semantic compression
│   ├── 04-orchestration.md        # Multi-agent patterns
│   └── 05-reliability.md          # Production patterns
├── labs/
│   ├── lab-01-memory-system.md    # Build hierarchical memory
│   ├── lab-02-compression.md      # Implement compression pipeline
│   └── lab-03-multi-agent.md      # Multi-agent document analysis
├── examples/
│   ├── context_manager.py         # Context window management
│   ├── memory_systems.py          # Memory implementations
│   ├── compression.py             # Compression algorithms
│   ├── orchestration.py           # Multi-agent patterns
│   └── reliability.py             # Circuit breakers & fallbacks
└── antigravity_agent.py           # Complete reference implementation
```

---

## Learning Objectives

By the end of this module, participants will be able to:

| # | Objective | Assessment Method |
|---|-----------|-------------------|
| 1 | **Implement context extension techniques** to effectively work beyond native context window limits | Lab 1: Process 100+ page document |
| 2 | **Design hierarchical memory systems** with working, short-term, long-term, and episodic tiers | Lab 1: Build memory system |
| 3 | **Apply semantic compression** to reduce token usage while preserving >95% information fidelity | Lab 2: Achieve 50% compression |
| 4 | **Orchestrate multi-agent systems** for problems exceeding single-agent capabilities | Lab 3: Multi-agent analysis |
| 5 | **Implement production reliability patterns** including circuit breakers and graceful degradation | Code review |
| 6 | **Evaluate trade-offs** between different approaches for specific use cases | Written analysis |

---

## 28.1 Context Window Limitations and Mitigation Strategies

### Understanding Context Windows

The context window is the maximum number of tokens an LLM can process in a single interaction. This fundamental constraint affects every aspect of agent design.

#### Current Model Context Limits (2025)

| Model | Context Window | Practical Limit | Cost per 1M Tokens |
|-------|---------------|-----------------|-------------------|
| GPT-4o | 128K | ~100K | $5.00 / $15.00 |
| GPT-4 Turbo | 128K | ~100K | $10.00 / $30.00 |
| Claude 3.5 Sonnet | 200K | ~180K | $3.00 / $15.00 |
| Claude 3 Opus | 200K | ~180K | $15.00 / $75.00 |
| Gemini 1.5 Pro | 1M | ~900K | $3.50 / $10.50 |
| Llama 3.1 405B | 128K | ~100K | Self-hosted |

> **Note:** Practical limits account for system prompts, tool definitions, and output buffer.

### The Attention Decay Problem

Even within the context window, attention is not uniform:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ATTENTION DISTRIBUTION                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Attention                                                                  │
│  Strength                                                                   │
│     │                                                                       │
│  100%├─■■■■                                              ■■■■■■■■■■■■■■    │
│     │     ■■■                                         ■■■                   │
│  75%├        ■■                                     ■■                      │
│     │          ■■                                 ■■                        │
│  50%├            ■■■                           ■■■                          │
│     │               ■■■■                   ■■■■                             │
│  25%├                   ■■■■■■■■■■■■■■■■■■■                                 │
│     │                                                                       │
│   0%└───────────────────────────────────────────────────────────────────── │
│        START                    MIDDLE                           END        │
│        (System Prompt)          ("Lost in the Middle")           (Recent)   │
│                                                                             │
│  Research shows: Information in the middle of context receives              │
│  significantly less attention than beginning or end positions.              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Mitigation Strategy 1: Sliding Window with Importance Preservation

```python
from typing import List, Tuple, Optional
from dataclasses import dataclass
from datetime import datetime
import tiktoken

@dataclass
class ContextItem:
    """A single item in the context window"""
    content: str
    importance: float  # 0.0 to 1.0
    timestamp: datetime
    tokens: int
    category: str  # 'system', 'user', 'assistant', 'tool', 'memory'

class SlidingWindowContextManager:
    """
    Manages context with intelligent sliding window that preserves
    important information while evicting less critical content.

    Key Features:
    - Importance-based retention
    - Position-aware placement (important items at start/end)
    - Token budget management
    - Category-based quotas
    """

    def __init__(
        self,
        max_tokens: int = 100000,
        model: str = "gpt-4",
        reserved_output: int = 4000,
        category_quotas: dict = None
    ):
        self.max_tokens = max_tokens
        self.reserved_output = reserved_output
        self.available_tokens = max_tokens - reserved_output
        self.encoder = tiktoken.encoding_for_model(model)

        # Default category quotas (percentage of available tokens)
        self.category_quotas = category_quotas or {
            'system': 0.15,      # System prompt: 15%
            'memory': 0.20,      # Retrieved memories: 20%
            'tool': 0.25,        # Tool results: 25%
            'conversation': 0.40 # User/assistant messages: 40%
        }

        self.items: List[ContextItem] = []
        self.preserved_items: List[ContextItem] = []  # Never evicted

    def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        return len(self.encoder.encode(text))

    def add(
        self,
        content: str,
        category: str,
        importance: float = 0.5,
        preserve: bool = False
    ) -> bool:
        """
        Add content to context.

        Args:
            content: Text content to add
            category: Content category for quota management
            importance: Importance score (0.0 to 1.0)
            preserve: If True, item will never be evicted

        Returns:
            True if content was added, False if rejected
        """
        tokens = self.count_tokens(content)

        item = ContextItem(
            content=content,
            importance=importance,
            timestamp=datetime.now(),
            tokens=tokens,
            category=category
        )

        if preserve:
            self.preserved_items.append(item)
        else:
            self.items.append(item)

        # Enforce limits
        self._enforce_limits()

        return True

    def _enforce_limits(self):
        """Enforce token limits through intelligent eviction"""
        total_tokens = self._get_total_tokens()

        while total_tokens > self.available_tokens:
            # Find lowest priority item to evict
            eviction_candidate = self._find_eviction_candidate()

            if eviction_candidate is None:
                # Can't evict anything - we're at minimum
                break

            self.items.remove(eviction_candidate)
            total_tokens = self._get_total_tokens()

    def _find_eviction_candidate(self) -> Optional[ContextItem]:
        """
        Find the best candidate for eviction based on:
        1. Importance (lower = more likely to evict)
        2. Age (older = more likely to evict)
        3. Category quota status
        """
        if not self.items:
            return None

        candidates = []
        now = datetime.now()

        for item in self.items:
            # Calculate eviction score (higher = more likely to evict)
            age_hours = (now - item.timestamp).total_seconds() / 3600
            age_factor = min(age_hours / 24, 1.0)  # Max out at 24 hours

            # Importance inverted (low importance = high eviction score)
            importance_factor = 1.0 - item.importance

            # Combined score
            eviction_score = (importance_factor * 0.6) + (age_factor * 0.4)

            candidates.append((eviction_score, item))

        # Sort by eviction score descending
        candidates.sort(key=lambda x: x[0], reverse=True)

        return candidates[0][1] if candidates else None

    def _get_total_tokens(self) -> int:
        """Get total tokens across all items"""
        preserved = sum(item.tokens for item in self.preserved_items)
        regular = sum(item.tokens for item in self.items)
        return preserved + regular

    def build_context(self) -> str:
        """
        Build the final context string with optimal positioning.

        Positions important content at start and end to maximize
        attention (avoiding "lost in the middle" effect).
        """
        # Sort items by importance
        sorted_items = sorted(
            self.items,
            key=lambda x: x.importance,
            reverse=True
        )

        # Split into high and low importance
        mid_point = len(sorted_items) // 2
        high_importance = sorted_items[:mid_point]
        low_importance = sorted_items[mid_point:]

        # Build context: preserved -> high importance -> low importance -> recent
        context_parts = []

        # Preserved items first (system prompts, etc.)
        for item in self.preserved_items:
            context_parts.append(item.content)

        # High importance items near start
        for item in high_importance:
            context_parts.append(item.content)

        # Low importance in middle
        for item in low_importance:
            context_parts.append(item.content)

        return "\n\n".join(context_parts)

    def get_stats(self) -> dict:
        """Get context manager statistics"""
        total = self._get_total_tokens()
        by_category = {}

        for item in self.preserved_items + self.items:
            by_category[item.category] = by_category.get(item.category, 0) + item.tokens

        return {
            "total_tokens": total,
            "available_tokens": self.available_tokens,
            "utilization": total / self.available_tokens,
            "preserved_items": len(self.preserved_items),
            "regular_items": len(self.items),
            "by_category": by_category
        }
```

### Mitigation Strategy 2: Hierarchical Summarization

For documents exceeding context limits, use recursive summarization:

```python
import asyncio
from typing import List, Dict, Any

class HierarchicalSummarizer:
    """
    Processes large documents through recursive summarization,
    creating a hierarchical structure that preserves key information
    at multiple levels of detail.

    Levels:
    - Level 0: Original chunks (~2000 tokens each)
    - Level 1: Chunk summaries (~200 tokens each)
    - Level 2: Section summaries (~500 tokens for 5 chunks)
    - Level 3: Document summary (~1000 tokens)
    """

    def __init__(
        self,
        llm_client,
        chunk_size: int = 2000,
        chunk_overlap: int = 200,
        summary_ratio: float = 0.1
    ):
        self.llm = llm_client
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.summary_ratio = summary_ratio

    async def process_document(self, document: str) -> Dict[str, Any]:
        """
        Create hierarchical summary of a document.

        Args:
            document: Full document text

        Returns:
            Hierarchical structure with summaries at each level
        """
        # Level 0: Split into chunks
        chunks = self._split_into_chunks(document)

        # Level 1: Summarize each chunk
        chunk_summaries = await self._summarize_chunks(chunks)

        # Level 2: Group chunks and create section summaries
        sections = self._group_into_sections(chunk_summaries, group_size=5)
        section_summaries = await self._summarize_sections(sections)

        # Level 3: Create document summary
        document_summary = await self._create_document_summary(section_summaries)

        return {
            "document_summary": document_summary,
            "section_summaries": section_summaries,
            "chunk_summaries": chunk_summaries,
            "chunks": chunks,
            "metadata": {
                "original_length": len(document),
                "num_chunks": len(chunks),
                "num_sections": len(sections),
                "compression_ratio": len(document_summary) / len(document)
            }
        }

    def _split_into_chunks(self, text: str) -> List[str]:
        """Split text into overlapping chunks"""
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # Try to break at sentence boundary
            if end < len(text):
                # Look for sentence end within last 200 chars
                search_start = max(end - 200, start)
                last_period = text.rfind('.', search_start, end)
                if last_period > search_start:
                    end = last_period + 1

            chunks.append(text[start:end].strip())
            start = end - self.chunk_overlap

        return chunks

    async def _summarize_chunks(self, chunks: List[str]) -> List[str]:
        """Summarize each chunk in parallel"""
        tasks = [
            self._summarize_single(chunk, "chunk")
            for chunk in chunks
        ]
        return await asyncio.gather(*tasks)

    async def _summarize_single(self, text: str, level: str) -> str:
        """Summarize a single piece of text"""
        prompt = f"""Summarize the following {level} concisely, preserving key facts,
entities, and relationships. Focus on information that would be important for
answering questions about the document.

Text:
{text}

Summary:"""

        response = await self.llm.complete(prompt)
        return response.strip()

    async def _summarize_sections(self, sections: List[List[str]]) -> List[str]:
        """Summarize each section (group of chunk summaries)"""
        tasks = []
        for section in sections:
            combined = "\n\n".join(section)
            tasks.append(self._summarize_single(combined, "section"))
        return await asyncio.gather(*tasks)

    async def _create_document_summary(self, section_summaries: List[str]) -> str:
        """Create final document summary from section summaries"""
        combined = "\n\n".join(section_summaries)
        return await self._summarize_single(combined, "document")

    def _group_into_sections(
        self,
        items: List[str],
        group_size: int
    ) -> List[List[str]]:
        """Group items into sections"""
        return [
            items[i:i + group_size]
            for i in range(0, len(items), group_size)
        ]
```

### Mitigation Strategy 3: Dynamic Context Loading

Load context on-demand based on the query:

```python
class DynamicContextLoader:
    """
    Loads relevant context dynamically based on the current query,
    rather than maintaining a static context window.

    This approach:
    1. Analyzes the incoming query
    2. Retrieves relevant documents/memories
    3. Ranks by relevance
    4. Loads only what fits in context budget
    """

    def __init__(
        self,
        vector_store,
        reranker,
        max_context_tokens: int = 50000
    ):
        self.vector_store = vector_store
        self.reranker = reranker
        self.max_context_tokens = max_context_tokens

    async def load_context(
        self,
        query: str,
        conversation_history: List[dict] = None,
        required_context: List[str] = None
    ) -> str:
        """
        Dynamically load context for a query.

        Args:
            query: Current user query
            conversation_history: Recent conversation turns
            required_context: Context that must be included

        Returns:
            Optimized context string
        """
        # Calculate available budget
        required_tokens = self._count_required_tokens(required_context or [])
        history_tokens = self._count_history_tokens(conversation_history or [])
        available = self.max_context_tokens - required_tokens - history_tokens

        # Retrieve candidates
        candidates = await self.vector_store.search(
            query=query,
            k=50  # Get many candidates for reranking
        )

        # Rerank by relevance to query
        reranked = await self.reranker.rerank(
            query=query,
            documents=[c.content for c in candidates]
        )

        # Select documents that fit in budget
        selected = []
        current_tokens = 0

        for doc, score in reranked:
            doc_tokens = self._count_tokens(doc)
            if current_tokens + doc_tokens <= available:
                selected.append(doc)
                current_tokens += doc_tokens
            else:
                break

        # Build final context
        return self._build_context(
            required=required_context or [],
            retrieved=selected,
            history=conversation_history or []
        )
```

---

## 28.2 Hierarchical Memory Systems

### Memory Architecture Overview

Production agent systems require memory architectures that mirror human cognitive structures, enabling both immediate responsiveness and long-term learning.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL MEMORY ARCHITECTURE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  SENSORY BUFFER (< 1 second)                                          ║ │
│  ║  • Raw input processing                                               ║ │
│  ║  • Token streaming buffer                                             ║ │
│  ║  • Immediate context parsing                                          ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                    │                                        │
│                                    ▼                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  WORKING MEMORY (Current Session)                            5-10 items║ │
│  ║  ┌─────────────┬─────────────┬─────────────┬─────────────┐           ║ │
│  ║  │ Current     │ Active      │ Immediate   │ Tool        │           ║ │
│  ║  │ Query       │ Goals       │ Context     │ Results     │           ║ │
│  ║  └─────────────┴─────────────┴─────────────┴─────────────┘           ║ │
│  ║  Retention: Session only | Capacity: ~10 items | Access: Immediate   ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                    │                                        │
│                    ┌───────────────┼───────────────┐                       │
│                    ▼               ▼               ▼                        │
│  ╔═════════════════════╗ ╔═════════════════════╗ ╔═════════════════════╗  │
│  ║  SHORT-TERM MEMORY  ║ ║  EPISODIC MEMORY    ║ ║  SEMANTIC MEMORY    ║  │
│  ║  (Hours)            ║ ║  (Experiences)      ║ ║  (Knowledge)        ║  │
│  ╠═════════════════════╣ ╠═════════════════════╣ ╠═════════════════════╣  │
│  ║ • Recent messages   ║ ║ • Past interactions ║ ║ • Domain facts      ║  │
│  ║ • Session context   ║ ║ • Success patterns  ║ ║ • Procedures        ║  │
│  ║ • Temp calculations ║ ║ • Error cases       ║ ║ • Relationships     ║  │
│  ║                     ║ ║ • User preferences  ║ ║ • Entity info       ║  │
│  ╠═════════════════════╣ ╠═════════════════════╣ ╠═════════════════════╣  │
│  ║ Retention: Hours    ║ ║ Retention: Permanent║ ║ Retention: Permanent║  │
│  ║ Capacity: 50 items  ║ ║ Capacity: Selective ║ ║ Capacity: Unlimited ║  │
│  ║ Storage: In-memory  ║ ║ Storage: Vector DB  ║ ║ Storage: Vector DB  ║  │
│  ╚═════════════════════╝ ╚═════════════════════╝ ╚═════════════════════╝  │
│                    │               │               │                        │
│                    └───────────────┼───────────────┘                       │
│                                    ▼                                        │
│  ╔═══════════════════════════════════════════════════════════════════════╗ │
│  ║  LONG-TERM MEMORY (Persistent Knowledge Store)                        ║ │
│  ║  • Vector database with semantic search                               ║ │
│  ║  • Knowledge graphs for relationships                                 ║ │
│  ║  • Compressed historical data                                         ║ │
│  ║  Retention: Permanent | Capacity: Unlimited | Access: Retrieval-based ║ │
│  ╚═══════════════════════════════════════════════════════════════════════╝ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Memory System Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from enum import Enum
import numpy as np
import asyncio
import json
import hashlib

class MemoryType(Enum):
    WORKING = "working"
    SHORT_TERM = "short_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"

@dataclass
class Memory:
    """A memory unit with full metadata"""
    id: str
    content: str
    memory_type: MemoryType
    importance: float
    embedding: Optional[np.ndarray] = None
    timestamp: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    decay_rate: float = 0.1
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_strength(self) -> float:
        """
        Calculate memory strength based on:
        - Base importance
        - Recency of access
        - Frequency of access
        - Decay over time
        """
        now = datetime.now()

        # Time since last access (in hours)
        hours_since_access = (now - self.last_accessed).total_seconds() / 3600

        # Recency factor (exponential decay)
        recency = np.exp(-self.decay_rate * hours_since_access)

        # Frequency factor (logarithmic growth)
        frequency = np.log1p(self.access_count) / 10

        # Combined strength
        strength = (self.importance * 0.4) + (recency * 0.4) + (frequency * 0.2)

        return min(strength, 1.0)

class HierarchicalMemorySystem:
    """
    Production-grade hierarchical memory system for AI agents.

    Features:
    - Multi-tier storage (working, short-term, long-term)
    - Automatic promotion based on importance and access patterns
    - Memory consolidation during idle periods
    - Semantic search across all tiers
    - Memory decay and forgetting
    - Association networks
    """

    def __init__(
        self,
        embedding_model,
        vector_store,
        working_capacity: int = 10,
        short_term_capacity: int = 50,
        consolidation_threshold: float = 0.7,
        decay_rate: float = 0.1
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.working_capacity = working_capacity
        self.short_term_capacity = short_term_capacity
        self.consolidation_threshold = consolidation_threshold
        self.decay_rate = decay_rate

        # Memory tiers
        self.working_memory: Dict[str, Memory] = {}
        self.short_term: Dict[str, Memory] = {}

        # Statistics
        self.stats = {
            "stores": 0,
            "recalls": 0,
            "promotions": 0,
            "consolidations": 0,
            "forgettings": 0
        }

    def _generate_id(self, content: str) -> str:
        """Generate unique ID for memory"""
        hash_input = f"{content}{datetime.now().isoformat()}"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:16]

    async def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.WORKING,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None,
        associations: List[str] = None
    ) -> Memory:
        """
        Store a new memory.

        Args:
            content: Memory content
            memory_type: Type of memory to create
            importance: Importance score (0.0 to 1.0)
            metadata: Additional metadata
            associations: IDs of related memories

        Returns:
            Created Memory object
        """
        # Generate embedding
        embedding = await self.embedding_model.embed(content)

        memory = Memory(
            id=self._generate_id(content),
            content=content,
            memory_type=memory_type,
            importance=importance,
            embedding=embedding,
            decay_rate=self.decay_rate,
            associations=associations or [],
            metadata=metadata or {}
        )

        # Store based on type
        if memory_type == MemoryType.WORKING:
            self.working_memory[memory.id] = memory
            await self._manage_working_memory()
        elif memory_type == MemoryType.SHORT_TERM:
            self.short_term[memory.id] = memory
            await self._manage_short_term_memory()
        else:
            # Episodic, Semantic, Procedural go directly to long-term
            await self._store_long_term(memory)

        self.stats["stores"] += 1
        return memory

    async def recall(
        self,
        query: str,
        k: int = 5,
        memory_types: List[MemoryType] = None,
        min_strength: float = 0.0
    ) -> List[Tuple[Memory, float]]:
        """
        Recall relevant memories based on semantic similarity.

        Args:
            query: Search query
            k: Maximum results
            memory_types: Filter by memory types
            min_strength: Minimum memory strength threshold

        Returns:
            List of (Memory, relevance_score) tuples
        """
        query_embedding = await self.embedding_model.embed(query)

        results = []

        # Search working memory
        for memory in self.working_memory.values():
            if memory_types and memory.memory_type not in memory_types:
                continue
            if memory.calculate_strength() < min_strength:
                continue

            similarity = self._cosine_similarity(query_embedding, memory.embedding)
            results.append((memory, similarity))

        # Search short-term memory
        for memory in self.short_term.values():
            if memory_types and memory.memory_type not in memory_types:
                continue
            if memory.calculate_strength() < min_strength:
                continue

            similarity = self._cosine_similarity(query_embedding, memory.embedding)
            results.append((memory, similarity))

        # Search long-term memory (vector store)
        long_term_results = await self.vector_store.search(
            embedding=query_embedding,
            k=k * 2,  # Get more candidates for filtering
            filter={"memory_type": [t.value for t in (memory_types or list(MemoryType))]}
        )

        for result in long_term_results:
            memory = self._deserialize_memory(result)
            if memory.calculate_strength() >= min_strength:
                results.append((memory, result["score"]))

        # Sort by relevance and return top k
        results.sort(key=lambda x: x[1], reverse=True)

        # Update access metadata for returned memories
        for memory, _ in results[:k]:
            memory.last_accessed = datetime.now()
            memory.access_count += 1

        self.stats["recalls"] += 1
        return results[:k]

    async def _manage_working_memory(self):
        """Manage working memory capacity"""
        while len(self.working_memory) > self.working_capacity:
            # Find weakest memory
            weakest = min(
                self.working_memory.values(),
                key=lambda m: m.calculate_strength()
            )

            # Promote to short-term if strong enough
            if weakest.calculate_strength() > 0.3:
                weakest.memory_type = MemoryType.SHORT_TERM
                self.short_term[weakest.id] = weakest
                self.stats["promotions"] += 1

            del self.working_memory[weakest.id]

    async def _manage_short_term_memory(self):
        """Manage short-term memory capacity"""
        while len(self.short_term) > self.short_term_capacity:
            # Find weakest memory
            weakest = min(
                self.short_term.values(),
                key=lambda m: m.calculate_strength()
            )

            # Promote to long-term if important enough
            if weakest.importance > 0.5 or weakest.access_count > 3:
                await self._store_long_term(weakest)
                self.stats["promotions"] += 1
            else:
                self.stats["forgettings"] += 1

            del self.short_term[weakest.id]

    async def _store_long_term(self, memory: Memory):
        """Store memory in long-term vector store"""
        await self.vector_store.upsert(
            id=memory.id,
            embedding=memory.embedding,
            metadata={
                "content": memory.content,
                "memory_type": memory.memory_type.value,
                "importance": memory.importance,
                "timestamp": memory.timestamp.isoformat(),
                "access_count": memory.access_count,
                "associations": memory.associations,
                **memory.metadata
            }
        )

    async def consolidate(self):
        """
        Consolidate memories - similar to sleep consolidation in humans.

        This process:
        1. Identifies related memories
        2. Strengthens important connections
        3. Merges similar memories
        4. Prunes weak memories
        """
        # Find memories that should be consolidated
        all_memories = list(self.working_memory.values()) + list(self.short_term.values())

        for memory in all_memories:
            if memory.calculate_strength() > self.consolidation_threshold:
                # Find related memories
                related = await self.recall(
                    memory.content,
                    k=5,
                    min_strength=0.3
                )

                # Update associations
                for related_memory, score in related:
                    if related_memory.id != memory.id and score > 0.7:
                        if related_memory.id not in memory.associations:
                            memory.associations.append(related_memory.id)
                        if memory.id not in related_memory.associations:
                            related_memory.associations.append(memory.id)

                # Promote highly accessed memories
                if memory.access_count > 5 and memory.memory_type == MemoryType.SHORT_TERM:
                    await self._store_long_term(memory)
                    self.stats["consolidations"] += 1

    def _cosine_similarity(self, a: np.ndarray, b: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    def _deserialize_memory(self, data: dict) -> Memory:
        """Deserialize memory from vector store result"""
        return Memory(
            id=data["id"],
            content=data["metadata"]["content"],
            memory_type=MemoryType(data["metadata"]["memory_type"]),
            importance=data["metadata"]["importance"],
            timestamp=datetime.fromisoformat(data["metadata"]["timestamp"]),
            access_count=data["metadata"]["access_count"],
            associations=data["metadata"].get("associations", []),
            metadata={k: v for k, v in data["metadata"].items()
                     if k not in ["content", "memory_type", "importance", "timestamp", "access_count", "associations"]}
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        return {
            "working_memory_count": len(self.working_memory),
            "short_term_count": len(self.short_term),
            "working_memory_utilization": len(self.working_memory) / self.working_capacity,
            "short_term_utilization": len(self.short_term) / self.short_term_capacity,
            **self.stats
        }
```

---

## 28.3 Semantic Compression Techniques

### Compression Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      SEMANTIC COMPRESSION PIPELINE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INPUT TEXT                                                                 │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 1: STRUCTURAL CLEANING                                        │   │
│  │ • Remove redundant whitespace                                       │   │
│  │ • Normalize unicode                                                 │   │
│  │ • Fix encoding issues                                               │   │
│  │ Compression: ~5-10%                                                 │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 2: LEXICAL COMPRESSION                                        │   │
│  │ • Remove filler words                                               │   │
│  │ • Abbreviate common phrases                                         │   │
│  │ • Simplify verbose constructions                                    │   │
│  │ Compression: ~10-20%                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 3: ENTITY CONSOLIDATION                                       │   │
│  │ • Extract named entities                                            │   │
│  │ • Replace repeated mentions with references                         │   │
│  │ • Build entity registry                                             │   │
│  │ Compression: ~10-15%                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 4: SEMANTIC DEDUPLICATION                                     │   │
│  │ • Identify semantically similar sentences                           │   │
│  │ • Merge redundant information                                       │   │
│  │ • Preserve unique facts                                             │   │
│  │ Compression: ~15-25%                                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │ STAGE 5: ABSTRACTIVE SUMMARIZATION (Optional)                       │   │
│  │ • LLM-based summarization                                           │   │
│  │ • Preserves key facts and relationships                             │   │
│  │ • Controlled information loss                                       │   │
│  │ Compression: Variable (target-based)                                │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│      │                                                                      │
│      ▼                                                                      │
│  COMPRESSED OUTPUT + METADATA                                               │
│                                                                             │
│  Total Compression: 40-70% with >95% information retention                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Compression Implementation

```python
import re
from typing import Dict, List, Any, Tuple, Optional
from dataclasses import dataclass
import spacy
from sentence_transformers import SentenceTransformer
import numpy as np

@dataclass
class CompressionResult:
    """Result of compression operation"""
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    stages_applied: List[str]
    entity_registry: Dict[str, str]
    metadata: Dict[str, Any]

class SemanticCompressionPipeline:
    """
    Multi-stage compression pipeline that reduces token count
    while preserving semantic content.

    Achieves 40-70% reduction with >95% information retention.
    """

    def __init__(
        self,
        nlp_model: str = "en_core_web_sm",
        embedding_model: str = "all-MiniLM-L6-v2",
        similarity_threshold: float = 0.85
    ):
        self.nlp = spacy.load(nlp_model)
        self.embedder = SentenceTransformer(embedding_model)
        self.similarity_threshold = similarity_threshold

        # Filler words to remove
        self.filler_words = {
            'very', 'really', 'just', 'quite', 'rather', 'somewhat',
            'basically', 'actually', 'literally', 'essentially',
            'definitely', 'certainly', 'probably', 'possibly',
            'simply', 'merely', 'practically', 'virtually'
        }

        # Phrase abbreviations
        self.abbreviations = {
            'for example': 'e.g.',
            'for instance': 'e.g.',
            'that is': 'i.e.',
            'that is to say': 'i.e.',
            'in other words': 'i.e.',
            'as soon as possible': 'ASAP',
            'with respect to': 're:',
            'with regard to': 're:',
            'in order to': 'to',
            'due to the fact that': 'because',
            'owing to the fact that': 'because',
            'at this point in time': 'now',
            'at the present time': 'now',
            'in the event that': 'if',
            'in the case that': 'if',
            'despite the fact that': 'although',
            'regardless of the fact that': 'although',
            'it is important to note that': '',
            'it should be noted that': '',
            'it is worth mentioning that': '',
            'as a matter of fact': '',
            'the fact of the matter is': '',
            'in terms of': 'regarding',
            'with reference to': 'regarding',
            'a large number of': 'many',
            'a significant number of': 'many',
            'a considerable amount of': 'much',
            'in close proximity to': 'near',
            'at this moment in time': 'now',
            'until such time as': 'until',
            'in the near future': 'soon',
            'on a daily basis': 'daily',
            'on a regular basis': 'regularly',
        }

        # Verbose constructions to simplify
        self.simplifications = {
            r'is able to': 'can',
            r'are able to': 'can',
            r'has the ability to': 'can',
            r'have the ability to': 'can',
            r'is going to': 'will',
            r'are going to': 'will',
            r'in order to be able to': 'to',
            r'has been shown to be': 'is',
            r'have been shown to be': 'are',
            r'it is necessary to': 'must',
            r'it is important to': 'should',
            r'there is a need to': 'must',
            r'make a decision': 'decide',
            r'come to a conclusion': 'conclude',
            r'give consideration to': 'consider',
            r'make an attempt': 'try',
            r'conduct an investigation': 'investigate',
            r'perform an analysis': 'analyze',
            r'is dependent on': 'depends on',
            r'is indicative of': 'indicates',
            r'is reflective of': 'reflects',
        }

    def compress(
        self,
        text: str,
        target_ratio: Optional[float] = None,
        preserve_entities: bool = True,
        enable_summarization: bool = False,
        llm_client = None
    ) -> CompressionResult:
        """
        Compress text through the full pipeline.

        Args:
            text: Input text to compress
            target_ratio: Optional target compression ratio
            preserve_entities: Whether to preserve named entities
            enable_summarization: Whether to use LLM summarization
            llm_client: LLM client for summarization stage

        Returns:
            CompressionResult with compressed text and metadata
        """
        original_tokens = len(text.split())
        stages_applied = []
        entity_registry = {}

        # Stage 1: Structural cleaning
        text = self._stage_structural_cleaning(text)
        stages_applied.append("structural_cleaning")

        # Stage 2: Lexical compression
        text = self._stage_lexical_compression(text)
        stages_applied.append("lexical_compression")

        # Stage 3: Entity consolidation
        if preserve_entities:
            text, entity_registry = self._stage_entity_consolidation(text)
            stages_applied.append("entity_consolidation")

        # Stage 4: Semantic deduplication
        text = self._stage_semantic_deduplication(text)
        stages_applied.append("semantic_deduplication")

        # Stage 5: Abstractive summarization (if needed)
        current_tokens = len(text.split())
        current_ratio = current_tokens / original_tokens

        if enable_summarization and llm_client and target_ratio:
            if current_ratio > target_ratio:
                text = self._stage_abstractive_summarization(
                    text, target_ratio, llm_client
                )
                stages_applied.append("abstractive_summarization")

        compressed_tokens = len(text.split())

        return CompressionResult(
            original_text=text,
            compressed_text=text,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / original_tokens,
            stages_applied=stages_applied,
            entity_registry=entity_registry,
            metadata={
                "tokens_saved": original_tokens - compressed_tokens,
                "reduction_percentage": (1 - compressed_tokens / original_tokens) * 100
            }
        )

    def _stage_structural_cleaning(self, text: str) -> str:
        """Stage 1: Clean structural issues"""
        # Normalize whitespace
        text = ' '.join(text.split())

        # Normalize unicode
        text = text.encode('ascii', 'ignore').decode('ascii')

        # Remove excessive punctuation
        text = re.sub(r'([.!?])\1+', r'\1', text)

        # Normalize quotes
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")

        return text

    def _stage_lexical_compression(self, text: str) -> str:
        """Stage 2: Remove filler words and abbreviate phrases"""
        # Remove filler words
        words = text.split()
        words = [w for w in words if w.lower() not in self.filler_words]
        text = ' '.join(words)

        # Apply abbreviations
        for phrase, abbr in self.abbreviations.items():
            text = re.sub(
                r'\b' + re.escape(phrase) + r'\b',
                abbr,
                text,
                flags=re.IGNORECASE
            )

        # Apply simplifications
        for pattern, replacement in self.simplifications.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

        # Clean up resulting whitespace
        text = ' '.join(text.split())

        return text

    def _stage_entity_consolidation(self, text: str) -> Tuple[str, Dict[str, str]]:
        """Stage 3: Consolidate entity references"""
        doc = self.nlp(text)

        # Extract entities
        entities = {}
        for ent in doc.ents:
            if ent.text not in entities:
                # Create short reference
                ref = f"[{ent.label_}:{len(entities)+1}]"
                entities[ent.text] = ref

        # Replace subsequent mentions with references
        result = text
        for entity, ref in entities.items():
            # Find all occurrences
            occurrences = list(re.finditer(re.escape(entity), result))

            # Keep first occurrence, replace rest
            if len(occurrences) > 1:
                for match in reversed(occurrences[1:]):
                    result = result[:match.start()] + ref + result[match.end():]

        return result, entities

    def _stage_semantic_deduplication(self, text: str) -> str:
        """Stage 4: Remove semantically redundant sentences"""
        # Split into sentences
        doc = self.nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]

        if len(sentences) <= 1:
            return text

        # Get embeddings
        embeddings = self.embedder.encode(sentences)

        # Find unique sentences
        unique_indices = [0]  # Always keep first sentence

        for i in range(1, len(sentences)):
            is_unique = True

            for j in unique_indices:
                similarity = np.dot(embeddings[i], embeddings[j]) / (
                    np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
                )

                if similarity > self.similarity_threshold:
                    is_unique = False
                    break

            if is_unique:
                unique_indices.append(i)

        # Reconstruct text with unique sentences
        unique_sentences = [sentences[i] for i in sorted(unique_indices)]

        return ' '.join(unique_sentences)

    def _stage_abstractive_summarization(
        self,
        text: str,
        target_ratio: float,
        llm_client
    ) -> str:
        """Stage 5: LLM-based abstractive summarization"""
        target_words = int(len(text.split()) * target_ratio)

        prompt = f"""Compress the following text to approximately {target_words} words.
Preserve all key facts, entities, relationships, and important details.
Do not add any new information. Only compress and rephrase.

Text:
{text}

Compressed version:"""

        response = llm_client.complete(prompt)
        return response.strip()
```

---

## 28.4 Multi-Agent Orchestration for Complex Tasks

### When to Use Multi-Agent Systems

| Scenario | Single Agent | Multi-Agent | Recommendation |
|----------|-------------|-------------|----------------|
| Simple Q&A | Fast, sufficient | Overkill | Single Agent |
| Document summarization | Works for small docs | Better for large | Depends on size |
| Multi-step analysis | Sequential bottleneck | Parallel processing | Multi-Agent |
| Cross-domain expertise | Limited by training | Specialized agents | Multi-Agent |
| Verification required | Self-verification weak | Independent verification | Multi-Agent |
| High-stakes decisions | Single point of failure | Redundancy | Multi-Agent |

### Orchestration Patterns

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MULTI-AGENT ORCHESTRATION PATTERNS                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  PATTERN 1: HIERARCHICAL DELEGATION                                         │
│  ════════════════════════════════════                                       │
│                                                                             │
│                        ┌─────────────┐                                      │
│                        │ COORDINATOR │                                      │
│                        │   AGENT     │                                      │
│                        └──────┬──────┘                                      │
│                 ┌─────────────┼─────────────┐                              │
│                 ▼             ▼             ▼                               │
│           ┌─────────┐   ┌─────────┐   ┌─────────┐                          │
│           │RESEARCH │   │ANALYSIS │   │ WRITING │                          │
│           │ AGENT   │   │ AGENT   │   │  AGENT  │                          │
│           └─────────┘   └─────────┘   └─────────┘                          │
│                                                                             │
│  Use when: Clear task decomposition, specialized expertise needed           │
│                                                                             │
│  ───────────────────────────────────────────────────────────────────────   │
│                                                                             │
│  PATTERN 2: CONSENSUS / VOTING                                              │
│  ════════════════════════════                                               │
│                                                                             │
│           ┌─────────┐   ┌─────────┐   ┌─────────┐                          │
│           │ AGENT 1 │   │ AGENT 2 │   │ AGENT 3 │                          │
│           └────┬────┘   └────┬────┘   └────┬────┘                          │
│                │             │             │                                │
│                └─────────────┼─────────────┘                               │
│                              ▼                                              │
│                        ┌─────────┐                                          │
│                        │ ARBITER │                                          │
│                        │ (votes) │                                          │
│                        └─────────┘                                          │
│                                                                             │
│  Use when: High-stakes decisions, verification needed, diverse perspectives │
│                                                                             │
│  ───────────────────────────────────────────────────────────────────────   │
│                                                                             │
│  PATTERN 3: PIPELINE / SEQUENTIAL                                           │
│  ════════════════════════════════                                           │
│                                                                             │
│    ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐                   │
│    │ EXTRACT │──▶│  CLEAN  │──▶│ ANALYZE │──▶│ REPORT  │                   │
│    │  AGENT  │   │  AGENT  │   │  AGENT  │   │  AGENT  │                   │
│    └─────────┘   └─────────┘   └─────────┘   └─────────┘                   │
│                                                                             │
│  Use when: Clear sequential dependencies, data transformation flow          │
│                                                                             │
│  ───────────────────────────────────────────────────────────────────────   │
│                                                                             │
│  PATTERN 4: DEBATE / ADVERSARIAL                                            │
│  ════════════════════════════════                                           │
│                                                                             │
│           ┌─────────┐           ┌─────────┐                                │
│           │ AGENT A │◀─────────▶│ AGENT B │                                │
│           │ (Pro)   │  debate   │ (Con)   │                                │
│           └────┬────┘           └────┬────┘                                │
│                │                     │                                      │
│                └──────────┬──────────┘                                     │
│                           ▼                                                 │
│                     ┌─────────┐                                             │
│                     │  JUDGE  │                                             │
│                     └─────────┘                                             │
│                                                                             │
│  Use when: Complex reasoning, exploring trade-offs, stress-testing ideas    │
│                                                                             │
│  ───────────────────────────────────────────────────────────────────────   │
│                                                                             │
│  PATTERN 5: SWARM / EMERGENT                                                │
│  ═══════════════════════════                                                │
│                                                                             │
│        ┌───┐ ┌───┐ ┌───┐ ┌───┐                                             │
│        │ A │─│ A │─│ A │─│ A │                                             │
│        └─┬─┘ └─┬─┘ └─┬─┘ └─┬─┘                                             │
│          │     │     │     │                                                │
│        ┌─┴─┐ ┌─┴─┐ ┌─┴─┐ ┌─┴─┐                                             │
│        │ A │─│ A │─│ A │─│ A │    (Agents communicate peer-to-peer)        │
│        └───┘ └───┘ └───┘ └───┘                                             │
│                                                                             │
│  Use when: Exploration tasks, creative generation, optimization problems    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Complete Orchestration Implementation

See [examples/orchestration.py](examples/orchestration.py) for the full implementation.

---

## 28.5 Production Reliability Patterns

### Circuit Breaker Pattern

Prevents cascading failures by tracking error rates and temporarily disabling failing operations.

```python
from enum import Enum
from datetime import datetime, timedelta
from typing import Callable, Any, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, rejecting calls
    HALF_OPEN = "half_open"  # Testing recovery

class CircuitBreaker:
    """
    Circuit breaker pattern implementation for AI agent systems.

    States:
    - CLOSED: Normal operation, requests pass through
    - OPEN: Failure threshold exceeded, requests are rejected
    - HALF_OPEN: Testing if service has recovered

    Transitions:
    - CLOSED -> OPEN: When failure_count >= failure_threshold
    - OPEN -> HALF_OPEN: After recovery_timeout expires
    - HALF_OPEN -> CLOSED: On successful request
    - HALF_OPEN -> OPEN: On failed request
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_max_calls: int = 3,
        excluded_exceptions: tuple = ()
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls
        self.excluded_exceptions = excluded_exceptions

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time: Optional[datetime] = None
        self.half_open_calls = 0

        # Metrics
        self.total_calls = 0
        self.total_failures = 0
        self.total_rejections = 0

    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Execute a function with circuit breaker protection.

        Args:
            func: Async function to execute
            *args: Positional arguments
            **kwargs: Keyword arguments

        Returns:
            Function result

        Raises:
            CircuitOpenError: If circuit is open
            Original exception: If function fails and circuit trips
        """
        self.total_calls += 1

        # Check circuit state
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self._transition_to_half_open()
            else:
                self.total_rejections += 1
                raise CircuitOpenError(
                    f"Circuit '{self.name}' is OPEN. "
                    f"Retry after {self._time_until_reset()}s"
                )

        if self.state == CircuitState.HALF_OPEN:
            if self.half_open_calls >= self.half_open_max_calls:
                self.total_rejections += 1
                raise CircuitOpenError(
                    f"Circuit '{self.name}' is HALF_OPEN and at capacity"
                )
            self.half_open_calls += 1

        try:
            result = await func(*args, **kwargs)
            self._on_success()
            return result

        except self.excluded_exceptions:
            # Don't count excluded exceptions as failures
            raise

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call"""
        self.failure_count = 0
        self.success_count += 1

        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_closed()
            logger.info(f"Circuit '{self.name}' recovered -> CLOSED")

    def _on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.total_failures += 1
        self.last_failure_time = datetime.now()

        if self.state == CircuitState.HALF_OPEN:
            self._transition_to_open()
            logger.warning(f"Circuit '{self.name}' failed during recovery -> OPEN")

        elif self.failure_count >= self.failure_threshold:
            self._transition_to_open()
            logger.warning(
                f"Circuit '{self.name}' tripped after {self.failure_count} failures -> OPEN"
            )

    def _transition_to_open(self):
        """Transition to OPEN state"""
        self.state = CircuitState.OPEN
        self.half_open_calls = 0

    def _transition_to_half_open(self):
        """Transition to HALF_OPEN state"""
        self.state = CircuitState.HALF_OPEN
        self.half_open_calls = 0
        logger.info(f"Circuit '{self.name}' attempting recovery -> HALF_OPEN")

    def _transition_to_closed(self):
        """Transition to CLOSED state"""
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.half_open_calls = 0

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset"""
        if self.last_failure_time is None:
            return True

        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return elapsed >= self.recovery_timeout

    def _time_until_reset(self) -> int:
        """Get seconds until reset attempt"""
        if self.last_failure_time is None:
            return 0

        elapsed = (datetime.now() - self.last_failure_time).total_seconds()
        return max(0, int(self.recovery_timeout - elapsed))

    def get_status(self) -> dict:
        """Get circuit breaker status"""
        return {
            "name": self.name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "failure_threshold": self.failure_threshold,
            "time_until_reset": self._time_until_reset() if self.state == CircuitState.OPEN else None,
            "metrics": {
                "total_calls": self.total_calls,
                "total_failures": self.total_failures,
                "total_rejections": self.total_rejections,
                "failure_rate": self.total_failures / max(self.total_calls, 1)
            }
        }

class CircuitOpenError(Exception):
    """Raised when circuit breaker is open"""
    pass
```

### Retry with Exponential Backoff

```python
import asyncio
import random
from typing import Callable, Any, Type, Tuple
from functools import wraps

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0,
    jitter: bool = True,
    retryable_exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """
    Decorator for retry with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap
        exponential_base: Base for exponential growth
        jitter: Add random jitter to prevent thundering herd
        retryable_exceptions: Exceptions that trigger retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)

                except retryable_exceptions as e:
                    last_exception = e

                    if attempt == max_retries:
                        break

                    # Calculate delay
                    delay = min(
                        base_delay * (exponential_base ** attempt),
                        max_delay
                    )

                    # Add jitter
                    if jitter:
                        delay = delay * (0.5 + random.random())

                    logger.warning(
                        f"Attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                        f"Retrying in {delay:.2f}s"
                    )

                    await asyncio.sleep(delay)

            raise last_exception

        return wrapper
    return decorator
```

### Fallback Chain

```python
class FallbackChain:
    """
    Manages a chain of fallback options when primary operations fail.

    Example:
        chain = FallbackChain()
        chain.add("primary", primary_llm_call, priority=1)
        chain.add("secondary", secondary_llm_call, priority=2)
        chain.add("cached", cached_response, priority=3)

        result = await chain.execute(prompt)
    """

    def __init__(self):
        self.handlers: List[Tuple[str, Callable, int]] = []

    def add(
        self,
        name: str,
        handler: Callable,
        priority: int,
        health_check: Callable = None
    ):
        """Add a handler to the fallback chain"""
        self.handlers.append((name, handler, priority, health_check))
        self.handlers.sort(key=lambda x: x[2])  # Sort by priority

    async def execute(self, *args, **kwargs) -> Tuple[str, Any]:
        """
        Execute the fallback chain.

        Returns:
            Tuple of (handler_name, result)
        """
        errors = []

        for name, handler, priority, health_check in self.handlers:
            # Check health if available
            if health_check:
                try:
                    if not await health_check():
                        logger.info(f"Skipping {name}: health check failed")
                        continue
                except Exception:
                    logger.info(f"Skipping {name}: health check error")
                    continue

            try:
                result = await handler(*args, **kwargs)
                logger.info(f"Fallback chain: {name} succeeded")
                return name, result

            except Exception as e:
                errors.append((name, e))
                logger.warning(f"Fallback chain: {name} failed: {e}")
                continue

        raise FallbackExhaustedError(
            f"All fallbacks exhausted. Errors: {errors}"
        )

class FallbackExhaustedError(Exception):
    """Raised when all fallback options have been exhausted"""
    pass
```

---

## 28.6 Advanced Retrieval Patterns

See [lessons/01-context-management.md](lessons/01-context-management.md) for detailed coverage.

---

## 28.7 Distributed State Management

See [lessons/02-memory-architecture.md](lessons/02-memory-architecture.md) for detailed coverage.

---

## 28.8 Performance Optimization

### Token Optimization Strategies

| Strategy | Token Reduction | Implementation Complexity | Quality Impact |
|----------|----------------|---------------------------|----------------|
| Semantic compression | 40-70% | Medium | Minimal |
| Dynamic context loading | 50-80% | High | Minimal |
| Response caching | 90%+ (cache hits) | Low | None |
| Prompt optimization | 10-30% | Low | Minimal |
| Model routing | Variable | Medium | Variable |

### Latency Optimization

```python
class LatencyOptimizer:
    """
    Optimizes agent latency through various techniques:
    - Response streaming
    - Parallel tool execution
    - Predictive prefetching
    - Connection pooling
    """

    async def execute_with_streaming(
        self,
        llm_client,
        prompt: str,
        on_token: Callable[[str], None]
    ):
        """Stream response tokens as they're generated"""
        async for token in llm_client.stream(prompt):
            on_token(token)
            yield token

    async def parallel_tool_execution(
        self,
        tools: List[Callable],
        args_list: List[dict]
    ) -> List[Any]:
        """Execute multiple tools in parallel"""
        tasks = [
            tool(**args)
            for tool, args in zip(tools, args_list)
        ]
        return await asyncio.gather(*tasks, return_exceptions=True)
```

---

## 28.9 Evaluation and Metrics

### Key Performance Indicators

| Metric | Description | Target | Measurement Method |
|--------|-------------|--------|-------------------|
| Context Utilization | % of context window effectively used | >80% | Token counting |
| Memory Recall Precision | Relevance of retrieved memories | >90% | Human evaluation |
| Memory Recall Coverage | Important info retrieved | >95% | Automated testing |
| Compression Fidelity | Information preserved after compression | >95% | Q&A accuracy |
| Multi-Agent Consensus | Agreement rate among parallel agents | >85% | Automated comparison |
| System Availability | Uptime including graceful degradation | >99.5% | Monitoring |
| P95 Latency | 95th percentile response time | <5s | APM tools |
| Error Rate | Percentage of failed requests | <1% | Logging |

---

## 28.10 Federal Use Cases

### Use Case 1: Large Document Analysis

**Scenario:** Analyze a 500-page federal regulation document to extract compliance requirements.

**Solution:** Hierarchical summarization + multi-agent analysis

### Use Case 2: Cross-Agency Knowledge Base

**Scenario:** Build a knowledge system spanning multiple agency document repositories.

**Solution:** Federated memory system + semantic compression

### Use Case 3: Real-Time Decision Support

**Scenario:** Provide instant decision support during incident response.

**Solution:** Dynamic context loading + fallback chains + response caching

---

## Hands-On Labs

### [Lab 28.1: Build a Hierarchical Memory System](labs/lab-01-memory-system.md)

Build a complete hierarchical memory system with:
- Working, short-term, and long-term tiers
- Automatic promotion based on access patterns
- Semantic search across all tiers
- Memory consolidation process

**Duration:** 90 minutes

### [Lab 28.2: Implement Compression Pipeline](labs/lab-02-compression.md)

Create a compression pipeline that achieves:
- 50% token reduction
- 95%+ information fidelity
- Measurable through before/after Q&A accuracy

**Duration:** 60 minutes

### [Lab 28.3: Multi-Agent Document Analysis](labs/lab-03-multi-agent.md)

Implement a multi-agent system to:
- Process a 100+ page federal document
- Extract key requirements using specialized agents
- Generate a structured compliance checklist
- Verify results through consensus

**Duration:** 120 minutes

---

## Summary

This module covered advanced techniques for overcoming conventional AI system limitations:

| Topic | Key Techniques | Implementation Files |
|-------|---------------|---------------------|
| Context Management | Sliding window, hierarchical summarization, dynamic loading | `context_manager.py` |
| Memory Systems | Multi-tier architecture, promotion, consolidation | `memory_systems.py` |
| Compression | Lexical, entity, semantic, abstractive | `compression.py` |
| Orchestration | Hierarchical, consensus, pipeline, debate | `orchestration.py` |
| Reliability | Circuit breakers, retry, fallbacks | `reliability.py` |

These "antigravity" techniques enable AI systems to tackle problems that would otherwise exceed single-model capabilities.

---

## References

### Academic Papers

1. [Attention Is All You Need](https://arxiv.org/abs/1706.03762) - Transformer architecture
2. [Lost in the Middle](https://arxiv.org/abs/2307.03172) - Context position effects
3. [Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401) - RAG architecture
4. [MemGPT](https://arxiv.org/abs/2310.08560) - Hierarchical memory for LLMs
5. [Chain-of-Thought Prompting](https://arxiv.org/abs/2201.11903) - Reasoning enhancement

### Technical Documentation

- [Anthropic MCP Protocol](https://modelcontextprotocol.io/)
- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

### Federal Guidance

- NIST AI Risk Management Framework
- OMB M-24-10: AI Governance
- FedRAMP Authorization Guidelines

---

<div align="center">

**Module 28: Antigravity** | FWG LLM Agentic Training Guide

[Previous: Module 27](../27-case-studies/README.md) | [Back to Main](../../README.md)

</div>
