<div align="center">

# Module 17: Deployment & Operations

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--10-green?style=for-the-badge" alt="Prerequisites"/>

*Production deployment strategies for federal LLM applications*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Design production LLM architectures
- [ ] Deploy models to cloud and on-premises environments
- [ ] Implement monitoring and observability
- [ ] Manage model versioning and updates
- [ ] Handle scaling and high availability

---

## 17.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                 FEDERAL LLM DEPLOYMENT ARCHITECTURE              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    LOAD BALANCER                          │   │
│  │              (AWS ALB / Azure App Gateway)               │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                 │
│         │                  │                  │                  │
│         ▼                  ▼                  ▼                  │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │  API Pod   │    │  API Pod   │    │  API Pod   │            │
│  │ (FastAPI)  │    │ (FastAPI)  │    │ (FastAPI)  │            │
│  └──────┬─────┘    └──────┬─────┘    └──────┬─────┘            │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                   MESSAGE QUEUE                           │   │
│  │                (Redis / RabbitMQ)                        │   │
│  └─────────────────────────┬────────────────────────────────┘   │
│                            │                                     │
│         ┌──────────────────┼──────────────────┐                 │
│         │                  │                  │                  │
│         ▼                  ▼                  ▼                  │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │  Worker    │    │  Worker    │    │  Worker    │            │
│  │ (Inference)│    │ (Inference)│    │ (Inference)│            │
│  └──────┬─────┘    └──────┬─────┘    └──────┬─────┘            │
│         │                  │                  │                  │
│         └──────────────────┼──────────────────┘                 │
│                            │                                     │
│                            ▼                                     │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    MODEL STORE                            │   │
│  │        (S3 / Azure Blob / Model Registry)                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Deployment Options

| Environment | Best For | Considerations |
|-------------|----------|----------------|
| **AWS GovCloud** | FedRAMP High | Air-gapped option available |
| **Azure Government** | DoD IL4-6 | Strong Microsoft integration |
| **On-Premises** | Air-gapped, classified | Full control, higher OpEx |
| **Hybrid** | Mixed workloads | Complexity in management |

---

## 17.2 Container Deployment

### Dockerfile for LLM API

```dockerfile
# Multi-stage build for production
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production image
FROM python:3.11-slim

# Security: Run as non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy wheels from builder
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=appuser:appuser . .

# Security hardening
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Deployment

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: llm-api
  labels:
    app: llm-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: llm-api
  template:
    metadata:
      labels:
        app: llm-api
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000

      containers:
      - name: llm-api
        image: registry.gov/llm-api:v1.0.0
        ports:
        - containerPort: 8000

        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"

        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: llm-secrets
              key: openai-api-key

        - name: LOG_LEVEL
          value: "INFO"

        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 10

        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5

        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          capabilities:
            drop:
              - ALL

      imagePullSecrets:
      - name: registry-credentials

---
apiVersion: v1
kind: Service
metadata:
  name: llm-api-service
spec:
  selector:
    app: llm-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: llm-api-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: llm-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 17.3 Monitoring & Observability

### Structured Logging

```python
import structlog
from datetime import datetime
import json

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

class LLMRequestLogger:
    """Log LLM requests with proper structure."""

    def log_request(
        self,
        request_id: str,
        user_id: str,
        model: str,
        prompt_tokens: int,
        completion_tokens: int,
        latency_ms: float,
        status: str
    ):
        logger.info(
            "llm_request",
            request_id=request_id,
            user_id=user_id,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_ms=latency_ms,
            status=status,
            event_type="llm_inference"
        )

    def log_error(
        self,
        request_id: str,
        error_type: str,
        error_message: str,
        stack_trace: str = None
    ):
        logger.error(
            "llm_error",
            request_id=request_id,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            event_type="llm_error"
        )
