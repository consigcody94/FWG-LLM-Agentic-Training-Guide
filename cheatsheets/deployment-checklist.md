# Deployment Checklist

<div align="center">

**Production Readiness for AI Systems in Federal Environments**

</div>

---

## Pre-Deployment Checklist

### 1. Security Review

```
□ Authentication & Authorization
  □ API authentication implemented
  □ Role-based access control (RBAC) configured
  □ API key rotation policy defined
  □ Service accounts have minimum required permissions

□ Data Protection
  □ TLS 1.3 enabled for all connections
  □ Encryption at rest configured (AES-256)
  □ PII/PHI handling procedures documented
  □ Data retention policies implemented

□ Input/Output Security
  □ Input validation implemented
  □ Prompt injection defenses in place
  □ Output filtering for sensitive data
  □ Rate limiting configured

□ Infrastructure Security
  □ Network segmentation configured
  □ Firewall rules reviewed
  □ Security groups properly scoped
  □ VPC/private networking enabled
```

### 2. Compliance Verification

```
□ Federal Requirements
  □ FedRAMP authorization status verified
  □ FISMA controls documented
  □ System Security Plan (SSP) updated
  □ Authority to Operate (ATO) obtained (if required)

□ AI-Specific Requirements
  □ NIST AI RMF alignment documented
  □ Algorithm impact assessment completed
  □ Bias testing performed
  □ Human oversight procedures defined

□ Documentation
  □ Architecture diagrams current
  □ Data flow diagrams complete
  □ API documentation published
  □ Runbooks created
```

### 3. Infrastructure Readiness

```
□ Compute Resources
  □ CPU/GPU capacity verified
  □ Memory requirements met
  □ Storage provisioned
  □ Autoscaling configured

□ Networking
  □ Load balancer configured
  □ DNS records created
  □ SSL certificates installed
  □ Health check endpoints working

□ Container/Orchestration
  □ Container images scanned
  □ Kubernetes manifests reviewed
  □ Resource limits set
  □ Pod security policies applied
```

---

## Deployment Configuration

### Environment Variables

```bash
# Required
APP_ENV=production
LOG_LEVEL=INFO
API_BASE_URL=https://api.your-domain.gov

# LLM Configuration
LLM_PROVIDER=azure_openai  # or bedrock
LLM_MODEL=gpt-4o
LLM_MAX_TOKENS=4000
LLM_TEMPERATURE=0.3

# Security
API_KEY_ENCRYPTION_KEY=${from_vault}
ALLOWED_ORIGINS=https://app.your-domain.gov

# Monitoring
TELEMETRY_ENDPOINT=https://metrics.your-domain.gov
TRACE_SAMPLE_RATE=0.1
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-service
  labels:
    app: ai-service
    version: v1.0.0
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: ai-service
  template:
    metadata:
      labels:
        app: ai-service
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: ai-service
        image: registry.your-domain.gov/ai-service:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "2Gi"
            cpu: "1000m"
          limits:
            memory: "4Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: LLM_API_KEY
          valueFrom:
            secretKeyRef:
              name: ai-secrets
              key: llm-api-key
```

### Health Check Endpoints

```python
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health():
    """Liveness probe - is the service running?"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

@app.get("/ready")
async def ready():
    """Readiness probe - is the service ready to accept traffic?"""
    checks = {
        "database": await check_database(),
        "llm_api": await check_llm_api(),
        "cache": await check_cache()
    }

    all_healthy = all(checks.values())
    return {
        "ready": all_healthy,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## Monitoring Setup

### Logging Configuration

```python
import structlog
import logging

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()

# Log AI requests
logger.info(
    "ai_request",
    request_id="abc-123",
    user_id="user-456",
    model="gpt-4o",
    input_tokens=150,
    output_tokens=200,
    latency_ms=1234,
    status="success"
)
```

### Metrics to Track

```yaml
# Key metrics for AI systems
metrics:
  # Latency
  - name: ai_request_duration_seconds
    type: histogram
    labels: [model, status]

  # Throughput
  - name: ai_requests_total
    type: counter
    labels: [model, status, endpoint]

  # Token Usage
  - name: ai_tokens_used_total
    type: counter
    labels: [model, token_type]  # input/output

  # Errors
  - name: ai_errors_total
    type: counter
    labels: [model, error_type]

  # Cost
  - name: ai_estimated_cost_dollars
    type: counter
    labels: [model]

  # Queue
  - name: ai_queue_depth
    type: gauge
    labels: [priority]
