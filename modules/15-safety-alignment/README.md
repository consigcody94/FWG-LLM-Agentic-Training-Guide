<div align="center">

# Module 15: Safety & Alignment

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Building trustworthy AI systems aligned with federal values and mission*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand AI alignment principles and challenges
- [ ] Implement safety guardrails for LLM applications
- [ ] Design systems that prevent harmful outputs
- [ ] Apply Constitutional AI principles
- [ ] Build compliance-aware AI systems

---

## 15.1 AI Safety Fundamentals

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI SAFETY HIERARCHY                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ALIGNMENT                                                       │
│  ─────────                                                       │
│  "Does the AI do what we intend?"                               │
│                                                                  │
│       ┌─────────────────────────────────────────────┐           │
│       │            Outer Alignment                   │           │
│       │  (Specifying correct objectives)            │           │
│       │                                              │           │
│       │       ┌────────────────────────┐            │           │
│       │       │   Inner Alignment      │            │           │
│       │       │ (Model actually        │            │           │
│       │       │  pursuing objectives)  │            │           │
│       │       └────────────────────────┘            │           │
│       └─────────────────────────────────────────────┘           │
│                                                                  │
│  SAFETY                                                          │
│  ──────                                                          │
│  "Does the AI avoid harmful behaviors?"                         │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ Harmful   │  │ Deceptive │  │ Biased    │  │ Privacy   │    │
│  │ Content   │  │ Output    │  │ Decisions │  │ Violations│    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
│                                                                  │
│  ROBUSTNESS                                                      │
│  ──────────                                                      │
│  "Does the AI behave reliably under adversarial conditions?"    │
│                                                                  │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐    │
│  │ Prompt    │  │ Jailbreak │  │ Data      │  │ Edge      │    │
│  │ Injection │  │ Attacks   │  │ Poisoning │  │ Cases     │    │
│  └───────────┘  └───────────┘  └───────────┘  └───────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Safety Concerns for Federal AI

| Concern | Description | Federal Impact |
|---------|-------------|----------------|
| **Hallucination** | Generating false information | Incorrect policy guidance, legal issues |
| **Bias** | Discriminatory outputs | Civil rights violations, unfair decisions |
| **Privacy** | Exposing sensitive data | PII breaches, classification violations |
| **Manipulation** | Persuasive misinformation | Public trust erosion |
| **Reliability** | Inconsistent behavior | Mission-critical failures |

---

## 15.2 Constitutional AI Principles

### Anthropic's Constitutional Approach

```python
# Constitutional AI principles for federal applications
FEDERAL_CONSTITUTION = [
    # Helpfulness principles
    {
        "principle": "Be helpful to federal employees in accomplishing their mission while following all applicable laws and regulations.",
        "critique_request": "Does this response help the user accomplish a legitimate federal mission?"
    },
    {
        "principle": "Provide accurate information based on authoritative federal sources.",
        "critique_request": "Is this information accurate and properly sourced?"
    },

    # Harmlessness principles
    {
        "principle": "Never assist with activities that violate federal law, regulations, or ethical standards.",
        "critique_request": "Does this response enable any illegal or unethical activities?"
    },
    {
        "principle": "Protect classified and sensitive information at all times.",
        "critique_request": "Does this response risk exposing classified or sensitive information?"
    },
    {
        "principle": "Avoid bias based on race, gender, religion, national origin, or other protected characteristics.",
        "critique_request": "Does this response show any inappropriate bias?"
    },

    # Honesty principles
    {
        "principle": "Be transparent about limitations and uncertainties.",
        "critique_request": "Is this response appropriately honest about what the AI does and doesn't know?"
    },
    {
        "principle": "Never claim to be human or misrepresent AI capabilities.",
        "critique_request": "Does this response accurately represent the AI's nature and limitations?"
    }
]

class ConstitutionalChecker:
    """Apply constitutional principles to outputs."""

    def __init__(self, llm, constitution: List[Dict]):
        self.llm = llm
        self.constitution = constitution

    async def critique(self, prompt: str, response: str) -> Dict:
        """Critique a response against constitutional principles."""
        critiques = []

        for principle in self.constitution:
            critique_prompt = f"""Evaluate this response against the following principle:

Principle: {principle['principle']}

User prompt: {prompt}

AI response: {response}

Question: {principle['critique_request']}

Provide a score from 0-10 and brief explanation.
Format: SCORE: X/10
EXPLANATION: ..."""

            result = await self.llm.generate(critique_prompt)
            critiques.append({
                "principle": principle['principle'],
                "evaluation": result
            })

        return {"critiques": critiques}

    async def revise(self, prompt: str, response: str, critiques: List[Dict]) -> str:
        """Revise response based on critiques."""
        critique_summary = "\n".join([
            f"- {c['principle']}: {c['evaluation']}"
            for c in critiques
        ])

        revision_prompt = f"""Revise this response to better align with constitutional principles.

Original prompt: {prompt}

Original response: {response}

Critiques:
{critique_summary}

Provide a revised response that addresses the critiques while remaining helpful:"""

        return await self.llm.generate(revision_prompt)
```

