# Lab 28.1: Build a Hierarchical Memory System

## Overview

In this lab, you will build a production-grade hierarchical memory system for AI agents. This system implements multiple memory tiers with automatic promotion, semantic search, and memory consolidation.

**Duration:** 90 minutes
**Difficulty:** Advanced
**Prerequisites:** Modules 10 (RAG Systems), 14 (Memory & Context)

## Learning Objectives

By completing this lab, you will:

1. Implement a multi-tier memory architecture
2. Build automatic memory promotion based on access patterns
3. Integrate semantic search across memory tiers
4. Create a memory consolidation process

## Requirements

### Software
- Python 3.10+
- pip packages: `sentence-transformers`, `chromadb`, `numpy`

### API Keys
- None required (uses local models and storage)

## Setup

```bash
# Create lab directory
mkdir -p lab-28-1-memory && cd lab-28-1-memory

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install sentence-transformers chromadb numpy pydantic
```

## Part 1: Memory Data Structures (20 minutes)

### Task 1.1: Define the Memory Item

Create `memory_item.py`:

```python
"""
Task: Define the Memory data class with all required fields.

Requirements:
1. Unique identifier
2. Content string
3. Memory type (enum: WORKING, SHORT_TERM, EPISODIC, SEMANTIC)
4. Importance score (0.0 to 1.0)
5. Embedding vector (optional)
6. Timestamps (created, last_accessed)
7. Access count
8. Decay rate
9. Associations (list of related memory IDs)
10. Metadata dictionary
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from enum import Enum
import numpy as np

class MemoryType(Enum):
    WORKING = "working"
    SHORT_TERM = "short_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"

@dataclass
class Memory:
    # TODO: Implement the Memory dataclass
    # Hint: Use field(default_factory=...) for mutable defaults
    pass

    def calculate_strength(self) -> float:
        """
        Calculate memory strength based on:
        - Base importance (40%)
        - Recency of access (40%)
        - Frequency of access (20%)

        Returns:
            float: Memory strength between 0.0 and 1.0
        """
        # TODO: Implement strength calculation
        pass
```

### Task 1.2: Implement Strength Calculation

The memory strength formula should be:

```
strength = (importance * 0.4) + (recency * 0.4) + (frequency * 0.2)

where:
- recency = exp(-decay_rate * hours_since_access)
- frequency = log(1 + access_count) / 10
```

**Expected Output:**
```python
memory = Memory(
    id="test_1",
    content="Test content",
    memory_type=MemoryType.WORKING,
    importance=0.8,
    timestamp=datetime.now(),
    last_accessed=datetime.now(),
    access_count=5,
    decay_rate=0.1
)
print(memory.calculate_strength())  # Should be ~0.45-0.55
```

## Part 2: Working Memory Tier (25 minutes)

### Task 2.1: Implement Working Memory

Create `working_memory.py`:

```python
"""
Task: Implement the working memory tier.

Working memory characteristics:
- Limited capacity (default: 10 items)
- Immediate access (no retrieval needed)
- Automatic overflow to short-term memory
- Eviction based on strength
"""

from typing import Dict, List, Optional
from memory_item import Memory, MemoryType

class WorkingMemory:
    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.memories: Dict[str, Memory] = {}

    def store(self, memory: Memory) -> bool:
        """
        Store a memory in working memory.

        If at capacity, evict the weakest memory first.

        Returns:
            bool: True if stored successfully
        """
        # TODO: Implement storage with eviction
        pass

    def recall(self, memory_id: str) -> Optional[Memory]:
        """
        Recall a specific memory by ID.

        Updates access metadata.
        """
        # TODO: Implement recall with access tracking
        pass

    def get_all(self) -> List[Memory]:
        """Return all memories in working memory"""
        # TODO: Implement
        pass

    def evict_weakest(self) -> Optional[Memory]:
        """
        Remove and return the weakest memory.

        Used for overflow to short-term memory.
        """
        # TODO: Implement eviction
        pass

    def get_stats(self) -> dict:
        """Return working memory statistics"""
        # TODO: Implement
        pass
```

### Task 2.2: Test Working Memory

Create `test_working_memory.py`:

