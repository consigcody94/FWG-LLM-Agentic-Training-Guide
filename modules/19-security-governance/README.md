<div align="center">

# Module 19: Security & Governance

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Federal security frameworks and governance for AI systems*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Apply NIST 800-53 controls to AI systems
- [ ] Implement FedRAMP requirements for LLM applications
- [ ] Design secure AI architectures for federal use
- [ ] Manage AI system authorization (ATO)
- [ ] Implement continuous monitoring for AI

---

## 19.1 Federal Security Framework

```
┌─────────────────────────────────────────────────────────────────┐
│                FEDERAL AI SECURITY FRAMEWORK                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  POLICY LAYER                                                    │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │   EO      │ │   OMB     │ │   NIST    │ │  Agency   │       │
│  │  14110    │ │  M-24-10  │ │  AI RMF   │ │  Policy   │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
│  STANDARDS LAYER                                                 │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │   NIST    │ │  FedRAMP  │ │   FISMA   │ │   FIPS    │       │
│  │  800-53   │ │           │ │           │ │  140-3    │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
│  IMPLEMENTATION LAYER                                            │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │  Access   │ │   Audit   │ │   Data    │ │  Incident │       │
│  │  Control  │ │  Logging  │ │Protection │ │  Response │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
│  OPERATIONAL LAYER                                               │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌───────────┐       │
│  │Continuous │ │Vulnerability│ │  Change   │ │  ConMon   │       │
│  │Monitoring │ │ Management │ │Management │ │ Reporting │       │
│  └───────────┘ └───────────┘ └───────────┘ └───────────┘       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Regulations

| Regulation | Scope | AI Relevance |
|------------|-------|--------------|
| **EO 14110** | All federal AI | Safety, security requirements |
| **OMB M-24-10** | Federal AI use | Governance, risk management |
| **NIST AI RMF** | AI systems | Risk management framework |
| **NIST 800-53** | Information systems | Security controls |
| **FedRAMP** | Cloud services | Authorization framework |

---

## 19.2 NIST 800-53 for AI Systems

### AI-Relevant Control Families

```python
AI_SECURITY_CONTROLS = {
    "AC": {  # Access Control
        "AC-2": {
            "name": "Account Management",
            "ai_implementation": """
                - Implement role-based access to AI systems
                - Manage API keys and service accounts
                - Track user access to AI capabilities
                - Review and disable unused accounts
            """
        },
        "AC-3": {
            "name": "Access Enforcement",
            "ai_implementation": """
                - Enforce least privilege for AI model access
                - Implement tenant isolation
                - Control access to training data
                - Restrict model modification capabilities
            """
        },
        "AC-6": {
            "name": "Least Privilege",
            "ai_implementation": """
                - Grant minimum necessary AI capabilities per role
                - Limit access to sensitive model endpoints
                - Restrict administrative functions
                - Implement just-in-time access for elevated permissions
            """
        }
    },
    "AU": {  # Audit and Accountability
        "AU-2": {
            "name": "Audit Events",
            "ai_implementation": """
                - Log all AI system interactions
                - Capture prompts and responses (sanitized)
                - Record model selection and configuration
                - Track token usage and costs
            """
        },
        "AU-3": {
            "name": "Content of Audit Records",
            "ai_implementation": """
                - Include: timestamp, user, tenant, model, action
                - Record input/output hashes for integrity
                - Capture system context and configuration
                - Log safety filter activations
            """
        },
        "AU-6": {
            "name": "Audit Review, Analysis, and Reporting",
            "ai_implementation": """
                - Automated analysis of AI usage patterns
                - Anomaly detection for unusual requests
                - Regular compliance reporting
                - Integration with SIEM systems
            """
        }
    },
    "SC": {  # System and Communications Protection
        "SC-8": {
            "name": "Transmission Confidentiality and Integrity",
            "ai_implementation": """
                - TLS 1.3 for all AI API communications
                - Encrypt prompts and responses in transit
                - Validate certificates for external AI services
                - Implement mutual TLS for service-to-service
            """
        },
        "SC-28": {
            "name": "Protection of Information at Rest",
            "ai_implementation": """
                - Encrypt stored prompts and responses
                - Secure model weights and configurations
                - Protect training data and embeddings
                - Encrypt vector database contents
            """
        }
    },
    "SI": {  # System and Information Integrity
        "SI-3": {
            "name": "Malicious Code Protection",
            "ai_implementation": """
                - Scan inputs for injection attacks
                - Validate model outputs for harmful content
                - Monitor for adversarial prompts
                - Implement content safety filters
            """
        },
        "SI-4": {
            "name": "System Monitoring",
            "ai_implementation": """
                - Monitor AI system performance
                - Track model behavior changes
                - Alert on anomalous outputs
                - Continuous evaluation of AI quality
            """
        }
    }
}
```

### Control Implementation

```python
from typing import Dict, List
from dataclasses import dataclass
from enum import Enum