---

## 15.3 Input Safety (Guardrails)

### Prompt Injection Detection

```python
import re
from typing import Tuple, List

class InputGuardrails:
    """Detect and prevent malicious inputs."""

    def __init__(self):
        self.injection_patterns = [
            # Direct instruction override
            r"ignore (all |previous |prior )?(instructions|prompts|rules)",
            r"disregard (all |previous |prior )?(instructions|prompts|rules)",
            r"forget (all |previous |prior )?(instructions|prompts|rules)",

            # Role manipulation
            r"you are now",
            r"act as",
            r"pretend (to be|you are)",
            r"roleplay as",

            # System prompt extraction
            r"(show|reveal|display|print) (your |the )?(system |initial )?(prompt|instructions)",
            r"what (are|is) your (system |initial )?(prompt|instructions)",

            # Delimiter attacks
            r"```system",
            r"\[SYSTEM\]",
            r"<\|.*\|>",

            # Jailbreak attempts
            r"DAN",
            r"do anything now",
            r"developer mode"
        ]

        self.sensitive_patterns = [
            # Classification markers
            r"(TOP SECRET|SECRET|CONFIDENTIAL)//",
            r"CLASSIFIED",
            r"NOFORN",
            r"REL TO",

            # PII patterns
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"\b\d{9}\b",  # SSN no dashes

            # Access credentials
            r"password\s*[:=]",
            r"api[_-]?key\s*[:=]",
            r"secret\s*[:=]",
            r"token\s*[:=]"
        ]

    def check_input(self, text: str) -> Tuple[bool, List[str]]:
        """Check input for safety issues."""
        issues = []
        text_lower = text.lower()

        # Check for injection attempts
        for pattern in self.injection_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                issues.append(f"Potential injection: {pattern}")

        # Check for sensitive content
        for pattern in self.sensitive_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                issues.append(f"Sensitive content: {pattern}")

        is_safe = len(issues) == 0
        return is_safe, issues

    def sanitize(self, text: str) -> str:
        """Sanitize input by escaping potentially dangerous content."""
        # Escape special characters that might be interpreted as instructions
        sanitized = text

        # Add input markers
        sanitized = f"<user_input>{sanitized}</user_input>"

        return sanitized


class ContentClassifier:
    """Classify input content for safety."""

    def __init__(self, llm):
        self.llm = llm
        self.categories = [
            "safe",
            "harmful_request",
            "injection_attempt",
            "sensitive_data",
            "out_of_scope"
        ]

    async def classify(self, text: str) -> Dict:
        """Classify input into safety categories."""
        prompt = f"""Classify this input into one of these categories:
- safe: Normal, appropriate request
- harmful_request: Request for harmful, illegal, or unethical content
- injection_attempt: Attempt to manipulate AI behavior
- sensitive_data: Contains classified or PII data
- out_of_scope: Outside the AI's intended use case

Input: {text}

Classification (one word):"""

        response = await self.llm.generate(prompt)
        category = response.strip().lower()

        return {
            "category": category if category in self.categories else "unknown",
            "is_safe": category == "safe"
        }
