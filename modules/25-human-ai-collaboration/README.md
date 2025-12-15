# Module 25: Human-AI Collaboration

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗  ██╗██╗   ██╗███╗   ███╗ █████╗ ███╗   ██╗     █████╗ ██╗             ║
║   ██║  ██║██║   ██║████╗ ████║██╔══██╗████╗  ██║    ██╔══██╗██║             ║
║   ███████║██║   ██║██╔████╔██║███████║██╔██╗ ██║    ███████║██║             ║
║   ██╔══██║██║   ██║██║╚██╔╝██║██╔══██║██║╚██╗██║    ██╔══██║██║             ║
║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║██║  ██║██║ ╚████║    ██║  ██║██║             ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝    ╚═╝  ╚═╝╚═╝             ║
║                                                                              ║
║           Effective Partnerships • Trust • Augmented Intelligence            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Learning Objectives

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  By the end of this module, you will be able to:                           │
│                                                                             │
│  □ Design effective human-AI collaboration patterns                        │
│  □ Build trust through transparency and explainability                     │
│  □ Implement feedback loops for continuous improvement                     │
│  □ Balance automation with human judgment                                   │
│  □ Create AI assistants that augment rather than replace                   │
│  □ Handle disagreements between human and AI recommendations               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 25.1 Collaboration Paradigms

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    HUMAN-AI COLLABORATION SPECTRUM                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  HUMAN CONTROL ◄──────────────────────────────────────────► AI AUTONOMY    │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐       │
│  │   HUMAN     │  │   HUMAN     │  │    AI       │  │    AI       │       │
│  │   DOES      │  │   DECIDES   │  │  DECIDES    │  │   DOES      │       │
│  │             │  │             │  │             │  │             │       │
│  │   AI        │  │    AI       │  │   HUMAN     │  │   HUMAN     │       │
│  │  ASSISTS    │  │  RECOMMENDS │  │  APPROVES   │  │  MONITORS   │       │
│  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘       │
│                                                                             │
│  Example:         Example:         Example:         Example:               │
│  AI drafts        AI suggests      AI auto-         AI handles            │
│  text, human      responses,       approves low     routine tasks,        │
│  writes final     human picks      risk items,      human handles         │
│                                    human reviews    exceptions            │
│                                    high risk                              │
│                                                                             │
│  ─────────────────────────────────────────────────────────────────────────│
│  FEDERAL PRINCIPLE: Maintain human accountability at all levels           │
│  ─────────────────────────────────────────────────────────────────────────│
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Collaboration Pattern Selection

| Scenario | Pattern | Rationale |
|----------|---------|-----------|
| **Policy decisions** | Human decides, AI assists | Requires human judgment |
| **Document drafting** | AI drafts, human reviews | Efficiency with oversight |
| **Data analysis** | AI analyzes, human interprets | Scale with context |
| **Routine processing** | AI executes, human monitors | Efficiency for low-risk |
| **Security decisions** | Human decides, AI recommends | Accountability requirement |
| **Customer service** | AI handles, escalates when needed | Hybrid approach |

---

## 25.2 Building Trust Through Explainability