class ControlStatus(Enum):
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    NOT_APPLICABLE = "not_applicable"

@dataclass
class ControlImplementation:
    """Document a security control implementation."""
    control_id: str
    status: ControlStatus
    implementation_description: str
    evidence_locations: List[str]
    responsible_party: str
    implementation_date: str
    last_assessed: str

class SecurityControlManager:
    """Manage NIST 800-53 controls for AI systems."""

    def __init__(self):
        self.implementations: Dict[str, ControlImplementation] = {}

    def document_implementation(
        self,
        control_id: str,
        status: ControlStatus,
        description: str,
        evidence: List[str],
        responsible: str
    ):
        """Document a control implementation."""
        self.implementations[control_id] = ControlImplementation(
            control_id=control_id,
            status=status,
            implementation_description=description,
            evidence_locations=evidence,
            responsible_party=responsible,
            implementation_date=datetime.utcnow().isoformat(),
            last_assessed=datetime.utcnow().isoformat()
        )

    def generate_ssp_section(self, control_id: str) -> str:
        """Generate SSP section for a control."""
        impl = self.implementations.get(control_id)
        if not impl:
            return f"Control {control_id}: Not documented"

        return f"""
## {control_id}

**Status:** {impl.status.value}

**Implementation Description:**
{impl.implementation_description}

**Evidence:**
{chr(10).join(['- ' + e for e in impl.evidence_locations])}

**Responsible Party:** {impl.responsible_party}

**Last Assessed:** {impl.last_assessed}
"""

    def assess_compliance(self) -> Dict:
        """Assess overall compliance posture."""
        total = len(self.implementations)
        by_status = {}

        for impl in self.implementations.values():
            status = impl.status.value
            by_status[status] = by_status.get(status, 0) + 1

        return {
            "total_controls": total,
            "by_status": by_status,
            "compliance_rate": by_status.get("implemented", 0) / max(total, 1)
        }


# Example implementation documentation
manager = SecurityControlManager()

manager.document_implementation(
    control_id="AC-2",
    status=ControlStatus.IMPLEMENTED,
    description="""
    AI system access is managed through Azure AD integration.
    - All users authenticate via SSO
    - API keys are managed through HashiCorp Vault
    - Service accounts use managed identities
    - Quarterly access reviews are conducted
    """,
    evidence=[
        "Azure AD configuration export",
        "Vault policy documentation",
        "Access review records in ServiceNow"
    ],
    responsible="Security Operations Team"
)
```

---

## 19.3 FedRAMP for AI Services

### Authorization Boundary

```
┌─────────────────────────────────────────────────────────────────┐
│                    FEDRAMP AUTHORIZATION BOUNDARY                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                   WITHIN BOUNDARY                        │    │
│  │                                                          │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │              AI Application Layer                  │  │    │
│  │  │  • API Gateway          • Safety Filters          │  │    │
│  │  │  • Business Logic       • Audit Logging           │  │    │
│  │  │  • RAG Pipeline         • User Management         │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  │                                                          │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │              Data Layer                            │  │    │
│  │  │  • Vector Database      • Conversation Store      │  │    │
│  │  │  • Document Store       • Audit Logs              │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  │                                                          │    │
│  │  ┌───────────────────────────────────────────────────┐  │    │
│  │  │              Infrastructure                        │  │    │
│  │  │  • Kubernetes           • Networking              │  │    │
│  │  │  • Container Registry   • Key Management          │  │    │
│  │  └───────────────────────────────────────────────────┘  │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                 LEVERAGED AUTHORIZATIONS                 │    │
│  │                                                          │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │    │
│  │  │    AWS      │  │   Azure     │  │   OpenAI    │     │    │
│  │  │  GovCloud   │  │   Gov't     │  │   (JAB P-ATO)│     │    │
│  │  │ (FedRAMP    │  │ (FedRAMP    │  │             │     │    │
│  │  │  High)      │  │  High)      │  │             │     │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘     │    │
│  │                                                          │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### FedRAMP Documentation

