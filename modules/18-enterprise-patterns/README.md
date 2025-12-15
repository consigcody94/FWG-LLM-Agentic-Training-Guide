<div align="center">

# Module 18: Enterprise Patterns

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--10-green?style=for-the-badge" alt="Prerequisites"/>

*Architectural patterns for large-scale federal LLM deployments*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Design enterprise-grade LLM architectures
- [ ] Implement multi-tenant LLM systems
- [ ] Build API gateways for LLM services
- [ ] Create audit and compliance frameworks
- [ ] Manage enterprise model governance

---

## 18.1 Enterprise Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                ENTERPRISE LLM ARCHITECTURE                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                     API GATEWAY                             │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │ │
│  │  │  Auth   │ │  Rate   │ │ Routing │ │  Audit  │          │ │
│  │  │         │ │ Limiting│ │         │ │         │          │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │ │
│  └───────────────────────────┬────────────────────────────────┘ │
│                              │                                   │
│         ┌────────────────────┼────────────────────┐             │
│         │                    │                    │              │
│         ▼                    ▼                    ▼              │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐        │
│  │  Service   │      │  Service   │      │  Service   │        │
│  │   Mesh     │      │   Mesh     │      │   Mesh     │        │
│  │  (Chat)    │      │  (RAG)     │      │  (Agent)   │        │
│  └──────┬─────┘      └──────┬─────┘      └──────┬─────┘        │
│         │                    │                    │              │
│         └────────────────────┼────────────────────┘             │
│                              │                                   │
│                              ▼                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    MODEL LAYER                              │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │ │
│  │  │ OpenAI  │ │ Claude  │ │  Local  │ │ Custom  │          │ │
│  │  │   API   │ │   API   │ │ Ollama  │ │ Models  │          │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                  DATA LAYER                                 │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐          │ │
│  │  │ Vector  │ │  Cache  │ │   SQL   │ │  Object │          │ │
│  │  │   DB    │ │  Redis  │ │   DB    │ │  Store  │          │ │
│  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘          │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Architecture Principles

| Principle | Description | Implementation |
|-----------|-------------|----------------|
| **Separation of Concerns** | Clear service boundaries | Microservices architecture |
| **Defense in Depth** | Multiple security layers | Gateway + Service + Data security |
| **Scalability** | Handle varying load | Auto-scaling, caching |
| **Observability** | Full visibility | Logging, metrics, tracing |
| **Resilience** | Graceful degradation | Circuit breakers, retries |

---

## 18.2 Multi-Tenancy

### Tenant Isolation