```python
"""
Explainable AI System
Build trust by showing reasoning
"""
from dataclasses import dataclass
from typing import Optional
from openai import OpenAI


@dataclass
class ExplainedDecision:
    """
    Decision with full explanation for human review
    """
    decision: str
    confidence: float
    reasoning: str
    evidence: list[str]
    alternatives_considered: list[dict]
    uncertainty_factors: list[str]
    recommended_action: str


class ExplainableAI:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                      EXPLAINABLE AI SYSTEM                              │
    │                                                                         │
    │  PRINCIPLE: Every AI recommendation must be understandable              │
    │                                                                         │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │                    EXPLANATION LAYERS                           │   │
    │  │                                                                 │   │
    │  │   1. WHAT: The decision/recommendation                         │   │
    │  │   2. WHY: Reasoning and evidence                               │   │
    │  │   3. HOW CONFIDENT: Uncertainty quantification                 │   │
    │  │   4. ALTERNATIVES: What else was considered                    │   │
    │  │   5. LIMITATIONS: What the AI doesn't know                     │   │
    │  │                                                                 │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def analyze_with_explanation(
        self,
        task: str,
        context: dict,
        options: list[str] = None
    ) -> ExplainedDecision:
        """
        Analyze and provide fully explainable recommendation
        """
        prompt = f"""Analyze this task and provide a recommendation with FULL explanation.

TASK: {task}

CONTEXT:
{json.dumps(context, indent=2)}

{f"OPTIONS TO CONSIDER: {options}" if options else ""}

Provide your analysis as JSON:
{{
    "decision": "your recommendation",
    "confidence": 0.0-1.0,
    "reasoning": "step-by-step explanation of how you reached this conclusion",
    "evidence": ["specific facts/data points that support this decision"],
    "alternatives_considered": [
        {{"option": "alternative 1", "pros": [...], "cons": [...], "why_not_chosen": "..."}}
    ],
    "uncertainty_factors": ["things that could change this recommendation"],
    "recommended_action": "what the human should do next"
}}

Be thorough and honest about limitations."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that provides fully explainable recommendations. Always show your reasoning."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return ExplainedDecision(
            decision=result["decision"],
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            evidence=result.get("evidence", []),
            alternatives_considered=result.get("alternatives_considered", []),
            uncertainty_factors=result.get("uncertainty_factors", []),
            recommended_action=result.get("recommended_action", "")
        )

    def explain_existing_decision(
        self,
        decision: str,
        context: dict
    ) -> str:
        """
        Generate plain-language explanation of a decision

        Use case: Explaining AI decisions to stakeholders
        """
        prompt = f"""Explain this decision in plain language that a non-technical person can understand.

DECISION: {decision}

CONTEXT:
{json.dumps(context, indent=2)}

Write a clear explanation that:
1. States what the decision is
2. Explains WHY this decision was made
3. Describes what data/factors influenced it
4. Notes any limitations or caveats
5. Suggests what questions the reader might want to ask

Keep it under 200 words. Use simple language."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def generate_decision_report(
        self,
        explained_decision: ExplainedDecision
    ) -> str:
        """
        Generate formatted report for human review
        """
        report = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                           AI DECISION REPORT                                ║
╚══════════════════════════════════════════════════════════════════════════════╝

RECOMMENDATION: {explained_decision.decision}
CONFIDENCE: {explained_decision.confidence * 100:.1f}%

────────────────────────────────────────────────────────────────────────────────
REASONING
────────────────────────────────────────────────────────────────────────────────
{explained_decision.reasoning}

────────────────────────────────────────────────────────────────────────────────
SUPPORTING EVIDENCE
────────────────────────────────────────────────────────────────────────────────
"""
        for i, evidence in enumerate(explained_decision.evidence, 1):
            report += f"  {i}. {evidence}\n"

        report += """
────────────────────────────────────────────────────────────────────────────────
ALTERNATIVES CONSIDERED
────────────────────────────────────────────────────────────────────────────────
"""
        for alt in explained_decision.alternatives_considered:
            report += f"""
  Option: {alt.get('option', 'N/A')}
  Pros: {', '.join(alt.get('pros', []))}
  Cons: {', '.join(alt.get('cons', []))}
  Why not chosen: {alt.get('why_not_chosen', 'N/A')}
"""

        report += """
────────────────────────────────────────────────────────────────────────────────
UNCERTAINTY FACTORS
────────────────────────────────────────────────────────────────────────────────
"""
        for factor in explained_decision.uncertainty_factors:
            report += f"  ⚠ {factor}\n"

        report += f"""
────────────────────────────────────────────────────────────────────────────────
RECOMMENDED ACTION
────────────────────────────────────────────────────────────────────────────────
{explained_decision.recommended_action}

════════════════════════════════════════════════════════════════════════════════
HUMAN REVIEWER: Please verify this recommendation before taking action.
════════════════════════════════════════════════════════════════════════════════
"""
        return report


# Usage
explainable = ExplainableAI(api_key="your-key")

decision = explainable.analyze_with_explanation(
    task="Should we approve this vendor for the software contract?",
    context={
        "vendor": "TechCorp Inc",
        "contract_value": 150000,
        "security_clearance": "Yes",
        "past_performance": "3 contracts, all satisfactory",
        "price_comparison": "10% above average"
    },
    options=["Approve", "Reject", "Request more information"]
)

print(explainable.generate_decision_report(decision))
```

