# Module 24: Workflow Automation with AI

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██╗      ██████╗ ██╗    ██╗    ║
║   ██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██║     ██╔═══██╗██║    ██║    ║
║   ██║ █╗ ██║██║   ██║██████╔╝█████╔╝ █████╗  ██║     ██║   ██║██║ █╗ ██║    ║
║   ██║███╗██║██║   ██║██╔══██╗██╔═██╗ ██╔══╝  ██║     ██║   ██║██║███╗██║    ║
║   ╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗██║     ███████╗╚██████╔╝╚███╔███╔╝    ║
║    ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝  ╚══╝╚══╝     ║
║                                                                              ║
║               Intelligent Process Automation • AI Workflows                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Learning Objectives

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  By the end of this module, you will be able to:                           │
│                                                                             │
│  □ Design AI-powered workflow automation systems                           │
│  □ Integrate LLMs into existing business processes                         │
│  □ Build intelligent document routing and classification                   │
│  □ Create automated approval workflows with AI decision support            │
│  □ Implement n8n and similar platforms for AI orchestration               │
│  □ Handle exceptions and human-in-the-loop patterns                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 24.1 Workflow Automation Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AI WORKFLOW AUTOMATION ARCHITECTURE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                         ┌─────────────────────┐                             │
│                         │    TRIGGER EVENT    │                             │
│                         │  (Email/Form/API)   │                             │
│                         └──────────┬──────────┘                             │
│                                    │                                        │
│                                    ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      AI CLASSIFICATION LAYER                        │  │
│   │   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐              │  │
│   │   │  Document   │   │  Intent     │   │  Priority   │              │  │
│   │   │  Type       │   │  Detection  │   │  Scoring    │              │  │
│   │   └─────────────┘   └─────────────┘   └─────────────┘              │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                    │                                        │
│              ┌─────────────────────┼─────────────────────┐                  │
│              │                     │                     │                  │
│              ▼                     ▼                     ▼                  │
│   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐         │
│   │   ROUTE A       │   │   ROUTE B       │   │   ROUTE C       │         │
│   │   Auto-Process  │   │   Human Review  │   │   Escalation    │         │
│   └────────┬────────┘   └────────┬────────┘   └────────┬────────┘         │
│            │                     │                     │                    │
│            └─────────────────────┼─────────────────────┘                    │
│                                  │                                          │
│                                  ▼                                          │
│                    ┌─────────────────────────┐                              │
│                    │   AI-ASSISTED ACTION    │                              │
│                    │  (Generate/Extract/     │                              │
│                    │   Transform/Respond)    │                              │
│                    └─────────────────────────┘                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Workflow Platform Comparison

| Platform | AI Integration | Best For | Federal Ready |
|----------|---------------|----------|---------------|
| **n8n** | Native + Custom | Complex workflows | Self-hosted ✓ |
| **Zapier** | OpenAI/Claude | Simple automation | Cloud only |
| **Make** | AI modules | Visual workflows | Cloud only |
| **Power Automate** | Azure OpenAI | Microsoft ecosystem | FedRAMP ✓ |
| **Apache Airflow** | Custom Python | Data pipelines | Self-hosted ✓ |
| **Temporal** | Custom workers | Mission-critical | Self-hosted ✓ |

---

## 24.2 Document Classification & Routing

