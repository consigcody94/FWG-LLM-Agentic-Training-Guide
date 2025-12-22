# AI Impact Assessment Template

<div align="center">

**Federal AI System Impact Assessment**

*Per NIST AI RMF and OMB M-24-10*

</div>

---

## System Information

| Field | Value |
|-------|-------|
| System Name | |
| System Owner | |
| Assessment Date | |
| Assessor(s) | |
| Version | |
| Classification | UNCLASSIFIED |

---

## Section 1: System Description

### 1.1 Purpose and Function

**What does this AI system do?**
```
[Describe the primary function and purpose of the AI system]
```

**What decisions or actions does it support?**
```
[Describe the decisions or actions the system supports or automates]
```

### 1.2 Stakeholders

| Stakeholder Type | Description | Contact |
|-----------------|-------------|---------|
| System Owner | | |
| Technical Lead | | |
| End Users | | |
| Affected Parties | | |
| Oversight Body | | |

### 1.3 AI Components

| Component | Description | Provider | Model/Version |
|-----------|-------------|----------|---------------|
| | | | |
| | | | |

---

## Section 2: Data Assessment

### 2.1 Training Data

**Data sources used for training or fine-tuning:**
```
[ ] Third-party pre-trained model (specify: ________________)
[ ] Custom training data (describe sources below)
[ ] Fine-tuning on agency data
[ ] No training performed (inference only)
```

**If custom data used:**
| Data Source | Classification | Volume | Date Range |
|-------------|---------------|--------|------------|
| | | | |

### 2.2 Inference Data

**What data does the system process in operation?**

| Data Type | Classification | PII Present? | Source |
|-----------|---------------|--------------|--------|
| | | [ ] Yes [ ] No | |
| | | [ ] Yes [ ] No | |

### 2.3 Data Governance

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Data classification completed | ⬜ | |
| PII handling compliant with Privacy Act | ⬜ | |
| Data retention policy defined | ⬜ | |
| Data minimization applied | ⬜ | |
| Consent obtained (if applicable) | ⬜ | |

---

## Section 3: Risk Assessment

### 3.1 Risk Level Determination

**Determine the risk level based on the following factors:**

| Factor | Low | Medium | High | Assessment |
|--------|-----|--------|------|------------|
| Rights Impact | No individual rights affected | Indirect impact on rights | Direct impact on civil rights or liberties | ⬜ Low ⬜ Med ⬜ High |
| Safety Impact | No safety implications | Potential indirect safety impact | Direct safety-of-life implications | ⬜ Low ⬜ Med ⬜ High |
| Scale | < 1,000 users | 1,000 - 100,000 users | > 100,000 users | ⬜ Low ⬜ Med ⬜ High |
| Autonomy | Advisory only, human decides | Supports human decision | Autonomous decision-making | ⬜ Low ⬜ Med ⬜ High |
| Reversibility | Easily reversed | Reversible with effort | Irreversible or difficult | ⬜ Low ⬜ Med ⬜ High |

**Overall Risk Level:** ⬜ Low ⬜ Medium ⬜ High

### 3.2 Rights-Impacting AI Assessment

**Does this system involve any of the following? (Per OMB M-24-10)**

| Category | Yes/No | If Yes, Describe Safeguards |
|----------|--------|---------------------------|
| Access to government services | ⬜ Yes ⬜ No | |
| Safety or security decisions | ⬜ Yes ⬜ No | |
| Civil rights or civil liberties | ⬜ Yes ⬜ No | |
| Access to critical resources | ⬜ Yes ⬜ No | |
| Human oversight circumvention | ⬜ Yes ⬜ No | |

**If any "Yes" above, this is Rights-Impacting AI requiring enhanced oversight.**

---

## Section 4: Fairness and Bias Assessment

### 4.1 Potential Bias Sources

| Source | Applicable? | Mitigation |
|--------|-------------|------------|
| Training data bias | ⬜ Yes ⬜ No ⬜ N/A | |
| Selection bias | ⬜ Yes ⬜ No ⬜ N/A | |
| Measurement bias | ⬜ Yes ⬜ No ⬜ N/A | |
| Algorithmic bias | ⬜ Yes ⬜ No ⬜ N/A | |
| Deployment context bias | ⬜ Yes ⬜ No ⬜ N/A | |

### 4.2 Demographic Analysis

**Protected classes potentially affected:**
```
[ ] Race/Ethnicity
[ ] Gender
[ ] Age
[ ] Disability
[ ] National Origin
[ ] Religion
[ ] Other: ________________
```

### 4.3 Bias Testing Results

| Metric | Baseline | After Mitigation | Target |
|--------|----------|------------------|--------|
| Demographic parity | | | |
| Equal opportunity | | | |
| Disparate impact ratio | | | |

---

## Section 5: Human Oversight

### 5.1 Oversight Model

**Select the oversight model:**
```
[ ] Human-in-the-loop: Human approves each AI decision
[ ] Human-on-the-loop: Human monitors and can intervene
[ ] Human-in-command: Human sets parameters, AI operates within bounds
[ ] Autonomous: No human oversight (requires justification)
```

