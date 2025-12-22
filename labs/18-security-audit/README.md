# Lab 18: Security Audit

<div align="center">

**Comprehensive FedRAMP and FISMA Compliance Assessment for AI Systems**

⭐⭐⭐⭐⭐ Master | ⏱️ 240 minutes | 📚 Module 19

</div>

---

## Learning Objectives

By the end of this lab, you will:

- [ ] Conduct a comprehensive security assessment of AI systems
- [ ] Map AI-specific risks to NIST 800-53 controls
- [ ] Evaluate FedRAMP compliance for AI deployments
- [ ] Document findings using federal reporting standards
- [ ] Create a Plan of Action and Milestones (POA&M)

---

## Prerequisites

- Completed Labs 00-17
- Understanding of NIST 800-53 controls
- Familiarity with FedRAMP requirements
- Access to a test AI system to audit

---

## Overview

This lab provides hands-on experience conducting a security audit of AI systems in a federal context. You will apply federal security frameworks to assess risks, evaluate controls, and document compliance status.

---

## Part 1: Pre-Audit Preparation (30 minutes)

### Step 1.1: Establish Audit Scope

Create `audit_scope.md`:

```markdown
# AI System Security Audit Scope

## System Information
- **System Name**: [e.g., FWG Document Assistant]
- **System Owner**: [Name/Organization]
- **Audit Date**: [Date]
- **Auditor(s)**: [Names]

## System Description
[Brief description of the AI system, its purpose, and key components]

## Architecture Overview
```
[User] --> [API Gateway] --> [AI Service] --> [Vector DB]
                                    |
                                    v
                              [LLM Provider]
```

## Data Classification
- **Highest Data Sensitivity**: [e.g., CUI, PII, Public]
- **Data Types Processed**: [List types]
- **Data Storage Locations**: [List locations]

## Compliance Requirements
- [ ] FedRAMP [High/Moderate/Low]
- [ ] FISMA
- [ ] NIST AI RMF
- [ ] Executive Order 14110
- [ ] OMB M-24-10
- [ ] Other: [specify]

## Audit Objectives
1. Assess security controls implementation
2. Identify AI-specific vulnerabilities
3. Evaluate compliance with federal requirements
4. Recommend remediation actions

## Boundaries
### In Scope
- AI model integration
- API security
- Data handling
- Access controls
- Monitoring capabilities

### Out of Scope
- Underlying cloud infrastructure (if using FedRAMP-authorized service)
- Physical security
- Personnel security (unless AI-specific)

## Timeline
| Phase | Duration | Dates |
|-------|----------|-------|
| Planning | 1 day | |
| Assessment | 2 days | |
| Reporting | 1 day | |
```

### Step 1.2: Gather Documentation

Collect these documents before starting:
- [ ] System Security Plan (SSP)
- [ ] Network diagrams
- [ ] Data flow diagrams
- [ ] API documentation
- [ ] Model cards (if available)
- [ ] Previous audit reports
- [ ] Incident reports

---

## Part 2: AI-Specific Control Assessment (60 minutes)

### Step 2.1: Create Assessment Checklist

Create `ai_controls_assessment.md`:

```markdown
# AI-Specific Security Controls Assessment

## 1. AI Model Security (AC - Access Control)

### AC-AI-1: Model Access Control
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| API authentication required | ⬜ | | |
| Role-based access to models | ⬜ | | |
| API key rotation policy | ⬜ | | |
| Service account management | ⬜ | | |

### AC-AI-2: Model Versioning
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Model versions tracked | ⬜ | | |
| Deployment history maintained | ⬜ | | |
| Rollback capability exists | ⬜ | | |

## 2. AI Data Protection (SC - System Communications)

### SC-AI-1: Training Data Protection
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Training data classified | ⬜ | | |
| Sensitive data excluded/anonymized | ⬜ | | |
| Data lineage documented | ⬜ | | |
| Data retention policy enforced | ⬜ | | |

### SC-AI-2: Inference Data Protection
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Input data validated | ⬜ | | |
| Output data filtered | ⬜ | | |
| Encryption in transit (TLS 1.3) | ⬜ | | |
| Encryption at rest | ⬜ | | |
| Logging excludes sensitive data | ⬜ | | |

## 3. AI Integrity (SI - System Integrity)

### SI-AI-1: Prompt Injection Protection
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Input sanitization implemented | ⬜ | | |
| System prompt protection | ⬜ | | |
| Delimiter handling | ⬜ | | |
| Output filtering | ⬜ | | |

### SI-AI-2: Model Integrity
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Model provenance verified | ⬜ | | |
| Model checksums validated | ⬜ | | |
| Adversarial testing performed | ⬜ | | |
| Performance monitoring active | ⬜ | | |

## 4. AI Audit (AU - Audit and Accountability)

### AU-AI-1: AI Activity Logging
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| All API calls logged | ⬜ | | |
| User identification captured | ⬜ | | |
| Prompt/response logging (sanitized) | ⬜ | | |
| Token usage tracked | ⬜ | | |
| Error conditions logged | ⬜ | | |

### AU-AI-2: AI Audit Review
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Regular log reviews | ⬜ | | |
| Anomaly detection | ⬜ | | |
| Incident correlation | ⬜ | | |
| Audit trail retention | ⬜ | | |

## 5. AI Risk Management (RA - Risk Assessment)

### RA-AI-1: AI Impact Assessment
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Algorithm impact assessment | ⬜ | | |
| Bias evaluation | ⬜ | | |
| Rights-impact analysis | ⬜ | | |
| Safety evaluation | ⬜ | | |

### RA-AI-2: Continuous Risk Monitoring
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Performance metrics monitored | ⬜ | | |
| Drift detection implemented | ⬜ | | |
| Feedback mechanism exists | ⬜ | | |
| Periodic reassessment scheduled | ⬜ | | |

## 6. AI Configuration Management (CM)

### CM-AI-1: AI Configuration Control
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| Baseline configurations documented | ⬜ | | |
| Change management process | ⬜ | | |
| Configuration drift monitoring | ⬜ | | |
| Secure defaults enforced | ⬜ | | |

## 7. AI Incident Response (IR)

### IR-AI-1: AI-Specific Incident Handling
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| AI incident types defined | ⬜ | | |
| Escalation procedures | ⬜ | | |
| Model isolation capability | ⬜ | | |
| Forensic procedures | ⬜ | | |

## 8. Human Oversight (New AI-Specific)

### HO-AI-1: Human-in-the-Loop
| Item | Status | Evidence | Notes |
|------|--------|----------|-------|
| High-risk decisions reviewed | ⬜ | | |
| Override capability exists | ⬜ | | |
| Escalation procedures | ⬜ | | |
| Training for reviewers | ⬜ | | |
```

---

## Part 3: Technical Testing (60 minutes)

### Step 3.1: Automated Security Scan

Create `scan_ai_system.py`:

```python
"""
Automated security scanning for AI systems.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List
from dataclasses import dataclass, field

@dataclass
class Finding:
    """Security finding from scan."""
    category: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    title: str
    description: str
    evidence: str
    recommendation: str
    control_mapping: List[str] = field(default_factory=list)

class AISecurityScanner:
    """Scanner for AI system security assessment."""

    def __init__(self, target_url: str, api_key: str = None):
        self.target_url = target_url.rstrip('/')
        self.api_key = api_key
        self.findings: List[Finding] = []

    def scan_all(self) -> List[Finding]:
        """Run all security scans."""
        self.check_tls()
        self.check_authentication()
        self.check_rate_limiting()
        self.check_input_validation()
        self.check_error_handling()
        self.check_headers()
        return self.findings

    def check_tls(self):
        """Check TLS configuration."""
        try:
            response = requests.get(self.target_url, timeout=10)
            if not self.target_url.startswith('https'):
                self.findings.append(Finding(
                    category="Transport Security",
                    severity="CRITICAL",
                    title="No HTTPS",
                    description="API endpoint does not use HTTPS",
                    evidence=f"URL: {self.target_url}",
                    recommendation="Enable HTTPS with TLS 1.3",
                    control_mapping=["SC-8", "SC-13"]
                ))
        except Exception as e:
            self.findings.append(Finding(
                category="Transport Security",
                severity="INFO",
                title="Connection Error",
                description=str(e),
                evidence="",
                recommendation="Verify endpoint availability"
            ))

    def check_authentication(self):
        """Check authentication requirements."""
        try:
            # Try unauthenticated request
            response = requests.post(
                f"{self.target_url}/chat",
                json={"message": "test"},
                timeout=10
            )
            if response.status_code == 200:
                self.findings.append(Finding(
                    category="Access Control",
                    severity="CRITICAL",
                    title="No Authentication Required",
                    description="API accepts requests without authentication",
                    evidence=f"Status: {response.status_code}",
                    recommendation="Implement API key or OAuth authentication",
                    control_mapping=["AC-2", "IA-2", "IA-8"]
                ))
        except:
            pass

    def check_rate_limiting(self):
        """Check rate limiting implementation."""
        try:
            responses = []
            for i in range(50):
                response = requests.post(
                    f"{self.target_url}/chat",
                    json={"message": "test"},
                    headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                    timeout=5
                )
                responses.append(response.status_code)

            if 429 not in responses:
                self.findings.append(Finding(
                    category="Availability",
                    severity="MEDIUM",
                    title="No Rate Limiting Detected",
                    description="API does not appear to implement rate limiting",
                    evidence=f"50 requests, no 429 responses",
                    recommendation="Implement rate limiting to prevent abuse",
                    control_mapping=["SC-5", "AU-6"]
                ))
        except:
            pass

    def check_input_validation(self):
        """Check input validation."""
        test_payloads = [
            {"message": "A" * 100000},  # Length test
            {"message": "<script>alert('xss')</script>"},  # XSS test
            {"message": "'; DROP TABLE users; --"},  # SQLi test
            {"message": "{{7*7}}"},  # Template injection
        ]

        for payload in test_payloads:
            try:
                response = requests.post(
                    f"{self.target_url}/chat",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                    timeout=30
                )
                # Check if suspicious content reflected
                if "<script>" in response.text or "49" in response.text:
                    self.findings.append(Finding(
                        category="Input Validation",
                        severity="HIGH",
                        title="Insufficient Input Validation",
                        description="API may be vulnerable to injection attacks",
                        evidence=f"Payload: {list(payload.values())[0][:50]}...",
                        recommendation="Implement strict input validation",
                        control_mapping=["SI-10", "SI-3"]
                    ))
            except:
                pass

    def check_error_handling(self):
        """Check error message exposure."""
        try:
            response = requests.post(
                f"{self.target_url}/chat",
                json={"invalid": "payload"},
                headers={"Authorization": f"Bearer {self.api_key}"} if self.api_key else {},
                timeout=10
            )
            error_indicators = ["traceback", "exception", "stack", "error at line", "debug"]
            if any(ind in response.text.lower() for ind in error_indicators):
                self.findings.append(Finding(
                    category="Information Disclosure",
                    severity="MEDIUM",
                    title="Verbose Error Messages",
                    description="API exposes detailed error information",
                    evidence=response.text[:200],
                    recommendation="Implement generic error responses",
                    control_mapping=["SI-11", "SC-7"]
                ))
        except:
            pass

    def check_headers(self):
        """Check security headers."""
        try:
            response = requests.get(self.target_url, timeout=10)
            required_headers = {
                "Strict-Transport-Security": "HSTS not configured",
                "X-Content-Type-Options": "Content type sniffing not prevented",
                "X-Frame-Options": "Clickjacking protection not enabled",
                "Content-Security-Policy": "CSP not configured"
            }

            for header, message in required_headers.items():
                if header not in response.headers:
                    self.findings.append(Finding(
                        category="Security Headers",
                        severity="LOW",
                        title=f"Missing {header}",
                        description=message,
                        evidence=f"Header not present in response",
                        recommendation=f"Add {header} header",
                        control_mapping=["SC-7", "SI-10"]
                    ))
        except:
            pass

    def generate_report(self) -> Dict:
        """Generate scan report."""
        severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "INFO": 0}
        for finding in self.findings:
            severity_counts[finding.severity] += 1

        return {
            "scan_date": datetime.now().isoformat(),
            "target": self.target_url,
            "summary": severity_counts,
            "findings": [
                {
                    "category": f.category,
                    "severity": f.severity,
                    "title": f.title,
                    "description": f.description,
                    "evidence": f.evidence,
                    "recommendation": f.recommendation,
                    "controls": f.control_mapping
                }
                for f in self.findings
            ]
        }


if __name__ == "__main__":
    import sys
    from rich import print

    # Demo scan
    print("[bold]AI Security Scanner Demo[/bold]\n")
    print("This scanner checks for common security issues in AI APIs.")
    print("In production, point this at your actual AI system endpoint.\n")

    # Create sample report for demo
    sample_findings = [
        Finding(
            category="Access Control",
            severity="HIGH",
            title="Weak API Key Policy",
            description="API keys do not expire",
            evidence="Key created 365+ days ago still valid",
            recommendation="Implement 90-day key rotation",
            control_mapping=["IA-5", "AC-2"]
        ),
        Finding(
            category="Logging",
            severity="MEDIUM",
            title="Incomplete Audit Logging",
            description="Prompt content not logged",
            evidence="Log analysis shows missing fields",
            recommendation="Log all prompts (sanitized)",
            control_mapping=["AU-2", "AU-3"]
        )
    ]

    print("[cyan]Sample Findings:[/cyan]")
    for f in sample_findings:
        color = {"CRITICAL": "red", "HIGH": "orange", "MEDIUM": "yellow"}.get(f.severity, "white")
        print(f"  [{color}]{f.severity}[/{color}] {f.title}: {f.description}")
```