```python
from typing import Dict, Optional
from dataclasses import dataclass
from enum import Enum

class TenantTier(Enum):
    FREE = "free"
    STANDARD = "standard"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"

@dataclass
class TenantConfig:
    """Tenant configuration."""
    tenant_id: str
    name: str
    tier: TenantTier
    rate_limits: Dict[str, int]
    allowed_models: list
    max_tokens_per_day: int
    data_retention_days: int
    custom_system_prompt: Optional[str] = None

class TenantManager:
    """Manage multi-tenant LLM access."""

    def __init__(self):
        self.tenants: Dict[str, TenantConfig] = {}
        self.usage: Dict[str, Dict] = {}

    def register_tenant(self, config: TenantConfig):
        """Register a new tenant."""
        self.tenants[config.tenant_id] = config
        self.usage[config.tenant_id] = {
            "tokens_today": 0,
            "requests_today": 0,
            "last_reset": datetime.utcnow().date()
        }

    def get_tenant_config(self, tenant_id: str) -> Optional[TenantConfig]:
        """Get tenant configuration."""
        return self.tenants.get(tenant_id)

    def check_rate_limit(
        self,
        tenant_id: str,
        model: str
    ) -> tuple[bool, str]:
        """Check if tenant is within rate limits."""
        config = self.tenants.get(tenant_id)
        if not config:
            return False, "Unknown tenant"

        usage = self.usage[tenant_id]

        # Check daily token limit
        if usage["tokens_today"] >= config.max_tokens_per_day:
            return False, "Daily token limit exceeded"

        # Check model access
        if model not in config.allowed_models:
            return False, f"Model {model} not allowed for this tenant"

        return True, "OK"

    def record_usage(
        self,
        tenant_id: str,
        tokens: int,
        model: str
    ):
        """Record tenant usage."""
        if tenant_id in self.usage:
            # Reset daily counters if needed
            today = datetime.utcnow().date()
            if self.usage[tenant_id]["last_reset"] != today:
                self.usage[tenant_id] = {
                    "tokens_today": 0,
                    "requests_today": 0,
                    "last_reset": today
                }

            self.usage[tenant_id]["tokens_today"] += tokens
            self.usage[tenant_id]["requests_today"] += 1


class TenantIsolatedLLM:
    """LLM wrapper with tenant isolation."""

    def __init__(
        self,
        llm_clients: Dict[str, Any],
        tenant_manager: TenantManager
    ):
        self.clients = llm_clients
        self.tenants = tenant_manager

    async def generate(
        self,
        tenant_id: str,
        model: str,
        messages: list,
        **kwargs
    ) -> Dict:
        """Generate with tenant isolation."""
        # Check tenant access
        allowed, reason = self.tenants.check_rate_limit(tenant_id, model)
        if not allowed:
            return {"error": reason, "status": "rate_limited"}

        # Get tenant config
        config = self.tenants.get_tenant_config(tenant_id)

        # Inject tenant system prompt if configured
        if config.custom_system_prompt:
            messages = self._inject_system_prompt(
                messages,
                config.custom_system_prompt
            )

        # Call LLM
        client = self.clients.get(model)
        if not client:
            return {"error": f"Model {model} not available"}

        response = await client.generate(messages, **kwargs)

        # Record usage
        self.tenants.record_usage(
            tenant_id,
            response.get("usage", {}).get("total_tokens", 0),
            model
        )

        return response

    def _inject_system_prompt(
        self,
        messages: list,
        system_prompt: str
    ) -> list:
        """Inject tenant system prompt."""
        if messages and messages[0].get("role") == "system":
            messages[0]["content"] = f"{system_prompt}\n\n{messages[0]['content']}"
        else:
            messages.insert(0, {"role": "system", "content": system_prompt})
        return messages
```

---

## 18.3 API Gateway

### Gateway Implementation

```python
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
import jwt
from datetime import datetime, timedelta

app = FastAPI()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)

class APIGateway:
    """Enterprise API gateway for LLM services."""

    def __init__(
        self,
        secret_key: str,
        tenant_manager: TenantManager
    ):
        self.secret_key = secret_key
        self.tenants = tenant_manager

    def create_api_key(
        self,
        tenant_id: str,
        scopes: list,
        expires_days: int = 365
    ) -> str:
        """Create API key for tenant."""
        payload = {
            "tenant_id": tenant_id,
            "scopes": scopes,
            "exp": datetime.utcnow() + timedelta(days=expires_days),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def validate_api_key(self, token: str) -> Dict:
        """Validate API key and return claims."""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=["HS256"]
            )
            return {"valid": True, "claims": payload}
        except jwt.ExpiredSignatureError:
            return {"valid": False, "error": "Token expired"}
        except jwt.InvalidTokenError:
            return {"valid": False, "error": "Invalid token"}

gateway = APIGateway(
    secret_key=os.environ["JWT_SECRET"],
    tenant_manager=TenantManager()
)

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Verify API token."""
    result = gateway.validate_api_key(credentials.credentials)
    if not result["valid"]:
        raise HTTPException(status_code=401, detail=result["error"])
    return result["claims"]

@app.post("/v1/chat/completions")
@limiter.limit("100/minute")
async def chat_completions(
    request: Request,
    claims: dict = Depends(verify_token)
):
    """Route chat completion requests."""
    tenant_id = claims["tenant_id"]

    # Check scopes
    if "chat" not in claims.get("scopes", []):
        raise HTTPException(status_code=403, detail="Insufficient scope")

    # Parse request
    body = await request.json()
    model = body.get("model", "gpt-4")

    # Route to appropriate backend
    response = await route_request(tenant_id, model, body)

    return response

async def route_request(
    tenant_id: str,
    model: str,
    body: dict
) -> dict:
    """Route request to appropriate backend."""
    # Model routing logic
    model_backends = {
        "gpt-4": "openai",
        "gpt-4o": "openai",
        "claude-3": "anthropic",
        "llama": "local"
    }

    backend = model_backends.get(model.split("-")[0], "openai")

    # Call backend
    # Implementation depends on backend type
    pass
```

