<div align="center">

# Prompt Engineering Cheatsheet

<img src="https://img.shields.io/badge/Quick_Reference-Prompt_Patterns-blue?style=for-the-badge" alt="Prompt Patterns"/>

</div>

---

## Core Prompting Patterns

### 1. Role Assignment

```
You are a [ROLE] specializing in [DOMAIN].
Your responsibilities include [RESPONSIBILITIES].
You should [BEHAVIORAL GUIDELINES].
```

**Example:**
```
You are a Federal Compliance Officer specializing in FedRAMP authorization.
Your responsibilities include reviewing security documentation and identifying gaps.
You should be precise, cite specific controls, and avoid speculation.
```

---

### 2. Chain-of-Thought (CoT)

```
[TASK]

Think through this step-by-step:
1. First, identify [INITIAL ANALYSIS]
2. Then, consider [SECONDARY FACTORS]
3. Finally, determine [CONCLUSION]

Show your reasoning at each step.
```

**Example:**
```
Evaluate whether this system meets NIST 800-53 AC-2 requirements.

Think through this step-by-step:
1. First, identify what AC-2 requires for account management
2. Then, consider how the described system implements these requirements
3. Finally, determine any gaps between requirements and implementation

Show your reasoning at each step.
```

---

### 3. Few-Shot Learning

```
Here are examples of [TASK]:

Example 1:
Input: [INPUT_1]
Output: [OUTPUT_1]

Example 2:
Input: [INPUT_2]
Output: [OUTPUT_2]

Now perform the same task for:
Input: [NEW_INPUT]
Output:
```

**Example:**
```
Here are examples of control implementation statements:

Example 1:
Control: AC-2(a)
Output: "The organization identifies and selects account types (privileged,
non-privileged, system, service) based on organizational mission requirements."

Example 2:
Control: AC-2(b)
Output: "Account managers are designated by the ISSO and approved by the
Authorizing Official for each information system."

Now write an implementation statement for:
Control: AC-2(c)
Output:
```

---

### 4. Structured Output

```
Analyze [INPUT] and provide your response in the following format:

## Summary
[Brief overview]

## Findings
- Finding 1: [Description]
- Finding 2: [Description]

## Recommendations
1. [Recommendation with priority]
2. [Recommendation with priority]

## Risk Rating
[Low/Medium/High] - [Justification]
```

---

### 5. Constraint Specification

```
[TASK]

Constraints:
- Output must be [LENGTH CONSTRAINT]
- Only include [SCOPE CONSTRAINT]
- Do not [EXCLUSION CONSTRAINT]
- Format as [FORMAT CONSTRAINT]
```

**Example:**
```
Summarize this security assessment report.

Constraints:
- Output must be under 500 words
- Only include critical and high findings
- Do not include remediation details (separate document)
- Format as executive briefing bullets
```

---

## Federal-Specific Patterns

### Compliance Assessment Pattern

```
Review the following [SYSTEM/DOCUMENT] against [FRAMEWORK] requirements.

For each applicable control:
1. Identify the control requirement
2. Assess the current implementation status
3. Note any gaps or deficiencies
4. Recommend remediation if needed

Framework: [NIST 800-53 / FedRAMP / FISMA]
Baseline: [Low / Moderate / High]
System Type: [Cloud / On-Premise / Hybrid]

[CONTENT TO ANALYZE]
```

### Policy Analysis Pattern

```
Analyze the following federal policy document:

Document: [POLICY NAME/NUMBER]
Context: [AGENCY/REGULATION CONTEXT]

Provide:
1. Key requirements summary
2. Affected stakeholders
3. Compliance timeline
4. Implementation considerations
5. Potential challenges

[POLICY TEXT]
```

### Documentation Generation Pattern

```
Generate a [DOCUMENT TYPE] for the following:

System Name: [NAME]
Impact Level: [FIPS 199 LEVEL]
Control: [CONTROL ID]

Required Sections:
- Control Description
- Implementation Status: [Implemented / Partially / Planned / N/A]
- Implementation Details
- Responsible Entities
- Assessment Procedures

Implementation Context:
[DESCRIPTION OF HOW CONTROL IS IMPLEMENTED]
```

---

## Output Format Templates

### JSON Output

```
Respond with valid JSON in this exact structure:
{
  "analysis": {
    "summary": "string",
    "findings": [
      {
        "id": "string",
        "severity": "critical|high|medium|low",
        "description": "string",
        "recommendation": "string"
      }
    ],
    "overall_risk": "high|medium|low",
    "confidence": 0.0-1.0
  }
}
```

### Markdown Table Output

```
Format your response as a markdown table with these columns:
| Control ID | Status | Finding | Recommendation |
```

### OSCAL-Compatible Output

```
Generate output compatible with OSCAL format:
- Use proper OSCAL terminology
- Include control-id references
- Format dates as ISO 8601
- Include responsible-parties where applicable
```

---

## Prompt Engineering Best Practices

### DO:
- Be specific about desired output format
- Provide context about the federal domain
- Include relevant examples
- Specify constraints clearly
- Request step-by-step reasoning for complex tasks

### DON'T:
- Use vague instructions like "be thorough"
- Assume the model knows agency-specific terms
- Request sensitive/classified information
- Skip input validation requirements
- Expect perfect compliance mapping without review

---

## Quick Reference Table

| Pattern | Use When | Key Elements |
|:--------|:---------|:-------------|
| **Role Assignment** | Need domain expertise | Role, domain, guidelines |
| **Chain-of-Thought** | Complex reasoning | Step-by-step instructions |
| **Few-Shot** | Specific format needed | 2-3 examples |
| **Structured Output** | Consistent format | Template structure |
| **Constraints** | Precise requirements | Explicit limitations |

---

## Token Optimization Tips

1. **Be concise** - Remove filler words
2. **Use abbreviations** - After first use, abbreviate (e.g., "NIST" after "National Institute of Standards and Technology")
3. **Reference don't repeat** - "Per the above" instead of restating
4. **Batch similar tasks** - Group related questions
5. **Prune examples** - Use minimum effective examples

---

<div align="center">

[📚 Return to Curriculum](../README.md)

</div>
