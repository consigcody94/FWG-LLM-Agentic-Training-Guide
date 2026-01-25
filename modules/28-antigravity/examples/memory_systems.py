"""
Hierarchical Memory Systems - Reference Implementation

This module provides a complete implementation of a multi-tier
memory system for AI agents, including working memory, short-term
memory, and long-term memory with vector storage.

Part of Module 28: Antigravity - Advanced Agent Techniques
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import math
import uuid
import json


class MemoryType(Enum):
    """Types of memory in the hierarchical system."""
    WORKING = "working"
    SHORT_TERM = "short_term"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"


@dataclass
class Memory:
    """
    Core memory data structure.

    Attributes:
        id: Unique identifier
        content: The memory content
        memory_type: Classification of memory type
        importance: Base importance score (0.0 to 1.0)
        embedding: Vector representation (optional)
        timestamp: When memory was created
        last_accessed: When memory was last retrieved
        access_count: Number of times accessed
        decay_rate: How quickly memory strength decays
        associations: Related memory IDs
        metadata: Additional key-value data
    """
    id: str
    content: str
    memory_type: MemoryType
    importance: float
    embedding: Optional[List[float]] = None
    timestamp: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)
    access_count: int = 0
    decay_rate: float = 0.1
    associations: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def calculate_strength(self) -> float:
        """
        Calculate memory strength based on importance, recency, and frequency.

        Formula:
            strength = (importance * 0.4) + (recency * 0.4) + (frequency * 0.2)

        Where:
            - recency = exp(-decay_rate * hours_since_access)
            - frequency = log(1 + access_count) / 10, capped at 1.0

        Returns:
            float: Memory strength between 0.0 and 1.0
        """
        # Calculate hours since last access
        hours_elapsed = (
            datetime.now() - self.last_accessed
        ).total_seconds() / 3600

        # Recency factor (exponential decay)
        recency = math.exp(-self.decay_rate * hours_elapsed)

        # Frequency factor (logarithmic scaling)
        frequency = min(math.log(1 + self.access_count) / 10, 1.0)

        # Combined strength
        strength = (
            self.importance * 0.4 +
            recency * 0.4 +
            frequency * 0.2
        )

        return min(max(strength, 0.0), 1.0)

    def access(self) -> "Memory":
        """Record an access to this memory."""
        self.last_accessed = datetime.now()
        self.access_count += 1
        return self

    def to_dict(self) -> Dict[str, Any]:
        """Convert memory to dictionary for serialization."""
        return {
            "id": self.id,
            "content": self.content,
            "memory_type": self.memory_type.value,
            "importance": self.importance,
            "embedding": self.embedding,
            "timestamp": self.timestamp.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
            "access_count": self.access_count,
            "decay_rate": self.decay_rate,
            "associations": self.associations,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Memory":
        """Create memory from dictionary."""
        return cls(
            id=data["id"],
            content=data["content"],
            memory_type=MemoryType(data["memory_type"]),
            importance=data["importance"],
            embedding=data.get("embedding"),
            timestamp=datetime.fromisoformat(data["timestamp"]),
            last_accessed=datetime.fromisoformat(data["last_accessed"]),
            access_count=data.get("access_count", 0),
            decay_rate=data.get("decay_rate", 0.1),
            associations=data.get("associations", []),
            metadata=data.get("metadata", {})
        )


class WorkingMemory:
    """
    Working memory tier - immediate, limited capacity storage.

    Characteristics:
        - Limited capacity (default: 10 items)
        - Immediate access (no retrieval delay)
        - Automatic eviction of weakest memories
        - Overflow triggers promotion to short-term memory
    """

    def __init__(self, capacity: int = 10):
        self.capacity = capacity
        self.memories: Dict[str, Memory] = {}

    def store(self, memory: Memory) -> Optional[Memory]:
        """
        Store a memory in working memory.

        If at capacity, evicts and returns the weakest memory.

        Returns:
            Optional[Memory]: Evicted memory if capacity exceeded
        """
        evicted = None

        # Check capacity
        if len(self.memories) >= self.capacity:
            evicted = self.evict_weakest()

        # Store new memory
        memory.memory_type = MemoryType.WORKING
        self.memories[memory.id] = memory

        return evicted

    def recall(self, memory_id: str) -> Optional[Memory]:
        """
        Recall a specific memory by ID.

        Updates access metadata on retrieval.
        """
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.access()
            return memory
        return None

    def get_all(self) -> List[Memory]:
        """Return all memories in working memory."""
        return list(self.memories.values())

    def evict_weakest(self) -> Optional[Memory]:
        """
        Remove and return the weakest memory.

        Used for overflow to short-term memory.
        """
        if not self.memories:
            return None

        # Find memory with lowest strength
        weakest_id = min(
            self.memories.keys(),
            key=lambda k: self.memories[k].calculate_strength()
        )

        return self.memories.pop(weakest_id)

    def remove(self, memory_id: str) -> Optional[Memory]:
        """Remove a specific memory by ID."""
        return self.memories.pop(memory_id, None)

    def clear(self):
        """Clear all working memory."""
        self.memories.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Return working memory statistics."""
        memories = list(self.memories.values())
        strengths = [m.calculate_strength() for m in memories]

        return {
            "count": len(self.memories),
            "capacity": self.capacity,
            "utilization": len(self.memories) / self.capacity,
            "avg_strength": sum(strengths) / len(strengths) if strengths else 0,
            "min_strength": min(strengths) if strengths else 0,
            "max_strength": max(strengths) if strengths else 0
        }