```python
"""Test cases for working memory"""
import unittest
from datetime import datetime
from memory_item import Memory, MemoryType
from working_memory import WorkingMemory

class TestWorkingMemory(unittest.TestCase):
    def test_basic_storage(self):
        wm = WorkingMemory(capacity=3)

        m1 = Memory(
            id="1", content="First", memory_type=MemoryType.WORKING,
            importance=0.5, timestamp=datetime.now(),
            last_accessed=datetime.now()
        )

        self.assertTrue(wm.store(m1))
        self.assertEqual(len(wm.get_all()), 1)

    def test_capacity_eviction(self):
        wm = WorkingMemory(capacity=2)

        # Store 3 memories (should evict 1)
        for i in range(3):
            wm.store(Memory(
                id=str(i), content=f"Memory {i}",
                memory_type=MemoryType.WORKING,
                importance=0.3 + (i * 0.1),
                timestamp=datetime.now(),
                last_accessed=datetime.now()
            ))

        self.assertEqual(len(wm.get_all()), 2)
        # Lowest importance should be evicted
        self.assertIsNone(wm.recall("0"))

    def test_recall_updates_access(self):
        wm = WorkingMemory()
        m = Memory(
            id="1", content="Test", memory_type=MemoryType.WORKING,
            importance=0.5, timestamp=datetime.now(),
            last_accessed=datetime.now(), access_count=0
        )
        wm.store(m)

        recalled = wm.recall("1")
        self.assertEqual(recalled.access_count, 1)

if __name__ == "__main__":
    unittest.main()
```

## Part 3: Hierarchical Memory System (30 minutes)

### Task 3.1: Implement the Full System

Create `hierarchical_memory.py`:

```python
"""
Task: Implement the complete hierarchical memory system.

Features:
1. Working memory (in-memory, limited capacity)
2. Short-term memory (in-memory, larger capacity)
3. Long-term memory (vector database)
4. Automatic promotion between tiers
5. Semantic search across all tiers
"""

from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb

from memory_item import Memory, MemoryType
from working_memory import WorkingMemory

class HierarchicalMemorySystem:
    def __init__(
        self,
        working_capacity: int = 10,
        short_term_capacity: int = 50,
        embedding_model: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./memory_db"
    ):
        # Initialize embedding model
        self.embedder = SentenceTransformer(embedding_model)

        # Initialize memory tiers
        self.working_memory = WorkingMemory(working_capacity)
        self.short_term: Dict[str, Memory] = {}
        self.short_term_capacity = short_term_capacity

        # Initialize vector store for long-term memory
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.long_term = self.client.get_or_create_collection(
            name="long_term_memory",
            metadata={"hnsw:space": "cosine"}
        )

        # Statistics
        self.stats = {
            "stores": 0,
            "recalls": 0,
            "promotions": 0
        }

    def _generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text"""
        return self.embedder.encode(text)

    async def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.WORKING,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> Memory:
        """
        Store a new memory.

        Workflow:
        1. Generate embedding
        2. Create Memory object
        3. Store in appropriate tier
        4. Handle overflow/promotion
        """
        # TODO: Implement complete store logic
        pass

    async def recall(
        self,
        query: str,
        k: int = 5,
        memory_types: List[MemoryType] = None,
        min_strength: float = 0.0
    ) -> List[Tuple[Memory, float]]:
        """
        Recall relevant memories using semantic search.

        Searches all tiers and combines results.

        Returns:
            List of (Memory, relevance_score) tuples
        """
        # TODO: Implement semantic search across tiers
        pass

    async def consolidate(self):
        """
        Consolidate memories (like sleep consolidation).

        Process:
        1. Find strong memories in short-term
        2. Identify associations
        3. Promote to long-term if warranted
        4. Update association networks
        """
        # TODO: Implement consolidation
        pass

    def _manage_short_term(self):
        """Manage short-term memory capacity"""
        while len(self.short_term) > self.short_term_capacity:
            # Find and promote/forget weakest
            weakest_id = min(
                self.short_term.keys(),
                key=lambda k: self.short_term[k].calculate_strength()
            )
            weakest = self.short_term.pop(weakest_id)

            # Promote if important enough
            if weakest.importance > 0.5 or weakest.access_count > 3:
                self._store_long_term(weakest)
                self.stats["promotions"] += 1

    def _store_long_term(self, memory: Memory):
        """Store memory in long-term vector database"""
        self.long_term.upsert(
            ids=[memory.id],
            embeddings=[memory.embedding.tolist()],
            metadatas=[{
                "content": memory.content,
                "memory_type": memory.memory_type.value,
                "importance": memory.importance,
                "timestamp": memory.timestamp.isoformat(),
                "access_count": memory.access_count
            }]
        )

    def get_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "working_memory": self.working_memory.get_stats(),
            "short_term_count": len(self.short_term),
            "long_term_count": self.long_term.count(),
            **self.stats
        }
```

