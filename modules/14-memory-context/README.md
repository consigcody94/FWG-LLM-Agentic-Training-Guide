<div align="center">

# Module 14: Memory & Context Management

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Building stateful AI systems with effective memory management*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand different memory architectures for LLM applications
- [ ] Implement conversation history management
- [ ] Build long-term memory systems
- [ ] Optimize context window usage
- [ ] Handle memory in federal applications securely

---

## 14.1 Memory Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    MEMORY HIERARCHY                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   CONTEXT WINDOW                         │   │
│  │                  (Working Memory)                        │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │   │
│  │  │   System    │  │   Recent    │  │   Current   │     │   │
│  │  │   Prompt    │  │   History   │  │   Input     │     │   │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 SHORT-TERM MEMORY                        │   │
│  │              (Session/Conversation)                      │   │
│  │  • Full conversation history                             │   │
│  │  • Recent context summaries                              │   │
│  │  • Active task state                                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                              │                                   │
│                              ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  LONG-TERM MEMORY                        │   │
│  │               (Persistent Storage)                       │   │
│  │  • User preferences                                      │   │
│  │  • Historical interactions                               │   │
│  │  • Learned patterns                                      │   │
│  │  • Knowledge base                                        │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Memory Types

| Type | Duration | Storage | Use Case |
|------|----------|---------|----------|
| **Working** | Single request | Context window | Current processing |
| **Short-term** | Session | In-memory/Cache | Conversation continuity |
| **Long-term** | Persistent | Database/Vector store | User history, preferences |
| **Episodic** | Event-based | Structured store | Specific interactions |
| **Semantic** | Permanent | Vector database | Knowledge and facts |

---

## 14.2 Conversation History Management

### Basic Buffer Memory

```python
from typing import List, Dict, Optional
from dataclasses import dataclass, field
from datetime import datetime
import tiktoken

@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict = field(default_factory=dict)

class ConversationBuffer:
    """Simple conversation history buffer."""

    def __init__(
        self,
        max_messages: int = 100,
        max_tokens: int = 4000,
        model: str = "gpt-4"
    ):
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.max_tokens = max_tokens
        self.tokenizer = tiktoken.encoding_for_model(model)

    def add_message(self, role: str, content: str, metadata: Dict = None):
        """Add a message to the buffer."""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)

        # Trim if needed
        self._trim_to_limits()

    def get_messages(self) -> List[Dict]:
        """Get messages in API format."""
        return [
            {"role": m.role, "content": m.content}
            for m in self.messages
        ]

    def count_tokens(self) -> int:
        """Count total tokens in buffer."""
        total = 0
        for message in self.messages:
            # Approximate token count per message
            total += len(self.tokenizer.encode(message.content))
            total += 4  # Overhead per message
        return total

    def _trim_to_limits(self):
        """Trim messages to stay within limits."""
        # Trim by message count
        while len(self.messages) > self.max_messages:
            self.messages.pop(0)

        # Trim by token count
        while self.count_tokens() > self.max_tokens and len(self.messages) > 1:
            self.messages.pop(0)

    def clear(self):
        """Clear conversation history."""
        self.messages = []
```

### Window Memory

```python
class SlidingWindowMemory:
    """Maintain a sliding window of recent messages."""

    def __init__(
        self,
        window_size: int = 10,
        include_system: bool = True
    ):
        self.window_size = window_size
        self.include_system = include_system
        self.all_messages: List[Message] = []
        self.system_message: Optional[Message] = None

    def add_message(self, role: str, content: str):
        if role == "system":
            self.system_message = Message(role=role, content=content)
        else:
            self.all_messages.append(Message(role=role, content=content))

    def get_window(self) -> List[Dict]:
        """Get current window of messages."""
        messages = []

        # Always include system message
        if self.include_system and self.system_message:
            messages.append({
                "role": "system",
                "content": self.system_message.content
            })

        # Get recent messages
        recent = self.all_messages[-self.window_size:]
        for m in recent:
            messages.append({"role": m.role, "content": m.content})

        return messages
```

### Summary Memory