```python
"""
Intelligent Document Classification System
Automated routing based on content analysis
"""
from openai import OpenAI
from enum import Enum
from dataclasses import dataclass
from typing import Optional
import json


class DocumentType(Enum):
    FOIA_REQUEST = "foia_request"
    CONTRACT = "contract"
    PERSONNEL_ACTION = "personnel_action"
    SECURITY_CLEARANCE = "security_clearance"
    BUDGET_REQUEST = "budget_request"
    CORRESPONDENCE = "correspondence"
    COMPLAINT = "complaint"
    UNKNOWN = "unknown"


class Priority(Enum):
    URGENT = 1
    HIGH = 2
    NORMAL = 3
    LOW = 4


@dataclass
class ClassificationResult:
    document_type: DocumentType
    priority: Priority
    confidence: float
    routing_recommendation: str
    extracted_metadata: dict
    requires_human_review: bool
    reasoning: str


class DocumentClassifier:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                     DOCUMENT CLASSIFIER                                 │
    │                                                                         │
    │  INPUT ──▶ EXTRACT ──▶ CLASSIFY ──▶ PRIORITIZE ──▶ ROUTE              │
    │                                                                         │
    │  Federal Document Types:                                                │
    │  • FOIA Requests (20-day deadline)                                     │
    │  • Personnel Actions (SF-50, SF-52)                                    │
    │  • Security Clearances (SF-86, SF-312)                                 │
    │  • Contracts & Procurement                                              │
    │  • Budget Requests & Justifications                                     │
    │  • Congressional Correspondence                                         │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

        self.classification_prompt = """You are a federal document classifier.

Analyze the following document and provide:
1. Document type (from: foia_request, contract, personnel_action, security_clearance, budget_request, correspondence, complaint, unknown)
2. Priority level (urgent, high, normal, low)
3. Confidence score (0.0-1.0)
4. Routing recommendation (which office/team should handle)
5. Key metadata extracted (dates, names, reference numbers)
6. Whether human review is required (true/false)
7. Reasoning for classification

Return as JSON:
{
    "document_type": "...",
    "priority": "...",
    "confidence": 0.0,
    "routing_recommendation": "...",
    "metadata": {},
    "requires_human_review": false,
    "reasoning": "..."
}"""

    def classify(self, document_text: str) -> ClassificationResult:
        """Classify a document and determine routing"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": self.classification_prompt},
                {"role": "user", "content": f"Document:\n\n{document_text}"}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        return ClassificationResult(
            document_type=DocumentType(result["document_type"]),
            priority=Priority[result["priority"].upper()],
            confidence=result["confidence"],
            routing_recommendation=result["routing_recommendation"],
            extracted_metadata=result.get("metadata", {}),
            requires_human_review=result["requires_human_review"],
            reasoning=result["reasoning"]
        )

    def batch_classify(
        self,
        documents: list[str]
    ) -> list[ClassificationResult]:
        """Classify multiple documents"""
        return [self.classify(doc) for doc in documents]


class WorkflowRouter:
    """Route classified documents to appropriate handlers"""

    def __init__(self):
        self.routing_rules = {
            DocumentType.FOIA_REQUEST: {
                "handler": "foia_office",
                "sla_hours": 480,  # 20 business days
                "auto_acknowledge": True
            },
            DocumentType.CONTRACT: {
                "handler": "procurement_office",
                "sla_hours": 72,
                "auto_acknowledge": False
            },
            DocumentType.PERSONNEL_ACTION: {
                "handler": "hr_office",
                "sla_hours": 24,
                "auto_acknowledge": True
            },
            DocumentType.SECURITY_CLEARANCE: {
                "handler": "security_office",
                "sla_hours": 48,
                "auto_acknowledge": False
            },
            DocumentType.BUDGET_REQUEST: {
                "handler": "budget_office",
                "sla_hours": 168,  # 7 days
                "auto_acknowledge": True
            },
            DocumentType.CORRESPONDENCE: {
                "handler": "executive_office",
                "sla_hours": 48,
                "auto_acknowledge": True
            },
            DocumentType.COMPLAINT: {
                "handler": "compliance_office",
                "sla_hours": 24,
                "auto_acknowledge": True
            }
        }

    def route(
        self,
        classification: ClassificationResult
    ) -> dict:
        """Determine routing for classified document"""

        rules = self.routing_rules.get(
            classification.document_type,
            {"handler": "general_inbox", "sla_hours": 72, "auto_acknowledge": False}
        )

        # Adjust SLA based on priority
        priority_multipliers = {
            Priority.URGENT: 0.25,
            Priority.HIGH: 0.5,
            Priority.NORMAL: 1.0,
            Priority.LOW: 1.5
        }

        adjusted_sla = rules["sla_hours"] * priority_multipliers[classification.priority]

        return {
            "destination": rules["handler"],
            "sla_hours": adjusted_sla,
            "auto_acknowledge": rules["auto_acknowledge"] and not classification.requires_human_review,
            "metadata": classification.extracted_metadata,
            "classification": classification.document_type.value,
            "priority": classification.priority.name,
            "confidence": classification.confidence
        }


# Usage
classifier = DocumentClassifier(api_key="your-key")
router = WorkflowRouter()

# Process incoming document
document = """
Subject: Freedom of Information Act Request

Dear FOIA Officer,

Under the Freedom of Information Act, 5 U.S.C. § 552, I am requesting access to
all records related to Contract Number GS-00F-1234 between January 1, 2023 and
December 31, 2023.

I am a journalist working on a story about federal procurement...
"""

classification = classifier.classify(document)
routing = router.route(classification)

print(f"Document Type: {classification.document_type.value}")
print(f"Priority: {classification.priority.name}")
print(f"Route to: {routing['destination']}")
print(f"SLA: {routing['sla_hours']} hours")
```

