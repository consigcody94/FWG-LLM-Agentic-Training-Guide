<div align="center">

# Module 21: Hybrid Architectures

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--10-green?style=for-the-badge" alt="Prerequisites"/>

*Combining cloud and local LLMs for optimal federal deployments*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Design hybrid cloud/local LLM architectures
- [ ] Implement intelligent routing between models
- [ ] Balance security, cost, and performance
- [ ] Build fallback and redundancy patterns
- [ ] Deploy air-gapped components effectively

---

## 21.1 Hybrid Architecture Patterns

```
┌─────────────────────────────────────────────────────────────────┐
│                    HYBRID LLM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                      API GATEWAY                         │    │
│  │              (Routing & Classification)                  │    │
│  └───────────────────────────┬─────────────────────────────┘    │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐        │
│  │   CLOUD    │      │   LOCAL    │      │AIR-GAPPED  │        │
│  │    LLMs    │      │    LLMs    │      │    LLMs    │        │
│  │            │      │            │      │            │        │
│  │ • GPT-4    │      │ • Ollama   │      │ • Llama    │        │
│  │ • Claude   │      │ • vLLM     │      │ • Mistral  │        │
│  │ • Gemini   │      │            │      │            │        │
│  └────────────┘      └────────────┘      └────────────┘        │
│        │                    │                    │               │
│        │                    │                    │               │
│  UNCLASSIFIED           CUI/PII            CLASSIFIED           │
│  Public data        Sensitive data      Air-gapped only         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Decision Matrix

| Data Type | Latency Req | Best Option | Reason |
|-----------|-------------|-------------|--------|
| Public | Low | Cloud API | Quality, speed |
| Public | High | Local | No network dependency |
| CUI | Any | Local/Private | Data sovereignty |
| PII | Any | Local | Compliance |
| Classified | Any | Air-gapped | Mandatory |

---

## 21.2 Intelligent Routing

```python
from enum import Enum
from typing import Dict, Optional, List
from dataclasses import dataclass

class DataClassification(Enum):
    UNCLASSIFIED = "unclassified"
    CUI = "cui"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"

class ModelLocation(Enum):
    CLOUD = "cloud"
    LOCAL = "local"
    AIR_GAPPED = "air_gapped"

@dataclass
class RoutingDecision:
    location: ModelLocation
    model: str
    reason: str
    fallback: Optional[str] = None

class HybridRouter:
    """Route requests to appropriate LLM based on classification and requirements."""

    def __init__(self, config: Dict):
        self.config = config

        # Model capabilities by location
        self.models = {
            ModelLocation.CLOUD: {
                "gpt-4o": {"quality": 0.95, "speed": 0.9, "cost": 0.3},
                "claude-3-5-sonnet": {"quality": 0.95, "speed": 0.85, "cost": 0.35},
                "gpt-4o-mini": {"quality": 0.8, "speed": 0.95, "cost": 0.9}
            },
            ModelLocation.LOCAL: {
                "llama-3-70b": {"quality": 0.85, "speed": 0.7, "cost": 0.95},
                "llama-3-8b": {"quality": 0.7, "speed": 0.9, "cost": 0.98},
                "mistral-7b": {"quality": 0.65, "speed": 0.92, "cost": 0.99}
            },
            ModelLocation.AIR_GAPPED: {
                "llama-3-70b": {"quality": 0.85, "speed": 0.6, "cost": 0.9},
                "mistral-7b": {"quality": 0.65, "speed": 0.85, "cost": 0.95}
            }
        }

    def route(
        self,
        classification: DataClassification,
        task_type: str,
        priority: str = "quality",
        latency_requirement_ms: int = None
    ) -> RoutingDecision:
        """Determine routing for request."""

        # Determine allowed locations based on classification
        allowed_locations = self._get_allowed_locations(classification)

        # Get best model for each allowed location
        candidates = []
        for location in allowed_locations:
            best = self._select_best_model(
                location,
                task_type,
                priority,
                latency_requirement_ms
            )
            if best:
                candidates.append((location, best))

        if not candidates:
            raise ValueError("No suitable model found for requirements")

        # Select final model
        if priority == "quality":
            candidates.sort(key=lambda x: x[1]["quality"], reverse=True)
        elif priority == "speed":
            candidates.sort(key=lambda x: x[1]["speed"], reverse=True)
        elif priority == "cost":
            candidates.sort(key=lambda x: x[1]["cost"], reverse=True)

        selected_location, selected_model = candidates[0]
        fallback = candidates[1] if len(candidates) > 1 else None

        return RoutingDecision(
            location=selected_location,
            model=selected_model["name"],
            reason=f"Best {priority} for {classification.value} data",
            fallback=fallback[1]["name"] if fallback else None
        )

    def _get_allowed_locations(
        self,
        classification: DataClassification
    ) -> List[ModelLocation]:
        """Get locations allowed for data classification."""
        if classification in [DataClassification.SECRET, DataClassification.TOP_SECRET]:
            return [ModelLocation.AIR_GAPPED]
        elif classification in [DataClassification.CUI, DataClassification.CONFIDENTIAL]:
            return [ModelLocation.LOCAL, ModelLocation.AIR_GAPPED]
        else:
            return [ModelLocation.CLOUD, ModelLocation.LOCAL]

    def _select_best_model(
        self,
        location: ModelLocation,
        task_type: str,
        priority: str,
        latency_req: int = None
    ) -> Optional[Dict]:
        """Select best model at a location."""
        available = self.models.get(location, {})

        candidates = []
        for name, attrs in available.items():
            # Check latency requirement
            if latency_req and attrs["speed"] < 0.5:
                continue

            candidates.append({
                "name": name,
                **attrs
            })

        if not candidates:
            return None

        # Sort by priority
        if priority == "quality":
            candidates.sort(key=lambda x: x["quality"], reverse=True)
        elif priority == "speed":
            candidates.sort(key=lambda x: x["speed"], reverse=True)
        elif priority == "cost":
            candidates.sort(key=lambda x: x["cost"], reverse=True)

        return candidates[0]


