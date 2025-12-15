<div align="center">

# Module 20: Cost Optimization

<img src="https://img.shields.io/badge/Duration-3_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Managing and optimizing LLM operational costs*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand LLM cost structures
- [ ] Implement token optimization strategies
- [ ] Design cost-effective architectures
- [ ] Build cost monitoring and alerting
- [ ] Balance cost with quality requirements

---

## 20.1 LLM Cost Structure

```
┌─────────────────────────────────────────────────────────────────┐
│                      LLM COST BREAKDOWN                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DIRECT COSTS                        INDIRECT COSTS              │
│  ────────────                        ──────────────              │
│                                                                  │
│  ┌────────────────┐                 ┌────────────────┐          │
│  │   API Costs    │                 │  Compute       │          │
│  │                │                 │                │          │
│  │  • Input tokens│                 │  • GPUs        │          │
│  │  • Output tokens│                │  • CPUs        │          │
│  │  • Fine-tuning │                 │  • Memory      │          │
│  └────────────────┘                 └────────────────┘          │
│                                                                  │
│  ┌────────────────┐                 ┌────────────────┐          │
│  │   Storage      │                 │  Development   │          │
│  │                │                 │                │          │
│  │  • Embeddings  │                 │  • Testing     │          │
│  │  • Documents   │                 │  • Iteration   │          │
│  │  • Logs        │                 │  • Evaluation  │          │
│  └────────────────┘                 └────────────────┘          │
│                                                                  │
│  ┌────────────────┐                 ┌────────────────┐          │
│  │   Bandwidth    │                 │  Operations    │          │
│  │                │                 │                │          │
│  │  • API calls   │                 │  • Monitoring  │          │
│  │  • Data transfer│                │  • Support     │          │
│  └────────────────┘                 └────────────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### API Pricing Comparison (2024)

| Model | Input ($/1M tokens) | Output ($/1M tokens) | Context |
|-------|---------------------|----------------------|---------|
| GPT-4o | $2.50 | $10.00 | 128K |
| GPT-4o-mini | $0.15 | $0.60 | 128K |
| Claude 3.5 Sonnet | $3.00 | $15.00 | 200K |
| Claude 3 Haiku | $0.25 | $1.25 | 200K |
| Gemini 1.5 Pro | $1.25 | $5.00 | 1M |
| Llama 3 70B (local) | ~$0.05* | ~$0.05* | 8K |

*Local costs based on compute; varies by hardware

---

## 20.2 Token Optimization

### Efficient Prompting

```python
from typing import List, Dict
import tiktoken

class TokenOptimizer:
    """Optimize token usage in LLM applications."""

    def __init__(self, model: str = "gpt-4"):
        self.tokenizer = tiktoken.encoding_for_model(model)

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.tokenizer.encode(text))

    def optimize_prompt(
        self,
        prompt: str,
        max_tokens: int
    ) -> str:
        """Optimize prompt to fit within token limit."""
        current_tokens = self.count_tokens(prompt)

        if current_tokens <= max_tokens:
            return prompt

        # Strategy 1: Remove unnecessary whitespace
        prompt = ' '.join(prompt.split())

        # Strategy 2: Abbreviate common phrases
        abbreviations = {
            "for example": "e.g.",
            "that is": "i.e.",
            "et cetera": "etc.",
            "information": "info",
            "approximately": "~"
        }

        for full, abbrev in abbreviations.items():
            prompt = prompt.replace(full, abbrev)

        # Strategy 3: Truncate if still over
        if self.count_tokens(prompt) > max_tokens:
            tokens = self.tokenizer.encode(prompt)
            prompt = self.tokenizer.decode(tokens[:max_tokens])

        return prompt

    def batch_for_efficiency(
        self,
        items: List[str],
        batch_size: int = 10
    ) -> List[List[str]]:
        """Batch items to reduce API calls."""
        batches = []
        current_batch = []
        current_tokens = 0

        for item in items:
            item_tokens = self.count_tokens(item)

            # Start new batch if this item would exceed limits
            if len(current_batch) >= batch_size or current_tokens + item_tokens > 4000:
                if current_batch:
                    batches.append(current_batch)
                current_batch = [item]
                current_tokens = item_tokens
            else:
                current_batch.append(item)
                current_tokens += item_tokens

        if current_batch:
            batches.append(current_batch)

        return batches