---

## 24.3 n8n Integration for AI Workflows

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         n8n AI WORKFLOW EXAMPLE                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ Webhook │───▶│ OpenAI  │───▶│  IF     │───▶│  Slack  │───▶│ Database│  │
│  │ Trigger │    │ Classify│    │ Router  │    │ Notify  │    │  Store  │  │
│  └─────────┘    └─────────┘    └─────────┘    └─────────┘    └─────────┘  │
│                                      │                                      │
│                                      │ (Low Confidence)                     │
│                                      ▼                                      │
│                               ┌─────────────┐                               │
│                               │   Human     │                               │
│                               │   Review    │                               │
│                               │   Queue     │                               │
│                               └─────────────┘                               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### n8n Workflow Configuration

```json
{
  "name": "AI Document Processing",
  "nodes": [
    {
      "name": "Webhook Trigger",
      "type": "n8n-nodes-base.webhook",
      "parameters": {
        "path": "document-intake",
        "httpMethod": "POST"
      },
      "position": [250, 300]
    },
    {
      "name": "OpenAI Classify",
      "type": "n8n-nodes-base.openAi",
      "parameters": {
        "resource": "chat",
        "model": "gpt-4o",
        "messages": {
          "values": [
            {
              "role": "system",
              "content": "Classify the document type. Return JSON with: type, priority, confidence"
            },
            {
              "role": "user",
              "content": "={{ $json.document_content }}"
            }
          ]
        },
        "options": {
          "responseFormat": "json_object"
        }
      },
      "position": [450, 300]
    },
    {
      "name": "Parse Classification",
      "type": "n8n-nodes-base.code",
      "parameters": {
        "language": "javaScript",
        "code": "const result = JSON.parse($json.message.content);\nreturn { json: { ...result, original: $('Webhook Trigger').first().json } };"
      },
      "position": [650, 300]
    },
    {
      "name": "Route by Type",
      "type": "n8n-nodes-base.switch",
      "parameters": {
        "dataType": "string",
        "value1": "={{ $json.type }}",
        "rules": [
          {"value": "foia_request", "output": 0},
          {"value": "contract", "output": 1},
          {"value": "complaint", "output": 2}
        ],
        "fallbackOutput": 3
      },
      "position": [850, 300]
    }
  ],
  "connections": {
    "Webhook Trigger": {
      "main": [[{"node": "OpenAI Classify", "type": "main", "index": 0}]]
    },
    "OpenAI Classify": {
      "main": [[{"node": "Parse Classification", "type": "main", "index": 0}]]
    },
    "Parse Classification": {
      "main": [[{"node": "Route by Type", "type": "main", "index": 0}]]
    }
  }
}
```

### Custom n8n Node for LLM Processing

```typescript
// Custom n8n node for federal document processing
import {
  IExecuteFunctions,
  INodeType,
  INodeTypeDescription,
  INodeExecutionData,
} from 'n8n-workflow';

export class FederalDocProcessor implements INodeType {
  description: INodeTypeDescription = {
    displayName: 'Federal Document Processor',
    name: 'federalDocProcessor',
    group: ['transform'],
    version: 1,
    description: 'Process federal documents with AI',
    defaults: {
      name: 'Federal Doc Processor',
    },
    inputs: ['main'],
    outputs: ['main'],
    properties: [
      {
        displayName: 'Operation',
        name: 'operation',
        type: 'options',
        options: [
          { name: 'Classify', value: 'classify' },
          { name: 'Extract Data', value: 'extract' },
          { name: 'Redact PII', value: 'redact' },
          { name: 'Generate Response', value: 'respond' },
        ],
        default: 'classify',
      },
      {
        displayName: 'Document Content',
        name: 'content',
        type: 'string',
        default: '',
        required: true,
        displayOptions: {
          show: { operation: ['classify', 'extract', 'redact'] },
        },
      },
      {
        displayName: 'Classification Context',
        name: 'context',
        type: 'string',
        default: '',
        description: 'Additional context for classification',
      },
    ],
  };

  async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
    const items = this.getInputData();
    const returnData: INodeExecutionData[] = [];

    const operation = this.getNodeParameter('operation', 0) as string;

    for (let i = 0; i < items.length; i++) {
      const content = this.getNodeParameter('content', i) as string;

      let result: any;

      switch (operation) {
        case 'classify':
          result = await this.classifyDocument(content);
          break;
        case 'extract':
          result = await this.extractData(content);
          break;
        case 'redact':
          result = await this.redactPII(content);
          break;
        case 'respond':
          result = await this.generateResponse(content);
          break;
      }

      returnData.push({ json: result });
    }

    return [returnData];
  }

  private async classifyDocument(content: string): Promise<object> {
    // Call OpenAI API for classification
    // Implementation here
    return { type: 'classified', confidence: 0.95 };
  }

  private async extractData(content: string): Promise<object> {
    // Extract structured data
    return { extracted: true };
  }

  private async redactPII(content: string): Promise<object> {
    // Identify and redact PII
    return { redacted: content, pii_found: [] };
  }

  private async generateResponse(content: string): Promise<object> {
    // Generate appropriate response
    return { response: '' };
  }
}
```