---

## 25.3 Effective Feedback Loops

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        FEEDBACK LOOP ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌──────────────────────────────────────────────────────────────────────┐ │
│   │                                                                      │ │
│   │      ┌──────────┐         ┌──────────┐         ┌──────────┐        │ │
│   │      │    AI    │────────▶│  HUMAN   │────────▶│ OUTCOME  │        │ │
│   │      │ SUGGESTS │         │ DECIDES  │         │ OBSERVED │        │ │
│   │      └──────────┘         └──────────┘         └──────────┘        │ │
│   │           ▲                                          │              │ │
│   │           │                                          │              │ │
│   │           │         ┌──────────────────┐            │              │ │
│   │           └─────────│    FEEDBACK      │◀───────────┘              │ │
│   │                     │   COLLECTION     │                           │ │
│   │                     └──────────────────┘                           │ │
│   │                                                                      │ │
│   └──────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│   FEEDBACK TYPES:                                                           │
│   • Explicit: Human corrects/approves AI suggestion                        │
│   • Implicit: Human modifies AI output (editing)                           │
│   • Outcome: Result tracking (did it work?)                                │
│   • Comparative: A/B testing of approaches                                 │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

```python
"""
Feedback Collection and Learning System
Continuously improve AI through human input
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Literal
from enum import Enum
import json


class FeedbackType(Enum):
    APPROVED = "approved"          # Human accepted AI suggestion
    MODIFIED = "modified"          # Human edited AI output
    REJECTED = "rejected"          # Human rejected AI suggestion
    OUTCOME_POSITIVE = "outcome_positive"  # Decision worked out
    OUTCOME_NEGATIVE = "outcome_negative"  # Decision didn't work


@dataclass
class FeedbackRecord:
    id: str
    timestamp: datetime
    ai_suggestion: str
    human_action: str
    feedback_type: FeedbackType
    context: dict
    human_reasoning: Optional[str] = None
    outcome_observed: Optional[str] = None


class FeedbackSystem:
    """
    Collect and analyze human feedback on AI recommendations
    """

    def __init__(self):
        self.feedback_records: list[FeedbackRecord] = []

    def record_feedback(
        self,
        ai_suggestion: str,
        human_action: str,
        feedback_type: FeedbackType,
        context: dict,
        human_reasoning: str = None
    ) -> FeedbackRecord:
        """Record human feedback on AI suggestion"""

        import uuid

        record = FeedbackRecord(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            ai_suggestion=ai_suggestion,
            human_action=human_action,
            feedback_type=feedback_type,
            context=context,
            human_reasoning=human_reasoning
        )

        self.feedback_records.append(record)
        return record

    def calculate_agreement_rate(
        self,
        time_window_days: int = 30
    ) -> dict:
        """Calculate how often humans agree with AI"""

        cutoff = datetime.now() - timedelta(days=time_window_days)
        recent = [r for r in self.feedback_records if r.timestamp > cutoff]

        if not recent:
            return {"error": "No recent feedback"}

        approved = sum(1 for r in recent if r.feedback_type == FeedbackType.APPROVED)
        modified = sum(1 for r in recent if r.feedback_type == FeedbackType.MODIFIED)
        rejected = sum(1 for r in recent if r.feedback_type == FeedbackType.REJECTED)
        total = len(recent)

        return {
            "total_interactions": total,
            "approved_rate": approved / total,
            "modified_rate": modified / total,
            "rejected_rate": rejected / total,
            "agreement_rate": (approved + modified * 0.5) / total,  # Partial credit for modifications
            "time_window_days": time_window_days
        }

    def analyze_rejection_patterns(self) -> list[dict]:
        """Find patterns in rejected suggestions"""

        rejections = [r for r in self.feedback_records
                     if r.feedback_type == FeedbackType.REJECTED]

        # Group by context patterns
        patterns = {}
        for r in rejections:
            # Extract key context elements
            key_elements = frozenset(r.context.keys())
            if key_elements not in patterns:
                patterns[key_elements] = []
            patterns[key_elements].append(r)

        return [
            {
                "context_type": list(key),
                "rejection_count": len(records),
                "common_reasons": self._extract_common_reasons(records)
            }
            for key, records in patterns.items()
        ]

    def _extract_common_reasons(
        self,
        records: list[FeedbackRecord]
    ) -> list[str]:
        """Extract common rejection reasons"""
        reasons = [r.human_reasoning for r in records if r.human_reasoning]
        # In production: use NLP to cluster similar reasons
        return reasons[:5]  # Top 5 for now

    def generate_improvement_suggestions(
        self,
        api_key: str
    ) -> str:
        """Use AI to analyze feedback and suggest improvements"""

        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        stats = self.calculate_agreement_rate()
        rejection_patterns = self.analyze_rejection_patterns()

        prompt = f"""Analyze this AI system feedback and suggest improvements:

AGREEMENT STATISTICS:
{json.dumps(stats, indent=2)}

REJECTION PATTERNS:
{json.dumps(rejection_patterns, indent=2)}

SAMPLE REJECTIONS (with human reasoning):
{json.dumps([{
    "ai_suggestion": r.ai_suggestion,
    "human_action": r.human_action,
    "reason": r.human_reasoning
} for r in self.feedback_records[:10] if r.feedback_type == FeedbackType.REJECTED], indent=2)}

Suggest:
1. What patterns cause AI suggestions to be rejected?
2. How could the AI better handle these cases?
3. Are there categories where the AI should defer to humans?
4. What additional context would help the AI make better suggestions?"""

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content


class InteractiveFeedback:
    """
    Real-time feedback collection during human-AI interaction
    """

    def __init__(self, feedback_system: FeedbackSystem):
        self.feedback_system = feedback_system

    def present_suggestion_with_feedback(
        self,
        suggestion: str,
        context: dict
    ) -> dict:
        """
        Present AI suggestion and collect structured feedback

        Returns feedback structure for logging
        """
        return {
            "suggestion": suggestion,
            "context": context,
            "feedback_options": [
                {"action": "accept", "label": "✓ Accept as-is"},
                {"action": "modify", "label": "✎ Accept with changes"},
                {"action": "reject", "label": "✗ Reject"},
                {"action": "defer", "label": "⏸ Decide later"}
            ],
            "feedback_prompts": {
                "modify": "What changes did you make and why?",
                "reject": "Why did you reject this suggestion?",
                "accept": "Any notes for future reference?"
            }
        }

    def collect_feedback(
        self,
        suggestion: str,
        action: str,
        human_result: str,
        context: dict,
        reasoning: str = None
    ) -> FeedbackRecord:
        """Collect and record feedback"""

        feedback_map = {
            "accept": FeedbackType.APPROVED,
            "modify": FeedbackType.MODIFIED,
            "reject": FeedbackType.REJECTED
        }

        return self.feedback_system.record_feedback(
            ai_suggestion=suggestion,
            human_action=human_result,
            feedback_type=feedback_map.get(action, FeedbackType.MODIFIED),
            context=context,
            human_reasoning=reasoning
        )


# Usage example
from datetime import timedelta

feedback_system = FeedbackSystem()
interactive = InteractiveFeedback(feedback_system)

# Simulate collecting feedback over time
feedback_system.record_feedback(
    ai_suggestion="Approve the request",
    human_action="Approved",
    feedback_type=FeedbackType.APPROVED,
    context={"type": "leave_request", "days": 2},
    human_reasoning=None
)

feedback_system.record_feedback(
    ai_suggestion="Reject the expense claim",
    human_action="Approved with conditions",
    feedback_type=FeedbackType.MODIFIED,
    context={"type": "expense", "amount": 500},
    human_reasoning="Valid business purpose confirmed verbally"
)

# Analyze patterns
stats = feedback_system.calculate_agreement_rate()
print(f"Agreement rate: {stats['agreement_rate']:.1%}")
```