---

## 18.4 Audit Framework

```python
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional
import json
import hashlib

@dataclass
class AuditEvent:
    """Audit event record."""
    event_id: str
    timestamp: datetime
    tenant_id: str
    user_id: str
    event_type: str
    resource: str
    action: str
    status: str
    metadata: Dict[str, Any]
    request_hash: str
    response_hash: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None

class AuditLogger:
    """Enterprise audit logging for LLM systems."""

    def __init__(self, storage_backend):
        self.storage = storage_backend

    def log_event(
        self,
        tenant_id: str,
        user_id: str,
        event_type: str,
        resource: str,
        action: str,
        status: str,
        request_data: Any,
        response_data: Any = None,
        ip_address: str = None,
        user_agent: str = None,
        metadata: Dict = None
    ) -> AuditEvent:
        """Log an audit event."""
        import uuid

        event = AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow(),
            tenant_id=tenant_id,
            user_id=user_id,
            event_type=event_type,
            resource=resource,
            action=action,
            status=status,
            metadata=metadata or {},
            request_hash=self._hash_content(request_data),
            response_hash=self._hash_content(response_data) if response_data else None,
            ip_address=ip_address,
            user_agent=user_agent
        )

        # Store event
        self.storage.store(event)

        return event

    def _hash_content(self, content: Any) -> str:
        """Create hash of content for integrity."""
        content_str = json.dumps(content, sort_keys=True, default=str)
        return hashlib.sha256(content_str.encode()).hexdigest()

    async def search_events(
        self,
        tenant_id: str = None,
        user_id: str = None,
        event_type: str = None,
        start_time: datetime = None,
        end_time: datetime = None,
        limit: int = 100
    ) -> list:
        """Search audit events."""
        filters = {}
        if tenant_id:
            filters["tenant_id"] = tenant_id
        if user_id:
            filters["user_id"] = user_id
        if event_type:
            filters["event_type"] = event_type
        if start_time:
            filters["timestamp_gte"] = start_time
        if end_time:
            filters["timestamp_lte"] = end_time

        return await self.storage.search(filters, limit=limit)

    def generate_compliance_report(
        self,
        tenant_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> Dict:
        """Generate compliance report."""
        events = self.search_events(
            tenant_id=tenant_id,
            start_time=start_date,
            end_time=end_date,
            limit=10000
        )

        report = {
            "tenant_id": tenant_id,
            "period": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "summary": {
                "total_events": len(events),
                "by_type": {},
                "by_status": {},
                "by_user": {}
            },
            "anomalies": [],
            "generated_at": datetime.utcnow().isoformat()
        }

        # Aggregate statistics
        for event in events:
            # By type
            event_type = event.event_type
            report["summary"]["by_type"][event_type] = \
                report["summary"]["by_type"].get(event_type, 0) + 1

            # By status
            status = event.status
            report["summary"]["by_status"][status] = \
                report["summary"]["by_status"].get(status, 0) + 1

            # By user
            user = event.user_id
            report["summary"]["by_user"][user] = \
                report["summary"]["by_user"].get(user, 0) + 1

        # Detect anomalies
        report["anomalies"] = self._detect_anomalies(events)

        return report

    def _detect_anomalies(self, events: list) -> list:
        """Detect anomalous patterns."""
        anomalies = []

        # High failure rate
        failures = [e for e in events if e.status == "error"]
        if len(failures) / max(len(events), 1) > 0.1:
            anomalies.append({
                "type": "high_failure_rate",
                "description": f"Failure rate: {len(failures)/len(events)*100:.1f}%"
            })

        # Unusual access patterns
        # Add more anomaly detection logic

        return anomalies
```