class ContextCompressor:
    """Compress context to reduce token usage."""

    def __init__(self, llm):
        self.llm = llm

    async def compress_context(
        self,
        context: str,
        target_tokens: int
    ) -> str:
        """Compress context while preserving key information."""
        current_tokens = self._count_tokens(context)

        if current_tokens <= target_tokens:
            return context

        compression_ratio = target_tokens / current_tokens

        prompt = f"""Compress the following text to approximately {int(compression_ratio * 100)}% of its length.
Preserve all key facts, names, dates, and important details.
Remove redundant information and verbose language.

Text to compress:
{context}

Compressed text:"""

        compressed = await self.llm.generate(prompt)

        return compressed

    async def extract_relevant_only(
        self,
        context: str,
        query: str,
        max_tokens: int
    ) -> str:
        """Extract only query-relevant portions of context."""
        prompt = f"""Given the user's query, extract only the relevant portions of the context.

Query: {query}

Context:
{context}

Extract the most relevant sentences that help answer the query (max {max_tokens} tokens):"""

        relevant = await self.llm.generate(prompt)

        return relevant
```

### Caching Strategies

```python
from functools import lru_cache
import hashlib
import json
from datetime import datetime, timedelta
import redis

class LLMCache:
    """Cache LLM responses to reduce API calls."""

    def __init__(
        self,
        redis_client: redis.Redis,
        ttl_seconds: int = 3600
    ):
        self.redis = redis_client
        self.ttl = ttl_seconds
        self.stats = {"hits": 0, "misses": 0}

    def _make_cache_key(
        self,
        model: str,
        messages: list,
        params: dict
    ) -> str:
        """Create cache key from request parameters."""
        key_data = {
            "model": model,
            "messages": messages,
            "params": {k: v for k, v in params.items() if k != "stream"}
        }
        key_string = json.dumps(key_data, sort_keys=True)
        return f"llm_cache:{hashlib.sha256(key_string.encode()).hexdigest()}"

    async def get_cached(
        self,
        model: str,
        messages: list,
        params: dict
    ) -> dict | None:
        """Get cached response if available."""
        key = self._make_cache_key(model, messages, params)
        cached = await self.redis.get(key)

        if cached:
            self.stats["hits"] += 1
            return json.loads(cached)

        self.stats["misses"] += 1
        return None

    async def set_cached(
        self,
        model: str,
        messages: list,
        params: dict,
        response: dict
    ):
        """Cache a response."""
        key = self._make_cache_key(model, messages, params)
        await self.redis.setex(
            key,
            self.ttl,
            json.dumps(response)
        )

    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        total = self.stats["hits"] + self.stats["misses"]
        return {
            **self.stats,
            "hit_rate": self.stats["hits"] / max(total, 1),
            "estimated_savings": self.stats["hits"] * 0.01  # Rough estimate
        }


class SemanticCache:
    """Cache based on semantic similarity, not exact match."""

    def __init__(
        self,
        embedding_model,
        vector_store,
        similarity_threshold: float = 0.95
    ):
        self.embedding = embedding_model
        self.store = vector_store
        self.threshold = similarity_threshold

    async def get_similar(
        self,
        query: str
    ) -> dict | None:
        """Get cached response for semantically similar query."""
        query_embedding = await self.embedding.embed([query])

        results = await self.store.search(
            embedding=query_embedding[0],
            top_k=1
        )

        if results and results[0]['score'] >= self.threshold:
            return results[0]['response']

        return None

    async def store_response(
        self,
        query: str,
        response: str
    ):
        """Store response with query embedding."""
        query_embedding = await self.embedding.embed([query])

        await self.store.insert({
            "query": query,
            "embedding": query_embedding[0],
            "response": response,
            "timestamp": datetime.utcnow().isoformat()
        })