class ShortTermMemory:
    """
    Short-term memory tier - larger capacity, moderate access time.

    Characteristics:
        - Larger capacity than working memory
        - Supports semantic search (with embeddings)
        - Automatic promotion to long-term based on criteria
    """

    def __init__(self, capacity: int = 50):
        self.capacity = capacity
        self.memories: Dict[str, Memory] = {}

    def store(self, memory: Memory) -> bool:
        """Store a memory, returning False if at capacity."""
        if len(self.memories) >= self.capacity:
            return False

        memory.memory_type = MemoryType.SHORT_TERM
        self.memories[memory.id] = memory
        return True

    def recall(self, memory_id: str) -> Optional[Memory]:
        """Recall a specific memory by ID."""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.access()
            return memory
        return None

    def search(
        self,
        query_embedding: List[float],
        k: int = 5,
        min_similarity: float = 0.0
    ) -> List[Tuple[Memory, float]]:
        """
        Search memories by embedding similarity.

        Args:
            query_embedding: Query vector
            k: Number of results to return
            min_similarity: Minimum similarity threshold

        Returns:
            List of (memory, similarity) tuples
        """
        results = []

        for memory in self.memories.values():
            if memory.embedding is None:
                continue

            similarity = self._cosine_similarity(
                query_embedding,
                memory.embedding
            )

            if similarity >= min_similarity:
                results.append((memory, similarity))

        # Sort by similarity and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def get_promotion_candidates(
        self,
        min_importance: float = 0.5,
        min_access_count: int = 3
    ) -> List[Memory]:
        """Get memories that should be promoted to long-term."""
        candidates = []
        for memory in self.memories.values():
            if (memory.importance >= min_importance or
                memory.access_count >= min_access_count):
                candidates.append(memory)
        return candidates

    def remove(self, memory_id: str) -> Optional[Memory]:
        """Remove a memory by ID."""
        return self.memories.pop(memory_id, None)

    def get_weakest(self) -> Optional[Memory]:
        """Get the weakest memory without removing it."""
        if not self.memories:
            return None

        return min(
            self.memories.values(),
            key=lambda m: m.calculate_strength()
        )

    def get_all(self) -> List[Memory]:
        """Return all memories."""
        return list(self.memories.values())

    def get_stats(self) -> Dict[str, Any]:
        """Return short-term memory statistics."""
        memories = list(self.memories.values())
        strengths = [m.calculate_strength() for m in memories]

        return {
            "count": len(self.memories),
            "capacity": self.capacity,
            "utilization": len(self.memories) / self.capacity,
            "avg_strength": sum(strengths) / len(strengths) if strengths else 0,
            "with_embeddings": sum(
                1 for m in memories if m.embedding is not None
            )
        }