---

## Part 4: Compliance Mapping (45 minutes)

### Step 4.1: Create NIST Control Mapping

Create `nist_ai_mapping.md`:

```markdown
# NIST 800-53 to AI System Control Mapping

## Access Control (AC)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| AC-2 | Model/API access management | ⬜ |
| AC-3 | Enforce authorized model access | ⬜ |
| AC-4 | Information flow between AI components | ⬜ |
| AC-6 | Least privilege for AI services | ⬜ |
| AC-17 | Remote access to AI systems | ⬜ |

## Audit and Accountability (AU)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| AU-2 | Define AI-auditable events | ⬜ |
| AU-3 | Content of AI audit records | ⬜ |
| AU-6 | Audit review for AI anomalies | ⬜ |
| AU-12 | Audit generation for AI activities | ⬜ |

## Configuration Management (CM)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| CM-2 | AI system baseline configuration | ⬜ |
| CM-3 | AI configuration change control | ⬜ |
| CM-6 | AI security configuration settings | ⬜ |
| CM-7 | AI least functionality | ⬜ |

## Identification and Authentication (IA)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| IA-2 | User identification for AI access | ⬜ |
| IA-5 | Authenticator management (API keys) | ⬜ |
| IA-8 | Identification for AI-to-AI comm | ⬜ |

## Risk Assessment (RA)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| RA-3 | AI-specific risk assessment | ⬜ |
| RA-5 | AI vulnerability scanning | ⬜ |

## System and Communications Protection (SC)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| SC-7 | AI boundary protection | ⬜ |
| SC-8 | AI data transmission protection | ⬜ |
| SC-13 | Cryptographic protection for AI | ⬜ |
| SC-28 | Protection of AI data at rest | ⬜ |

## System and Information Integrity (SI)

| Control | AI Application | Implementation Status |
|---------|---------------|----------------------|
| SI-3 | AI malicious code protection | ⬜ |
| SI-4 | AI system monitoring | ⬜ |
| SI-10 | AI input validation | ⬜ |
| SI-11 | AI error handling | ⬜ |
```

---

## Part 5: Documentation and Reporting (45 minutes)

### Step 5.1: Create POA&M Template

Create `poam_template.md`:

```markdown
# Plan of Action and Milestones (POA&M)

## System Information
- **System Name**:
- **FISMA System ID**:
- **Assessment Date**:
- **POA&M Created**:
- **System Owner**:

---

## Finding #1

### Basic Information
| Field | Value |
|-------|-------|
| POA&M ID | AI-2025-001 |
| Weakness Description | [Description] |
| Weakness Source | Security Assessment |
| Point of Contact | [Name] |

### Risk Assessment
| Field | Value |
|-------|-------|
| Severity | [CRITICAL/HIGH/MEDIUM/LOW] |
| Likelihood | [HIGH/MEDIUM/LOW] |
| Impact | [HIGH/MEDIUM/LOW] |
| Overall Risk | [CRITICAL/HIGH/MEDIUM/LOW] |

### Control Mapping
| Framework | Control(s) |
|-----------|-----------|
| NIST 800-53 | [e.g., AC-2, IA-5] |
| FedRAMP | [e.g., AC-2 (FedRAMP)] |
| NIST AI RMF | [e.g., MEASURE 2.1] |

### Remediation
| Field | Value |
|-------|-------|
| Scheduled Completion | [Date] |
| Actual Completion | |
| Milestones | 1. [Milestone] by [Date] |
| | 2. [Milestone] by [Date] |
| Resources Required | [Resources] |
| Cost Estimate | [Cost] |
| Status | Open |

### Comments
[Additional context, dependencies, or risks]

---

## Summary Statistics

| Severity | Open | In Progress | Completed |
|----------|------|-------------|-----------|
| Critical | | | |
| High | | | |
| Medium | | | |
| Low | | | |
| **Total** | | | |

## Next Review Date: [Date]
```

### Step 5.2: Create Executive Summary Template

Create `executive_summary.md`:

```markdown
# AI System Security Audit - Executive Summary

## Overview

**System**: [System Name]
**Audit Period**: [Start Date] - [End Date]
**Classification**: UNCLASSIFIED // FOR OFFICIAL USE ONLY

---

## Key Findings

### Overall Risk Rating: [CRITICAL/HIGH/MEDIUM/LOW]

| Category | Findings | Severity |
|----------|----------|----------|
| Access Control | X | [Highest] |
| Data Protection | X | [Highest] |
| Prompt Security | X | [Highest] |
| Logging & Monitoring | X | [Highest] |
| **Total** | **XX** | |

---

## Critical Findings Requiring Immediate Action

1. **[Finding Title]**
   - Risk: [Description]
   - Recommended Action: [Action]
   - Timeline: Immediate

2. **[Finding Title]**
   - Risk: [Description]
   - Recommended Action: [Action]
   - Timeline: 30 days

---

## Compliance Status

| Requirement | Status | Notes |
|-------------|--------|-------|
| FedRAMP | ⬜ Partial | [Notes] |
| FISMA | ⬜ Partial | [Notes] |
| NIST AI RMF | ⬜ Partial | [Notes] |
| EO 14110 | ⬜ Partial | [Notes] |

---

## Recommendations

### Immediate (0-30 days)
1. [Recommendation]
2. [Recommendation]

### Short-term (30-90 days)
1. [Recommendation]
2. [Recommendation]

### Long-term (90+ days)
1. [Recommendation]
2. [Recommendation]

---

## Resource Requirements

| Resource | Estimated Cost | Priority |
|----------|---------------|----------|
| [Resource] | $XX,XXX | High |
| [Resource] | $XX,XXX | Medium |

---

## Conclusion

[Summary paragraph with overall assessment and path forward]

---

**Prepared by**: [Name], [Title]
**Reviewed by**: [Name], [Title]
**Approved by**: [Name], [Title]
**Date**: [Date]
```

---

## Exercises

### Exercise 1: Conduct Assessment
Perform a complete security assessment of a test AI system.

### Exercise 2: Write POA&M
Create a POA&M for findings from your assessment.

### Exercise 3: Present Findings
Prepare and deliver an executive briefing on audit results.

---

## Knowledge Check

1. **What NIST 800-53 controls are most relevant to AI systems?**

2. **How does AI security differ from traditional software security?**

3. **What additional controls might be needed for high-risk AI?**

4. **How should AI-specific risks be documented in a POA&M?**

---

## Next Steps

**Next Lab:** [Lab 19: Cost Analysis →](../19-cost-analysis/README.md)

---

<div align="center">

**Lab 18 Complete!** 🎉

</div>