```

---

## 20.3 Model Selection Strategy

```python
class ModelRouter:
    """Route requests to appropriate models based on cost/quality tradeoff."""

    def __init__(self, models: Dict[str, Dict]):
        self.models = models
        self.usage_stats = {}

    def select_model(
        self,
        task_type: str,
        complexity: str,
        budget_constraint: float = None
    ) -> str:
        """Select optimal model for task."""

        # Define model capabilities
        model_rankings = {
            "simple_qa": ["gpt-4o-mini", "claude-3-haiku", "gpt-4o"],
            "complex_reasoning": ["gpt-4o", "claude-3-5-sonnet", "gpt-4o-mini"],
            "code_generation": ["gpt-4o", "claude-3-5-sonnet", "gpt-4o-mini"],
            "summarization": ["gpt-4o-mini", "claude-3-haiku", "gpt-4o"],
            "classification": ["gpt-4o-mini", "claude-3-haiku", "gpt-4o"]
        }

        # Get ranked models for task
        candidates = model_rankings.get(task_type, ["gpt-4o-mini"])

        # Filter by complexity
        if complexity == "low":
            # Prefer cheaper models
            candidates = candidates[:2]
        elif complexity == "high":
            # Prefer more capable models
            candidates = candidates[-2:]

        # Filter by budget
        if budget_constraint:
            candidates = [
                m for m in candidates
                if self._estimate_cost(m) <= budget_constraint
            ]

        return candidates[0] if candidates else "gpt-4o-mini"

    def _estimate_cost(self, model: str, avg_tokens: int = 1000) -> float:
        """Estimate cost per request for model."""
        pricing = {
            "gpt-4o": 0.0125,  # Per 1K tokens (avg input/output)
            "gpt-4o-mini": 0.00075,
            "claude-3-5-sonnet": 0.018,
            "claude-3-haiku": 0.0015
        }
        return pricing.get(model, 0.01) * (avg_tokens / 1000)


class CostAwareWrapper:
    """Wrapper that optimizes for cost while maintaining quality."""

    def __init__(
        self,
        clients: Dict[str, Any],
        router: ModelRouter,
        budget_per_request: float = 0.10
    ):
        self.clients = clients
        self.router = router
        self.budget = budget_per_request

    async def generate(
        self,
        messages: list,
        task_type: str = "general",
        min_quality: float = 0.8
    ) -> Dict:
        """Generate with cost optimization."""

        # Estimate complexity
        complexity = self._estimate_complexity(messages)

        # Select model
        model = self.router.select_model(
            task_type=task_type,
            complexity=complexity,
            budget_constraint=self.budget
        )

        # Try cheaper model first
        response = await self.clients[model].generate(messages)

        # If quality check fails, retry with better model
        quality = await self._assess_quality(response)
        if quality < min_quality:
            # Upgrade to better model
            better_model = self.router.select_model(
                task_type=task_type,
                complexity="high"
            )
            response = await self.clients[better_model].generate(messages)

        return response

    def _estimate_complexity(self, messages: list) -> str:
        """Estimate task complexity from messages."""
        total_length = sum(len(m.get("content", "")) for m in messages)

        if total_length < 500:
            return "low"
        elif total_length < 2000:
            return "medium"
        else:
            return "high"