class ContentClassifier:
    """Classify content to determine routing."""

    def __init__(self, llm=None):
        self.llm = llm
        self.patterns = {
            DataClassification.CUI: [
                r"CONTROLLED",
                r"CUI//",
                r"FOUO",
                r"\b(SSN|social security)\b",
                r"\b\d{3}-\d{2}-\d{4}\b"  # SSN pattern
            ],
            DataClassification.CONFIDENTIAL: [
                r"CONFIDENTIAL//",
                r"CONFIDENTIAL\b"
            ],
            DataClassification.SECRET: [
                r"SECRET//",
                r"\bSECRET\b"
            ],
            DataClassification.TOP_SECRET: [
                r"TOP SECRET//",
                r"TS//",
                r"TOP SECRET\b"
            ]
        }

    def classify(self, content: str) -> DataClassification:
        """Classify content based on patterns and indicators."""
        import re

        # Check from highest to lowest classification
        for classification in reversed(list(DataClassification)):
            patterns = self.patterns.get(classification, [])
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    return classification

        return DataClassification.UNCLASSIFIED
```

---

## 21.3 Fallback Patterns

```python
class FallbackManager:
    """Manage fallback between LLM providers."""

    def __init__(
        self,
        primary_client,
        fallback_clients: List,
        max_retries: int = 3
    ):
        self.primary = primary_client
        self.fallbacks = fallback_clients
        self.max_retries = max_retries
        self.health_status = {}

    async def generate(
        self,
        messages: list,
        **kwargs
    ) -> Dict:
        """Generate with fallback support."""
        clients = [self.primary] + self.fallbacks

        last_error = None
        for client in clients:
            if not self._is_healthy(client):
                continue

            try:
                response = await client.generate(messages, **kwargs)
                return response
            except Exception as e:
                last_error = e
                self._mark_unhealthy(client)
                continue

        raise last_error or Exception("All providers failed")

    def _is_healthy(self, client) -> bool:
        """Check if client is healthy."""
        status = self.health_status.get(id(client))
        if not status:
            return True

        # Check if cooldown has passed
        if datetime.utcnow() > status["unhealthy_until"]:
            del self.health_status[id(client)]
            return True

        return False

    def _mark_unhealthy(self, client, cooldown_seconds: int = 60):
        """Mark client as temporarily unhealthy."""
        self.health_status[id(client)] = {
            "unhealthy_until": datetime.utcnow() + timedelta(seconds=cooldown_seconds),
            "reason": "Request failed"
        }


class CircuitBreaker:
    """Circuit breaker pattern for LLM calls."""

    def __init__(
        self,
        failure_threshold: int = 5,
        reset_timeout: int = 60
    ):
        self.failure_threshold = failure_threshold
        self.reset_timeout = reset_timeout
        self.failures = 0
        self.last_failure = None
        self.state = "closed"  # closed, open, half-open

    def can_execute(self) -> bool:
        """Check if circuit allows execution."""
        if self.state == "closed":
            return True

        if self.state == "open":
            # Check if we should try again
            if self._should_reset():
                self.state = "half-open"
                return True
            return False

        if self.state == "half-open":
            return True

        return False

    def record_success(self):
        """Record successful execution."""
        self.failures = 0
        self.state = "closed"

    def record_failure(self):
        """Record failed execution."""
        self.failures += 1
        self.last_failure = datetime.utcnow()

        if self.failures >= self.failure_threshold:
            self.state = "open"

    def _should_reset(self) -> bool:
        """Check if circuit should reset."""
        if not self.last_failure:
            return True

        elapsed = (datetime.utcnow() - self.last_failure).total_seconds()
        return elapsed >= self.reset_timeout