### Task 3.2: Implement Semantic Search

The recall method should:

1. Generate query embedding
2. Search working memory (cosine similarity)
3. Search short-term memory (cosine similarity)
4. Search long-term memory (vector database query)
5. Combine and rank results
6. Update access metadata for returned memories

```python
async def recall(
    self,
    query: str,
    k: int = 5,
    memory_types: List[MemoryType] = None,
    min_strength: float = 0.0
) -> List[Tuple[Memory, float]]:
    """
    Implementation hints:

    1. Generate query embedding:
       query_embedding = self._generate_embedding(query)

    2. Search working memory:
       for memory in self.working_memory.get_all():
           similarity = cosine_similarity(query_embedding, memory.embedding)
           if similarity > threshold:
               results.append((memory, similarity))

    3. Search short-term:
       Similar to working memory

    4. Search long-term (using ChromaDB):
       results = self.long_term.query(
           query_embeddings=[query_embedding.tolist()],
           n_results=k * 2
       )

    5. Combine, filter by strength, sort, return top k
    """
    pass
```

## Part 4: Integration Test (15 minutes)

### Task 4.1: Create Integration Test

Create `test_integration.py`:

```python
"""
Integration test for hierarchical memory system.

Scenario: Document analysis assistant that:
1. Stores key facts from documents
2. Recalls relevant information for questions
3. Consolidates important patterns
"""

import asyncio
from hierarchical_memory import HierarchicalMemorySystem
from memory_item import MemoryType

async def main():
    # Initialize system
    memory = HierarchicalMemorySystem(
        working_capacity=5,
        short_term_capacity=20
    )

    # Simulate document analysis
    facts = [
        ("The Federal AI Act requires agencies to inventory all AI systems.", 0.9),
        ("AI systems must be tested for bias before deployment.", 0.85),
        ("Annual reviews are required for high-impact AI.", 0.8),
        ("Low-risk AI systems have reduced documentation requirements.", 0.6),
        ("Agencies must designate a Chief AI Officer.", 0.9),
        ("Public notice is required for rights-impacting AI.", 0.85),
        ("AI procurement must follow FedRAMP guidelines.", 0.7),
        ("Training data must be documented and auditable.", 0.75),
    ]

    print("=== Storing Facts ===")
    for content, importance in facts:
        await memory.store(
            content=content,
            memory_type=MemoryType.SEMANTIC,
            importance=importance
        )
        print(f"Stored: {content[:50]}...")

    print("\n=== Memory Stats ===")
    print(memory.get_stats())

    # Test recall
    print("\n=== Recall Test ===")
    queries = [
        "What are the requirements for AI system testing?",
        "Who is responsible for AI oversight?",
        "What documentation is needed?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        results = await memory.recall(query, k=3)
        for mem, score in results:
            print(f"  [{score:.3f}] {mem.content[:60]}...")

    # Test consolidation
    print("\n=== Consolidation ===")
    await memory.consolidate()
    print("Consolidation complete")
    print(memory.get_stats())

if __name__ == "__main__":
    asyncio.run(main())
```

## Deliverables

1. **memory_item.py** - Memory data class with strength calculation
2. **working_memory.py** - Working memory tier implementation
3. **hierarchical_memory.py** - Complete system implementation
4. **test_integration.py** - Integration test with results

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Memory strength calculation is accurate | 15 |
| Working memory handles capacity correctly | 20 |
| Semantic search returns relevant results | 25 |
| Memory promotion works correctly | 20 |
| Consolidation identifies associations | 10 |
| Code quality and documentation | 10 |
| **Total** | **100** |

## Extension Challenges

1. **Add episodic memory**: Store complete interaction sequences
2. **Implement forgetting**: Remove memories that decay below threshold
3. **Add memory editing**: Update existing memories with new information
4. **Create memory visualization**: Build a simple UI to explore memory contents

## Solution

A complete solution is available in `examples/memory_systems.py`.