```

---

## 20.4 Cost Monitoring

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import Dict, List
import asyncio

@dataclass
class UsageRecord:
    """Record of LLM usage."""
    timestamp: datetime
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost: float
    tenant_id: str
    user_id: str
    request_type: str

class CostMonitor:
    """Monitor and track LLM costs."""

    def __init__(self, storage):
        self.storage = storage
        self.pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
            "claude-3-haiku": {"input": 0.25, "output": 1.25}
        }
        self.alerts = []

    def calculate_cost(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int
    ) -> float:
        """Calculate cost for a request."""
        pricing = self.pricing.get(model, {"input": 5.0, "output": 15.0})

        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]

        return input_cost + output_cost

    async def record_usage(
        self,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        tenant_id: str,
        user_id: str,
        request_type: str = "chat"
    ):
        """Record a usage event."""
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)

        record = UsageRecord(
            timestamp=datetime.utcnow(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
            tenant_id=tenant_id,
            user_id=user_id,
            request_type=request_type
        )

        await self.storage.insert(record)

        # Check alerts
        await self._check_alerts(tenant_id, cost)

    async def get_daily_cost(
        self,
        tenant_id: str,
        date: date = None
    ) -> float:
        """Get total cost for a day."""
        date = date or date.today()

        records = await self.storage.query(
            tenant_id=tenant_id,
            date=date
        )

        return sum(r.cost for r in records)

    async def get_monthly_report(
        self,
        tenant_id: str,
        year: int,
        month: int
    ) -> Dict:
        """Generate monthly cost report."""
        records = await self.storage.query(
            tenant_id=tenant_id,
            year=year,
            month=month
        )

        report = {
            "tenant_id": tenant_id,
            "period": f"{year}-{month:02d}",
            "total_cost": sum(r.cost for r in records),
            "total_requests": len(records),
            "total_tokens": sum(r.prompt_tokens + r.completion_tokens for r in records),
            "by_model": {},
            "by_user": {},
            "by_day": {}
        }

        for record in records:
            # By model
            if record.model not in report["by_model"]:
                report["by_model"][record.model] = {"cost": 0, "requests": 0}
            report["by_model"][record.model]["cost"] += record.cost
            report["by_model"][record.model]["requests"] += 1

            # By user
            if record.user_id not in report["by_user"]:
                report["by_user"][record.user_id] = {"cost": 0, "requests": 0}
            report["by_user"][record.user_id]["cost"] += record.cost
            report["by_user"][record.user_id]["requests"] += 1

            # By day
            day = record.timestamp.date().isoformat()
            if day not in report["by_day"]:
                report["by_day"][day] = 0
            report["by_day"][day] += record.cost

        return report

    def set_alert(
        self,
        tenant_id: str,
        threshold: float,
        period: str = "daily"
    ):
        """Set cost alert for tenant."""
        self.alerts.append({
            "tenant_id": tenant_id,
            "threshold": threshold,
            "period": period,
            "triggered": False
        })

    async def _check_alerts(self, tenant_id: str, new_cost: float):
        """Check if any alerts should be triggered."""
        for alert in self.alerts:
            if alert["tenant_id"] != tenant_id or alert["triggered"]:
                continue

            if alert["period"] == "daily":
                current = await self.get_daily_cost(tenant_id)
            else:
                current = new_cost  # Implement other periods as needed

            if current >= alert["threshold"]:
                alert["triggered"] = True
                await self._send_alert(tenant_id, current, alert["threshold"])

    async def _send_alert(
        self,
        tenant_id: str,
        current: float,
        threshold: float
    ):
        """Send cost alert notification."""
        # Implement notification logic
        print(f"ALERT: Tenant {tenant_id} exceeded ${threshold} (current: ${current:.2f})")
```

---

## 20.5 Cost Optimization Strategies

```
┌─────────────────────────────────────────────────────────────────┐
│                COST OPTIMIZATION STRATEGIES                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  IMMEDIATE WINS                    LONG-TERM STRATEGIES         │
│  ──────────────                    ─────────────────────        │
│                                                                  │
│  ┌────────────────┐               ┌────────────────┐            │
│  │ Prompt         │               │ Model          │            │
│  │ Optimization   │               │ Distillation   │            │
│  │ (20-40% save)  │               │ (80%+ save)    │            │
│  └────────────────┘               └────────────────┘            │
│                                                                  │
│  ┌────────────────┐               ┌────────────────┐            │
│  │ Response       │               │ Fine-tuning    │            │
│  │ Caching        │               │                │            │
│  │ (30-50% save)  │               │ (50-70% save)  │            │
│  └────────────────┘               └────────────────┘            │
│                                                                  │
│  ┌────────────────┐               ┌────────────────┐            │
│  │ Model          │               │ Local          │            │
│  │ Tiering        │               │ Deployment     │            │
│  │ (40-60% save)  │               │ (90%+ save)    │            │
│  └────────────────┘               └────────────────┘            │
│                                                                  │
│  ┌────────────────┐               ┌────────────────┐            │
│  │ Batching       │               │ Hybrid         │            │
│  │ Requests       │               │ Architecture   │            │
│  │ (10-20% save)  │               │ (Variable)     │            │
│  └────────────────┘               └────────────────┘            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Hands-On Lab

### Lab 20.1: Implement Cost Optimization

Build a cost-optimized LLM application:
1. Implement token counting and optimization
2. Add response caching
3. Build model routing based on complexity
4. Create cost monitoring dashboard
5. Set up alerts and budget enforcement

---

## Knowledge Check

1. What are the main cost drivers in LLM applications?
2. How does semantic caching differ from exact-match caching?
3. When should you use cheaper vs more capable models?
4. What metrics should you track for cost optimization?

---

<div align="center">

[← Module 19: Security & Governance](../19-security-governance/README.md) | [Home](../../README.md) | [Module 21: Hybrid Architectures →](../21-hybrid-architectures/README.md)

</div>