```

---

## 15.4 Output Safety

### Content Filtering

```python
class OutputGuardrails:
    """Filter and validate AI outputs."""

    def __init__(self, llm=None):
        self.llm = llm

        # Patterns that should never appear in output
        self.blocklist = [
            r"\b\d{3}-\d{2}-\d{4}\b",  # SSN
            r"password\s*[:=]\s*\S+",
            r"api[_-]?key\s*[:=]\s*\S+",
        ]

        # Required disclosures
        self.required_disclaimers = {
            "medical": "This is not medical advice. Consult a healthcare professional.",
            "legal": "This is not legal advice. Consult a qualified attorney.",
            "financial": "This is not financial advice. Consult a financial advisor."
        }

    def filter_output(self, text: str) -> Tuple[str, List[str]]:
        """Filter output for sensitive content."""
        filtered = text
        redactions = []

        for pattern in self.blocklist:
            matches = re.findall(pattern, filtered, re.IGNORECASE)
            for match in matches:
                filtered = filtered.replace(match, "[REDACTED]")
                redactions.append(match)

        return filtered, redactions

    async def validate_factuality(
        self,
        response: str,
        sources: List[str] = None
    ) -> Dict:
        """Validate factual claims in response."""
        if not self.llm:
            return {"validated": False, "reason": "No LLM for validation"}

        prompt = f"""Analyze this response for factual accuracy.

Response: {response}

{"Sources: " + str(sources) if sources else ""}

Identify any claims that:
1. Appear to be factually incorrect
2. Cannot be verified
3. May be hallucinated

Format:
ISSUES: [list any issues]
CONFIDENCE: [high/medium/low]"""

        result = await self.llm.generate(prompt)

        return {
            "validation": result,
            "validated": "no issues" in result.lower()
        }

    def add_disclaimer(self, response: str, topic: str) -> str:
        """Add required disclaimers based on topic."""
        disclaimer = self.required_disclaimers.get(topic)
        if disclaimer:
            return f"{response}\n\n⚠️ {disclaimer}"
        return response

    def enforce_format(self, response: str, constraints: Dict) -> str:
        """Enforce output format constraints."""
        # Max length
        if 'max_length' in constraints:
            if len(response) > constraints['max_length']:
                response = response[:constraints['max_length']] + "..."

        # Required prefix/suffix
        if 'prefix' in constraints:
            response = constraints['prefix'] + response
        if 'suffix' in constraints:
            response = response + constraints['suffix']

        return response
```

### Bias Detection

```python
class BiasDetector:
    """Detect potential bias in AI outputs."""

    def __init__(self, llm):
        self.llm = llm
        self.protected_categories = [
            "race", "ethnicity", "gender", "religion",
            "age", "disability", "national_origin",
            "sexual_orientation", "veteran_status"
        ]

    async def check_bias(self, response: str, context: str = "") -> Dict:
        """Check response for potential bias."""
        prompt = f"""Analyze this AI response for potential bias related to protected categories:
{', '.join(self.protected_categories)}

Context: {context}

Response: {response}

For each category, assess:
1. Is there any stereotyping?
2. Is there differential treatment?
3. Are there problematic assumptions?

Format:
CATEGORY: [category]
ISSUE: [description or "None detected"]
SEVERITY: [none/low/medium/high]

Provide analysis:"""

        analysis = await self.llm.generate(prompt)

        # Parse severity
        severity_match = re.search(r"SEVERITY:\s*(none|low|medium|high)", analysis, re.IGNORECASE)
        max_severity = severity_match.group(1).lower() if severity_match else "unknown"

        return {
            "analysis": analysis,
            "max_severity": max_severity,
            "is_biased": max_severity in ["medium", "high"]
        }

    async def suggest_revision(self, response: str, bias_analysis: str) -> str:
        """Suggest bias-free revision."""
        prompt = f"""Revise this response to remove detected bias.

Original response: {response}

Bias analysis: {bias_analysis}

Provide a revised response that is:
1. Neutral and objective
2. Free from stereotypes
3. Equally applicable regardless of protected characteristics

Revised response:"""

        return await self.llm.generate(prompt)