---

## 25.4 Collaboration Interface Design

```python
"""
AI Assistant Interface Patterns
Effective UX for human-AI collaboration
"""
from dataclasses import dataclass
from typing import Literal


@dataclass
class AssistantMessage:
    """
    Structured message from AI assistant
    """
    content: str
    confidence: float
    message_type: Literal["suggestion", "question", "information", "warning"]
    sources: list[str] = None
    actions: list[dict] = None
    requires_response: bool = False


class CollaborativeAssistant:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                 COLLABORATIVE ASSISTANT PATTERNS                        │
    │                                                                         │
    │  ┌─────────────────────────────────────────────────────────────────┐   │
    │  │                    INTERACTION MODES                            │   │
    │  │                                                                 │   │
    │  │   PROACTIVE              REACTIVE              ON-DEMAND       │   │
    │  │   ┌─────────┐           ┌─────────┐           ┌─────────┐     │   │
    │  │   │  AI     │           │  Human  │           │  Human  │     │   │
    │  │   │ notices │           │  asks,  │           │ invokes │     │   │
    │  │   │ & alerts│           │ AI helps│           │   AI    │     │   │
    │  │   └─────────┘           └─────────┘           └─────────┘     │   │
    │  │                                                                 │   │
    │  │   "I noticed an         "How should I        "Analyze this    │   │
    │  │    error here..."       handle this?"         document"       │   │
    │  │                                                                 │   │
    │  └─────────────────────────────────────────────────────────────────┘   │
    │                                                                         │
    │  KEY PRINCIPLES:                                                        │
    │  • Never interrupt critical tasks                                      │
    │  • Always allow dismissal                                              │
    │  • Show confidence clearly                                             │
    │  • Explain reasoning on demand                                         │
    │  • Remember user preferences                                           │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.user_preferences = {}
        self.interaction_history = []

    def proactive_suggestion(
        self,
        observation: str,
        context: dict,
        urgency: Literal["low", "medium", "high"] = "medium"
    ) -> AssistantMessage:
        """
        Generate proactive suggestion based on observation

        Called when AI notices something user might want to know
        """
        prompt = f"""You noticed something that might help the user.

OBSERVATION: {observation}
CONTEXT: {json.dumps(context)}
URGENCY: {urgency}

Generate a helpful, non-intrusive message that:
1. Briefly states what you noticed
2. Offers to help if wanted
3. Can be easily dismissed
4. Shows appropriate confidence level

Keep it concise (1-2 sentences).
Don't be presumptuous - you're offering help, not directing."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=150
        )

        return AssistantMessage(
            content=response.choices[0].message.content,
            confidence=0.8,
            message_type="suggestion",
            requires_response=False,
            actions=[
                {"label": "Tell me more", "action": "expand"},
                {"label": "Not now", "action": "dismiss"},
                {"label": "Don't show this again", "action": "disable"}
            ]
        )

    def answer_question(
        self,
        question: str,
        context: dict
    ) -> AssistantMessage:
        """
        Respond to direct user question
        """
        prompt = f"""Answer this question helpfully and accurately.

QUESTION: {question}
CONTEXT: {json.dumps(context)}

Provide:
1. Direct answer to the question
2. Your confidence level (as percentage)
3. Any caveats or limitations
4. Sources if applicable

Be honest about uncertainty. If you don't know, say so."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Be accurate and honest about your limitations."
                },
                {"role": "user", "content": prompt}
            ]
        )

        return AssistantMessage(
            content=response.choices[0].message.content,
            confidence=0.85,  # Would be extracted from response in production
            message_type="information",
            requires_response=False,
            actions=[
                {"label": "Ask follow-up", "action": "continue"},
                {"label": "Thanks!", "action": "complete"}
            ]
        )

    def request_clarification(
        self,
        unclear_point: str,
        options: list[str] = None
    ) -> AssistantMessage:
        """
        Ask user for clarification when needed
        """
        content = f"I need a bit more information: {unclear_point}"

        if options:
            content += "\n\nDid you mean:\n"
            for i, opt in enumerate(options, 1):
                content += f"  {i}. {opt}\n"

        return AssistantMessage(
            content=content,
            confidence=0.5,
            message_type="question",
            requires_response=True,
            actions=[
                {"label": opt, "action": f"select_{i}"}
                for i, opt in enumerate(options or [], 1)
            ] + [{"label": "Something else", "action": "custom"}]
        )

    def warn_about_risk(
        self,
        risk_description: str,
        severity: Literal["info", "warning", "critical"]
    ) -> AssistantMessage:
        """
        Alert user to potential issues
        """
        prefixes = {
            "info": "💡 Note:",
            "warning": "⚠️ Warning:",
            "critical": "🚨 Critical:"
        }

        return AssistantMessage(
            content=f"{prefixes[severity]} {risk_description}",
            confidence=0.9,
            message_type="warning",
            requires_response=severity == "critical",
            actions=[
                {"label": "Understood", "action": "acknowledge"},
                {"label": "Tell me more", "action": "expand"},
                {"label": "Proceed anyway", "action": "override"}
            ] if severity != "critical" else [
                {"label": "Stop and review", "action": "stop"},
                {"label": "I understand the risk, proceed", "action": "override_confirm"}
            ]
        )


def format_assistant_response(message: AssistantMessage) -> str:
    """Format assistant message for display"""

    confidence_bar = "█" * int(message.confidence * 10) + "░" * (10 - int(message.confidence * 10))

    output = f"""
┌─────────────────────────────────────────────────────────────┐
│ AI ASSISTANT                                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ {message.content[:55]}
│ {message.content[55:110] if len(message.content) > 55 else ''}
│                                                             │
│ Confidence: [{confidence_bar}] {message.confidence*100:.0f}%
│                                                             │
"""

    if message.actions:
        output += "│ Actions:                                                │\n"
        for action in message.actions:
            output += f"│   [{action['label']}]                                    \n"

    output += "└─────────────────────────────────────────────────────────┘"

    return output
```