---

## 24.4 Approval Workflow with AI Decision Support

```python
"""
AI-Assisted Approval Workflow
Provides recommendations while maintaining human oversight
"""
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
from typing import Optional
import json


class ApprovalDecision(Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    NEEDS_INFO = "needs_more_info"
    ESCALATE = "escalate"
    PENDING = "pending"


@dataclass
class ApprovalRequest:
    id: str
    type: str
    requestor: str
    amount: Optional[float]
    description: str
    supporting_docs: list[str]
    submitted_at: datetime
    deadline: Optional[datetime]


@dataclass
class AIRecommendation:
    decision: ApprovalDecision
    confidence: float
    reasoning: str
    risk_factors: list[str]
    similar_cases: list[dict]
    suggested_conditions: list[str]


class ApprovalWorkflow:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                   AI-ASSISTED APPROVAL WORKFLOW                         │
    │                                                                         │
    │  ┌──────────┐    ┌──────────────┐    ┌──────────────┐                  │
    │  │ REQUEST  │───▶│ AI ANALYSIS  │───▶│ HUMAN REVIEW │                  │
    │  │ INTAKE   │    │ & RECOMMEND  │    │ & DECISION   │                  │
    │  └──────────┘    └──────────────┘    └──────────────┘                  │
    │                         │                    │                          │
    │                         ▼                    ▼                          │
    │                  ┌─────────────────────────────────┐                    │
    │                  │        AUDIT LOG               │                    │
    │                  │  (AI recommendation + Human    │                    │
    │                  │   decision + reasoning)        │                    │
    │                  └─────────────────────────────────┘                    │
    │                                                                         │
    │  KEY PRINCIPLE: AI advises, humans decide                              │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)
        self.audit_log = []

    def analyze_request(
        self,
        request: ApprovalRequest,
        policy_context: str = ""
    ) -> AIRecommendation:
        """
        Analyze approval request and generate recommendation

        IMPORTANT: This is a RECOMMENDATION only.
        Final decision must be made by authorized human.
        """

        prompt = f"""Analyze this approval request and provide a recommendation.

REQUEST DETAILS:
- Type: {request.type}
- Requestor: {request.requestor}
- Amount: ${request.amount if request.amount else 'N/A'}
- Description: {request.description}
- Deadline: {request.deadline or 'No deadline'}

POLICY CONTEXT:
{policy_context}

Provide analysis as JSON:
{{
    "recommendation": "approved|rejected|needs_more_info|escalate",
    "confidence": 0.0-1.0,
    "reasoning": "detailed explanation",
    "risk_factors": ["list of concerns"],
    "similar_cases": ["brief descriptions of similar past cases"],
    "suggested_conditions": ["conditions if recommending approval"]
}}

IMPORTANT: This is advisory only. Flag any edge cases for human review."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an approval workflow advisor. Provide thorough analysis but always emphasize that final decisions require human judgment."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)

        recommendation = AIRecommendation(
            decision=ApprovalDecision(result["recommendation"]),
            confidence=result["confidence"],
            reasoning=result["reasoning"],
            risk_factors=result.get("risk_factors", []),
            similar_cases=result.get("similar_cases", []),
            suggested_conditions=result.get("suggested_conditions", [])
        )

        # Log AI recommendation
        self._log_event({
            "type": "ai_recommendation",
            "request_id": request.id,
            "recommendation": recommendation.decision.value,
            "confidence": recommendation.confidence,
            "timestamp": datetime.now().isoformat()
        })

        return recommendation

    def record_human_decision(
        self,
        request_id: str,
        ai_recommendation: AIRecommendation,
        human_decision: ApprovalDecision,
        human_reasoning: str,
        approver_id: str
    ) -> dict:
        """
        Record final human decision alongside AI recommendation

        Federal Requirement: Full audit trail with accountability
        """
        audit_record = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "ai_recommendation": {
                "decision": ai_recommendation.decision.value,
                "confidence": ai_recommendation.confidence,
                "reasoning": ai_recommendation.reasoning
            },
            "human_decision": {
                "decision": human_decision.value,
                "reasoning": human_reasoning,
                "approver_id": approver_id,
                "agreed_with_ai": ai_recommendation.decision == human_decision
            }
        }

        self._log_event(audit_record)

        return audit_record

    def _log_event(self, event: dict):
        """Append to audit log"""
        self.audit_log.append(event)
        # In production: persist to database/audit system


class MultiLevelApproval:
    """
    Multi-level approval workflow with AI at each level

    Example: Purchase requests with tiered approval
    """

    def __init__(self, workflow: ApprovalWorkflow):
        self.workflow = workflow

        # Define approval levels
        self.levels = [
            {"name": "Supervisor", "max_amount": 2500, "role": "supervisor"},
            {"name": "Manager", "max_amount": 10000, "role": "manager"},
            {"name": "Director", "max_amount": 50000, "role": "director"},
            {"name": "Executive", "max_amount": float('inf'), "role": "executive"}
        ]

    def determine_approval_chain(
        self,
        request: ApprovalRequest
    ) -> list[dict]:
        """Determine required approval levels"""
        chain = []

        for level in self.levels:
            chain.append(level)
            if request.amount and request.amount <= level["max_amount"]:
                break

        return chain

    def process_approval_chain(
        self,
        request: ApprovalRequest,
        policy_context: str = ""
    ) -> dict:
        """
        Process through approval chain with AI support at each level
        """
        chain = self.determine_approval_chain(request)

        results = {
            "request_id": request.id,
            "approval_chain": [],
            "current_status": "pending"
        }

        for level in chain:
            # Get AI recommendation for this level
            ai_rec = self.workflow.analyze_request(
                request,
                f"{policy_context}\n\nApproval Level: {level['name']}"
            )

            results["approval_chain"].append({
                "level": level["name"],
                "role_required": level["role"],
                "ai_recommendation": ai_rec.decision.value,
                "ai_confidence": ai_rec.confidence,
                "ai_reasoning": ai_rec.reasoning,
                "human_decision": "pending",
                "human_reasoning": None
            })

        return results


# Usage example
workflow = ApprovalWorkflow(api_key="your-key")
multi_level = MultiLevelApproval(workflow)

# Create a purchase request
request = ApprovalRequest(
    id="PR-2024-001",
    type="purchase_request",
    requestor="John.Smith@agency.gov",
    amount=15000.00,
    description="Software licenses for development team - Annual renewal",
    supporting_docs=["quote.pdf", "justification.docx"],
    submitted_at=datetime.now(),
    deadline=datetime(2024, 2, 15)
)

# Process through approval chain
result = multi_level.process_approval_chain(
    request,
    policy_context="Standard procurement policy applies. Prior approval existed for similar amount."
)

print(json.dumps(result, indent=2, default=str))
```