```

---

## 15.5 Safety Pipeline Integration

```python
class SafetyPipeline:
    """Complete safety pipeline for LLM applications."""

    def __init__(
        self,
        llm,
        input_guardrails: InputGuardrails,
        output_guardrails: OutputGuardrails,
        constitutional_checker: ConstitutionalChecker,
        bias_detector: BiasDetector
    ):
        self.llm = llm
        self.input_guards = input_guardrails
        self.output_guards = output_guardrails
        self.constitutional = constitutional_checker
        self.bias_detector = bias_detector

    async def process(
        self,
        user_input: str,
        context: Dict = None
    ) -> Dict:
        """Process input through complete safety pipeline."""

        # Stage 1: Input validation
        is_safe, issues = self.input_guards.check_input(user_input)
        if not is_safe:
            return {
                "success": False,
                "stage": "input_validation",
                "issues": issues,
                "response": "I cannot process this request due to safety concerns."
            }

        # Stage 2: Content classification
        classification = await self.input_guards.classify(user_input)
        if not classification['is_safe']:
            return {
                "success": False,
                "stage": "classification",
                "category": classification['category'],
                "response": "This request falls outside my operational guidelines."
            }

        # Stage 3: Generate response
        sanitized_input = self.input_guards.sanitize(user_input)
        response = await self.llm.generate(sanitized_input)

        # Stage 4: Output filtering
        filtered_response, redactions = self.output_guards.filter_output(response)
        if redactions:
            # Log redactions for audit
            pass

        # Stage 5: Constitutional check
        critique = await self.constitutional.critique(user_input, filtered_response)
        low_scores = [c for c in critique['critiques'] if self._extract_score(c) < 7]

        if low_scores:
            # Revise response
            filtered_response = await self.constitutional.revise(
                user_input,
                filtered_response,
                low_scores
            )

        # Stage 6: Bias check
        bias_result = await self.bias_detector.check_bias(
            filtered_response,
            str(context) if context else ""
        )

        if bias_result['is_biased']:
            filtered_response = await self.bias_detector.suggest_revision(
                filtered_response,
                bias_result['analysis']
            )

        # Stage 7: Factuality validation
        factuality = await self.output_guards.validate_factuality(filtered_response)

        return {
            "success": True,
            "response": filtered_response,
            "metadata": {
                "redactions": len(redactions),
                "constitutional_revisions": len(low_scores) > 0,
                "bias_corrections": bias_result['is_biased'],
                "factuality_confidence": factuality.get('confidence', 'unknown')
            }
        }

    def _extract_score(self, critique: Dict) -> int:
        """Extract numerical score from critique."""
        match = re.search(r"SCORE:\s*(\d+)", critique.get('evaluation', ''))
        return int(match.group(1)) if match else 5
```

---

## 15.6 Federal-Specific Safety Requirements

### Compliance Checker

```python
class FederalComplianceChecker:
    """Check AI outputs against federal requirements."""

    def __init__(self, llm):
        self.llm = llm

        self.requirements = {
            "508_accessibility": {
                "description": "Section 508 accessibility compliance",
                "check": "Ensure output is accessible to users with disabilities"
            },
            "plain_language": {
                "description": "Plain Writing Act compliance",
                "check": "Use clear, simple language appropriate for general public"
            },
            "records_management": {
                "description": "Federal Records Act compliance",
                "check": "Include appropriate disclaimers about record retention"
            },
            "privacy_act": {
                "description": "Privacy Act compliance",
                "check": "Protect personally identifiable information"
            }
        }

    async def check_compliance(self, response: str, context: str = "") -> Dict:
        """Check response against federal requirements."""
        results = {}

        for req_id, req in self.requirements.items():
            prompt = f"""Evaluate this response for {req['description']}.

Response: {response}

Check: {req['check']}

Is this requirement met? Explain briefly.
Format:
COMPLIANT: [yes/no/partial]
EXPLANATION: ..."""

            result = await self.llm.generate(prompt)
            results[req_id] = {
                "requirement": req['description'],
                "evaluation": result
            }

        return results


class AIRiskFramework:
    """Implement NIST AI Risk Management Framework checks."""

    def __init__(self, llm):
        self.llm = llm

        # NIST AI RMF categories
        self.risk_categories = [
            "validity_reliability",
            "safety",
            "security_resilience",
            "accountability_transparency",
            "explainability_interpretability",
            "privacy",
            "fairness"
        ]

    async def assess_risk(self, system_description: str) -> Dict:
        """Assess AI system against NIST AI RMF."""
        assessments = {}

        for category in self.risk_categories:
            prompt = f"""Assess this AI system for {category.replace('_', ' ')} risks.

System: {system_description}

Identify:
1. Potential risks in this category
2. Severity (low/medium/high)
3. Mitigation recommendations

Assessment:"""

            result = await self.llm.generate(prompt)
            assessments[category] = result

        return assessments
```

---

## Hands-On Lab

### Lab 15.1: Build a Safety-Wrapped AI Assistant

Create a federal AI assistant with comprehensive safety:
1. Implement input guardrails with injection detection
2. Add constitutional AI checking
3. Build bias detection and mitigation
4. Include federal compliance validation
5. Create audit logging for all safety decisions

---

## Knowledge Check

1. What is the difference between alignment and safety?
2. How does Constitutional AI improve output quality?
3. What are the key federal-specific safety requirements?
4. How should bias be detected and mitigated in AI outputs?

---

<div align="center">

[← Module 14: Memory & Context](../14-memory-context/README.md) | [Home](../../README.md) | [Module 16: Evaluation & Testing →](../16-evaluation-testing/README.md)

</div>