```python
class SummaryMemory:
    """Compress old conversations into summaries."""

    def __init__(
        self,
        llm,
        max_tokens: int = 2000,
        summary_threshold: int = 1500
    ):
        self.llm = llm
        self.max_tokens = max_tokens
        self.summary_threshold = summary_threshold
        self.messages: List[Message] = []
        self.summary: str = ""

    async def add_message(self, role: str, content: str):
        self.messages.append(Message(role=role, content=content))

        # Check if summarization needed
        if self._should_summarize():
            await self._summarize_old_messages()

    def _should_summarize(self) -> bool:
        """Check if we need to summarize."""
        token_count = sum(
            len(m.content.split()) * 1.3  # Rough estimate
            for m in self.messages
        )
        return token_count > self.summary_threshold

    async def _summarize_old_messages(self):
        """Summarize older messages."""
        # Keep recent messages
        keep_count = 4
        to_summarize = self.messages[:-keep_count]
        to_keep = self.messages[-keep_count:]

        if not to_summarize:
            return

        # Create summary
        conversation = "\n".join([
            f"{m.role}: {m.content}" for m in to_summarize
        ])

        prompt = f"""Summarize this conversation concisely, preserving key information:

Previous Summary: {self.summary}

New Messages:
{conversation}

Summary:"""

        response = await self.llm.generate(prompt)
        self.summary = response

        # Update messages
        self.messages = to_keep

    def get_context(self) -> List[Dict]:
        """Get context including summary."""
        messages = []

        if self.summary:
            messages.append({
                "role": "system",
                "content": f"Previous conversation summary: {self.summary}"
            })

        for m in self.messages:
            messages.append({"role": m.role, "content": m.content})

        return messages
```

---

## 14.3 Long-Term Memory Systems

### Vector-Based Memory

```python
from typing import List, Dict, Any
import numpy as np
from datetime import datetime

class VectorMemory:
    """Long-term memory using vector embeddings."""

    def __init__(
        self,
        embedding_model,
        vector_store,
        relevance_threshold: float = 0.7
    ):
        self.embedding = embedding_model
        self.store = vector_store
        self.threshold = relevance_threshold

    async def store_memory(
        self,
        content: str,
        metadata: Dict[str, Any] = None
    ):
        """Store a memory with embeddings."""
        embedding = await self.embedding.embed([content])

        memory = {
            "content": content,
            "embedding": embedding[0],
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }

        await self.store.insert(memory)

    async def recall(
        self,
        query: str,
        top_k: int = 5,
        filters: Dict = None
    ) -> List[Dict]:
        """Recall relevant memories."""
        query_embedding = await self.embedding.embed([query])

        results = await self.store.search(
            embedding=query_embedding[0],
            top_k=top_k,
            filters=filters
        )

        # Filter by relevance threshold
        relevant = [
            r for r in results
            if r['score'] >= self.threshold
        ]

        return relevant

    async def forget(self, memory_id: str):
        """Remove a memory."""
        await self.store.delete(memory_id)

    async def decay_old_memories(self, days: int = 90):
        """Apply decay to old memories."""
        cutoff = datetime.utcnow() - timedelta(days=days)
        old_memories = await self.store.query(
            filters={"timestamp": {"$lt": cutoff.isoformat()}}
        )

        for memory in old_memories:
            # Reduce relevance weight for old memories
            memory['metadata']['decay_factor'] = 0.5
            await self.store.update(memory)
```

### Entity Memory

```python
from dataclasses import dataclass
from typing import Dict, List, Optional
import json

@dataclass
class Entity:
    """Represents a named entity in memory."""
    name: str
    entity_type: str
    attributes: Dict[str, Any]
    mentions: List[Dict]
    created_at: datetime
    updated_at: datetime

class EntityMemory:
    """Track and remember entities from conversations."""

    def __init__(self, llm, storage):
        self.llm = llm
        self.storage = storage
        self.entities: Dict[str, Entity] = {}

    async def extract_entities(self, text: str) -> List[Dict]:
        """Extract entities from text using LLM."""
        prompt = f"""Extract named entities from this text. Return JSON array.

Text: {text}

Format:
[{{"name": "...", "type": "person|organization|system|policy|...", "attributes": {{}}}}]

Entities:"""

        response = await self.llm.generate(prompt)
        try:
            return json.loads(response)
        except:
            return []

    async def update_from_message(self, message: str, context: Dict = None):
        """Update entity memory from a message."""
        entities = await self.extract_entities(message)

        for entity_data in entities:
            name = entity_data['name']

            if name in self.entities:
                # Update existing entity
                existing = self.entities[name]
                existing.attributes.update(entity_data.get('attributes', {}))
                existing.mentions.append({
                    "context": message[:100],
                    "timestamp": datetime.utcnow().isoformat()
                })
                existing.updated_at = datetime.utcnow()
            else:
                # Create new entity
                self.entities[name] = Entity(
                    name=name,
                    entity_type=entity_data['type'],
                    attributes=entity_data.get('attributes', {}),
                    mentions=[{
                        "context": message[:100],
                        "timestamp": datetime.utcnow().isoformat()
                    }],
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )

    def get_entity_context(self, query: str) -> str:
        """Get relevant entity context for a query."""
        relevant_entities = []

        for name, entity in self.entities.items():
            if name.lower() in query.lower():
                relevant_entities.append(entity)

        if not relevant_entities:
            return ""

        context = "Known entities:\n"
        for entity in relevant_entities:
            context += f"- {entity.name} ({entity.entity_type}): {entity.attributes}\n"

        return context
```