---

## 24.5 Email Processing Automation

```python
"""
Intelligent Email Processing System
Auto-categorize, respond, and route emails
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Email:
    id: str
    sender: str
    subject: str
    body: str
    received_at: datetime
    attachments: list[str]
    thread_id: Optional[str] = None


class EmailProcessor:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    EMAIL PROCESSING PIPELINE                            │
    │                                                                         │
    │  ┌──────────┐   ┌────────────┐   ┌────────────┐   ┌────────────┐      │
    │  │ RECEIVE  │──▶│  CLASSIFY  │──▶│  EXTRACT   │──▶│   ROUTE    │      │
    │  │  EMAIL   │   │  INTENT    │   │  ENTITIES  │   │  OR ACT    │      │
    │  └──────────┘   └────────────┘   └────────────┘   └────────────┘      │
    │                        │                                 │             │
    │                        ▼                                 ▼             │
    │                 ┌─────────────────────────────────────────────┐        │
    │                 │         AUTO-RESPONSE OPTIONS              │        │
    │                 │  • Acknowledgment                          │        │
    │                 │  • Information Request                     │        │
    │                 │  • Standard Response                       │        │
    │                 │  • Draft for Human Review                  │        │
    │                 └─────────────────────────────────────────────┘        │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(self, api_key: str):
        from openai import OpenAI
        self.client = OpenAI(api_key=api_key)

        self.auto_response_templates = {
            "acknowledgment": """Thank you for your email. We have received your message and will respond within {sla} business days.

Your reference number is: {ref_number}

If this is urgent, please call our main line at {phone_number}.

Best regards,
{agency_name}""",

            "info_request": """Thank you for contacting {agency_name}.

To better assist you, we need the following additional information:
{required_info}

Please reply to this email with the requested information.

Reference: {ref_number}""",

            "foia_ack": """This acknowledges receipt of your Freedom of Information Act (FOIA) request.

Request Number: {ref_number}
Date Received: {date_received}

Under FOIA, we have 20 business days to respond to your request. We will contact you if we need additional information or clarification.

FOIA Office
{agency_name}"""
        }

    def process_email(self, email: Email) -> dict:
        """Process incoming email with AI"""

        # Step 1: Classify intent
        classification = self._classify_email(email)

        # Step 2: Extract key entities
        entities = self._extract_entities(email)

        # Step 3: Determine action
        action = self._determine_action(classification, entities)

        # Step 4: Generate response if applicable
        response = None
        if action["auto_respond"]:
            response = self._generate_response(email, classification, entities)

        return {
            "email_id": email.id,
            "classification": classification,
            "entities": entities,
            "action": action,
            "response_draft": response
        }

    def _classify_email(self, email: Email) -> dict:
        """Classify email intent and category"""

        prompt = f"""Classify this email:

From: {email.sender}
Subject: {email.subject}
Body: {email.body[:2000]}

Classify:
1. Category: (inquiry, complaint, foia_request, service_request, feedback, spam, other)
2. Sentiment: (positive, neutral, negative, urgent)
3. Priority: (low, medium, high, urgent)
4. Response needed: (yes, no, maybe)
5. Complexity: (simple, moderate, complex)

Return as JSON."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def _extract_entities(self, email: Email) -> dict:
        """Extract key entities from email"""

        prompt = f"""Extract entities from this email:

{email.body[:3000]}

Extract:
- Person names
- Organization names
- Dates mentioned
- Reference numbers (case numbers, tracking IDs)
- Phone numbers
- Specific requests/asks
- Key topics

Return as JSON with lists for each entity type."""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)

    def _determine_action(
        self,
        classification: dict,
        entities: dict
    ) -> dict:
        """Determine appropriate action based on analysis"""

        action = {
            "auto_respond": False,
            "response_type": None,
            "route_to": None,
            "create_ticket": False,
            "priority": classification.get("priority", "medium")
        }

        category = classification.get("category", "other")

        if category == "foia_request":
            action["auto_respond"] = True
            action["response_type"] = "foia_ack"
            action["route_to"] = "foia_office"
            action["create_ticket"] = True

        elif category == "inquiry" and classification.get("complexity") == "simple":
            action["auto_respond"] = True
            action["response_type"] = "acknowledgment"

        elif category == "complaint":
            action["auto_respond"] = True
            action["response_type"] = "acknowledgment"
            action["route_to"] = "complaints_team"
            action["create_ticket"] = True
            action["priority"] = "high"

        elif category == "spam":
            action["auto_respond"] = False
            action["route_to"] = "spam_folder"

        else:
            action["auto_respond"] = True
            action["response_type"] = "acknowledgment"
            action["route_to"] = "general_inbox"

        return action

    def _generate_response(
        self,
        email: Email,
        classification: dict,
        entities: dict
    ) -> str:
        """Generate appropriate response"""

        response_type = classification.get("response_type", "acknowledgment")

        if response_type in self.auto_response_templates:
            # Use template
            template = self.auto_response_templates[response_type]
            return template.format(
                sla="5",
                ref_number=f"REF-{email.id}",
                phone_number="1-800-XXX-XXXX",
                agency_name="Federal Agency",
                date_received=email.received_at.strftime("%Y-%m-%d"),
                required_info="[To be filled]"
            )

        # Generate custom response with AI
        prompt = f"""Draft a professional response to this email:

Original Email:
From: {email.sender}
Subject: {email.subject}
Body: {email.body[:1500]}

Classification: {classification}

Requirements:
- Professional federal government tone
- Acknowledge their message
- Provide next steps if applicable
- Include reference number: REF-{email.id}
- Keep it concise"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are drafting email responses for a federal agency. Be professional, helpful, and accurate."
                },
                {"role": "user", "content": prompt}
            ]
        )

        return response.choices[0].message.content


# Batch processing
async def process_email_batch(
    emails: list[Email],
    processor: EmailProcessor
) -> list[dict]:
    """Process multiple emails concurrently"""
    import asyncio

    async def process_one(email: Email) -> dict:
        return processor.process_email(email)

    tasks = [process_one(email) for email in emails]
    return await asyncio.gather(*tasks)
```