```

### Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi import FastAPI, Response

# Define metrics
REQUEST_COUNT = Counter(
    'llm_requests_total',
    'Total LLM requests',
    ['model', 'status', 'endpoint']
)

REQUEST_LATENCY = Histogram(
    'llm_request_latency_seconds',
    'LLM request latency',
    ['model', 'endpoint'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

TOKENS_USED = Counter(
    'llm_tokens_total',
    'Total tokens used',
    ['model', 'type']  # type: prompt or completion
)

ACTIVE_REQUESTS = Gauge(
    'llm_active_requests',
    'Currently active LLM requests',
    ['model']
)

MODEL_CACHE_SIZE = Gauge(
    'llm_model_cache_bytes',
    'Model cache size in bytes'
)

app = FastAPI()

@app.get("/metrics")
def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain"
    )

class MetricsMiddleware:
    """Middleware to collect metrics."""

    async def __call__(self, request, call_next):
        model = request.headers.get("X-Model", "unknown")
        endpoint = request.url.path

        ACTIVE_REQUESTS.labels(model=model).inc()

        start_time = time.time()
        try:
            response = await call_next(request)
            status = "success" if response.status_code < 400 else "error"
        except Exception:
            status = "error"
            raise
        finally:
            latency = time.time() - start_time
            REQUEST_COUNT.labels(
                model=model,
                status=status,
                endpoint=endpoint
            ).inc()
            REQUEST_LATENCY.labels(
                model=model,
                endpoint=endpoint
            ).observe(latency)
            ACTIVE_REQUESTS.labels(model=model).dec()

        return response
```

### Health Checks

```python
from fastapi import FastAPI, HTTPException
from datetime import datetime
import asyncio

app = FastAPI()

class HealthChecker:
    """Comprehensive health checking."""

    def __init__(self):
        self.checks = {}

    def register_check(self, name: str, check_fn):
        """Register a health check."""
        self.checks[name] = check_fn

    async def run_checks(self) -> dict:
        """Run all health checks."""
        results = {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "checks": {}
        }

        for name, check_fn in self.checks.items():
            try:
                start = time.time()
                await asyncio.wait_for(check_fn(), timeout=5.0)
                results["checks"][name] = {
                    "status": "healthy",
                    "latency_ms": (time.time() - start) * 1000
                }
            except asyncio.TimeoutError:
                results["checks"][name] = {
                    "status": "unhealthy",
                    "error": "timeout"
                }
                results["status"] = "unhealthy"
            except Exception as e:
                results["checks"][name] = {
                    "status": "unhealthy",
                    "error": str(e)
                }
                results["status"] = "unhealthy"

        return results

health_checker = HealthChecker()

# Register checks
async def check_database():
    # Check database connection
    pass

async def check_llm_api():
    # Check LLM API availability
    pass

async def check_vector_store():
    # Check vector database
    pass

health_checker.register_check("database", check_database)
health_checker.register_check("llm_api", check_llm_api)
health_checker.register_check("vector_store", check_vector_store)

@app.get("/health")
async def health():
    """Liveness probe."""
    return {"status": "alive"}

@app.get("/ready")
async def ready():
    """Readiness probe with dependency checks."""
    results = await health_checker.run_checks()
    if results["status"] != "healthy":
        raise HTTPException(status_code=503, detail=results)
    return results
```

---

## 17.4 Model Management

### Model Registry

```python
from dataclasses import dataclass
from typing import Optional, Dict, List
from datetime import datetime
import hashlib
import json

@dataclass
class ModelVersion:
    """Model version metadata."""
    model_id: str
    version: str
    created_at: datetime
    created_by: str
    description: str
    config: Dict
    metrics: Dict
    status: str  # staging, production, archived
    checksum: str

class ModelRegistry:
    """Manage model versions and deployments."""

    def __init__(self, storage_backend):
        self.storage = storage_backend
        self.versions: Dict[str, List[ModelVersion]] = {}

    def register_model(
        self,
        model_id: str,
        version: str,
        model_path: str,
        config: Dict,
        metrics: Dict,
        created_by: str,
        description: str = ""
    ) -> ModelVersion:
        """Register a new model version."""
        # Calculate checksum
        checksum = self._calculate_checksum(model_path)

        version_info = ModelVersion(
            model_id=model_id,
            version=version,
            created_at=datetime.utcnow(),
            created_by=created_by,
            description=description,
            config=config,
            metrics=metrics,
            status="staging",
            checksum=checksum
        )

        # Store metadata
        if model_id not in self.versions:
            self.versions[model_id] = []
        self.versions[model_id].append(version_info)

        # Upload model to storage
        self.storage.upload(model_path, f"{model_id}/{version}")

        return version_info

    def promote_to_production(
        self,
        model_id: str,
        version: str,
        approver: str
    ):
        """Promote a model version to production."""
        # Demote current production
        for v in self.versions.get(model_id, []):
            if v.status == "production":
                v.status = "archived"

        # Promote new version
        for v in self.versions.get(model_id, []):
            if v.version == version:
                v.status = "production"
                return v

        raise ValueError(f"Version {version} not found")

    def get_production_model(self, model_id: str) -> Optional[ModelVersion]:
        """Get the current production model."""
        for v in self.versions.get(model_id, []):
            if v.status == "production":
                return v
        return None

    def rollback(self, model_id: str, target_version: str):
        """Rollback to a previous version."""
        return self.promote_to_production(
            model_id,
            target_version,
            approver="system_rollback"
        )

    def _calculate_checksum(self, path: str) -> str:
        """Calculate file checksum."""
        hasher = hashlib.sha256()
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
```