```python
class FedRAMPDocumentation:
    """Generate FedRAMP documentation for AI systems."""

    def __init__(self, system_info: Dict):
        self.system = system_info

    def generate_boundary_diagram(self) -> str:
        """Generate authorization boundary description."""
        return f"""
# Authorization Boundary

## System: {self.system['name']}

### Components Within Boundary

| Component | Function | Data Processed |
|-----------|----------|----------------|
| API Gateway | Request routing, authentication | User requests |
| AI Application | Business logic, RAG pipeline | User queries, documents |
| Vector Database | Embedding storage, similarity search | Document embeddings |
| Audit System | Logging, compliance reporting | All system events |

### External Dependencies

| Service | FedRAMP Status | Inheritance |
|---------|----------------|-------------|
| AWS GovCloud | FedRAMP High | IaaS controls |
| OpenAI API | In Process | API-level controls |

### Data Flow

1. User requests enter through API Gateway (authenticated)
2. Requests processed by AI Application with safety checks
3. RAG queries Vector Database for context
4. External AI API called for generation
5. Response filtered and logged
6. Response returned to user
"""

    def generate_crm(self) -> str:
        """Generate Customer Responsibility Matrix."""
        return f"""
# Customer Responsibility Matrix

## {self.system['name']}

| Control | CSP Responsibility | Customer Responsibility |
|---------|-------------------|------------------------|
| AC-2 | Provide IAM service | Manage user accounts |
| AU-2 | Provide logging infrastructure | Configure audit events |
| SC-8 | Provide TLS termination | Configure certificates |
| SC-28 | Provide encryption service | Manage encryption keys |

## AI-Specific Responsibilities

| Capability | CSP | Customer |
|------------|-----|----------|
| Model Safety | Built-in filters | Custom policies |
| Prompt Security | Basic protection | Input validation |
| Output Filtering | Content moderation | Business rules |
| Audit Logging | Log storage | Log review |
"""

    def generate_poam(self, findings: List[Dict]) -> str:
        """Generate Plan of Action and Milestones."""
        poam_entries = []

        for i, finding in enumerate(findings, 1):
            poam_entries.append(f"""
### POA&M-{i:04d}

**Control:** {finding['control']}

**Finding:** {finding['description']}

**Risk Level:** {finding['risk']}

**Remediation Plan:** {finding['remediation']}

**Milestone Date:** {finding['target_date']}

**Status:** {finding['status']}
""")

        return f"""
# Plan of Action and Milestones

## System: {self.system['name']}

{''.join(poam_entries)}
"""
```

---

## 19.4 AI-Specific Security Controls