---

## 24.6 Exception Handling & Human-in-the-Loop

```python
"""
Exception Handling and Human-in-the-Loop Patterns
Graceful degradation when AI is uncertain
"""
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Any
import asyncio


class EscalationReason(Enum):
    LOW_CONFIDENCE = "low_confidence"
    POLICY_EXCEPTION = "policy_exception"
    HIGH_VALUE = "high_value"
    SENSITIVE_CONTENT = "sensitive_content"
    CONFLICTING_SIGNALS = "conflicting_signals"
    SYSTEM_ERROR = "system_error"


@dataclass
class HumanTask:
    id: str
    type: str
    context: dict
    ai_analysis: dict
    escalation_reason: EscalationReason
    priority: int
    assigned_to: str = None
    status: str = "pending"


class HumanInTheLoop:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │                    HUMAN-IN-THE-LOOP PATTERNS                           │
    │                                                                         │
    │  ┌───────────────────────────────────────────────────────────────────┐ │
    │  │                     CONFIDENCE THRESHOLD                         │ │
    │  │                                                                   │ │
    │  │   HIGH (>0.9)      MEDIUM (0.7-0.9)     LOW (<0.7)              │ │
    │  │   ┌─────────┐      ┌─────────────┐      ┌───────────┐           │ │
    │  │   │  AUTO   │      │  EXECUTE +  │      │  HUMAN    │           │ │
    │  │   │ EXECUTE │      │   NOTIFY    │      │  REVIEW   │           │ │
    │  │   └─────────┘      └─────────────┘      └───────────┘           │ │
    │  │                                                                   │ │
    │  └───────────────────────────────────────────────────────────────────┘ │
    │                                                                         │
    │  ESCALATION TRIGGERS:                                                   │
    │  • Confidence below threshold                                          │
    │  • Policy exceptions detected                                          │
    │  • High-value transactions                                             │
    │  • Sensitive/PII content                                               │
    │  • Conflicting classification signals                                  │
    │                                                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """

    def __init__(
        self,
        confidence_threshold: float = 0.85,
        high_value_threshold: float = 10000
    ):
        self.confidence_threshold = confidence_threshold
        self.high_value_threshold = high_value_threshold
        self.human_queue: list[HumanTask] = []
        self.callbacks: dict[str, Callable] = {}

    def should_escalate(
        self,
        ai_result: dict,
        context: dict
    ) -> tuple[bool, EscalationReason]:
        """Determine if human review is needed"""

        confidence = ai_result.get("confidence", 0)

        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return True, EscalationReason.LOW_CONFIDENCE

        # Check for high-value items
        if context.get("amount", 0) > self.high_value_threshold:
            return True, EscalationReason.HIGH_VALUE

        # Check for sensitive content flags
        if ai_result.get("contains_pii") or ai_result.get("sensitive_content"):
            return True, EscalationReason.SENSITIVE_CONTENT

        # Check for policy exceptions
        if ai_result.get("policy_exception"):
            return True, EscalationReason.POLICY_EXCEPTION

        # Check for conflicting signals
        if ai_result.get("conflicting_indicators"):
            return True, EscalationReason.CONFLICTING_SIGNALS

        return False, None

    def create_human_task(
        self,
        task_type: str,
        context: dict,
        ai_analysis: dict,
        reason: EscalationReason,
        priority: int = 5
    ) -> HumanTask:
        """Create a task for human review"""

        import uuid

        task = HumanTask(
            id=str(uuid.uuid4()),
            type=task_type,
            context=context,
            ai_analysis=ai_analysis,
            escalation_reason=reason,
            priority=priority
        )

        self.human_queue.append(task)
        self._notify_queue_update()

        return task

    def process_with_fallback(
        self,
        ai_processor: Callable,
        context: dict,
        fallback_handler: Callable = None
    ) -> dict:
        """
        Process with AI, fall back to human if needed
        """
        try:
            # Attempt AI processing
            ai_result = ai_processor(context)

            # Check if escalation needed
            needs_escalation, reason = self.should_escalate(ai_result, context)

            if needs_escalation:
                task = self.create_human_task(
                    task_type="review",
                    context=context,
                    ai_analysis=ai_result,
                    reason=reason
                )

                return {
                    "status": "pending_human_review",
                    "task_id": task.id,
                    "reason": reason.value,
                    "ai_recommendation": ai_result
                }

            return {
                "status": "auto_processed",
                "result": ai_result
            }

        except Exception as e:
            # System error - always escalate
            task = self.create_human_task(
                task_type="error_review",
                context=context,
                ai_analysis={"error": str(e)},
                reason=EscalationReason.SYSTEM_ERROR,
                priority=1  # High priority
            )

            if fallback_handler:
                return fallback_handler(context, e)

            return {
                "status": "error",
                "task_id": task.id,
                "error": str(e)
            }

    def complete_human_task(
        self,
        task_id: str,
        decision: dict,
        reviewer_id: str
    ) -> dict:
        """Record human decision on escalated task"""

        task = next((t for t in self.human_queue if t.id == task_id), None)
        if not task:
            return {"error": "Task not found"}

        task.status = "completed"

        return {
            "task_id": task_id,
            "human_decision": decision,
            "reviewer": reviewer_id,
            "ai_recommendation": task.ai_analysis,
            "agreed_with_ai": self._compare_decisions(
                task.ai_analysis,
                decision
            )
        }

    def _compare_decisions(
        self,
        ai_analysis: dict,
        human_decision: dict
    ) -> bool:
        """Compare AI recommendation to human decision"""
        ai_rec = ai_analysis.get("recommendation", "").lower()
        human_dec = human_decision.get("decision", "").lower()
        return ai_rec == human_dec

    def _notify_queue_update(self):
        """Notify subscribers of queue changes"""
        if "queue_update" in self.callbacks:
            self.callbacks["queue_update"](self.human_queue)

    def on_queue_update(self, callback: Callable):
        """Register callback for queue updates"""
        self.callbacks["queue_update"] = callback


# Usage example
hitl = HumanInTheLoop(
    confidence_threshold=0.85,
    high_value_threshold=10000
)

def mock_ai_processor(context: dict) -> dict:
    """Simulated AI processing"""
    return {
        "classification": "purchase_request",
        "confidence": 0.72,  # Below threshold
        "recommendation": "approve",
        "risk_factors": ["unusual vendor"]
    }

# Process with human fallback
result = hitl.process_with_fallback(
    ai_processor=mock_ai_processor,
    context={"type": "purchase", "amount": 5000}
)

print(f"Status: {result['status']}")
# Output: Status: pending_human_review
```