### Blue-Green Deployment

```python
class BlueGreenDeployer:
    """Blue-green deployment for LLM services."""

    def __init__(self, k8s_client, namespace: str):
        self.k8s = k8s_client
        self.namespace = namespace

    async def deploy_green(
        self,
        model_version: str,
        image: str
    ):
        """Deploy new version as green."""
        # Create green deployment
        deployment = {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "metadata": {
                "name": "llm-api-green",
                "labels": {
                    "app": "llm-api",
                    "version": model_version,
                    "color": "green"
                }
            },
            "spec": {
                "replicas": 3,
                "selector": {
                    "matchLabels": {
                        "app": "llm-api",
                        "color": "green"
                    }
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "llm-api",
                            "color": "green"
                        }
                    },
                    "spec": {
                        "containers": [{
                            "name": "llm-api",
                            "image": image,
                            "env": [{
                                "name": "MODEL_VERSION",
                                "value": model_version
                            }]
                        }]
                    }
                }
            }
        }

        await self.k8s.create_deployment(
            self.namespace,
            deployment
        )

    async def switch_traffic(
        self,
        target_color: str
    ):
        """Switch traffic to target color."""
        # Update service selector
        service_patch = {
            "spec": {
                "selector": {
                    "app": "llm-api",
                    "color": target_color
                }
            }
        }

        await self.k8s.patch_service(
            self.namespace,
            "llm-api-service",
            service_patch
        )

    async def cleanup_old(self, color: str):
        """Remove old deployment."""
        await self.k8s.delete_deployment(
            self.namespace,
            f"llm-api-{color}"
        )
```

---

## 17.5 Disaster Recovery

```python
class DisasterRecovery:
    """Disaster recovery procedures for LLM systems."""

    def __init__(self, config: Dict):
        self.config = config
        self.backup_locations = config['backup_locations']

    async def create_backup(self) -> Dict:
        """Create system backup."""
        backup_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")

        backup_manifest = {
            "backup_id": backup_id,
            "timestamp": datetime.utcnow().isoformat(),
            "components": []
        }

        # Backup model registry
        model_backup = await self._backup_models(backup_id)
        backup_manifest["components"].append(model_backup)

        # Backup vector database
        vector_backup = await self._backup_vectors(backup_id)
        backup_manifest["components"].append(vector_backup)

        # Backup configuration
        config_backup = await self._backup_config(backup_id)
        backup_manifest["components"].append(config_backup)

        # Store manifest
        await self._store_manifest(backup_id, backup_manifest)

        return backup_manifest

    async def restore_from_backup(
        self,
        backup_id: str,
        target_environment: str
    ) -> Dict:
        """Restore system from backup."""
        manifest = await self._get_manifest(backup_id)

        restore_status = {
            "backup_id": backup_id,
            "target": target_environment,
            "components": []
        }

        for component in manifest["components"]:
            status = await self._restore_component(
                component,
                target_environment
            )
            restore_status["components"].append(status)

        return restore_status

    async def test_recovery(self) -> Dict:
        """Test disaster recovery procedures."""
        results = {
            "timestamp": datetime.utcnow().isoformat(),
            "tests": []
        }

        # Test backup creation
        backup_test = await self._test_backup_creation()
        results["tests"].append(backup_test)

        # Test restore to staging
        restore_test = await self._test_restore_staging()
        results["tests"].append(restore_test)

        # Test failover
        failover_test = await self._test_failover()
        results["tests"].append(failover_test)

        return results
```

---

## Hands-On Lab

### Lab 17.1: Deploy LLM Application to Kubernetes

Deploy a complete LLM application:
1. Build and push container image
2. Create Kubernetes manifests
3. Set up monitoring with Prometheus
4. Implement blue-green deployment
5. Configure auto-scaling

---

## Knowledge Check

1. What are the key considerations for federal cloud deployment?
2. How should LLM applications be monitored in production?
3. What is blue-green deployment and when should it be used?
4. How do you handle model versioning in production?

---

<div align="center">

[← Module 16: Evaluation & Testing](../16-evaluation-testing/README.md) | [Home](../../README.md) | [Module 18: Enterprise Patterns →](../18-enterprise-patterns/README.md)

</div>