```python
class AISecurityControls:
    """Implement AI-specific security controls."""

    def __init__(self, config: Dict):
        self.config = config

    # Prompt Injection Protection
    async def validate_input(self, user_input: str) -> Dict:
        """Validate user input for injection attacks."""
        issues = []

        # Check for known injection patterns
        injection_patterns = [
            r"ignore\s+(previous|prior|all)\s+instructions",
            r"system\s*prompt",
            r"<\|.*\|>",
            r"\[INST\]",
            r"```system"
        ]

        for pattern in injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                issues.append({
                    "type": "injection_attempt",
                    "pattern": pattern,
                    "severity": "high"
                })

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    # Output Validation
    async def validate_output(self, output: str) -> Dict:
        """Validate AI output for sensitive content."""
        issues = []

        # Check for PII
        pii_patterns = {
            "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
            "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "phone": r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b"
        }

        for pii_type, pattern in pii_patterns.items():
            if re.search(pattern, output):
                issues.append({
                    "type": "pii_detected",
                    "pii_type": pii_type,
                    "severity": "high"
                })

        # Check for classification markers
        classification_patterns = [
            r"(TOP SECRET|SECRET|CONFIDENTIAL)//",
            r"CLASSIFIED",
            r"NOFORN"
        ]

        for pattern in classification_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                issues.append({
                    "type": "classification_marker",
                    "severity": "critical"
                })

        return {
            "valid": len(issues) == 0,
            "issues": issues
        }

    # Model Integrity
    def verify_model_integrity(self, model_path: str, expected_hash: str) -> bool:
        """Verify model file integrity."""
        import hashlib

        sha256_hash = hashlib.sha256()
        with open(model_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                sha256_hash.update(chunk)

        actual_hash = sha256_hash.hexdigest()
        return actual_hash == expected_hash

    # Rate Limiting
    async def check_rate_limit(
        self,
        user_id: str,
        endpoint: str
    ) -> tuple[bool, str]:
        """Check rate limits for user."""
        key = f"rate:{user_id}:{endpoint}"

        # Get current count
        current = await self.redis.get(key) or 0

        limit = self.config.get("rate_limits", {}).get(endpoint, 100)

        if int(current) >= limit:
            return False, "Rate limit exceeded"

        # Increment counter
        await self.redis.incr(key)
        await self.redis.expire(key, 60)  # 1 minute window

        return True, "OK"

    # Data Classification
    def classify_data(self, content: str) -> str:
        """Classify data sensitivity level."""
        # Check for classification indicators
        if re.search(r"(TOP SECRET|TS//)", content, re.IGNORECASE):
            return "TOP_SECRET"
        if re.search(r"(SECRET//|SECRET\b)", content, re.IGNORECASE):
            return "SECRET"
        if re.search(r"(CONFIDENTIAL//|CONFIDENTIAL\b)", content, re.IGNORECASE):
            return "CONFIDENTIAL"
        if re.search(r"(CUI//|CONTROLLED)", content, re.IGNORECASE):
            return "CUI"

        # Check for PII indicators
        if re.search(r"\b\d{3}-\d{2}-\d{4}\b", content):
            return "CUI"  # SSN indicates CUI

        return "UNCLASSIFIED"
```

---

## 19.5 Continuous Monitoring

```python
class ContinuousMonitoring:
    """Implement ConMon for AI systems."""

    def __init__(self, config: Dict):
        self.config = config
        self.metrics = {}

    async def collect_security_metrics(self) -> Dict:
        """Collect security metrics for ConMon reporting."""
        metrics = {
            "timestamp": datetime.utcnow().isoformat(),
            "access_control": await self._collect_ac_metrics(),
            "audit": await self._collect_audit_metrics(),
            "vulnerability": await self._collect_vuln_metrics(),
            "ai_specific": await self._collect_ai_metrics()
        }

        return metrics

    async def _collect_ac_metrics(self) -> Dict:
        """Collect access control metrics."""
        return {
            "active_users": await self._count_active_users(),
            "api_keys_active": await self._count_api_keys(),
            "failed_auth_attempts": await self._count_failed_auth(),
            "privilege_changes": await self._count_privilege_changes()
        }

    async def _collect_audit_metrics(self) -> Dict:
        """Collect audit metrics."""
        return {
            "events_logged": await self._count_audit_events(),
            "events_by_type": await self._audit_events_by_type(),
            "anomalies_detected": await self._count_anomalies()
        }

    async def _collect_vuln_metrics(self) -> Dict:
        """Collect vulnerability metrics."""
        return {
            "open_vulnerabilities": await self._count_open_vulns(),
            "critical_vulns": await self._count_critical_vulns(),
            "avg_remediation_time": await self._avg_remediation_time()
        }

    async def _collect_ai_metrics(self) -> Dict:
        """Collect AI-specific security metrics."""
        return {
            "injection_attempts": await self._count_injection_attempts(),
            "safety_filter_triggers": await self._count_safety_triggers(),
            "pii_detections": await self._count_pii_detections(),
            "model_drift_score": await self._calculate_model_drift()
        }

    def generate_conmon_report(self, metrics: Dict) -> str:
        """Generate ConMon report."""
        return f"""
# Continuous Monitoring Report

**System:** {self.config['system_name']}
**Period:** {metrics['timestamp']}

## Access Control

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Active Users | {metrics['access_control']['active_users']} | N/A | ✅ |
| Failed Auth | {metrics['access_control']['failed_auth_attempts']} | <100 | {'✅' if metrics['access_control']['failed_auth_attempts'] < 100 else '⚠️'} |

## Audit and Accountability

| Metric | Value | Status |
|--------|-------|--------|
| Events Logged | {metrics['audit']['events_logged']} | ✅ |
| Anomalies | {metrics['audit']['anomalies_detected']} | {'✅' if metrics['audit']['anomalies_detected'] < 10 else '⚠️'} |

## AI-Specific Security

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Injection Attempts | {metrics['ai_specific']['injection_attempts']} | <50 | {'✅' if metrics['ai_specific']['injection_attempts'] < 50 else '⚠️'} |
| Safety Triggers | {metrics['ai_specific']['safety_filter_triggers']} | N/A | ✅ |
| PII Detections | {metrics['ai_specific']['pii_detections']} | 0 | {'✅' if metrics['ai_specific']['pii_detections'] == 0 else '❌'} |

## Recommendations

{'- Review increased injection attempts' if metrics['ai_specific']['injection_attempts'] > 20 else ''}
{'- Investigate PII detections immediately' if metrics['ai_specific']['pii_detections'] > 0 else ''}
"""
```

---

## Hands-On Lab

### Lab 19.1: Implement Security Controls

Implement comprehensive security for an AI system:
1. Map NIST 800-53 controls to AI functionality
2. Document control implementations
3. Build continuous monitoring dashboard
4. Create POA&M for gaps
5. Generate compliance reports

---

## Knowledge Check

1. Which NIST 800-53 control families are most relevant to AI systems?
2. How do you document AI systems in FedRAMP authorization?
3. What AI-specific security controls should be implemented?
4. What metrics should be tracked for continuous monitoring?

---

<div align="center">

[← Module 18: Enterprise Patterns](../18-enterprise-patterns/README.md) | [Home](../../README.md) | [Module 20: Cost Optimization →](../20-cost-optimization/README.md)

</div>