---

## 25.5 Handling Disagreements

```python
"""
Human-AI Disagreement Resolution
When human and AI recommendations conflict
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class DisagreementResolution(Enum):
    HUMAN_OVERRIDES = "human_overrides"
    AI_DEFERS = "ai_defers"
    ESCALATE = "escalate"
    REQUEST_MORE_INFO = "request_more_info"
    CONSENSUS_REACHED = "consensus_reached"


@dataclass
class DisagreementRecord:
    ai_recommendation: str
    ai_confidence: float
    ai_reasoning: str
    human_position: str
    human_reasoning: str
    resolution: DisagreementResolution
    final_decision: str
    outcome: Optional[str] = None


class DisagreementHandler:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                  DISAGREEMENT RESOLUTION FRAMEWORK                      │
    │                                                                         │
    │  WHEN HUMAN AND AI DISAGREE:                                           │
    │                                                                         │
    │  1. DOCUMENT THE DISAGREEMENT                                          │
    │     • Record both positions with reasoning                             │
    │     • Note confidence levels                                           │
    │                                                                         │
    │  2. EVALUATE THE SITUATION                                             │
    │     ┌──────────────────────────────────────────────────────────────┐   │
    │     │  AI Confidence High    │  AI Confidence Low                 │   │
    │     ├────────────────────────┼────────────────────────────────────┤   │
    │     │  Human Very Confident: │  Human Very Confident:             │   │
    │     │  → Escalate or discuss │  → Human decides                   │   │
    │     │                        │                                    │   │
    │     │  Human Uncertain:      │  Human Uncertain:                  │   │
    │     │  → Gather more info    │  → Escalate for guidance           │   │
    │     └────────────────────────┴────────────────────────────────────┘   │
    │                                                                         │
    │  3. RESOLVE AND RECORD                                                 │
    │     • Document final decision                                          │
    │     • Track outcome for learning                                       │
    │                                                                         │
    │  PRINCIPLE: Human always has final say, but disagreements are          │
    │  opportunities for learning and system improvement                     │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.disagreement_log: list[DisagreementRecord] = []

    def analyze_disagreement(
        self,
        ai_recommendation: str,
        ai_confidence: float,
        ai_reasoning: str,
        human_position: str,
        human_reasoning: str
    ) -> dict:
        """
        Analyze a disagreement and suggest resolution path
        """
        prompt = f"""Analyze this human-AI disagreement:

AI RECOMMENDATION: {ai_recommendation}
AI CONFIDENCE: {ai_confidence * 100:.0f}%
AI REASONING: {ai_reasoning}

HUMAN POSITION: {human_position}
HUMAN REASONING: {human_reasoning}

Analyze:
1. What's the core point of disagreement?
2. What information might resolve it?
3. What are the risks of each position?
4. Is there a middle ground?
5. Who has better information for this decision?

IMPORTANT: The human always has final authority.
Your role is to help understand the disagreement, not to argue.

Return as JSON:
{{
    "core_disagreement": "what they disagree about",
    "missing_information": ["what might help"],
    "ai_position_risks": ["risks if AI is followed"],
    "human_position_risks": ["risks if human is followed"],
    "possible_middle_ground": "compromise if any",
    "recommended_resolution": "escalate|human_decides|gather_more_info|discuss_further",
    "key_question": "one question that might resolve this"
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def facilitate_discussion(
        self,
        disagreement: dict,
        ai_position: str,
        human_concerns: list[str]
    ) -> str:
        """
        Generate AI response that acknowledges human concerns
        """
        prompt = f"""The human has concerns about your recommendation.

YOUR RECOMMENDATION: {ai_position}

HUMAN CONCERNS:
{chr(10).join(f'- {c}' for c in human_concerns)}

Write a response that:
1. Acknowledges their concerns are valid
2. Explains your reasoning without being defensive
3. Asks clarifying questions if helpful
4. Offers to adjust your recommendation if new information warrants it
5. Ultimately defers to their judgment

Be collaborative, not adversarial. You're on the same team."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    def record_resolution(
        self,
        ai_recommendation: str,
        ai_confidence: float,
        ai_reasoning: str,
        human_position: str,
        human_reasoning: str,
        resolution: DisagreementResolution,
        final_decision: str
    ) -> DisagreementRecord:
        """Record how disagreement was resolved"""

        record = DisagreementRecord(
            ai_recommendation=ai_recommendation,
            ai_confidence=ai_confidence,
            ai_reasoning=ai_reasoning,
            human_position=human_position,
            human_reasoning=human_reasoning,
            resolution=resolution,
            final_decision=final_decision
        )

        self.disagreement_log.append(record)
        return record

    def update_outcome(
        self,
        record_id: int,
        outcome: str
    ):
        """Update record with actual outcome for learning"""
        if record_id < len(self.disagreement_log):
            self.disagreement_log[record_id].outcome = outcome

    def analyze_patterns(self) -> dict:
        """Analyze disagreement patterns for system improvement"""

        if not self.disagreement_log:
            return {"message": "No disagreements recorded"}

        total = len(self.disagreement_log)
        human_overrides = sum(1 for d in self.disagreement_log
                             if d.resolution == DisagreementResolution.HUMAN_OVERRIDES)

        # Track outcomes when human overrode AI
        human_override_outcomes = [
            d.outcome for d in self.disagreement_log
            if d.resolution == DisagreementResolution.HUMAN_OVERRIDES and d.outcome
        ]

        return {
            "total_disagreements": total,
            "human_override_rate": human_overrides / total if total > 0 else 0,
            "resolution_distribution": {
                r.value: sum(1 for d in self.disagreement_log if d.resolution == r)
                for r in DisagreementResolution
            },
            "human_override_outcomes": human_override_outcomes[:10]  # Sample
        }


# Usage
handler = DisagreementHandler(api_key="your-key")

# Analyze a disagreement
analysis = handler.analyze_disagreement(
    ai_recommendation="Reject the contractor application",
    ai_confidence=0.85,
    ai_reasoning="Past performance score of 2.3/5 is below threshold",
    human_position="Approve with conditions",
    human_reasoning="Their recent work has improved and they're the only qualified bidder"
)

print(json.dumps(analysis, indent=2))

# Facilitate productive discussion
response = handler.facilitate_discussion(
    disagreement=analysis,
    ai_position="Reject the contractor application",
    human_concerns=[
        "They're the only qualified bidder",
        "Recent work shows improvement",
        "Time constraints make re-bidding impractical"
    ]
)

print(response)
```