---

## Hands-On Lab: Build an Intelligent Request Processing System

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  LAB: Federal Request Processing Workflow                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  BUILD a complete workflow automation system that:                          │
│                                                                             │
│  1. Receives requests via API webhook                                       │
│  2. Classifies request type and priority with AI                           │
│  3. Routes to appropriate queue                                            │
│  4. Generates acknowledgment response                                       │
│  5. Creates tracking ticket                                                │
│  6. Escalates to human when confidence is low                              │
│                                                                             │
│  DELIVERABLES:                                                              │
│  □ Document classifier with >90% accuracy                                  │
│  □ Routing logic for 5+ document types                                     │
│  □ Auto-response generation                                                │
│  □ Human-in-the-loop escalation                                            │
│  □ Audit logging                                                           │
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
│  1. When should an AI workflow escalate to human review?                   │
│                                                                             │
│  2. What are the key components of a document classification system?       │
│                                                                             │
│  3. How do you maintain audit trails in AI-assisted approval workflows?    │
│                                                                             │
│  4. What's the difference between auto-response and AI-generated response? │
│                                                                             │
│  5. How do you handle system errors in automated workflows?                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Summary

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  MODULE 24 SUMMARY: WORKFLOW AUTOMATION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  KEY PATTERNS:                                                              │
│  ├── Document Classification: AI categorizes and prioritizes              │
│  ├── Intelligent Routing: Content-based destination selection             │
│  ├── AI-Assisted Approval: Recommendations with human oversight           │
│  └── Human-in-the-Loop: Graceful escalation when uncertain                │
│                                                                             │
│  FEDERAL REQUIREMENTS:                                                      │
│  ├── Complete audit trails                                                 │
│  ├── Human accountability for decisions                                    │
│  ├── SLA tracking and compliance                                           │
│  └── Exception handling and escalation                                     │
│                                                                             │
│  NEXT: Module 25 - Human-AI Collaboration                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

*Federal Working Group LLM Training Program - Module 24*