class LongTermMemory:
    """
    Long-term memory tier - persistent storage with vector search.

    In production, this would use a vector database like ChromaDB,
    Pinecone, or Weaviate. This implementation uses in-memory storage
    for demonstration.
    """

    def __init__(self):
        self.memories: Dict[str, Memory] = {}
        self.embeddings: Dict[str, List[float]] = {}

    def store(self, memory: Memory):
        """Store a memory in long-term storage."""
        memory.memory_type = MemoryType.SEMANTIC
        self.memories[memory.id] = memory

        if memory.embedding is not None:
            self.embeddings[memory.id] = memory.embedding

    def recall(self, memory_id: str) -> Optional[Memory]:
        """Recall a specific memory by ID."""
        if memory_id in self.memories:
            memory = self.memories[memory_id]
            memory.access()
            return memory
        return None

    def search(
        self,
        query_embedding: List[float],
        k: int = 10,
        min_similarity: float = 0.0,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Tuple[Memory, float]]:
        """
        Search long-term memory using vector similarity.

        Args:
            query_embedding: Query vector
            k: Number of results
            min_similarity: Minimum similarity threshold
            filter_metadata: Optional metadata filters

        Returns:
            List of (memory, similarity) tuples
        """
        results = []

        for memory_id, embedding in self.embeddings.items():
            memory = self.memories.get(memory_id)
            if memory is None:
                continue

            # Apply metadata filter
            if filter_metadata:
                if not all(
                    memory.metadata.get(k) == v
                    for k, v in filter_metadata.items()
                ):
                    continue

            similarity = self._cosine_similarity(query_embedding, embedding)

            if similarity >= min_similarity:
                results.append((memory, similarity))

        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """Calculate cosine similarity."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def count(self) -> int:
        """Return count of stored memories."""
        return len(self.memories)

    def get_stats(self) -> Dict[str, Any]:
        """Return long-term memory statistics."""
        return {
            "count": len(self.memories),
            "with_embeddings": len(self.embeddings)
        }


class HierarchicalMemorySystem:
    """
    Complete hierarchical memory system.

    Orchestrates working, short-term, and long-term memory tiers
    with automatic promotion and semantic search capabilities.
    """

    def __init__(
        self,
        working_capacity: int = 10,
        short_term_capacity: int = 50,
        embedding_fn=None
    ):
        self.working = WorkingMemory(working_capacity)
        self.short_term = ShortTermMemory(short_term_capacity)
        self.long_term = LongTermMemory()

        # Embedding function - replace with actual model
        self.embedding_fn = embedding_fn or self._default_embedding

        # Statistics
        self.stats = {
            "stores": 0,
            "recalls": 0,
            "promotions": 0,
            "consolidations": 0
        }

    def _default_embedding(self, text: str) -> List[float]:
        """
        Default embedding function (random for demo).

        Replace with actual embedding model in production.
        """
        import hashlib
        # Deterministic pseudo-random based on content
        hash_bytes = hashlib.sha256(text.encode()).digest()
        return [b / 255.0 for b in hash_bytes[:64]]

    def store(
        self,
        content: str,
        memory_type: MemoryType = MemoryType.WORKING,
        importance: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> Memory:
        """
        Store a new memory in the system.

        Memories start in working memory and can be promoted
        based on importance and access patterns.
        """
        # Generate embedding
        embedding = self.embedding_fn(content)

        # Create memory
        memory = Memory(
            id=str(uuid.uuid4()),
            content=content,
            memory_type=memory_type,
            importance=importance,
            embedding=embedding,
            metadata=metadata or {}
        )

        # Store based on type
        if memory_type == MemoryType.WORKING:
            evicted = self.working.store(memory)

            # Handle overflow to short-term
            if evicted:
                self._promote_to_short_term(evicted)

        elif memory_type == MemoryType.SHORT_TERM:
            if not self.short_term.store(memory):
                # Short-term full, manage capacity
                self._manage_short_term_capacity()
                self.short_term.store(memory)

        elif memory_type in (MemoryType.EPISODIC, MemoryType.SEMANTIC):
            self.long_term.store(memory)

        self.stats["stores"] += 1
        return memory

    def recall(
        self,
        query: str,
        k: int = 5,
        search_all_tiers: bool = True
    ) -> List[Tuple[Memory, float]]:
        """
        Recall relevant memories using semantic search.

        Args:
            query: Search query
            k: Number of results
            search_all_tiers: Whether to search all memory tiers

        Returns:
            List of (memory, relevance) tuples
        """
        query_embedding = self.embedding_fn(query)
        results = []

        # Search working memory
        for memory in self.working.get_all():
            if memory.embedding:
                similarity = self._cosine_similarity(
                    query_embedding,
                    memory.embedding
                )
                results.append((memory, similarity))

        if search_all_tiers:
            # Search short-term
            st_results = self.short_term.search(
                query_embedding, k=k * 2
            )
            results.extend(st_results)

            # Search long-term
            lt_results = self.long_term.search(
                query_embedding, k=k * 2
            )
            results.extend(lt_results)

        # Deduplicate and sort
        seen_ids = set()
        unique_results = []
        for memory, score in results:
            if memory.id not in seen_ids:
                seen_ids.add(memory.id)
                unique_results.append((memory, score))

        unique_results.sort(key=lambda x: x[1], reverse=True)

        # Update access on returned memories
        for memory, _ in unique_results[:k]:
            memory.access()

        self.stats["recalls"] += 1
        return unique_results[:k]

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """Calculate cosine similarity."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _promote_to_short_term(self, memory: Memory):
        """Promote a memory from working to short-term."""
        if not self.short_term.store(memory):
            self._manage_short_term_capacity()
            self.short_term.store(memory)
        self.stats["promotions"] += 1

    def _manage_short_term_capacity(self):
        """Manage short-term memory capacity."""
        # Get weakest memory
        weakest = self.short_term.get_weakest()
        if weakest:
            self.short_term.remove(weakest.id)

            # Promote to long-term if worthy
            if weakest.importance > 0.5 or weakest.access_count > 3:
                self.long_term.store(weakest)
                self.stats["promotions"] += 1

    def consolidate(self):
        """
        Consolidate memories (simulate sleep consolidation).

        Process:
        1. Find strong memories in short-term
        2. Identify associations
        3. Promote worthy memories to long-term
        4. Update association networks
        """
        # Get promotion candidates
        candidates = self.short_term.get_promotion_candidates(
            min_importance=0.6,
            min_access_count=2
        )

        # Promote each candidate
        for memory in candidates:
            # Find associations
            associations = self._find_associations(memory)
            memory.associations = associations

            # Move to long-term
            self.short_term.remove(memory.id)
            self.long_term.store(memory)
            self.stats["promotions"] += 1

        self.stats["consolidations"] += 1

    def _find_associations(self, memory: Memory) -> List[str]:
        """Find memories associated with the given memory."""
        if memory.embedding is None:
            return []

        # Search for similar memories
        results = self.long_term.search(
            memory.embedding,
            k=5,
            min_similarity=0.7
        )

        return [m.id for m, _ in results if m.id != memory.id]

    def get_stats(self) -> Dict[str, Any]:
        """Get comprehensive system statistics."""
        return {
            "working_memory": self.working.get_stats(),
            "short_term_memory": self.short_term.get_stats(),
            "long_term_memory": self.long_term.get_stats(),
            "operations": self.stats
        }

    def export_memories(self) -> Dict[str, Any]:
        """Export all memories for persistence."""
        return {
            "working": [m.to_dict() for m in self.working.get_all()],
            "short_term": [m.to_dict() for m in self.short_term.get_all()],
            "long_term": [
                self.long_term.memories[id].to_dict()
                for id in self.long_term.memories
            ]
        }

    def import_memories(self, data: Dict[str, Any]):
        """Import memories from exported data."""
        for memory_data in data.get("working", []):
            memory = Memory.from_dict(memory_data)
            self.working.memories[memory.id] = memory

        for memory_data in data.get("short_term", []):
            memory = Memory.from_dict(memory_data)
            self.short_term.memories[memory.id] = memory

        for memory_data in data.get("long_term", []):
            memory = Memory.from_dict(memory_data)
            self.long_term.store(memory)


