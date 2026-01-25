"""
Context Window Management - Reference Implementation

This module provides production-ready context window management strategies
for handling documents and conversations that exceed LLM token limits.

Part of Module 28: Antigravity - Advanced Agent Techniques
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import hashlib
import json


@dataclass
class ContextChunk:
    """Represents a chunk of context with metadata."""
    id: str
    content: str
    token_count: int
    priority: float  # 0.0 to 1.0, higher = more important
    timestamp: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __hash__(self):
        return hash(self.id)


@dataclass
class ContextWindow:
    """Represents the current context window state."""
    chunks: List[ContextChunk]
    total_tokens: int
    max_tokens: int
    utilization: float

    @property
    def available_tokens(self) -> int:
        return self.max_tokens - self.total_tokens


class TokenCounter:
    """
    Token counting utility.

    In production, replace with actual tokenizer (tiktoken, transformers, etc.)
    """

    def __init__(self, chars_per_token: float = 4.0):
        self.chars_per_token = chars_per_token

    def count(self, text: str) -> int:
        """Estimate token count for text."""
        return int(len(text) / self.chars_per_token)

    def count_messages(self, messages: List[Dict[str, str]]) -> int:
        """Count tokens in a list of messages."""
        total = 0
        for msg in messages:
            # Account for message structure overhead
            total += 4  # role, content markers
            total += self.count(msg.get("role", ""))
            total += self.count(msg.get("content", ""))
        return total


class ContextStrategy(ABC):
    """Abstract base class for context management strategies."""

    @abstractmethod
    def manage(
        self,
        chunks: List[ContextChunk],
        max_tokens: int,
        query: Optional[str] = None
    ) -> List[ContextChunk]:
        """Select and order chunks to fit within token limit."""
        pass


class SlidingWindowStrategy(ContextStrategy):
    """
    Sliding window context management.

    Keeps the most recent context, discarding oldest content
    when the window overflows.
    """

    def __init__(self, overlap_tokens: int = 200):
        self.overlap_tokens = overlap_tokens

    def manage(
        self,
        chunks: List[ContextChunk],
        max_tokens: int,
        query: Optional[str] = None
    ) -> List[ContextChunk]:
        """Keep most recent chunks that fit in window."""
        # Sort by timestamp (newest first for selection)
        sorted_chunks = sorted(
            chunks,
            key=lambda c: c.timestamp,
            reverse=True
        )

        selected = []
        current_tokens = 0

        for chunk in sorted_chunks:
            if current_tokens + chunk.token_count <= max_tokens:
                selected.append(chunk)
                current_tokens += chunk.token_count
            else:
                break

        # Return in chronological order
        return sorted(selected, key=lambda c: c.timestamp)


class PriorityBasedStrategy(ContextStrategy):
    """
    Priority-based context management.

    Selects chunks based on importance scores, ensuring
    critical information is always included.
    """

    def __init__(
        self,
        system_reserve: int = 500,
        always_include_threshold: float = 0.9
    ):
        self.system_reserve = system_reserve
        self.always_include_threshold = always_include_threshold

    def manage(
        self,
        chunks: List[ContextChunk],
        max_tokens: int,
        query: Optional[str] = None
    ) -> List[ContextChunk]:
        """Select chunks by priority score."""
        available = max_tokens - self.system_reserve

        # Separate must-include from optional
        must_include = [
            c for c in chunks
            if c.priority >= self.always_include_threshold
        ]
        optional = [
            c for c in chunks
            if c.priority < self.always_include_threshold
        ]

        # Sort optional by priority
        optional.sort(key=lambda c: c.priority, reverse=True)

        selected = list(must_include)
        current_tokens = sum(c.token_count for c in selected)

        # Add optional chunks by priority
        for chunk in optional:
            if current_tokens + chunk.token_count <= available:
                selected.append(chunk)
                current_tokens += chunk.token_count

        # Return in original order (by timestamp)
        return sorted(selected, key=lambda c: c.timestamp)


class HierarchicalSummaryStrategy(ContextStrategy):
    """
    Hierarchical summarization strategy.

    Maintains summaries at different granularity levels,
    using detailed content for recent items and summaries
    for older content.
    """

    def __init__(
        self,
        summarizer_fn=None,
        summary_ratio: float = 0.2
    ):
        self.summarizer = summarizer_fn or self._default_summarize
        self.summary_ratio = summary_ratio
        self.summary_cache: Dict[str, str] = {}

    def _default_summarize(self, text: str) -> str:
        """Default summarization (truncation). Replace with LLM call."""
        target_len = int(len(text) * self.summary_ratio)
        if len(text) <= target_len:
            return text
        return text[:target_len] + "..."

    def _get_or_create_summary(self, chunk: ContextChunk) -> str:
        """Get cached summary or create new one."""
        if chunk.id not in self.summary_cache:
            self.summary_cache[chunk.id] = self.summarizer(chunk.content)
        return self.summary_cache[chunk.id]

    def manage(
        self,
        chunks: List[ContextChunk],
        max_tokens: int,
        query: Optional[str] = None
    ) -> List[ContextChunk]:
        """Use summaries for old content, full content for recent."""
        if not chunks:
            return []

        # Sort by timestamp
        sorted_chunks = sorted(chunks, key=lambda c: c.timestamp)

        # Determine split point (70% budget for recent, 30% for summaries)
        recent_budget = int(max_tokens * 0.7)
        summary_budget = max_tokens - recent_budget

        # Select recent chunks
        recent = []
        recent_tokens = 0
        for chunk in reversed(sorted_chunks):
            if recent_tokens + chunk.token_count <= recent_budget:
                recent.insert(0, chunk)
                recent_tokens += chunk.token_count
            else:
                break

        # Create summary chunks for older content
        older_chunks = [c for c in sorted_chunks if c not in recent]
        summarized = []
        summary_tokens = 0

        for chunk in older_chunks:
            summary_content = self._get_or_create_summary(chunk)
            summary_chunk = ContextChunk(
                id=f"{chunk.id}_summary",
                content=summary_content,
                token_count=int(chunk.token_count * self.summary_ratio),
                priority=chunk.priority,
                timestamp=chunk.timestamp,
                metadata={**chunk.metadata, "is_summary": True}
            )

            if summary_tokens + summary_chunk.token_count <= summary_budget:
                summarized.append(summary_chunk)
                summary_tokens += summary_chunk.token_count

        return summarized + recent


class DynamicContextLoader:
    """
    Dynamic context loading with on-demand retrieval.

    Maintains a working set of context and loads additional
    content based on query relevance.
    """

    def __init__(
        self,
        max_tokens: int = 8000,
        working_set_ratio: float = 0.6,
        retrieval_fn=None
    ):
        self.max_tokens = max_tokens
        self.working_set_tokens = int(max_tokens * working_set_ratio)
        self.retrieval_fn = retrieval_fn
        self.working_set: List[ContextChunk] = []
        self.token_counter = TokenCounter()

    def add_to_working_set(self, chunk: ContextChunk) -> bool:
        """Add chunk to working set if space available."""
        current = sum(c.token_count for c in self.working_set)
        if current + chunk.token_count <= self.working_set_tokens:
            self.working_set.append(chunk)
            return True
        return False

    def get_context_for_query(
        self,
        query: str,
        k: int = 5
    ) -> Tuple[List[ContextChunk], int]:
        """
        Get context for a query.

        Combines working set with query-relevant retrieved content.

        Returns:
            Tuple of (chunks, total_tokens)
        """
        # Start with working set
        context = list(self.working_set)
        current_tokens = sum(c.token_count for c in context)

        # Retrieve relevant content if retrieval function provided
        if self.retrieval_fn:
            available = self.max_tokens - current_tokens
            retrieved = self.retrieval_fn(query, k=k)

            for chunk in retrieved:
                if current_tokens + chunk.token_count <= self.max_tokens:
                    if chunk not in context:
                        context.append(chunk)
                        current_tokens += chunk.token_count

        return context, current_tokens

    def clear_working_set(self):
        """Clear the working set."""
        self.working_set = []


class ContextWindowManager:
    """
    Main context window manager.

    Coordinates context management strategies and provides
    a unified interface for context operations.
    """

    def __init__(
        self,
        max_tokens: int = 8000,
        strategy: ContextStrategy = None,
        system_prompt_tokens: int = 500
    ):
        self.max_tokens = max_tokens
        self.strategy = strategy or SlidingWindowStrategy()
        self.system_prompt_tokens = system_prompt_tokens
        self.token_counter = TokenCounter()
        self.chunks: List[ContextChunk] = []
        self._chunk_id_counter = 0

    def _generate_chunk_id(self) -> str:
        """Generate unique chunk ID."""
        self._chunk_id_counter += 1
        return f"chunk_{self._chunk_id_counter}_{datetime.now().timestamp()}"

    def add_content(
        self,
        content: str,
        priority: float = 0.5,
        metadata: Dict[str, Any] = None
    ) -> ContextChunk:
        """Add content to the context pool."""
        chunk = ContextChunk(
            id=self._generate_chunk_id(),
            content=content,
            token_count=self.token_counter.count(content),
            priority=priority,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.chunks.append(chunk)
        return chunk

    def add_message(
        self,
        role: str,
        content: str,
        priority: float = 0.5
    ) -> ContextChunk:
        """Add a conversation message."""
        return self.add_content(
            content=content,
            priority=priority,
            metadata={"role": role, "type": "message"}
        )

    def get_context(
        self,
        query: Optional[str] = None
    ) -> ContextWindow:
        """Get managed context window."""
        available = self.max_tokens - self.system_prompt_tokens

        selected = self.strategy.manage(
            chunks=self.chunks,
            max_tokens=available,
            query=query
        )

        total_tokens = sum(c.token_count for c in selected)

        return ContextWindow(
            chunks=selected,
            total_tokens=total_tokens + self.system_prompt_tokens,
            max_tokens=self.max_tokens,
            utilization=total_tokens / available
        )

    def format_for_llm(
        self,
        query: Optional[str] = None,
        format_type: str = "messages"
    ) -> Any:
        """
        Format context for LLM consumption.

        Args:
            query: Optional query for relevance-based selection
            format_type: "messages" for chat format, "text" for raw

        Returns:
            Formatted context (list of messages or string)
        """
        window = self.get_context(query)

        if format_type == "text":
            return "\n\n".join(c.content for c in window.chunks)

        # Default: messages format
        messages = []
        for chunk in window.chunks:
            role = chunk.metadata.get("role", "user")
            messages.append({
                "role": role,
                "content": chunk.content
            })

        return messages

    def get_stats(self) -> Dict[str, Any]:
        """Get context manager statistics."""
        window = self.get_context()
        return {
            "total_chunks": len(self.chunks),
            "selected_chunks": len(window.chunks),
            "total_tokens": window.total_tokens,
            "max_tokens": window.max_tokens,
            "utilization": f"{window.utilization:.1%}",
            "available_tokens": window.available_tokens
        }

    def prune_old_chunks(self, max_age_hours: float = 24.0):
        """Remove chunks older than specified age."""
        cutoff = datetime.now().timestamp() - (max_age_hours * 3600)
        self.chunks = [
            c for c in self.chunks
            if c.timestamp.timestamp() > cutoff
        ]


# Convenience functions
def create_sliding_window_manager(
    max_tokens: int = 8000,
    overlap: int = 200
) -> ContextWindowManager:
    """Create a manager with sliding window strategy."""
    return ContextWindowManager(
        max_tokens=max_tokens,
        strategy=SlidingWindowStrategy(overlap_tokens=overlap)
    )


def create_priority_manager(
    max_tokens: int = 8000,
    always_include_threshold: float = 0.9
) -> ContextWindowManager:
    """Create a manager with priority-based strategy."""
    return ContextWindowManager(
        max_tokens=max_tokens,
        strategy=PriorityBasedStrategy(
            always_include_threshold=always_include_threshold
        )
    )


def create_hierarchical_manager(
    max_tokens: int = 8000,
    summarizer_fn=None
) -> ContextWindowManager:
    """Create a manager with hierarchical summarization."""
    return ContextWindowManager(
        max_tokens=max_tokens,
        strategy=HierarchicalSummaryStrategy(summarizer_fn=summarizer_fn)
    )


# Example usage
if __name__ == "__main__":
    # Create manager
    manager = create_sliding_window_manager(max_tokens=4000)

    # Add some content
    manager.add_message("user", "What is the Federal AI Act?", priority=0.8)
    manager.add_message(
        "assistant",
        "The Federal AI Act establishes requirements for AI systems "
        "used by federal agencies, including risk assessments, "
        "documentation, and oversight mechanisms.",
        priority=0.7
    )
    manager.add_message(
        "user",
        "What are the key requirements?",
        priority=0.9
    )

    # Add document content
    manager.add_content(
        "Section 1: All agencies shall maintain an inventory of AI systems. "
        "Section 2: High-risk AI requires human oversight. "
        "Section 3: Annual compliance reports are mandatory.",
        priority=0.6,
        metadata={"source": "federal_ai_act.pdf", "type": "document"}
    )

    # Get context
    window = manager.get_context()
    print(f"Context utilization: {window.utilization:.1%}")
    print(f"Total tokens: {window.total_tokens}/{window.max_tokens}")

    # Format for LLM
    messages = manager.format_for_llm()
    print(f"\nMessages for LLM ({len(messages)} messages):")
    for msg in messages:
        print(f"  [{msg['role']}]: {msg['content'][:50]}...")

    # Stats
    print(f"\nStats: {manager.get_stats()}")