### 5.2 Oversight Mechanisms

| Mechanism | Implemented? | Description |
|-----------|--------------|-------------|
| Human review of high-risk decisions | ⬜ | |
| Override capability | ⬜ | |
| Escalation procedures | ⬜ | |
| Regular audit reviews | ⬜ | |
| Performance monitoring | ⬜ | |

### 5.3 Staffing for Oversight

| Role | FTE Required | Currently Staffed? |
|------|--------------|-------------------|
| AI System Monitor | | ⬜ Yes ⬜ No |
| Decision Reviewer | | ⬜ Yes ⬜ No |
| Technical Support | | ⬜ Yes ⬜ No |

---

## Section 6: Transparency and Explainability

### 6.1 Notice to Users

| Requirement | Status | Implementation |
|-------------|--------|----------------|
| Users informed AI is in use | ⬜ | |
| Explanation of AI role provided | ⬜ | |
| Opt-out available (if applicable) | ⬜ | |
| Contact for questions provided | ⬜ | |

### 6.2 Explainability

**Can the system explain its outputs?**
```
[ ] Full explanation available for each decision
[ ] General explanation of decision factors
[ ] Black box - limited explainability
[ ] Not applicable (non-decision system)
```

**Explainability approach:**
```
[Describe how decisions/outputs are explained to users and oversight]
```

---

## Section 7: Security Assessment

### 7.1 Security Controls

| Control | Status | Evidence |
|---------|--------|----------|
| Authentication required | ⬜ | |
| Authorization controls | ⬜ | |
| Encryption at rest | ⬜ | |
| Encryption in transit | ⬜ | |
| Audit logging | ⬜ | |
| Input validation | ⬜ | |
| Prompt injection protection | ⬜ | |

### 7.2 Adversarial Robustness

| Testing | Completed? | Results |
|---------|------------|---------|
| Prompt injection testing | ⬜ | |
| Data poisoning resistance | ⬜ | |
| Model extraction prevention | ⬜ | |
| Evasion attack testing | ⬜ | |

---

## Section 8: Compliance Mapping

### 8.1 Regulatory Requirements

| Requirement | Applicable? | Status | Notes |
|-------------|-------------|--------|-------|
| FedRAMP | ⬜ Yes ⬜ No | ⬜ Compliant | |
| FISMA | ⬜ Yes ⬜ No | ⬜ Compliant | |
| Privacy Act | ⬜ Yes ⬜ No | ⬜ Compliant | |
| Section 508 | ⬜ Yes ⬜ No | ⬜ Compliant | |
| EO 14110 | ⬜ Yes ⬜ No | ⬜ Compliant | |
| OMB M-24-10 | ⬜ Yes ⬜ No | ⬜ Compliant | |

### 8.2 NIST AI RMF Alignment

| Function | Practices | Status |
|----------|-----------|--------|
| **GOVERN** | Roles defined | ⬜ |
| | Policies established | ⬜ |
| | Accountability clear | ⬜ |
| **MAP** | Context documented | ⬜ |
| | Stakeholders identified | ⬜ |
| | Impacts assessed | ⬜ |
| **MEASURE** | Metrics defined | ⬜ |
| | Testing performed | ⬜ |
| | Monitoring planned | ⬜ |
| **MANAGE** | Risks prioritized | ⬜ |
| | Mitigations in place | ⬜ |
| | Response plans ready | ⬜ |

---

## Section 9: Recommendations

### 9.1 Required Actions Before Deployment

| # | Action | Priority | Owner | Due Date |
|---|--------|----------|-------|----------|
| 1 | | ⬜ Critical ⬜ High ⬜ Medium | | |
| 2 | | ⬜ Critical ⬜ High ⬜ Medium | | |
| 3 | | ⬜ Critical ⬜ High ⬜ Medium | | |

### 9.2 Ongoing Monitoring Requirements

| Metric | Frequency | Threshold | Action if Exceeded |
|--------|-----------|-----------|-------------------|
| | | | |
| | | | |

### 9.3 Review Schedule

| Review Type | Frequency | Next Review Date |
|-------------|-----------|------------------|
| Impact reassessment | Annual | |
| Bias monitoring | Quarterly | |
| Security review | Annual | |
| Performance evaluation | Monthly | |

---

## Section 10: Approval

### 10.1 Assessment Certification

I certify that this assessment accurately represents the AI system and its impacts.

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Assessor | | | |
| Technical Lead | | | |
| Privacy Officer | | | |
| Security Officer | | | |

### 10.2 Deployment Authorization

**Recommendation:** ⬜ Approve ⬜ Approve with Conditions ⬜ Deny

**Conditions (if applicable):**
```
[List any conditions that must be met before or during deployment]
```

**Authorizing Official:**

| Name | Title | Signature | Date |
|------|-------|-----------|------|
| | | | |

---

*This template aligns with NIST AI RMF, OMB M-24-10, and federal AI governance requirements.*