---

## 14.4 Context Window Optimization

### Token Budget Management

```python
class TokenBudgetManager:
    """Manage token budget across context components."""

    def __init__(
        self,
        total_budget: int = 8000,
        model: str = "gpt-4"
    ):
        self.total_budget = total_budget
        self.tokenizer = tiktoken.encoding_for_model(model)

        # Budget allocation
        self.allocations = {
            "system_prompt": 0.15,      # 15%
            "memory_context": 0.20,     # 20%
            "conversation": 0.40,       # 40%
            "current_input": 0.15,      # 15%
            "output_reserve": 0.10      # 10% reserved for output
        }

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.tokenizer.encode(text))

    def get_budget(self, component: str) -> int:
        """Get token budget for a component."""
        return int(self.total_budget * self.allocations[component])

    def fit_to_budget(
        self,
        content: str,
        component: str,
        strategy: str = "truncate_start"
    ) -> str:
        """Fit content to component budget."""
        budget = self.get_budget(component)
        tokens = self.count_tokens(content)

        if tokens <= budget:
            return content

        # Apply truncation strategy
        if strategy == "truncate_start":
            # Remove from beginning
            encoded = self.tokenizer.encode(content)
            truncated = encoded[-budget:]
            return self.tokenizer.decode(truncated)

        elif strategy == "truncate_end":
            # Remove from end
            encoded = self.tokenizer.encode(content)
            truncated = encoded[:budget]
            return self.tokenizer.decode(truncated)

        elif strategy == "middle_out":
            # Keep start and end, remove middle
            encoded = self.tokenizer.encode(content)
            half = budget // 2
            truncated = encoded[:half] + encoded[-half:]
            return self.tokenizer.decode(truncated)

        return content

    def build_context(
        self,
        system_prompt: str,
        memory: str,
        conversation: List[Dict],
        current_input: str
    ) -> List[Dict]:
        """Build optimized context within budget."""
        messages = []

        # System prompt (highest priority)
        system = self.fit_to_budget(system_prompt, "system_prompt")
        messages.append({"role": "system", "content": system})

        # Add memory context to system
        if memory:
            memory_fitted = self.fit_to_budget(memory, "memory_context")
            messages[0]["content"] += f"\n\nRelevant Context:\n{memory_fitted}"

        # Conversation history (truncate oldest first)
        conv_budget = self.get_budget("conversation")
        conv_tokens = 0
        included_messages = []

        for msg in reversed(conversation):
            msg_tokens = self.count_tokens(msg["content"]) + 4
            if conv_tokens + msg_tokens <= conv_budget:
                included_messages.insert(0, msg)
                conv_tokens += msg_tokens
            else:
                break

        messages.extend(included_messages)

        # Current input
        input_fitted = self.fit_to_budget(current_input, "current_input")
        messages.append({"role": "user", "content": input_fitted})

        return messages
```

### Priority-Based Context Selection

```python
class PriorityContextSelector:
    """Select context items by priority and relevance."""

    def __init__(self, embedding_model, token_budget: int):
        self.embedding = embedding_model
        self.budget = token_budget

    async def select_context(
        self,
        query: str,
        context_items: List[Dict],
        priorities: Dict[str, int] = None
    ) -> List[Dict]:
        """Select most relevant context items within budget."""

        # Default priorities
        priorities = priorities or {
            "system": 100,
            "entity": 80,
            "recent_message": 60,
            "memory": 40,
            "background": 20
        }

        # Calculate relevance scores
        query_embedding = await self.embedding.embed([query])

        scored_items = []
        for item in context_items:
            # Get embedding if not cached
            if 'embedding' not in item:
                item['embedding'] = await self.embedding.embed([item['content']])

            # Calculate similarity
            similarity = np.dot(query_embedding[0], item['embedding'][0])

            # Combine with priority
            priority = priorities.get(item.get('type', 'background'), 20)
            score = similarity * 0.7 + (priority / 100) * 0.3

            scored_items.append({
                **item,
                'score': score
            })

        # Sort by score
        scored_items.sort(key=lambda x: x['score'], reverse=True)

        # Select within budget
        selected = []
        used_tokens = 0

        for item in scored_items:
            item_tokens = len(item['content'].split()) * 1.3
            if used_tokens + item_tokens <= self.budget:
                selected.append(item)
                used_tokens += item_tokens

        return selected
```

