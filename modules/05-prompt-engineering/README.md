<div align="center">

# Module 05: Prompt Engineering

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_01--02-orange?style=for-the-badge" alt="Prerequisites"/>

*The art and science of communicating effectively with LLMs*

</div>

---

## 📋 Learning Objectives

By the end of this module, you will be able to:

- [ ] Design effective prompts using proven patterns
- [ ] Implement Chain-of-Thought and ReAct reasoning
- [ ] Create robust system prompts for federal applications
- [ ] Optimize prompts for accuracy and cost efficiency
- [ ] Debug and iterate on prompt performance

---

## 📑 Table of Contents

1. [Prompt Anatomy](#1-prompt-anatomy)
2. [Few-Shot Learning](#2-few-shot-learning)
3. [Chain-of-Thought Prompting](#3-chain-of-thought-prompting)
4. [ReAct Prompting](#4-react-prompting)
5. [System Prompts](#5-system-prompts)
6. [Prompt Optimization](#6-prompt-optimization)

---

## 1. Prompt Anatomy

### The Structure of Effective Prompts

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         PROMPT ANATOMY                                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  1. CONTEXT / ROLE                                                     │ ║
║  │  "You are a federal compliance expert specializing in FedRAMP..."      │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  2. TASK / INSTRUCTION                                                 │ ║
║  │  "Analyze the following system description for security gaps..."       │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  3. INPUT / DATA                                                       │ ║
║  │  "System Description: The application uses AWS S3 for storage..."      │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  4. OUTPUT FORMAT                                                      │ ║
║  │  "Respond in JSON format with: {findings: [], risk_level: string}"     │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                    │                                         ║
║                                    ▼                                         ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │  5. CONSTRAINTS / GUARDRAILS                                           │ ║
║  │  "Only cite published NIST controls. Do not speculate on findings."    │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Example: Complete Prompt

```markdown
**ROLE:**
You are a Senior Federal Compliance Analyst with 15 years of experience
in FedRAMP and FISMA assessments. You specialize in cloud security
architectures and have conducted over 100 security control assessments.

**TASK:**
Evaluate the provided system architecture against NIST 800-53 Moderate
baseline controls and identify potential security gaps.

**INPUT:**
System Architecture Description:
- Web application hosted on AWS GovCloud
- Uses RDS PostgreSQL for data storage
- Authentication via AWS Cognito
- No encryption at rest currently implemented
- Logs stored in CloudWatch for 30 days

**OUTPUT FORMAT:**
Provide your analysis in this structure:
1. COMPLIANT CONTROLS: List controls that appear satisfied
2. GAPS IDENTIFIED: List controls with deficiencies
3. RISK RATING: Overall risk (Critical/High/Medium/Low)
4. RECOMMENDATIONS: Prioritized remediation steps

**CONSTRAINTS:**
- Only reference NIST 800-53 Rev 5 controls
- Do not assume any controls not explicitly described
- Be specific about control IDs (e.g., SC-28, AU-4)
- Focus on Moderate baseline requirements
```

---

## 2. Few-Shot Learning

### Concept

Few-shot learning provides examples in the prompt to guide the model's response format and reasoning.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         FEW-SHOT LEARNING                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                                                                      │    ║
║  │   ZERO-SHOT          FEW-SHOT (2-3)        MANY-SHOT (5+)          │    ║
║  │                                                                      │    ║
║  │   "Classify this     "Here are examples:   Extensive examples       │    ║
║  │    document"         Doc A → Category 1    but higher token         │    ║
║  │                      Doc B → Category 2    cost                     │    ║
║  │   Quick but may      Now classify Doc C"                            │    ║
║  │   lack precision                          Most accurate             │    ║
║  │                      Good balance         but expensive             │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Example: Control Implementation Statements

```markdown
Generate NIST 800-53 control implementation statements following these examples:

**Example 1:**
Control: AC-2(a) - Account Management | Account Types
Statement: "The organization identifies and selects the following account types
for the information system: privileged accounts (system administrators, database
administrators), non-privileged accounts (standard users), system accounts
(service accounts), and emergency accounts (break-glass access)."

**Example 2:**
Control: AU-3 - Content of Audit Records
Statement: "The information system generates audit records containing information
that establishes the type of event, when the event occurred, where the event
occurred, the source of the event, the outcome of the event, and the identity
of individuals or subjects associated with the event."

**Now generate a statement for:**
Control: SC-28 - Protection of Information at Rest
Statement:
```

---

## 3. Chain-of-Thought Prompting

### The Technique

Chain-of-Thought (CoT) prompting encourages the model to show its reasoning step-by-step.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CHAIN-OF-THOUGHT REASONING                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WITHOUT CoT:                                                                ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  Q: Does this system require FedRAMP High authorization?            │    ║
║  │  A: Yes. ← (No reasoning visible, harder to verify)                 │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  WITH CoT:                                                                   ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  Q: Does this system require FedRAMP High authorization?            │    ║
║  │     Think through this step-by-step.                                │    ║
║  │                                                                      │    ║
║  │  A: Let me analyze this step-by-step:                               │    ║
║  │                                                                      │    ║
║  │  Step 1: Identify the data types                                    │    ║
║  │  - The system processes law enforcement sensitive data              │    ║
║  │  - Contains PII of protected witnesses                              │    ║
║  │                                                                      │    ║
║  │  Step 2: Determine impact levels per FIPS 199                       │    ║
║  │  - Confidentiality: HIGH (disclosure could cause grave harm)        │    ║
║  │  - Integrity: HIGH (modification could endanger lives)              │    ║
║  │  - Availability: MODERATE (24-hour recovery acceptable)             │    ║
║  │                                                                      │    ║
║  │  Step 3: Apply high-water mark                                      │    ║
║  │  - Overall impact: HIGH (highest of the three)                      │    ║
║  │                                                                      │    ║
║  │  Step 4: Map to FedRAMP                                             │    ║
║  │  - FIPS 199 HIGH maps to FedRAMP High baseline                      │    ║
║  │                                                                      │    ║
║  │  Conclusion: Yes, FedRAMP High authorization is required because    │    ║
║  │  the system processes data with HIGH confidentiality and integrity  │    ║
║  │  impact levels.                                                     │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### CoT Prompt Template

```markdown
[TASK DESCRIPTION]

Think through this step-by-step:

1. First, identify the key factors that need to be considered
2. Then, analyze each factor individually
3. Next, consider how these factors interact
4. Finally, synthesize your analysis into a conclusion

Show your reasoning at each step before providing your final answer.
```

---

## 4. ReAct Prompting

### Reasoning + Acting

ReAct combines reasoning with action-taking, ideal for tasks requiring tool use.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                            ReAct PATTERN                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                                                                      │    ║
║  │  THOUGHT → ACTION → OBSERVATION → THOUGHT → ACTION → ... → ANSWER   │    ║
║  │                                                                      │    ║
║  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │    ║
║  │  │ THOUGHT  │───▶│  ACTION  │───▶│OBSERVATION│                      │    ║
║  │  │          │    │          │    │           │                      │    ║
║  │  │"I need to│    │search_   │    │"Found 3   │                      │    ║
║  │  │ find the │    │controls( │    │ relevant  │                      │    ║
║  │  │ relevant │    │ 'access')│    │ controls" │                      │    ║
║  │  │ controls"│    │          │    │           │                      │    ║
║  │  └──────────┘    └──────────┘    └──────────┘                       │    ║
║  │       │                                │                             │    ║
║  │       └────────────────────────────────┘                             │    ║
║  │                      │                                               │    ║
║  │                      ▼                                               │    ║
║  │              ┌──────────┐                                           │    ║
║  │              │  FINAL   │                                           │    ║
║  │              │  ANSWER  │                                           │    ║
║  │              └──────────┘                                           │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### ReAct Example

```markdown
You have access to these tools:
- search_controls(query): Search NIST 800-53 controls
- get_control_details(control_id): Get full control text
- check_implementation(system_id, control_id): Check if control is implemented

Question: What access control gaps exist in System-X?

Thought: I need to first search for access control related NIST controls
Action: search_controls("access control")
Observation: Found controls: AC-1, AC-2, AC-3, AC-4, AC-5, AC-6, AC-7...

Thought: Let me check the implementation status of the core access controls
Action: check_implementation("System-X", "AC-2")
Observation: AC-2 status: Partially Implemented - missing periodic review

Thought: I should check AC-3 as well for access enforcement
Action: check_implementation("System-X", "AC-3")
Observation: AC-3 status: Implemented

Thought: Let me check AC-6 for least privilege
Action: check_implementation("System-X", "AC-6")
Observation: AC-6 status: Not Implemented - no role-based access

Thought: I now have enough information to answer
Final Answer: System-X has the following access control gaps:
1. AC-2 (Account Management): Partially implemented - periodic account reviews not conducted
2. AC-6 (Least Privilege): Not implemented - role-based access control not configured
```

---

## 5. System Prompts

### Federal System Prompt Template

```markdown
# IDENTITY AND PURPOSE

You are [ROLE NAME], a [EXPERTISE AREA] specialist working for [AGENCY/CONTEXT].
Your primary function is to [PRIMARY RESPONSIBILITY].

# CORE CAPABILITIES

You are able to:
- [Capability 1]
- [Capability 2]
- [Capability 3]

# KNOWLEDGE DOMAINS

Your expertise includes:
- [Domain 1 with specifics]
- [Domain 2 with specifics]
- [Domain 3 with specifics]

# BEHAVIORAL GUIDELINES

When responding, you must:
1. [Guideline 1 - e.g., "Always cite specific control IDs"]
2. [Guideline 2 - e.g., "Acknowledge uncertainty explicitly"]
3. [Guideline 3 - e.g., "Prioritize findings by risk level"]

# CONSTRAINTS AND LIMITATIONS

You must NOT:
- [Constraint 1 - e.g., "Speculate on classified information"]
- [Constraint 2 - e.g., "Provide legal advice"]
- [Constraint 3 - e.g., "Claim certainty without evidence"]

# OUTPUT PREFERENCES

Unless otherwise specified:
- Use [format preference]
- Include [required elements]
- Organize by [organization method]

# INTERACTION STYLE

Communicate in a [tone description] manner that is:
- [Style attribute 1]
- [Style attribute 2]
- [Style attribute 3]
```

### Example: Federal Compliance Assistant

```markdown
# IDENTITY AND PURPOSE

You are the Federal Compliance Assistant, an AI specialist in federal
information security frameworks and compliance requirements. You serve
federal agency personnel who need guidance on security controls,
compliance documentation, and risk assessment.

# CORE CAPABILITIES

You are able to:
- Analyze systems against NIST 800-53, FedRAMP, and FISMA requirements
- Generate compliance documentation including SSP sections and POA&M entries
- Explain control requirements in plain language
- Identify gaps between current state and compliance requirements
- Recommend remediation approaches prioritized by risk

# KNOWLEDGE DOMAINS

Your expertise includes:
- NIST 800-53 Rev 5 security and privacy controls
- FedRAMP authorization process (Low, Moderate, High baselines)
- FISMA requirements and reporting
- NIST Cybersecurity Framework
- Cloud security architecture (AWS, Azure, GCP)
- Federal PKI and identity management

# BEHAVIORAL GUIDELINES

When responding, you must:
1. Always cite specific control IDs when referencing requirements (e.g., AC-2, SC-28)
2. Distinguish between control requirements and implementation guidance
3. Acknowledge when questions fall outside your knowledge scope
4. Prioritize findings by potential impact (Critical > High > Medium > Low)
5. Provide actionable recommendations, not just observations

# CONSTRAINTS AND LIMITATIONS

You must NOT:
- Provide definitive compliance determinations (only assessors can do that)
- Speculate on classified systems or data handling procedures
- Give legal advice on liability or contractual matters
- Claim that any guidance supersedes official agency policies
- Generate fake audit evidence or falsify compliance status

# OUTPUT PREFERENCES

Unless otherwise specified:
- Use markdown formatting for readability
- Include control IDs in parentheses after requirements
- Organize findings by control family (AC, AU, SC, etc.)
- Provide both technical and non-technical explanations when helpful

# INTERACTION STYLE

Communicate in a professional, precise manner that is:
- Clear and jargon-free when possible (define acronyms on first use)
- Thorough but concise (comprehensive without being verbose)
- Practical (focus on actionable guidance)
- Appropriately cautious (acknowledge limitations and uncertainties)
```

---

## 6. Prompt Optimization

### Optimization Strategies

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      PROMPT OPTIMIZATION STRATEGIES                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1. CLARITY OPTIMIZATION                                                     ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  ❌ "Make it better"                                                │    ║
║  │  ✅ "Improve readability by breaking into sections with headers"    │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  2. TOKEN EFFICIENCY                                                         ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  ❌ "Please provide a comprehensive and detailed analysis of..."    │    ║
║  │  ✅ "Analyze:" (context makes verbosity unnecessary)                │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  3. OUTPUT STRUCTURE                                                         ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  ❌ "Tell me about the findings"                                    │    ║
║  │  ✅ "List findings as: | Control | Status | Gap | Priority |"       │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  4. CONSTRAINT SPECIFICATION                                                 ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  ❌ "Give me a short answer"                                        │    ║
║  │  ✅ "Respond in 3 sentences or fewer"                               │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  5. EXAMPLE ANCHORING                                                        ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │  ❌ "Format it nicely"                                              │    ║
║  │  ✅ "Format like this example: [provide concrete example]"          │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Iterative Refinement Process

```python
# Prompt testing framework
from dataclasses import dataclass
from typing import List, Dict
import json

@dataclass
class PromptTest:
    prompt: str
    expected_elements: List[str]
    test_inputs: List[str]

def evaluate_prompt(prompt: str, test_cases: List[Dict]) -> Dict:
    """Evaluate prompt performance across test cases."""
    results = {
        "accuracy": 0,
        "consistency": 0,
        "format_compliance": 0,
        "avg_tokens": 0
    }

    for test in test_cases:
        response = call_llm(prompt.format(**test["input"]))

        # Check expected elements
        for element in test["expected"]:
            if element.lower() in response.lower():
                results["accuracy"] += 1

        # Check format compliance
        if validate_format(response, test.get("format")):
            results["format_compliance"] += 1

    # Normalize scores
    total = len(test_cases)
    results["accuracy"] /= total
    results["format_compliance"] /= total

    return results

# Test different prompt versions
prompts_to_test = [
    "Analyze this system: {system_desc}",
    "As a security analyst, evaluate: {system_desc}",
    """You are a FedRAMP assessor. Analyze the system below for compliance gaps.
    System: {system_desc}
    Output format: | Control | Status | Finding |"""
]

for prompt in prompts_to_test:
    scores = evaluate_prompt(prompt, test_cases)
    print(f"Prompt: {prompt[:50]}...")
    print(f"Scores: {scores}\n")
```

---

## 🧪 Exercises

### Exercise 5.1: Role Design
Design a system prompt for a federal procurement assistant.

### Exercise 5.2: Few-Shot Library
Create a library of few-shot examples for common federal document types.

### Exercise 5.3: CoT Implementation
Apply Chain-of-Thought prompting to a complex compliance decision.

### Exercise 5.4: Prompt A/B Testing
Compare two prompt variants on accuracy and consistency metrics.

---

## 📝 Assessment

### Knowledge Check

1. What are the five components of effective prompt anatomy?
2. When should you use few-shot vs. zero-shot prompting?
3. How does Chain-of-Thought improve reasoning accuracy?
4. What elements should a federal system prompt include?
5. How do you measure prompt effectiveness?

---

## ➡️ Next Module

[Module 06: MCP Protocol](../06-mcp-protocol/README.md)

---

<div align="center">

[⬆ Back to Top](#module-05-prompt-engineering) · [📚 Return to Curriculum](../../README.md)

</div>