```

---

## 21.4 Air-Gapped Deployment

```python
class AirGappedLLMService:
    """LLM service for air-gapped environments."""

    def __init__(self, config: Dict):
        self.config = config
        self.model = None
        self.tokenizer = None

    def load_model(self, model_path: str):
        """Load model from local storage."""
        from transformers import AutoModelForCausalLM, AutoTokenizer
        import torch

        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            torch_dtype=torch.float16,
            device_map="auto"
        )

    async def generate(
        self,
        messages: list,
        max_tokens: int = 2048,
        temperature: float = 0.7
    ) -> Dict:
        """Generate response locally."""
        # Format messages for model
        prompt = self._format_messages(messages)

        inputs = self.tokenizer(
            prompt,
            return_tensors="pt"
        ).to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            do_sample=True
        )

        response = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )

        # Extract just the generated part
        generated = response[len(prompt):]

        return {
            "content": generated,
            "model": self.config["model_name"],
            "usage": {
                "prompt_tokens": len(inputs["input_ids"][0]),
                "completion_tokens": len(outputs[0]) - len(inputs["input_ids"][0]),
                "total_tokens": len(outputs[0])
            }
        }

    def _format_messages(self, messages: list) -> str:
        """Format messages for model."""
        formatted = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                formatted += f"System: {content}\n\n"
            elif role == "user":
                formatted += f"User: {content}\n\n"
            elif role == "assistant":
                formatted += f"Assistant: {content}\n\n"

        formatted += "Assistant:"
        return formatted


class AirGappedRAG:
    """RAG system for air-gapped environments."""

    def __init__(
        self,
        llm: AirGappedLLMService,
        embedding_model_path: str,
        vector_db_path: str
    ):
        self.llm = llm
        self._load_embedding_model(embedding_model_path)
        self._load_vector_db(vector_db_path)

    def _load_embedding_model(self, path: str):
        """Load embedding model from local storage."""
        from sentence_transformers import SentenceTransformer

        self.embedding_model = SentenceTransformer(path)

    def _load_vector_db(self, path: str):
        """Load vector database from local storage."""
        import chromadb
        from chromadb.config import Settings

        self.vector_db = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory=path,
            anonymized_telemetry=False
        ))
        self.collection = self.vector_db.get_collection("documents")

    async def query(
        self,
        question: str,
        n_results: int = 5
    ) -> Dict:
        """Query with RAG."""
        # Get relevant documents
        query_embedding = self.embedding_model.encode([question])[0]

        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )

        # Build context
        context = "\n\n".join(results["documents"][0])

        # Generate response
        messages = [
            {
                "role": "system",
                "content": f"Answer based on the following context:\n\n{context}"
            },
            {
                "role": "user",
                "content": question
            }
        ]

        response = await self.llm.generate(messages)

        return {
            "answer": response["content"],
            "sources": results["metadatas"][0],
            "model": response["model"]
        }
```

---

## 21.5 Synchronization Patterns

```python
class ModelSynchronizer:
    """Synchronize models between environments."""

    def __init__(
        self,
        source_storage,
        target_storage
    ):
        self.source = source_storage
        self.target = target_storage

    async def sync_model(
        self,
        model_id: str,
        version: str
    ) -> Dict:
        """Sync a model to target environment."""
        # Get model metadata
        metadata = await self.source.get_metadata(model_id, version)

        # Verify model integrity
        checksum = await self.source.get_checksum(model_id, version)

        # Download model files
        files = await self.source.list_files(model_id, version)

        sync_results = []
        for file in files:
            # Download from source
            data = await self.source.download(model_id, version, file)

            # Upload to target
            await self.target.upload(model_id, version, file, data)

            # Verify
            target_checksum = await self.target.get_checksum(model_id, version, file)
            sync_results.append({
                "file": file,
                "success": target_checksum == checksum.get(file)
            })

        return {
            "model_id": model_id,
            "version": version,
            "files_synced": len(sync_results),
            "results": sync_results
        }


class ConfigSynchronizer:
    """Synchronize configuration between environments."""

    def __init__(self, config_store):
        self.store = config_store

    def export_config(self, environment: str) -> Dict:
        """Export configuration for transfer to air-gapped environment."""
        config = {
            "environment": environment,
            "exported_at": datetime.utcnow().isoformat(),
            "model_configs": self._export_model_configs(),
            "routing_rules": self._export_routing_rules(),
            "safety_filters": self._export_safety_filters()
        }

        return config

    def import_config(self, config: Dict):
        """Import configuration in air-gapped environment."""
        # Validate config
        self._validate_config(config)

        # Apply configurations
        self._apply_model_configs(config["model_configs"])
        self._apply_routing_rules(config["routing_rules"])
        self._apply_safety_filters(config["safety_filters"])

        return {"imported": True, "timestamp": datetime.utcnow().isoformat()}
```

---

## Hands-On Lab

### Lab 21.1: Build Hybrid LLM System

Create a hybrid deployment:
1. Deploy local Ollama instance
2. Configure cloud API fallback
3. Implement intelligent routing
4. Add content classification
5. Test failover scenarios

---

## Knowledge Check

1. When should requests be routed to local vs cloud LLMs?
2. How do you implement content classification for routing?
3. What fallback patterns should be implemented?
4. How do you sync models to air-gapped environments?

---

<div align="center">

[← Module 20: Cost Optimization](../20-cost-optimization/README.md) | [Home](../../README.md) | [Module 22: Real-Time Streaming →](../22-real-time-streaming/README.md)

</div>