---

## 18.5 Model Governance

```python
class ModelGovernance:
    """Enterprise model governance framework."""

    def __init__(self, config: Dict):
        self.config = config
        self.approved_models: Dict[str, Dict] = {}
        self.usage_policies: Dict[str, Dict] = {}

    def register_approved_model(
        self,
        model_id: str,
        provider: str,
        capabilities: list,
        restrictions: list,
        data_classification: str,
        approval_info: Dict
    ):
        """Register an approved model for enterprise use."""
        self.approved_models[model_id] = {
            "provider": provider,
            "capabilities": capabilities,
            "restrictions": restrictions,
            "data_classification": data_classification,
            "approval": approval_info,
            "registered_at": datetime.utcnow().isoformat()
        }

    def check_model_approval(
        self,
        model_id: str,
        use_case: str,
        data_classification: str
    ) -> tuple[bool, str]:
        """Check if model is approved for use case."""
        if model_id not in self.approved_models:
            return False, f"Model {model_id} not approved"

        model = self.approved_models[model_id]

        # Check data classification compatibility
        classification_hierarchy = [
            "UNCLASSIFIED",
            "CUI",
            "CONFIDENTIAL",
            "SECRET",
            "TOP_SECRET"
        ]

        model_level = classification_hierarchy.index(
            model["data_classification"]
        )
        data_level = classification_hierarchy.index(data_classification)

        if data_level > model_level:
            return False, f"Model not approved for {data_classification} data"

        # Check use case restrictions
        if use_case in model["restrictions"]:
            return False, f"Model restricted for {use_case}"

        return True, "Approved"

    def create_usage_policy(
        self,
        policy_id: str,
        name: str,
        allowed_models: list,
        max_tokens_per_request: int,
        allowed_use_cases: list,
        required_approvals: list
    ):
        """Create a usage policy."""
        self.usage_policies[policy_id] = {
            "name": name,
            "allowed_models": allowed_models,
            "max_tokens_per_request": max_tokens_per_request,
            "allowed_use_cases": allowed_use_cases,
            "required_approvals": required_approvals,
            "created_at": datetime.utcnow().isoformat()
        }

    def enforce_policy(
        self,
        policy_id: str,
        model: str,
        use_case: str,
        tokens: int
    ) -> tuple[bool, str]:
        """Enforce usage policy."""
        if policy_id not in self.usage_policies:
            return False, "Unknown policy"

        policy = self.usage_policies[policy_id]

        if model not in policy["allowed_models"]:
            return False, f"Model {model} not allowed by policy"

        if use_case not in policy["allowed_use_cases"]:
            return False, f"Use case {use_case} not allowed"

        if tokens > policy["max_tokens_per_request"]:
            return False, f"Request exceeds max tokens ({policy['max_tokens_per_request']})"

        return True, "Policy satisfied"
```

---

## Hands-On Lab

### Lab 18.1: Build Enterprise LLM Platform

Create an enterprise-grade LLM platform:
1. Implement multi-tenant isolation
2. Build API gateway with authentication
3. Add comprehensive audit logging
4. Create model governance framework
5. Deploy with high availability

---

## Knowledge Check

1. How do you implement tenant isolation in multi-tenant LLM systems?
2. What should an enterprise API gateway provide?
3. What audit events are essential for federal compliance?
4. How do you implement model governance?

---

<div align="center">

[← Module 17: Deployment & Ops](../17-deployment-ops/README.md) | [Home](../../README.md) | [Module 19: Security & Governance →](../19-security-governance/README.md)

</div>