# Example usage
if __name__ == "__main__":
    # Create memory system
    memory = HierarchicalMemorySystem(
        working_capacity=5,
        short_term_capacity=20
    )

    # Store some facts
    facts = [
        ("The Federal AI Act requires risk assessments.", 0.9),
        ("AI systems must be tested for bias.", 0.85),
        ("Annual reviews are required for high-impact AI.", 0.8),
        ("Agencies must designate a Chief AI Officer.", 0.9),
        ("Public notice is required for rights-impacting AI.", 0.85),
        ("Training data must be documented.", 0.75),
    ]

    print("=== Storing Facts ===")
    for content, importance in facts:
        memory.store(content, importance=importance)
        print(f"Stored: {content[:40]}...")

    print("\n=== Memory Stats ===")
    stats = memory.get_stats()
    print(f"Working: {stats['working_memory']['count']} items")
    print(f"Short-term: {stats['short_term_memory']['count']} items")
    print(f"Long-term: {stats['long_term_memory']['count']} items")

    # Test recall
    print("\n=== Recall Test ===")
    queries = [
        "What are the testing requirements?",
        "Who is responsible for AI oversight?",
    ]

    for query in queries:
        print(f"\nQuery: {query}")
        results = memory.recall(query, k=3)
        for mem, score in results:
            print(f"  [{score:.3f}] {mem.content[:50]}...")

    # Consolidation
    print("\n=== Consolidation ===")
    memory.consolidate()
    print("Consolidation complete")
    print(f"Stats: {memory.get_stats()['operations']}")