---

## 25.6 Team Dynamics with AI

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI IN TEAM ENVIRONMENTS                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      TEAM + AI CONFIGURATION                        │  │
│   │                                                                     │  │
│   │        ┌──────────┐                                                │  │
│   │        │  TEAM    │                                                │  │
│   │        │  LEAD    │                                                │  │
│   │        └────┬─────┘                                                │  │
│   │             │                                                       │  │
│   │      ┌──────┴──────┐                                               │  │
│   │      │             │                                               │  │
│   │  ┌───┴────┐   ┌────┴───┐   ┌─────────┐                            │  │
│   │  │ TEAM   │   │ TEAM   │   │   AI    │                            │  │
│   │  │MEMBER A│   │MEMBER B│   │ASSISTANT│                            │  │
│   │  └────────┘   └────────┘   └─────────┘                            │  │
│   │                                                                     │  │
│   │  AI ROLES IN TEAMS:                                                │  │
│   │  • Research assistant (gather information)                         │  │
│   │  • Draft generator (initial content creation)                      │  │
│   │  • Quality checker (review and validation)                         │  │
│   │  • Meeting summarizer (capture decisions)                          │  │
│   │  • Process coordinator (track tasks)                               │  │
│   │                                                                     │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│   BEST PRACTICES:                                                           │
│   • Clearly define AI's role and limitations to all team members          │
│   • Establish when AI suggestions need human sign-off                      │
│   • Create feedback channels for AI performance                            │
│   • Regular calibration sessions (is AI helping or hindering?)            │
│   • Don't let AI become a crutch - maintain human skills                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Hands-On Lab: Build a Collaborative AI Assistant

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAB: Federal Policy Analyst Assistant                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BUILD an AI assistant that collaborates with policy analysts:              │
│                                                                             │
│  1. Helps research policy questions                                        │
│  2. Drafts policy briefs (human writes final)                             │
│  3. Identifies potential issues in draft policies                          │
│  4. Tracks changes and maintains version history                           │
│  5. Learns from analyst feedback                                           │
│                                                                             │
│  REQUIREMENTS:                                                              │
│  □ Clear explanation of all recommendations                                │
│  □ Confidence levels displayed                                             │
│  □ Easy feedback collection                                                │
│  □ Disagreement handling workflow                                          │
│  □ Audit trail of AI suggestions vs human decisions                        │
│                                                                             │
│  SUCCESS CRITERIA:                                                          │
│  • Analysts report AI is helpful, not frustrating                          │
│  • Agreement rate >80% (AI suggestions accepted/modified)                  │
│  • Clear documentation of all AI involvement                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Knowledge Check

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ✓ COMPREHENSION QUESTIONS                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. What are the four collaboration paradigms on the human-AI spectrum?    │
│                                                                             │
│  2. How do you build trust through explainability?                         │
│                                                                             │
│  3. What types of feedback improve AI performance over time?               │
│                                                                             │
│  4. How should disagreements between human and AI be resolved?             │
│                                                                             │
│  5. What's the key principle of human-AI collaboration in federal context? │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MODULE 25 SUMMARY: HUMAN-AI COLLABORATION                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  KEY PRINCIPLES:                                                            │
│  ├── Humans maintain accountability and final decision authority           │
│  ├── AI augments human capabilities, doesn't replace judgment              │
│  ├── Transparency builds trust - explain all recommendations               │
│  └── Feedback loops enable continuous improvement                          │
│                                                                             │
│  COLLABORATION PATTERNS:                                                    │
│  ├── Human decides, AI assists (policy, security)                         │
│  ├── AI drafts, human finalizes (documents, responses)                    │
│  ├── AI executes, human monitors (routine processing)                     │
│  └── Graceful escalation when uncertain                                   │
│                                                                             │
│  NEXT: Module 26 - Future Trends                                           │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Federal Working Group LLM Training Program - Module 25*