---

## 14.5 Secure Memory for Federal Applications

```python
from cryptography.fernet import Fernet
from typing import Optional
import hashlib

class SecureMemoryStore:
    """Encrypted memory storage for federal applications."""

    def __init__(
        self,
        encryption_key: bytes,
        classification_level: str = "UNCLASSIFIED"
    ):
        self.cipher = Fernet(encryption_key)
        self.classification = classification_level
        self.storage: Dict[str, bytes] = {}

    def _encrypt(self, data: str) -> bytes:
        """Encrypt data."""
        return self.cipher.encrypt(data.encode())

    def _decrypt(self, data: bytes) -> str:
        """Decrypt data."""
        return self.cipher.decrypt(data).decode()

    def _hash_id(self, identifier: str) -> str:
        """Create secure hash of identifier."""
        return hashlib.sha256(identifier.encode()).hexdigest()

    async def store(
        self,
        key: str,
        content: str,
        metadata: Dict = None,
        user_clearance: str = "UNCLASSIFIED"
    ):
        """Store encrypted memory."""
        # Check clearance
        if not self._check_clearance(user_clearance):
            raise PermissionError("Insufficient clearance")

        # Encrypt content
        encrypted = self._encrypt(content)

        # Store with hashed key
        hashed_key = self._hash_id(key)
        self.storage[hashed_key] = {
            "content": encrypted,
            "metadata": metadata or {},
            "classification": self.classification,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def retrieve(
        self,
        key: str,
        user_clearance: str = "UNCLASSIFIED"
    ) -> Optional[str]:
        """Retrieve and decrypt memory."""
        hashed_key = self._hash_id(key)

        if hashed_key not in self.storage:
            return None

        record = self.storage[hashed_key]

        # Check clearance for retrieval
        if not self._check_clearance(user_clearance, record['classification']):
            raise PermissionError("Insufficient clearance for this memory")

        return self._decrypt(record['content'])

    async def delete(self, key: str):
        """Securely delete memory."""
        hashed_key = self._hash_id(key)
        if hashed_key in self.storage:
            # Overwrite before delete
            self.storage[hashed_key]['content'] = b'\x00' * len(
                self.storage[hashed_key]['content']
            )
            del self.storage[hashed_key]

    def _check_clearance(
        self,
        user_clearance: str,
        required: str = None
    ) -> bool:
        """Check if user has required clearance."""
        clearance_levels = {
            "UNCLASSIFIED": 0,
            "CUI": 1,
            "CONFIDENTIAL": 2,
            "SECRET": 3,
            "TOP_SECRET": 4
        }

        required = required or self.classification
        user_level = clearance_levels.get(user_clearance, 0)
        required_level = clearance_levels.get(required, 0)

        return user_level >= required_level


class AuditedMemory:
    """Memory with comprehensive audit logging."""

    def __init__(self, base_memory, audit_logger):
        self.memory = base_memory
        self.audit = audit_logger

    async def store(self, key: str, content: str, user_id: str, **kwargs):
        await self.audit.log({
            "action": "memory_store",
            "key_hash": hashlib.sha256(key.encode()).hexdigest(),
            "user_id": user_id,
            "content_size": len(content),
            "timestamp": datetime.utcnow().isoformat()
        })

        return await self.memory.store(key, content, **kwargs)

    async def retrieve(self, key: str, user_id: str, **kwargs):
        result = await self.memory.retrieve(key, **kwargs)

        await self.audit.log({
            "action": "memory_retrieve",
            "key_hash": hashlib.sha256(key.encode()).hexdigest(),
            "user_id": user_id,
            "found": result is not None,
            "timestamp": datetime.utcnow().isoformat()
        })

        return result

    async def delete(self, key: str, user_id: str):
        await self.audit.log({
            "action": "memory_delete",
            "key_hash": hashlib.sha256(key.encode()).hexdigest(),
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        })

        return await self.memory.delete(key)
```

---

## Hands-On Lab

### Lab 14.1: Build Secure Conversation Memory

Implement a memory system for a federal chatbot:
1. Create encrypted conversation storage
2. Implement sliding window with summarization
3. Add entity extraction and tracking
4. Build audit logging for all memory operations

---

## Knowledge Check

1. What are the tradeoffs between buffer and summary memory?
2. How should sensitive information be handled in long-term memory?
3. What strategies help fit context within token limits?
4. How do you implement memory access controls?

---

<div align="center">

[← Module 13: Tool Use](../13-tool-use-functions/README.md) | [Home](../../README.md) | [Module 15: Safety & Alignment →](../15-safety-alignment/README.md)

</div>