```

### Alert Rules

```yaml
# Prometheus alerting rules
groups:
- name: ai-service-alerts
  rules:
  - alert: AIServiceHighErrorRate
    expr: |
      sum(rate(ai_errors_total[5m])) /
      sum(rate(ai_requests_total[5m])) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "AI service error rate above 5%"

  - alert: AIServiceHighLatency
    expr: |
      histogram_quantile(0.95, rate(ai_request_duration_seconds_bucket[5m])) > 10
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "AI service P95 latency above 10 seconds"

  - alert: AIServiceHighCost
    expr: |
      sum(increase(ai_estimated_cost_dollars[1h])) > 100
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "AI service cost exceeds $100/hour"
```

---

## Rollback Procedures

### Pre-Deployment Snapshot

```bash
# Before deploying, capture current state
kubectl get deployment ai-service -o yaml > backup/ai-service-$(date +%Y%m%d).yaml

# Capture config
kubectl get configmap ai-service-config -o yaml > backup/config-$(date +%Y%m%d).yaml

# Capture secrets (encrypted)
kubectl get secret ai-service-secrets -o yaml | \
  sops -e /dev/stdin > backup/secrets-$(date +%Y%m%d).yaml.enc
```

### Rollback Commands

```bash
# Kubernetes rollback
kubectl rollout undo deployment/ai-service

# Rollback to specific revision
kubectl rollout undo deployment/ai-service --to-revision=2

# Check rollout status
kubectl rollout status deployment/ai-service

# Verify pods
kubectl get pods -l app=ai-service
```

### Rollback Decision Matrix

| Condition | Action |
|-----------|--------|
| Error rate > 10% | Immediate rollback |
| P95 latency > 30s | Investigate, rollback if persists |
| Cost spike > 3x | Investigate, may need rollback |
| Security issue | Immediate rollback |
| Functionality broken | Immediate rollback |

---

## Go-Live Checklist

### Day Before Launch

```
□ Final code review completed
□ Security scan passed
□ Load testing completed
□ Runbooks reviewed by on-call team
□ Rollback procedure tested
□ Communication plan finalized
□ Stakeholder notification sent
```

### Launch Day

```
□ Pre-deployment
  □ Team assembled and ready
  □ Monitoring dashboards open
  □ Communication channels active
  □ Previous deployment backup verified

□ Deployment
  □ Deployment initiated
  □ Health checks passing
  □ Smoke tests executed
  □ Gradual traffic shift (if canary)

□ Post-deployment
  □ All health checks green
  □ Error rates normal
  □ Latency within SLA
  □ Cost tracking nominal
  □ Team on standby for 30 minutes
```

### Post-Launch (First 24 Hours)

```
□ Monitor dashboards continuously
□ Review overnight alerts
□ Check log patterns for anomalies
□ Verify backup jobs completed
□ Collect initial user feedback
□ Document any issues encountered
□ Update runbooks if needed
```

---

## Traffic Management

### Canary Deployment

```yaml
# Istio VirtualService for canary
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: ai-service
spec:
  hosts:
  - ai-service
  http:
  - match:
    - headers:
        x-canary:
          exact: "true"
    route:
    - destination:
        host: ai-service
        subset: canary
  - route:
    - destination:
        host: ai-service
        subset: stable
      weight: 95
    - destination:
        host: ai-service
        subset: canary
      weight: 5
```

### Blue-Green Deployment

```bash
# Switch traffic from blue to green
kubectl patch service ai-service -p \
  '{"spec":{"selector":{"version":"green"}}}'

# Verify switch
kubectl get endpoints ai-service

# Rollback to blue
kubectl patch service ai-service -p \
  '{"spec":{"selector":{"version":"blue"}}}'
```

---

## Disaster Recovery

### Backup Checklist

```
□ Configuration backups
  □ Kubernetes manifests
  □ Terraform state
  □ Secrets (encrypted)

□ Data backups
  □ Vector databases
  □ Conversation history
  □ User data

□ Model artifacts
  □ Model weights (if self-hosted)
  □ Fine-tuning data
  □ Evaluation datasets
```

### Recovery Time Objectives

| Component | RTO | RPO |
|-----------|-----|-----|
| API Service | 15 min | 0 |
| Vector Database | 1 hour | 1 hour |
| Conversation History | 4 hours | 1 hour |
| Analytics | 24 hours | 24 hours |

---

## Documentation Requirements

```
□ Technical Documentation
  □ Architecture diagram
  □ API documentation (OpenAPI)
  □ Deployment procedures
  □ Configuration reference

□ Operational Documentation
  □ Runbooks for common issues
  □ Escalation procedures
  □ On-call rotation
  □ Incident response plan

□ Compliance Documentation
  □ Security controls implemented
  □ Audit log locations
  □ Data handling procedures
  □ Privacy impact assessment
```

---

<div align="center">

**Deploy with confidence. Monitor continuously. Be ready to rollback.**

</div>
