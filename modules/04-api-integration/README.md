<div align="center">

# Module 04: API Integration

<img src="https://img.shields.io/badge/Duration-6_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_01-orange?style=for-the-badge" alt="Prerequisites"/>

*Master the art of integrating LLM APIs into federal applications*

</div>

---

## 📋 Learning Objectives

By the end of this module, you will be able to:

- [ ] Understand the fundamental architecture of RESTful APIs and how LLM providers implement them
- [ ] Authenticate and connect to major LLM provider APIs using industry-standard security practices
- [ ] Implement proper error handling and retry logic that meets federal reliability standards
- [ ] Design rate-limiting strategies for production use in high-availability environments
- [ ] Choose appropriate API configurations for federal workloads based on compliance requirements
- [ ] Build secure API integrations meeting FedRAMP, FISMA, and agency-specific requirements
- [ ] Track and optimize API costs across multiple providers
- [ ] Implement streaming responses for real-time user experiences
- [ ] Use function calling and tool use to extend LLM capabilities
- [ ] Design fault-tolerant systems with proper fallback strategies

---

## 📑 Table of Contents

1. [Understanding APIs: The Foundation](#1-understanding-apis-the-foundation)
2. [API Landscape Overview](#2-api-landscape-overview)
3. [OpenAI API Deep Dive](#3-openai-api-deep-dive)
4. [Anthropic Claude API Deep Dive](#4-anthropic-claude-api-deep-dive)
5. [Google AI API Deep Dive](#5-google-ai-api-deep-dive)
6. [Azure OpenAI Service](#6-azure-openai-service)
7. [AWS Bedrock](#7-aws-bedrock)
8. [Authentication and Security](#8-authentication-and-security)
9. [Error Handling Strategies](#9-error-handling-strategies)
10. [Rate Limiting and Throttling](#10-rate-limiting-and-throttling)
11. [Cost Management and Optimization](#11-cost-management-and-optimization)
12. [Production Architecture Patterns](#12-production-architecture-patterns)
13. [Federal Compliance Considerations](#13-federal-compliance-considerations)
14. [Exercises](#14-exercises)
15. [Assessment](#15-assessment)

---

## 1. Understanding APIs: The Foundation

Before diving into LLM-specific APIs, it's crucial to understand what APIs are and how they work. This foundation will help you troubleshoot issues, design robust systems, and make informed architectural decisions.

### What is an API?

**API** stands for **Application Programming Interface**. Think of it as a contract between two pieces of software that defines how they can communicate with each other. Just as a restaurant menu defines what you can order and how to order it, an API defines what operations you can perform and how to request them.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        THE API COMMUNICATION MODEL                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   ┌─────────────────┐                           ┌─────────────────┐         ║
║   │                 │                           │                 │         ║
║   │  YOUR           │    HTTP Request           │  LLM PROVIDER   │         ║
║   │  APPLICATION    │ ────────────────────────► │  SERVER         │         ║
║   │                 │                           │                 │         ║
║   │  (Client)       │    HTTP Response          │  (API Server)   │         ║
║   │                 │ ◄──────────────────────── │                 │         ║
║   │                 │                           │                 │         ║
║   └─────────────────┘                           └─────────────────┘         ║
║                                                                              ║
║   The client sends a REQUEST containing:                                     ║
║   • HTTP Method (POST, GET, etc.)                                           ║
║   • Headers (Authentication, Content-Type)                                   ║
║   • Body (Your prompt, parameters)                                          ║
║                                                                              ║
║   The server sends a RESPONSE containing:                                    ║
║   • Status Code (200 OK, 429 Rate Limited, etc.)                            ║
║   • Headers (Rate limit info, request ID)                                   ║
║   • Body (The LLM's response, token counts)                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### HTTP: The Language of Web APIs

All major LLM APIs use **HTTP (Hypertext Transfer Protocol)** as their communication protocol. Understanding HTTP is essential for working with these APIs effectively.

#### HTTP Methods

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                           HTTP METHODS IN LLM APIs                           │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  POST   │ Create/Submit - Used for most LLM operations                      │
│         │ Example: POST /v1/chat/completions                                 │
│         │ Purpose: Send a prompt, receive a completion                       │
│         │                                                                    │
│  GET    │ Retrieve - Get information without modification                   │
│         │ Example: GET /v1/models                                            │
│         │ Purpose: List available models, check status                       │
│         │                                                                    │
│  DELETE │ Remove - Delete resources                                         │
│         │ Example: DELETE /v1/files/{file_id}                               │
│         │ Purpose: Remove uploaded files, cancel jobs                        │
│         │                                                                    │
│  PUT    │ Update/Replace - Modify existing resources                        │
│         │ Example: PUT /v1/assistants/{assistant_id}                        │
│         │ Purpose: Update assistant configurations                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### HTTP Status Codes

Understanding status codes is critical for error handling:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      HTTP STATUS CODES YOU'LL ENCOUNTER                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  2xx SUCCESS - Your request worked                                          ║
║  ──────────────────────────────────────────────────────────────────────     ║
║  200 OK              │ Request succeeded, response contains data            ║
║  201 Created         │ Resource was created (e.g., new assistant)           ║
║  204 No Content      │ Success, but no response body (e.g., delete)         ║
║                                                                              ║
║  4xx CLIENT ERRORS - Something wrong with your request                      ║
║  ──────────────────────────────────────────────────────────────────────     ║
║  400 Bad Request     │ Invalid JSON, missing required fields                ║
║  401 Unauthorized    │ Invalid or missing API key                           ║
║  403 Forbidden       │ Valid key but insufficient permissions               ║
║  404 Not Found       │ Model or resource doesn't exist                      ║
║  422 Unprocessable   │ Valid JSON but invalid parameter values              ║
║  429 Too Many Reqs   │ Rate limit exceeded - MUST implement retry           ║
║                                                                              ║
║  5xx SERVER ERRORS - Problem on provider's side                             ║
║  ──────────────────────────────────────────────────────────────────────     ║
║  500 Internal Error  │ Provider server error - retry with backoff           ║
║  502 Bad Gateway     │ Provider infrastructure issue                        ║
║  503 Unavailable     │ Service temporarily down - retry later               ║
║  504 Gateway Timeout │ Request took too long - may need to retry            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### The Anatomy of an API Request

Let's break down exactly what happens when you make an API call to an LLM provider:

```python
# This is what your code looks like:
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# But under the hood, this HTTP request is sent:
"""
POST /v1/chat/completions HTTP/1.1
Host: api.openai.com
Authorization: Bearer sk-your-api-key-here
Content-Type: application/json
User-Agent: OpenAI-Python/1.0.0

{
    "model": "gpt-4o",
    "messages": [
        {"role": "user", "content": "Hello!"}
    ]
}
"""
```

Let's examine each component:

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       ANATOMY OF AN LLM API REQUEST                          │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  REQUEST LINE                                                                │
│  ───────────────────────────────────────────────────────────────────────    │
│  POST /v1/chat/completions HTTP/1.1                                         │
│  │    │                    │                                                 │
│  │    │                    └─ Protocol version                              │
│  │    └─ Endpoint path (what operation to perform)                          │
│  └─ HTTP method (POST = send data)                                          │
│                                                                              │
│  HEADERS (Metadata about the request)                                        │
│  ───────────────────────────────────────────────────────────────────────    │
│  Host: api.openai.com          │ Which server to connect to                 │
│  Authorization: Bearer sk-...  │ Your API key for authentication            │
│  Content-Type: application/json│ Format of the request body                 │
│  User-Agent: OpenAI-Python/1.0 │ What client library you're using           │
│                                                                              │
│  BODY (The actual data you're sending)                                       │
│  ───────────────────────────────────────────────────────────────────────    │
│  {                                                                           │
│    "model": "gpt-4o",           │ Which model to use                        │
│    "messages": [...],           │ The conversation history                  │
│    "temperature": 0.7,          │ Optional: creativity level                │
│    "max_tokens": 1000           │ Optional: response length limit           │
│  }                                                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### The Anatomy of an API Response

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                       ANATOMY OF AN LLM API RESPONSE                         │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  STATUS LINE                                                                 │
│  ───────────────────────────────────────────────────────────────────────    │
│  HTTP/1.1 200 OK                                                            │
│  │        │   │                                                              │
│  │        │   └─ Human-readable status                                      │
│  │        └─ Status code (200 = success)                                    │
│  └─ Protocol version                                                         │
│                                                                              │
│  RESPONSE HEADERS                                                            │
│  ───────────────────────────────────────────────────────────────────────    │
│  x-request-id: req_abc123      │ Unique ID for debugging/support            │
│  x-ratelimit-limit-requests: 60│ Your requests per minute limit             │
│  x-ratelimit-remaining: 55     │ Requests left in current window            │
│  x-ratelimit-reset-requests: 1s│ When the limit resets                      │
│  openai-processing-ms: 2345    │ How long the model took to respond         │
│                                                                              │
│  RESPONSE BODY                                                               │
│  ───────────────────────────────────────────────────────────────────────    │
│  {                                                                           │
│    "id": "chatcmpl-abc123",            │ Unique completion ID               │
│    "object": "chat.completion",         │ Response type                      │
│    "created": 1699000000,               │ Unix timestamp                     │
│    "model": "gpt-4o-2024-08-06",       │ Exact model version used           │
│    "choices": [{                                                             │
│      "index": 0,                        │ Choice number                      │
│      "message": {                                                            │
│        "role": "assistant",             │ Who generated this                 │
│        "content": "Hello! How can..."   │ The actual response                │
│      },                                                                      │
│      "finish_reason": "stop"            │ Why generation ended               │
│    }],                                                                       │
│    "usage": {                                                                │
│      "prompt_tokens": 10,               │ Tokens in your input               │
│      "completion_tokens": 25,           │ Tokens in the response             │
│      "total_tokens": 35                 │ Total tokens (for billing)         │
│    }                                                                         │
│  }                                                                           │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
```

### Understanding Tokens and Billing

A critical concept for API usage is **tokens**—the units by which LLM providers measure and charge for usage.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          UNDERSTANDING TOKENS                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WHAT IS A TOKEN?                                                            ║
║  A token is a chunk of text that the model processes. It's NOT the same     ║
║  as a word! Tokens are determined by the model's tokenizer.                 ║
║                                                                              ║
║  TOKENIZATION EXAMPLES (GPT-4 tokenizer):                                   ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  "Hello"           → 1 token   ["Hello"]                                    ║
║  "Hello, world!"   → 4 tokens  ["Hello", ",", " world", "!"]                ║
║  "FedRAMP"         → 3 tokens  ["Fed", "R", "AMP"]                          ║
║  "authentication"  → 2 tokens  ["authentic", "ation"]                       ║
║  "123456"          → 3 tokens  ["123", "456"]                               ║
║  "🇺🇸"             → 4 tokens  (emojis are expensive!)                       ║
║                                                                              ║
║  RULE OF THUMB:                                                              ║
║  • English text: ~4 characters per token, or ~0.75 words per token          ║
║  • Code: Usually more tokens due to special characters                       ║
║  • Non-English: Often more tokens per word                                  ║
║                                                                              ║
║  WHY TOKENS MATTER FOR FEDERAL APPLICATIONS:                                 ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  1. COST: You pay per token (input + output separately)                     ║
║  2. LIMITS: Models have maximum context windows (token limits)              ║
║  3. LATENCY: More tokens = longer response times                            ║
║  4. BUDGET: Must track token usage for procurement compliance               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Synchronous vs. Streaming Responses

LLM APIs offer two modes of receiving responses:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SYNCHRONOUS VS STREAMING RESPONSES                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  SYNCHRONOUS (Default)                                                       ║
║  ───────────────────────────────────────────────────────────────────────    ║
║                                                                              ║
║  Client                              Server                                  ║
║    │                                   │                                     ║
║    │──── Request ─────────────────────►│                                     ║
║    │                                   │ Processing...                       ║
║    │                                   │ (may take 10-60+ seconds)           ║
║    │                                   │                                     ║
║    │◄─── Complete Response ────────────│                                     ║
║    │                                                                         ║
║                                                                              ║
║  Pros: Simple to implement, easy error handling                             ║
║  Cons: User waits with no feedback, timeout risks                           ║
║  Use when: Backend processing, batch jobs, short responses                  ║
║                                                                              ║
║  ═══════════════════════════════════════════════════════════════════════    ║
║                                                                              ║
║  STREAMING (Server-Sent Events)                                              ║
║  ───────────────────────────────────────────────────────────────────────    ║
║                                                                              ║
║  Client                              Server                                  ║
║    │                                   │                                     ║
║    │──── Request (stream=true) ───────►│                                     ║
║    │                                   │                                     ║
║    │◄─── chunk: "The "                 │                                     ║
║    │◄─── chunk: "answer "              │                                     ║
║    │◄─── chunk: "is "                  │                                     ║
║    │◄─── chunk: "42."                  │                                     ║
║    │◄─── chunk: [DONE]                 │                                     ║
║    │                                                                         ║
║                                                                              ║
║  Pros: Immediate feedback, better UX, reduced timeout risk                  ║
║  Cons: More complex to implement, harder error handling                     ║
║  Use when: User-facing applications, long responses, chatbots               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 2. API Landscape Overview

The LLM API ecosystem can be categorized into two main types: **Direct Provider APIs** and **Cloud Provider Wrappers**. Understanding this distinction is crucial for federal applications.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         LLM API ECOSYSTEM                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                      DIRECT PROVIDER APIs                               │║
║  │  (Connect directly to the AI company's servers)                         │║
║  │                                                                          │║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │║
║  │   │   OpenAI     │  │  Anthropic   │  │   Google     │                 │║
║  │   │              │  │              │  │              │                 │║
║  │   │ • GPT-4o     │  │ • Claude 4   │  │ • Gemini 2.0 │                 │║
║  │   │ • GPT-4      │  │ • Claude 3.5 │  │ • Gemini 1.5 │                 │║
║  │   │ • o1/o3      │  │ • Claude 3   │  │ • Embeddings │                 │║
║  │   │ • Embeddings │  │ • Haiku      │  │ • Imagen     │                 │║
║  │   │ • DALL-E     │  │              │  │              │                 │║
║  │   └──────────────┘  └──────────────┘  └──────────────┘                 │║
║  │                                                                          │║
║  │   Characteristics:                                                       │║
║  │   • Latest models available first                                        │║
║  │   • Direct relationship with provider                                    │║
║  │   • May NOT have FedRAMP authorization                                  │║
║  │   • Data may leave US jurisdiction                                      │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    CLOUD PROVIDER WRAPPERS                              │║
║  │  (Access AI models through your existing cloud provider)                │║
║  │                                                                          │║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │║
║  │   │ Azure OpenAI │  │ AWS Bedrock  │  │  GCP Vertex  │                 │║
║  │   │              │  │              │  │              │                 │║
║  │   │ • GPT Models │  │ • Claude     │  │ • Gemini     │                 │║
║  │   │ • FedRAMP ✓  │  │ • Llama 3    │  │ • PaLM       │                 │║
║  │   │ • Gov Cloud  │  │ • Titan      │  │ • Codey      │                 │║
║  │   │ • HIPAA ✓    │  │ • Mistral    │  │ • FedRAMP ✓  │                 │║
║  │   │              │  │ • FedRAMP ✓  │  │              │                 │║
║  │   └──────────────┘  └──────────────┘  └──────────────┘                 │║
║  │                                                                          │║
║  │   Characteristics:                                                       │║
║  │   • Integrated with existing cloud contracts (important for govt!)      │║
║  │   • FedRAMP authorized options available                                │║
║  │   • May have older model versions                                       │║
║  │   • Consolidated billing through cloud provider                          │║
║  │   • Better enterprise features (IAM, VPC, logging)                      │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Provider Comparison Matrix

Understanding the capabilities and limitations of each provider helps you make informed decisions:

| Feature | OpenAI Direct | Anthropic Direct | Google Direct | Azure OpenAI | AWS Bedrock | GCP Vertex |
|:--------|:-------------:|:----------------:|:-------------:|:------------:|:-----------:|:----------:|
| **FedRAMP High** | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| **FedRAMP Moderate** | ⏳ | ⏳ | ✅ | ✅ | ✅ | ✅ |
| **GovCloud Available** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **IL4/IL5 Support** | ❌ | ❌ | ❌ | ✅ | ✅ | ⏳ |
| **SSO/SAML** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Data Residency Control** | Limited | Limited | Config | Full | Full | Full |
| **VPC/Private Endpoints** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Customer-Managed Keys** | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| **Audit Logging** | Basic | Basic | Full | Full | Full | Full |
| **SLA** | 99.9% | 99.9% | 99.9% | 99.95% | 99.9% | 99.9% |
| **Latest Models** | ✅ First | ✅ First | ✅ First | Delayed | Delayed | ✅ First |

### Decision Framework for Federal Use

```
╔══════════════════════════════════════════════════════════════════════════════╗
║              WHICH API SHOULD I USE? (Federal Decision Tree)                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  START: What is your data classification?                                    ║
║         │                                                                    ║
║         ├─► CUI/FOUO/Sensitive ────────────► Use FedRAMP High               ║
║         │                                     • Azure OpenAI GovCloud        ║
║         │                                     • AWS Bedrock GovCloud         ║
║         │                                                                    ║
║         ├─► Internal/Non-sensitive ────────► Use FedRAMP Moderate           ║
║         │                                     • Azure OpenAI Commercial      ║
║         │                                     • AWS Bedrock Commercial       ║
║         │                                     • GCP Vertex AI                ║
║         │                                                                    ║
║         └─► Public Information Only ───────► Any Provider (with approval)   ║
║                                               • Consider direct APIs         ║
║                                               • Still follow agency policy   ║
║                                                                              ║
║  ADDITIONAL CONSIDERATIONS:                                                  ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  • Do you have existing cloud contracts? → Use that provider's wrapper      ║
║  • Need latest model features? → May need direct API + approval             ║
║  • High volume? → Cloud wrappers often have better enterprise pricing       ║
║  • Need audit trail? → Cloud wrappers integrate with CloudTrail/Monitor     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 3. OpenAI API Deep Dive

OpenAI's API is one of the most widely used LLM APIs and often serves as a reference implementation. Understanding it thoroughly will help you work with other APIs as well.

### Understanding OpenAI's API Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       OPENAI API ARCHITECTURE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ENDPOINT STRUCTURE                                                          ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Base URL: https://api.openai.com/v1                                        ║
║                                                                              ║
║  /chat/completions      │ Main conversation endpoint                        ║
║  /embeddings            │ Text embeddings for semantic search               ║
║  /images/generations    │ DALL-E image generation                           ║
║  /audio/transcriptions  │ Whisper speech-to-text                            ║
║  /audio/speech          │ Text-to-speech                                    ║
║  /models                │ List available models                             ║
║  /files                 │ File upload/management                            ║
║  /assistants            │ Assistants API (stateful conversations)           ║
║  /threads               │ Conversation threads for Assistants               ║
║                                                                              ║
║  MODEL TIERS                                                                 ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Flagship:    GPT-4o, GPT-4 Turbo    │ Best quality, higher cost            ║
║  Reasoning:   o1, o1-mini, o3        │ Complex reasoning, very high cost    ║
║  Efficient:   GPT-4o-mini            │ Good quality, lower cost             ║
║  Legacy:      GPT-3.5-turbo          │ Fastest, lowest cost                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Authentication Setup

OpenAI uses API keys for authentication. Here's how to set this up securely:

```python
"""
OpenAI Authentication - Secure Setup Guide

NEVER hardcode API keys in your code. Always use one of these methods:
1. Environment variables (recommended for most cases)
2. Secret management services (recommended for production)
3. Configuration files with proper permissions (development only)
"""

import os
from openai import OpenAI

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 1: Environment Variable (Recommended)
# ═══════════════════════════════════════════════════════════════════════════
# Set in your environment:
#   export OPENAI_API_KEY="sk-..."
#   export OPENAI_ORG_ID="org-..."  # Optional, for organization accounts

# The client automatically reads from environment variables
client = OpenAI()  # Reads OPENAI_API_KEY automatically

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 2: Explicit Configuration (When you need control)
# ═══════════════════════════════════════════════════════════════════════════
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # Still from env, but explicit
    organization=os.environ.get("OPENAI_ORG_ID"),  # For org accounts
    timeout=60.0,      # Request timeout in seconds
    max_retries=3,     # Automatic retries on transient errors
)

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 3: Secret Manager Integration (Production)
# ═══════════════════════════════════════════════════════════════════════════
# Example with AWS Secrets Manager
import boto3
from botocore.exceptions import ClientError

def get_openai_key_from_aws():
    """Retrieve OpenAI API key from AWS Secrets Manager."""
    secret_name = "federal-app/openai-api-key"
    region_name = "us-gov-west-1"  # GovCloud region

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise Exception(f"Failed to retrieve secret: {e}")

# Use in production
# client = OpenAI(api_key=get_openai_key_from_aws())
```

### Chat Completions: The Core Endpoint

The `/chat/completions` endpoint is the most important endpoint. Let's understand every parameter:

```python
from openai import OpenAI

client = OpenAI()

# ═══════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE CHAT COMPLETION EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════

response = client.chat.completions.create(
    # ─────────────────────────────────────────────────────────────────────
    # MODEL SELECTION
    # ─────────────────────────────────────────────────────────────────────
    model="gpt-4o",
    # Options:
    # • "gpt-4o"        - Latest flagship, best for complex tasks ($2.50/$10 per 1M tokens)
    # • "gpt-4o-mini"   - Cost-effective, good for most tasks ($0.15/$0.60 per 1M tokens)
    # • "gpt-4-turbo"   - Previous flagship, 128K context
    # • "o1"            - Reasoning model, for complex logic (very expensive)
    # • "gpt-3.5-turbo" - Legacy, fastest and cheapest

    # ─────────────────────────────────────────────────────────────────────
    # MESSAGES: The conversation history
    # ─────────────────────────────────────────────────────────────────────
    messages=[
        # SYSTEM MESSAGE: Sets the AI's behavior and persona
        # This is crucial for federal applications - define compliance requirements here
        {
            "role": "system",
            "content": """You are a federal compliance expert assistant.

            Guidelines:
            - Always cite specific regulations (FAR, DFARS, NIST, OMB)
            - Never provide legal advice; recommend consulting legal counsel
            - Flag any potential ITAR/EAR concerns
            - Use formal, professional language appropriate for government communication
            - If unsure, say so rather than speculating
            """
        },

        # USER MESSAGE: The human's input
        {
            "role": "user",
            "content": "What are the FedRAMP authorization levels and their requirements?"
        },

        # ASSISTANT MESSAGE: Previous AI responses (for context)
        # Include these for multi-turn conversations
        # {
        #     "role": "assistant",
        #     "content": "Previous response here..."
        # },
    ],

    # ─────────────────────────────────────────────────────────────────────
    # GENERATION PARAMETERS
    # ─────────────────────────────────────────────────────────────────────

    # TEMPERATURE: Controls randomness/creativity (0.0 to 2.0)
    # • 0.0 = Deterministic, always same output for same input
    # • 0.3-0.5 = Low creativity, good for factual/compliance work
    # • 0.7 = Balanced (default)
    # • 1.0+ = High creativity, good for brainstorming
    # For federal compliance work, use 0.0-0.3 for accuracy
    temperature=0.3,

    # MAX_TOKENS: Maximum response length
    # • 1 token ≈ 4 characters in English
    # • Set based on expected response length
    # • Higher values don't force longer responses
    # • Important for cost control
    max_tokens=2000,

    # TOP_P: Nucleus sampling (alternative to temperature)
    # • 1.0 = Consider all tokens (default)
    # • 0.9 = Consider tokens comprising top 90% probability
    # • Lower values = more focused responses
    # Generally, adjust temperature OR top_p, not both
    top_p=1.0,

    # FREQUENCY_PENALTY: Reduces word repetition (-2.0 to 2.0)
    # • 0.0 = No penalty (default)
    # • 0.5 = Mild discouragement of repetition
    # • 1.0+ = Strong discouragement
    # Useful for longer documents
    frequency_penalty=0.0,

    # PRESENCE_PENALTY: Encourages new topics (-2.0 to 2.0)
    # • 0.0 = No penalty (default)
    # • 0.5 = Mild encouragement of new topics
    # Useful for brainstorming, less useful for focused Q&A
    presence_penalty=0.0,

    # STOP: Sequences that will stop generation
    # Useful for structured outputs
    stop=None,  # Example: stop=["END", "---"]

    # N: Number of completions to generate
    # Useful for getting multiple options
    # Note: You pay for all generated tokens
    n=1,

    # SEED: For reproducible outputs (when possible)
    # Same seed + same inputs = same outputs (mostly)
    # Useful for testing and debugging
    seed=42,

    # USER: Unique identifier for the end user
    # Helps OpenAI detect and prevent abuse
    # Use a hash, not PII
    user="user-abc123",

    # RESPONSE_FORMAT: Structure the output
    # • {"type": "text"} = Default, free-form text
    # • {"type": "json_object"} = Force valid JSON output
    response_format={"type": "text"},
)

# ═══════════════════════════════════════════════════════════════════════════
# PROCESSING THE RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

# The response object contains multiple fields:
print("=" * 60)
print("RESPONSE ANALYSIS")
print("=" * 60)

# Unique identifier for this completion
print(f"Completion ID: {response.id}")

# The actual response text
message = response.choices[0].message
print(f"\nRole: {message.role}")
print(f"\nContent:\n{message.content}")

# Why did generation stop?
# • "stop" = Natural end or hit stop sequence
# • "length" = Hit max_tokens limit (response may be truncated!)
# • "content_filter" = Content was filtered (important for compliance!)
# • "tool_calls" = Model wants to call a function
finish_reason = response.choices[0].finish_reason
print(f"\nFinish Reason: {finish_reason}")
if finish_reason == "length":
    print("⚠️  WARNING: Response was truncated! Consider increasing max_tokens.")
if finish_reason == "content_filter":
    print("⚠️  WARNING: Content was filtered by safety systems.")

# Token usage (critical for billing and monitoring)
usage = response.usage
print(f"\nToken Usage:")
print(f"  Input tokens:  {usage.prompt_tokens}")
print(f"  Output tokens: {usage.completion_tokens}")
print(f"  Total tokens:  {usage.total_tokens}")

# Calculate cost (GPT-4o pricing as of 2025)
input_cost = (usage.prompt_tokens / 1_000_000) * 2.50
output_cost = (usage.completion_tokens / 1_000_000) * 10.00
total_cost = input_cost + output_cost
print(f"\nEstimated Cost: ${total_cost:.6f}")
```

### Streaming Responses

For real-time user experiences, streaming is essential:

```python
from openai import OpenAI

client = OpenAI()

def stream_completion(prompt: str, system_prompt: str = None):
    """
    Stream a completion with real-time output.

    Streaming is crucial for user-facing applications because:
    1. Users see immediate feedback (better UX)
    2. Reduces perceived latency
    3. Allows users to stop generation if response is wrong
    4. Prevents HTTP timeout issues with long responses
    """

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    # Create a streaming response
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        stream=True,  # This enables streaming
        max_tokens=2000,
        temperature=0.3,
    )

    # Track tokens for cost calculation
    collected_content = []

    print("Assistant: ", end="", flush=True)

    # Process each chunk as it arrives
    for chunk in stream:
        # Each chunk contains a delta (incremental update)
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            collected_content.append(content)
            print(content, end="", flush=True)

        # Check if we've reached the end
        if chunk.choices[0].finish_reason:
            print(f"\n\n[Finished: {chunk.choices[0].finish_reason}]")

    return "".join(collected_content)

# Example usage
response = stream_completion(
    prompt="Explain NIST 800-53 security controls in detail.",
    system_prompt="You are a federal cybersecurity expert."
)
```

### Function Calling (Tool Use)

Function calling allows the model to interact with external systems:

```python
import json
from openai import OpenAI

client = OpenAI()

# ═══════════════════════════════════════════════════════════════════════════
# DEFINE TOOLS (Functions the model can call)
# ═══════════════════════════════════════════════════════════════════════════

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_regulations",
            "description": """Search the federal regulations database for specific
            requirements. Use this when the user asks about FAR, DFARS, NIST,
            or other federal regulations.""",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query for regulations"
                    },
                    "regulation_type": {
                        "type": "string",
                        "enum": ["FAR", "DFARS", "NIST", "OMB", "FISMA", "FedRAMP"],
                        "description": "The type of regulation to search"
                    },
                    "section": {
                        "type": "string",
                        "description": "Specific section number if known (e.g., '52.204-21')"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_contractor_status",
            "description": "Check a contractor's status in SAM.gov",
            "parameters": {
                "type": "object",
                "properties": {
                    "cage_code": {
                        "type": "string",
                        "description": "The contractor's CAGE code"
                    },
                    "uei": {
                        "type": "string",
                        "description": "The contractor's Unique Entity ID"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_small_business_threshold",
            "description": "Calculate if a business qualifies as small business for a given NAICS code",
            "parameters": {
                "type": "object",
                "properties": {
                    "naics_code": {
                        "type": "string",
                        "description": "The NAICS code for the industry"
                    },
                    "annual_revenue": {
                        "type": "number",
                        "description": "Annual revenue in dollars"
                    },
                    "employee_count": {
                        "type": "integer",
                        "description": "Number of employees"
                    }
                },
                "required": ["naics_code"]
            }
        }
    }
]

# ═══════════════════════════════════════════════════════════════════════════
# IMPLEMENT THE ACTUAL FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def search_regulations(query: str, regulation_type: str = None, section: str = None) -> dict:
    """
    Simulated regulation search. In production, this would query
    a real database or API like regulations.gov
    """
    # This is a simulation - replace with real implementation
    return {
        "results": [
            {
                "regulation": regulation_type or "FAR",
                "section": section or "52.204-21",
                "title": "Basic Safeguarding of Covered Contractor Information Systems",
                "summary": "Requires contractors to apply basic safeguarding requirements..."
            }
        ],
        "total_results": 1
    }

def check_contractor_status(cage_code: str = None, uei: str = None) -> dict:
    """Simulated SAM.gov lookup"""
    return {
        "status": "Active",
        "expiration_date": "2025-12-31",
        "exclusions": None
    }

def calculate_small_business_threshold(naics_code: str, annual_revenue: float = None,
                                       employee_count: int = None) -> dict:
    """Simulated SBA threshold calculation"""
    return {
        "naics_code": naics_code,
        "threshold_type": "revenue",
        "threshold_value": 30000000,
        "qualifies": annual_revenue < 30000000 if annual_revenue else "Need revenue data"
    }

# Map function names to implementations
function_map = {
    "search_regulations": search_regulations,
    "check_contractor_status": check_contractor_status,
    "calculate_small_business_threshold": calculate_small_business_threshold
}

# ═══════════════════════════════════════════════════════════════════════════
# HANDLE THE CONVERSATION WITH TOOL CALLS
# ═══════════════════════════════════════════════════════════════════════════

def chat_with_tools(user_message: str):
    """
    Complete conversation flow with tool calling.

    The flow works like this:
    1. User sends message
    2. Model decides if it needs to call a tool
    3. If yes, model returns tool_calls instead of content
    4. We execute the tools and send results back
    5. Model generates final response with tool results
    """

    messages = [
        {
            "role": "system",
            "content": """You are a federal contracting assistant. Use the available
            tools to look up regulations, check contractor status, and calculate
            thresholds. Always cite your sources."""
        },
        {"role": "user", "content": user_message}
    ]

    # First API call - model decides what to do
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # "auto" = model decides, "none" = never use tools
                             # {"type": "function", "function": {"name": "..."}} = force specific tool
    )

    assistant_message = response.choices[0].message

    # Check if the model wants to call tools
    if assistant_message.tool_calls:
        print(f"Model is calling {len(assistant_message.tool_calls)} tool(s)...")

        # Add the assistant's message (with tool calls) to history
        messages.append(assistant_message)

        # Execute each tool call
        for tool_call in assistant_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"  Calling: {function_name}")
            print(f"  Arguments: {function_args}")

            # Execute the function
            if function_name in function_map:
                result = function_map[function_name](**function_args)
            else:
                result = {"error": f"Unknown function: {function_name}"}

            print(f"  Result: {result}")

            # Add tool result to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

        # Second API call - model generates response with tool results
        final_response = client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            tools=tools,
        )

        return final_response.choices[0].message.content

    else:
        # No tools needed, return direct response
        return assistant_message.content

# Example usage
result = chat_with_tools(
    "What are the cybersecurity requirements in FAR 52.204-21?"
)
print("\n" + "=" * 60)
print("FINAL RESPONSE:")
print("=" * 60)
print(result)
```

---

## 4. Anthropic Claude API Deep Dive

Anthropic's Claude API has a different philosophy and structure from OpenAI. Understanding these differences is important for choosing the right API and implementing correctly.

### Claude API Philosophy

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CLAUDE API DESIGN PHILOSOPHY                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  KEY DIFFERENCES FROM OPENAI:                                                ║
║  ───────────────────────────────────────────────────────────────────────    ║
║                                                                              ║
║  1. SYSTEM PROMPT IS SEPARATE                                                ║
║     • OpenAI: System prompt is a message with role="system"                 ║
║     • Claude: System prompt is a top-level parameter                         ║
║     • Why: Claude treats system prompts as special instructions              ║
║                                                                              ║
║  2. CONTENT CAN BE MULTI-MODAL                                               ║
║     • OpenAI: Content is usually a string                                    ║
║     • Claude: Content is always an array of content blocks                   ║
║     • Why: Native support for images, tool results, etc.                     ║
║                                                                              ║
║  3. TOKEN COUNTING IS EXPLICIT                                               ║
║     • OpenAI: Reports total_tokens                                          ║
║     • Claude: Separately reports input_tokens and output_tokens              ║
║     • Why: Different pricing for input vs output                             ║
║                                                                              ║
║  4. NO FUNCTION "CALLING" - IT'S TOOL "USE"                                 ║
║     • OpenAI: Model "calls" functions                                        ║
║     • Claude: Model "uses" tools                                             ║
║     • Same concept, different terminology and schema                         ║
║                                                                              ║
║  5. STRONGER SAFETY GUARDRAILS                                               ║
║     • Claude is trained with Constitutional AI principles                    ║
║     • May refuse more requests than other models                             ║
║     • Better for federal applications requiring safety                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Authentication Setup

```python
import anthropic
import os

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 1: Environment Variable (Recommended)
# ═══════════════════════════════════════════════════════════════════════════
# Set: export ANTHROPIC_API_KEY="sk-ant-..."

client = anthropic.Anthropic()  # Reads from ANTHROPIC_API_KEY

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 2: Explicit Configuration
# ═══════════════════════════════════════════════════════════════════════════
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY"),
    timeout=60.0,           # Request timeout
    max_retries=3,          # Automatic retry count
    default_headers={       # Custom headers for all requests
        "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"  # Enable features
    }
)

# ═══════════════════════════════════════════════════════════════════════════
# METHOD 3: For AWS Bedrock (Federal Recommended)
# ═══════════════════════════════════════════════════════════════════════════
from anthropic import AnthropicBedrock

bedrock_client = AnthropicBedrock(
    aws_region="us-gov-west-1",  # GovCloud region
    # Uses your AWS credentials automatically
)
```

### Messages API: The Core Endpoint

```python
import anthropic

client = anthropic.Anthropic()

# ═══════════════════════════════════════════════════════════════════════════
# COMPREHENSIVE CLAUDE MESSAGE EXAMPLE
# ═══════════════════════════════════════════════════════════════════════════

message = client.messages.create(
    # ─────────────────────────────────────────────────────────────────────
    # MODEL SELECTION
    # ─────────────────────────────────────────────────────────────────────
    model="claude-sonnet-4-20250514",
    # Options:
    # • "claude-sonnet-4-20250514"   - Latest, best balance of speed/quality
    # • "claude-3-5-sonnet-20241022" - Previous Sonnet, excellent for most tasks
    # • "claude-3-opus-20240229"     - Most capable, slower, expensive
    # • "claude-3-haiku-20240307"    - Fastest, cheapest, good for simple tasks

    # ─────────────────────────────────────────────────────────────────────
    # MAX TOKENS (Required!)
    # ─────────────────────────────────────────────────────────────────────
    # Unlike OpenAI, this is REQUIRED in Claude API
    max_tokens=4096,

    # ─────────────────────────────────────────────────────────────────────
    # SYSTEM PROMPT (Top-level, not in messages!)
    # ─────────────────────────────────────────────────────────────────────
    system="""You are a federal compliance analyst specializing in cybersecurity
    frameworks. You help government contractors understand and implement
    NIST, FedRAMP, and CMMC requirements.

    Guidelines:
    - Cite specific control numbers and frameworks
    - Distinguish between requirements and recommendations
    - Note when requirements vary by impact level (Low/Moderate/High)
    - Recommend consulting with assessors for official guidance
    """,

    # ─────────────────────────────────────────────────────────────────────
    # MESSAGES (Conversation history)
    # ─────────────────────────────────────────────────────────────────────
    messages=[
        {
            "role": "user",
            "content": "What's the difference between FedRAMP Moderate and High?"
        }
    ],

    # ─────────────────────────────────────────────────────────────────────
    # GENERATION PARAMETERS
    # ─────────────────────────────────────────────────────────────────────

    # TEMPERATURE (0.0 to 1.0)
    # Claude's default is 1.0, but for compliance work use lower
    temperature=0.3,

    # TOP_P (0.0 to 1.0)
    # Nucleus sampling - usually keep at default
    top_p=1.0,

    # TOP_K (integer)
    # Only sample from top K tokens - Claude-specific parameter
    # Lower values = more focused responses
    top_k=40,

    # STOP SEQUENCES
    # Custom strings that stop generation
    stop_sequences=["END_RESPONSE", "---"],

    # METADATA
    # For tracking and analytics
    metadata={
        "user_id": "analyst-123",  # Your internal user tracking
    }
)

# ═══════════════════════════════════════════════════════════════════════════
# PROCESSING THE RESPONSE
# ═══════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("CLAUDE RESPONSE ANALYSIS")
print("=" * 60)

# Response ID
print(f"Message ID: {message.id}")

# Model actually used (may differ from requested if version changes)
print(f"Model: {message.model}")

# Stop reason
# • "end_turn" = Natural completion
# • "max_tokens" = Hit token limit (may be truncated!)
# • "stop_sequence" = Hit a stop sequence
# • "tool_use" = Model wants to use a tool
print(f"Stop Reason: {message.stop_reason}")

# Content is an array of content blocks
for block in message.content:
    if block.type == "text":
        print(f"\nResponse:\n{block.text}")
    elif block.type == "tool_use":
        print(f"\nTool Use: {block.name}")
        print(f"Input: {block.input}")

# Token usage (input and output priced differently!)
print(f"\nToken Usage:")
print(f"  Input tokens:  {message.usage.input_tokens}")
print(f"  Output tokens: {message.usage.output_tokens}")

# Calculate cost (Claude 3.5 Sonnet pricing)
input_cost = (message.usage.input_tokens / 1_000_000) * 3.00
output_cost = (message.usage.output_tokens / 1_000_000) * 15.00
print(f"\nEstimated Cost: ${input_cost + output_cost:.6f}")
```

### Streaming with Claude

```python
import anthropic

client = anthropic.Anthropic()

def stream_claude_response(prompt: str, system: str = None):
    """
    Stream Claude responses with proper event handling.

    Claude uses Server-Sent Events (SSE) with specific event types:
    - message_start: Beginning of response
    - content_block_start: Start of a content block
    - content_block_delta: Incremental text
    - content_block_stop: End of content block
    - message_delta: Usage stats update
    - message_stop: End of response
    """

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system=system or "You are a helpful assistant.",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    ) as stream:

        print("Assistant: ", end="", flush=True)

        for text in stream.text_stream:
            print(text, end="", flush=True)

        print("\n")

        # Get final message with usage stats
        final_message = stream.get_final_message()
        print(f"Input tokens: {final_message.usage.input_tokens}")
        print(f"Output tokens: {final_message.usage.output_tokens}")

# Alternative: Manual event handling for more control
def stream_with_events(prompt: str):
    """Handle each SSE event type explicitly."""

    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:

        for event in stream:
            if event.type == "message_start":
                print(f"Starting response (ID: {event.message.id})")

            elif event.type == "content_block_start":
                print(f"Content block {event.index} starting...")

            elif event.type == "content_block_delta":
                if event.delta.type == "text_delta":
                    print(event.delta.text, end="", flush=True)

            elif event.type == "content_block_stop":
                print(f"\nContent block {event.index} complete")

            elif event.type == "message_delta":
                print(f"\nStop reason: {event.delta.stop_reason}")
                print(f"Output tokens: {event.usage.output_tokens}")

            elif event.type == "message_stop":
                print("Response complete")
```

### Tool Use with Claude

Claude's tool use is similar to OpenAI's function calling but with some differences:

```python
import anthropic
import json

client = anthropic.Anthropic()

# ═══════════════════════════════════════════════════════════════════════════
# DEFINE TOOLS
# ═══════════════════════════════════════════════════════════════════════════

tools = [
    {
        "name": "get_security_control",
        "description": """Retrieve details about a NIST 800-53 security control.
        Use this when the user asks about specific controls like AC-2, AU-3, etc.""",
        "input_schema": {
            "type": "object",
            "properties": {
                "control_id": {
                    "type": "string",
                    "description": "The control ID (e.g., 'AC-2', 'AU-3', 'SC-7')"
                },
                "baseline": {
                    "type": "string",
                    "enum": ["low", "moderate", "high"],
                    "description": "The security baseline to check against"
                },
                "include_enhancements": {
                    "type": "boolean",
                    "description": "Whether to include control enhancements"
                }
            },
            "required": ["control_id"]
        }
    },
    {
        "name": "search_incidents",
        "description": "Search for cybersecurity incidents in the database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                },
                "severity": {
                    "type": "string",
                    "enum": ["low", "medium", "high", "critical"],
                    "description": "Filter by severity"
                },
                "date_range_days": {
                    "type": "integer",
                    "description": "Number of days to search back"
                }
            },
            "required": ["query"]
        }
    }
]

# ═══════════════════════════════════════════════════════════════════════════
# IMPLEMENT TOOLS
# ═══════════════════════════════════════════════════════════════════════════

def get_security_control(control_id: str, baseline: str = "moderate",
                        include_enhancements: bool = False) -> dict:
    """Simulated NIST control lookup."""
    controls = {
        "AC-2": {
            "title": "Account Management",
            "family": "Access Control",
            "description": "Manage information system accounts...",
            "baseline_allocation": {
                "low": "AC-2",
                "moderate": "AC-2 (1)(2)(3)(4)",
                "high": "AC-2 (1)(2)(3)(4)(5)(11)(12)(13)"
            }
        }
    }
    return controls.get(control_id.upper(), {"error": "Control not found"})

def search_incidents(query: str, severity: str = None,
                    date_range_days: int = 30) -> dict:
    """Simulated incident search."""
    return {
        "results": [
            {"id": "INC-001", "title": "Phishing attempt detected", "severity": "medium"}
        ],
        "total": 1
    }

tool_functions = {
    "get_security_control": get_security_control,
    "search_incidents": search_incidents
}

# ═══════════════════════════════════════════════════════════════════════════
# CONVERSATION WITH TOOL USE
# ═══════════════════════════════════════════════════════════════════════════

def chat_with_claude_tools(user_message: str):
    """Complete conversation with Claude tool use."""

    messages = [{"role": "user", "content": user_message}]

    # First call
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        system="You are a federal cybersecurity analyst. Use the available tools to provide accurate information.",
        messages=messages,
        tools=tools,
    )

    # Check if Claude wants to use tools
    while response.stop_reason == "tool_use":
        # Find tool use blocks
        tool_use_blocks = [b for b in response.content if b.type == "tool_use"]

        # Add assistant's response to history
        messages.append({"role": "assistant", "content": response.content})

        # Execute tools and collect results
        tool_results = []
        for tool_use in tool_use_blocks:
            print(f"Using tool: {tool_use.name}")
            print(f"Input: {tool_use.input}")

            # Execute the tool
            func = tool_functions.get(tool_use.name)
            if func:
                result = func(**tool_use.input)
            else:
                result = {"error": f"Unknown tool: {tool_use.name}"}

            print(f"Result: {result}\n")

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": json.dumps(result)
            })

        # Add tool results to messages
        messages.append({"role": "user", "content": tool_results})

        # Get next response
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system="You are a federal cybersecurity analyst.",
            messages=messages,
            tools=tools,
        )

    # Extract final text response
    text_blocks = [b for b in response.content if b.type == "text"]
    return text_blocks[0].text if text_blocks else ""

# Example
result = chat_with_claude_tools("Tell me about NIST control AC-2")
print("Final Response:")
print(result)
```

### Vision (Image Analysis) with Claude

```python
import anthropic
import base64
from pathlib import Path

client = anthropic.Anthropic()

def analyze_image(image_path: str, question: str) -> str:
    """
    Analyze an image using Claude's vision capabilities.

    This is useful for federal applications like:
    - Analyzing system architecture diagrams
    - Reviewing network topology images
    - Examining screenshots for compliance evidence
    - Processing scanned documents
    """

    # Read and encode the image
    image_path = Path(image_path)

    # Determine media type
    suffix_to_media = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp"
    }
    media_type = suffix_to_media.get(image_path.suffix.lower(), "image/png")

    # Read and base64 encode
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Create message with image
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text

# Example: Analyze a system architecture diagram
# result = analyze_image(
#     "architecture_diagram.png",
#     "Review this system architecture for security concerns. Identify any potential vulnerabilities or compliance issues."
# )

# You can also use URLs for publicly accessible images
def analyze_image_url(url: str, question: str) -> str:
    """Analyze an image from a URL."""

    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": url
                        }
                    },
                    {
                        "type": "text",
                        "text": question
                    }
                ]
            }
        ]
    )

    return message.content[0].text
```

---

## 5. Google AI API Deep Dive

Google's Gemini API offers a different approach with strong multimodal capabilities.

### Setup and Authentication

```python
import google.generativeai as genai
import os

# ═══════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════

# Method 1: API Key (for Google AI Studio)
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Method 2: For Vertex AI (GCP - Federal recommended)
# Uses Application Default Credentials or service account
# from google.cloud import aiplatform
# aiplatform.init(project="your-project", location="us-central1")

# ═══════════════════════════════════════════════════════════════════════════
# MODEL INITIALIZATION
# ═══════════════════════════════════════════════════════════════════════════

# Available models:
# • gemini-2.0-flash-exp  - Latest, fastest
# • gemini-1.5-pro        - Best quality
# • gemini-1.5-flash      - Fast, cost-effective
# • gemini-1.0-pro        - Previous generation

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    system_instruction="""You are a federal technology advisor specializing
    in cloud migration and modernization for government agencies.""",
    generation_config=genai.GenerationConfig(
        temperature=0.3,
        top_p=0.95,
        top_k=40,
        max_output_tokens=4096,
    ),
    safety_settings={
        "HARM_CATEGORY_HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
)
```

### Generate Content

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# ═══════════════════════════════════════════════════════════════════════════
# SIMPLE GENERATION
# ═══════════════════════════════════════════════════════════════════════════

response = model.generate_content(
    "Explain the Cloud Smart strategy for federal agencies.",
    generation_config=genai.GenerationConfig(
        temperature=0.3,
        max_output_tokens=2048,
    )
)

print(response.text)

# Check safety ratings
for rating in response.candidates[0].safety_ratings:
    print(f"{rating.category}: {rating.probability}")

# ═══════════════════════════════════════════════════════════════════════════
# STREAMING GENERATION
# ═══════════════════════════════════════════════════════════════════════════

response = model.generate_content(
    "Describe the steps to achieve FedRAMP authorization.",
    stream=True
)

for chunk in response:
    print(chunk.text, end="", flush=True)
```

### Chat Sessions (Multi-turn Conversations)

```python
import google.generativeai as genai

model = genai.GenerativeModel("gemini-1.5-pro")

# Start a chat session
chat = model.start_chat(history=[])

# First turn
response = chat.send_message("What is FedRAMP?")
print(f"Assistant: {response.text}\n")

# Second turn (context is maintained)
response = chat.send_message("What are the different authorization levels?")
print(f"Assistant: {response.text}\n")

# Third turn
response = chat.send_message("Which level is required for classified data?")
print(f"Assistant: {response.text}\n")

# Access conversation history
print("\n--- Conversation History ---")
for message in chat.history:
    role = message.role
    text = message.parts[0].text[:100] + "..." if len(message.parts[0].text) > 100 else message.parts[0].text
    print(f"{role}: {text}")
```

### Function Calling with Gemini

```python
import google.generativeai as genai

# Define functions
def get_agency_budget(agency_name: str, fiscal_year: int) -> dict:
    """Get IT budget information for a federal agency."""
    # Simulated data
    budgets = {
        "DOD": {"fy2024": 46000000000, "fy2025": 48000000000},
        "DHS": {"fy2024": 8500000000, "fy2025": 9000000000},
    }
    agency_data = budgets.get(agency_name.upper(), {})
    return {
        "agency": agency_name,
        "fiscal_year": fiscal_year,
        "it_budget": agency_data.get(f"fy{fiscal_year}", "Not available")
    }

# Create model with function declarations
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    tools=[{
        "function_declarations": [{
            "name": "get_agency_budget",
            "description": "Get IT budget information for a federal agency",
            "parameters": {
                "type": "object",
                "properties": {
                    "agency_name": {
                        "type": "string",
                        "description": "Name or acronym of the federal agency (e.g., DOD, DHS)"
                    },
                    "fiscal_year": {
                        "type": "integer",
                        "description": "The fiscal year (e.g., 2024, 2025)"
                    }
                },
                "required": ["agency_name", "fiscal_year"]
            }
        }]
    }]
)

# Start chat
chat = model.start_chat()
response = chat.send_message("What's the IT budget for DOD in FY2025?")

# Check if model wants to call a function
if response.candidates[0].content.parts[0].function_call:
    fc = response.candidates[0].content.parts[0].function_call
    print(f"Function call: {fc.name}")
    print(f"Arguments: {dict(fc.args)}")

    # Execute the function
    result = get_agency_budget(**dict(fc.args))

    # Send result back
    response = chat.send_message(
        genai.protos.Content(
            parts=[genai.protos.Part(
                function_response=genai.protos.FunctionResponse(
                    name=fc.name,
                    response={"result": result}
                )
            )]
        )
    )
    print(f"Final response: {response.text}")
```

---

## 6. Azure OpenAI Service

Azure OpenAI is the **recommended choice for most federal applications** because it offers OpenAI models within Azure's FedRAMP-authorized infrastructure.

### Understanding Azure OpenAI Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    AZURE OPENAI ARCHITECTURE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  KEY DIFFERENCE: Deployments vs Models                                       ║
║  ───────────────────────────────────────────────────────────────────────    ║
║                                                                              ║
║  OpenAI Direct:                                                              ║
║    client.chat.completions.create(model="gpt-4o")                           ║
║                                            │                                 ║
║                                            └── Model name directly          ║
║                                                                              ║
║  Azure OpenAI:                                                               ║
║    client.chat.completions.create(model="my-gpt4-deployment")               ║
║                                            │                                 ║
║                                            └── Deployment name you created  ║
║                                                                              ║
║  WHY? Azure requires you to "deploy" a model before using it:               ║
║  1. Go to Azure Portal                                                       ║
║  2. Create Azure OpenAI resource                                            ║
║  3. Create a deployment (choose model + give it a name)                     ║
║  4. Use deployment name in API calls                                        ║
║                                                                              ║
║  BENEFITS:                                                                   ║
║  • Control which models are available                                        ║
║  • Set quotas per deployment                                                ║
║  • Version control (pin to specific model versions)                         ║
║  • Cost allocation to different deployments                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Setup and Authentication

```python
from openai import AzureOpenAI
import os

# ═══════════════════════════════════════════════════════════════════════════
# AZURE COMMERCIAL
# ═══════════════════════════════════════════════════════════════════════════

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",  # API version (update periodically)
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],  # e.g., https://your-resource.openai.azure.com
)

# ═══════════════════════════════════════════════════════════════════════════
# AZURE GOVERNMENT (FedRAMP High)
# ═══════════════════════════════════════════════════════════════════════════

gov_client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_GOV_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://your-resource.openai.azure.us",  # Note: .azure.us
)

# ═══════════════════════════════════════════════════════════════════════════
# USING AZURE ACTIVE DIRECTORY (Recommended for production)
# ═══════════════════════════════════════════════════════════════════════════

from azure.identity import DefaultAzureCredential, get_bearer_token_provider

# This uses your Azure AD credentials
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(),
    "https://cognitiveservices.azure.com/.default"
)

client_with_aad = AzureOpenAI(
    azure_ad_token_provider=token_provider,
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)
```

### Using Azure OpenAI

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
)

# ═══════════════════════════════════════════════════════════════════════════
# CHAT COMPLETION
# ═══════════════════════════════════════════════════════════════════════════

response = client.chat.completions.create(
    model="gpt-4o-deployment",  # YOUR deployment name, not the model name!
    messages=[
        {
            "role": "system",
            "content": "You are a federal acquisition specialist."
        },
        {
            "role": "user",
            "content": "What is the simplified acquisition threshold?"
        }
    ],
    temperature=0.3,
    max_tokens=1000,
)

print(response.choices[0].message.content)

# ═══════════════════════════════════════════════════════════════════════════
# STREAMING
# ═══════════════════════════════════════════════════════════════════════════

stream = client.chat.completions.create(
    model="gpt-4o-deployment",
    messages=[{"role": "user", "content": "Explain the FAR Part 15 process"}],
    stream=True,
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)

# ═══════════════════════════════════════════════════════════════════════════
# EMBEDDINGS
# ═══════════════════════════════════════════════════════════════════════════

embedding_response = client.embeddings.create(
    model="text-embedding-ada-deployment",  # Your embedding deployment name
    input="Federal acquisition regulations"
)

embedding_vector = embedding_response.data[0].embedding
print(f"Embedding dimensions: {len(embedding_vector)}")
```

### Azure-Specific Features

```python
# ═══════════════════════════════════════════════════════════════════════════
# CONTENT FILTERING (Azure-specific)
# ═══════════════════════════════════════════════════════════════════════════

"""
Azure OpenAI has additional content filtering beyond OpenAI's:
- Hate
- Violence
- Self-harm
- Sexual content

Responses include content filter results:
"""

response = client.chat.completions.create(
    model="gpt-4o-deployment",
    messages=[{"role": "user", "content": "Your message here"}]
)

# Check content filter results (if available)
if hasattr(response.choices[0], 'content_filter_results'):
    filters = response.choices[0].content_filter_results
    print(f"Hate: {filters.hate.filtered}")
    print(f"Violence: {filters.violence.filtered}")

# ═══════════════════════════════════════════════════════════════════════════
# LIST DEPLOYMENTS
# ═══════════════════════════════════════════════════════════════════════════

# You can list deployments via Azure Management API or Azure CLI:
# az cognitiveservices account deployment list --name your-resource --resource-group your-rg
```

---

## 7. AWS Bedrock

AWS Bedrock provides access to multiple model providers (including Claude, Llama, and Amazon's Titan) through a unified API within AWS's FedRAMP-authorized infrastructure.

### Understanding Bedrock Architecture

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        AWS BEDROCK ARCHITECTURE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  AVAILABLE MODEL FAMILIES                                                    ║
║  ───────────────────────────────────────────────────────────────────────    ║
║                                                                              ║
║  Anthropic Claude:                                                           ║
║  • anthropic.claude-3-5-sonnet-20241022-v2:0                                ║
║  • anthropic.claude-3-opus-20240229-v1:0                                    ║
║  • anthropic.claude-3-haiku-20240307-v1:0                                   ║
║                                                                              ║
║  Meta Llama:                                                                 ║
║  • meta.llama3-70b-instruct-v1:0                                            ║
║  • meta.llama3-8b-instruct-v1:0                                             ║
║                                                                              ║
║  Amazon Titan:                                                               ║
║  • amazon.titan-text-premier-v1:0                                           ║
║  • amazon.titan-embed-text-v2:0                                             ║
║                                                                              ║
║  Mistral:                                                                    ║
║  • mistral.mistral-large-2407-v1:0                                          ║
║  • mistral.mistral-small-2402-v1:0                                          ║
║                                                                              ║
║  REGIONAL AVAILABILITY                                                       ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Commercial: us-east-1, us-west-2, eu-west-1, etc.                          ║
║  GovCloud:   us-gov-west-1                                                  ║
║  Note: Not all models available in all regions!                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Setup and Authentication

```python
import boto3
import json

# ═══════════════════════════════════════════════════════════════════════════
# BASIC SETUP (Commercial)
# ═══════════════════════════════════════════════════════════════════════════

bedrock_runtime = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)

# ═══════════════════════════════════════════════════════════════════════════
# GOVCLOUD SETUP
# ═══════════════════════════════════════════════════════════════════════════

# For GovCloud, you need credentials configured for the GovCloud partition
bedrock_gov = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-gov-west-1'
)

# ═══════════════════════════════════════════════════════════════════════════
# WITH EXPLICIT CREDENTIALS (Not recommended - use IAM roles)
# ═══════════════════════════════════════════════════════════════════════════

session = boto3.Session(
    aws_access_key_id='AKIA...',
    aws_secret_access_key='...',
    region_name='us-east-1'
)
bedrock_runtime = session.client('bedrock-runtime')
```

### Invoking Models

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# ═══════════════════════════════════════════════════════════════════════════
# CLAUDE ON BEDROCK
# ═══════════════════════════════════════════════════════════════════════════

def invoke_claude(prompt: str, system: str = None, max_tokens: int = 1024):
    """Invoke Claude via Bedrock."""

    messages = [{"role": "user", "content": prompt}]

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "messages": messages,
        "temperature": 0.3,
    }

    if system:
        body["system"] = system

    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

# Usage
response = invoke_claude(
    prompt="What are the key requirements of CMMC Level 2?",
    system="You are a federal cybersecurity compliance expert."
)
print(response)

# ═══════════════════════════════════════════════════════════════════════════
# LLAMA ON BEDROCK
# ═══════════════════════════════════════════════════════════════════════════

def invoke_llama(prompt: str, max_tokens: int = 1024):
    """Invoke Llama via Bedrock."""

    body = {
        "prompt": f"<s>[INST] {prompt} [/INST]",
        "max_gen_len": max_tokens,
        "temperature": 0.3,
        "top_p": 0.9,
    }

    response = bedrock.invoke_model(
        modelId="meta.llama3-70b-instruct-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["generation"]

# ═══════════════════════════════════════════════════════════════════════════
# TITAN ON BEDROCK
# ═══════════════════════════════════════════════════════════════════════════

def invoke_titan(prompt: str, max_tokens: int = 1024):
    """Invoke Amazon Titan via Bedrock."""

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": max_tokens,
            "temperature": 0.3,
            "topP": 0.9,
        }
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-text-premier-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]
```

### Streaming with Bedrock

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def stream_claude_bedrock(prompt: str):
    """Stream Claude responses via Bedrock."""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3,
    }

    response = bedrock.invoke_model_with_response_stream(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        body=json.dumps(body),
        contentType="application/json"
    )

    print("Assistant: ", end="", flush=True)

    for event in response["body"]:
        chunk = json.loads(event["chunk"]["bytes"])

        if chunk["type"] == "content_block_delta":
            text = chunk["delta"].get("text", "")
            print(text, end="", flush=True)

        elif chunk["type"] == "message_stop":
            print("\n")

        elif chunk["type"] == "message_delta":
            # Final usage stats
            if "usage" in chunk:
                print(f"\nOutput tokens: {chunk['usage']['output_tokens']}")

# Usage
stream_claude_bedrock("Explain the FedRAMP authorization process step by step.")
```

### Bedrock Embeddings

```python
import boto3
import json

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def get_titan_embedding(text: str) -> list:
    """Get embeddings using Amazon Titan."""

    body = {
        "inputText": text,
        "dimensions": 1024,  # Options: 256, 512, 1024
        "normalize": True
    }

    response = bedrock.invoke_model(
        modelId="amazon.titan-embed-text-v2:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())
    return result["embedding"]

# Usage
embedding = get_titan_embedding("Federal cybersecurity requirements")
print(f"Embedding dimensions: {len(embedding)}")
```

---

## 8. Authentication and Security

Security is paramount for federal applications. This section covers authentication best practices and security considerations.

### API Key Security

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      API KEY SECURITY CHECKLIST                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ✅ DO:                                                                      ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  • Store keys in environment variables or secret managers                    ║
║  • Use separate keys for dev/staging/production                             ║
║  • Rotate keys periodically (every 90 days minimum)                         ║
║  • Audit key usage regularly                                                ║
║  • Use least-privilege principles (organization API keys)                   ║
║  • Implement key rotation without downtime                                  ║
║                                                                              ║
║  ❌ DON'T:                                                                   ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  • Hardcode keys in source code                                             ║
║  • Commit keys to version control                                           ║
║  • Share keys via email or chat                                             ║
║  • Use the same key across environments                                     ║
║  • Log API keys (even in debug mode)                                        ║
║  • Include keys in error messages                                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Secure Configuration Management

```python
"""
Production-grade API key management for federal applications.
"""

import os
from abc import ABC, abstractmethod
from typing import Optional
import logging

# Configure logging to NOT include sensitive data
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecretProvider(ABC):
    """Abstract base class for secret providers."""

    @abstractmethod
    def get_secret(self, key: str) -> str:
        pass

class EnvironmentSecretProvider(SecretProvider):
    """Get secrets from environment variables (development)."""

    def get_secret(self, key: str) -> str:
        value = os.environ.get(key)
        if not value:
            raise ValueError(f"Environment variable {key} not set")
        return value

class AWSSecretsManagerProvider(SecretProvider):
    """Get secrets from AWS Secrets Manager (production)."""

    def __init__(self, region: str = "us-east-1"):
        import boto3
        self.client = boto3.client('secretsmanager', region_name=region)

    def get_secret(self, key: str) -> str:
        import json
        try:
            response = self.client.get_secret_value(SecretId=key)
            # Handle both string and JSON secrets
            if 'SecretString' in response:
                secret = response['SecretString']
                try:
                    return json.loads(secret).get('api_key', secret)
                except json.JSONDecodeError:
                    return secret
            raise ValueError(f"Secret {key} has no string value")
        except Exception as e:
            logger.error(f"Failed to retrieve secret: {key}")
            raise

class AzureKeyVaultProvider(SecretProvider):
    """Get secrets from Azure Key Vault (production)."""

    def __init__(self, vault_url: str):
        from azure.keyvault.secrets import SecretClient
        from azure.identity import DefaultAzureCredential
        self.client = SecretClient(
            vault_url=vault_url,
            credential=DefaultAzureCredential()
        )

    def get_secret(self, key: str) -> str:
        try:
            return self.client.get_secret(key).value
        except Exception as e:
            logger.error(f"Failed to retrieve secret: {key}")
            raise

class APIKeyManager:
    """
    Unified API key manager for federal applications.

    Usage:
        # Development
        manager = APIKeyManager(EnvironmentSecretProvider())

        # Production (AWS)
        manager = APIKeyManager(AWSSecretsManagerProvider("us-gov-west-1"))

        # Production (Azure)
        manager = APIKeyManager(AzureKeyVaultProvider("https://myvault.vault.azure.net"))

        # Get keys
        openai_key = manager.get_openai_key()
        anthropic_key = manager.get_anthropic_key()
    """

    def __init__(self, provider: SecretProvider):
        self.provider = provider
        self._cache = {}

    def get_openai_key(self) -> str:
        return self._get_cached("OPENAI_API_KEY")

    def get_anthropic_key(self) -> str:
        return self._get_cached("ANTHROPIC_API_KEY")

    def get_google_key(self) -> str:
        return self._get_cached("GOOGLE_API_KEY")

    def get_azure_openai_key(self) -> str:
        return self._get_cached("AZURE_OPENAI_API_KEY")

    def _get_cached(self, key: str) -> str:
        if key not in self._cache:
            self._cache[key] = self.provider.get_secret(key)
        return self._cache[key]

    def clear_cache(self):
        """Clear cached keys (call after rotation)."""
        self._cache.clear()
```

### Request Signing and Verification

```python
"""
For applications that need to verify request authenticity.
"""

import hmac
import hashlib
import time
from typing import Tuple

def sign_request(payload: str, secret: str, timestamp: int = None) -> Tuple[str, int]:
    """
    Create a signature for a request.

    Args:
        payload: The request body
        secret: Your shared secret
        timestamp: Unix timestamp (uses current time if not provided)

    Returns:
        Tuple of (signature, timestamp)
    """
    if timestamp is None:
        timestamp = int(time.time())

    message = f"{timestamp}.{payload}".encode()
    signature = hmac.new(
        secret.encode(),
        message,
        hashlib.sha256
    ).hexdigest()

    return signature, timestamp

def verify_signature(payload: str, signature: str, timestamp: int,
                    secret: str, max_age_seconds: int = 300) -> bool:
    """
    Verify a request signature.

    Args:
        payload: The request body
        signature: The signature to verify
        timestamp: The timestamp from the request
        secret: Your shared secret
        max_age_seconds: Maximum age of request (default 5 minutes)

    Returns:
        True if valid, False otherwise
    """
    # Check timestamp age
    current_time = int(time.time())
    if abs(current_time - timestamp) > max_age_seconds:
        return False

    # Verify signature
    expected_signature, _ = sign_request(payload, secret, timestamp)
    return hmac.compare_digest(signature, expected_signature)
```

---

## 9. Error Handling Strategies

Robust error handling is essential for production federal applications.

### Understanding LLM API Errors

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      LLM API ERROR TAXONOMY                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TRANSIENT ERRORS (Should retry)                                            ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  429 Rate Limit    │ Too many requests; back off and retry                  ║
║  500 Server Error  │ Provider issue; retry with backoff                     ║
║  502 Bad Gateway   │ Infrastructure issue; retry                            ║
║  503 Unavailable   │ Service down; retry with longer delay                  ║
║  504 Timeout       │ Request too slow; retry or reduce complexity           ║
║  Connection Error  │ Network issue; check connectivity, retry               ║
║                                                                              ║
║  PERMANENT ERRORS (Do NOT retry)                                            ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  400 Bad Request   │ Invalid request format; fix the request                ║
║  401 Unauthorized  │ Invalid API key; check credentials                     ║
║  403 Forbidden     │ Permission denied; check access rights                 ║
║  404 Not Found     │ Model/resource doesn't exist; check name               ║
║  422 Unprocessable │ Invalid parameters; review and fix                     ║
║                                                                              ║
║  CONTENT ERRORS (Handle specially)                                          ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Content Filtered  │ Input/output blocked by safety; rephrase               ║
║  Context Length    │ Input too long; reduce or summarize                    ║
║  Max Tokens        │ Output truncated; increase limit or chunk              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Production-Grade Error Handling

```python
"""
Comprehensive error handling for LLM APIs in federal applications.
"""

from openai import OpenAI, APIError, RateLimitError, APIConnectionError, APITimeoutError
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
    after_log
)
import logging
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)

class ErrorCategory(Enum):
    TRANSIENT = "transient"       # Should retry
    PERMANENT = "permanent"       # Should not retry
    CONTENT = "content"           # Content-related issue
    UNKNOWN = "unknown"

@dataclass
class APIErrorInfo:
    """Structured error information."""
    category: ErrorCategory
    error_code: str
    message: str
    should_retry: bool
    retry_after: Optional[int] = None
    suggestions: List[str] = None

def categorize_error(error: Exception) -> APIErrorInfo:
    """Categorize an API error for appropriate handling."""

    if isinstance(error, RateLimitError):
        return APIErrorInfo(
            category=ErrorCategory.TRANSIENT,
            error_code="rate_limit",
            message=str(error),
            should_retry=True,
            retry_after=60,  # Default; check headers for actual value
            suggestions=[
                "Wait and retry with exponential backoff",
                "Consider reducing request frequency",
                "Request a rate limit increase if needed"
            ]
        )

    elif isinstance(error, APITimeoutError):
        return APIErrorInfo(
            category=ErrorCategory.TRANSIENT,
            error_code="timeout",
            message=str(error),
            should_retry=True,
            suggestions=[
                "Increase timeout setting",
                "Reduce prompt/max_tokens size",
                "Retry with exponential backoff"
            ]
        )

    elif isinstance(error, APIConnectionError):
        return APIErrorInfo(
            category=ErrorCategory.TRANSIENT,
            error_code="connection_error",
            message=str(error),
            should_retry=True,
            suggestions=[
                "Check network connectivity",
                "Verify firewall/proxy settings",
                "Check if provider is experiencing issues"
            ]
        )

    elif isinstance(error, APIError):
        status_code = getattr(error, 'status_code', None)

        if status_code == 400:
            return APIErrorInfo(
                category=ErrorCategory.PERMANENT,
                error_code="bad_request",
                message=str(error),
                should_retry=False,
                suggestions=[
                    "Check request format and parameters",
                    "Validate JSON structure",
                    "Review API documentation"
                ]
            )

        elif status_code == 401:
            return APIErrorInfo(
                category=ErrorCategory.PERMANENT,
                error_code="unauthorized",
                message=str(error),
                should_retry=False,
                suggestions=[
                    "Verify API key is correct",
                    "Check if key has expired",
                    "Ensure key has required permissions"
                ]
            )

        elif status_code in (500, 502, 503):
            return APIErrorInfo(
                category=ErrorCategory.TRANSIENT,
                error_code=f"server_error_{status_code}",
                message=str(error),
                should_retry=True,
                suggestions=[
                    "Retry with exponential backoff",
                    "Check provider status page",
                    "Consider fallback provider"
                ]
            )

    return APIErrorInfo(
        category=ErrorCategory.UNKNOWN,
        error_code="unknown",
        message=str(error),
        should_retry=False,
        suggestions=["Review error details", "Contact support if persistent"]
    )

class ResilientLLMClient:
    """
    Production-ready LLM client with comprehensive error handling.
    """

    def __init__(self, client: OpenAI, max_retries: int = 3):
        self.client = client
        self.max_retries = max_retries

    @retry(
        retry=retry_if_exception_type((RateLimitError, APIConnectionError, APITimeoutError)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=60),
        before_sleep=before_sleep_log(logger, logging.WARNING),
        after=after_log(logger, logging.INFO)
    )
    def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-4o",
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make a chat completion with automatic retry logic.

        Returns a dict with:
        - content: The response text
        - usage: Token usage info
        - model: Model used
        - error: Error info if any (None on success)
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            # Check for content filtering
            finish_reason = response.choices[0].finish_reason
            if finish_reason == "content_filter":
                return {
                    "content": None,
                    "usage": response.usage.model_dump() if response.usage else None,
                    "model": response.model,
                    "error": APIErrorInfo(
                        category=ErrorCategory.CONTENT,
                        error_code="content_filtered",
                        message="Content was filtered by safety systems",
                        should_retry=False,
                        suggestions=["Rephrase the prompt", "Remove sensitive content"]
                    )
                }

            # Check for truncation
            if finish_reason == "length":
                logger.warning("Response was truncated due to max_tokens limit")

            return {
                "content": response.choices[0].message.content,
                "usage": response.usage.model_dump() if response.usage else None,
                "model": response.model,
                "finish_reason": finish_reason,
                "error": None
            }

        except Exception as e:
            error_info = categorize_error(e)

            # Log the error
            logger.error(
                f"API call failed: {error_info.error_code} - {error_info.message}"
            )

            # Re-raise if should retry (tenacity will handle)
            if error_info.should_retry:
                raise

            # Return error info for permanent errors
            return {
                "content": None,
                "usage": None,
                "model": model,
                "error": error_info
            }

# Usage example
client = OpenAI()
resilient_client = ResilientLLMClient(client)

result = resilient_client.complete(
    messages=[{"role": "user", "content": "Hello!"}],
    model="gpt-4o",
    temperature=0.3
)

if result["error"]:
    print(f"Error: {result['error'].message}")
    print(f"Suggestions: {result['error'].suggestions}")
else:
    print(f"Response: {result['content']}")
```

### Circuit Breaker Pattern

```python
"""
Circuit breaker to prevent cascade failures.
"""

import time
from enum import Enum
from threading import Lock
from typing import Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """
    Circuit breaker for LLM API calls.

    Prevents overwhelming a failing service and allows it time to recover.

    Usage:
        breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

        @breaker
        def call_api():
            return client.chat.completions.create(...)
    """

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_max_calls: int = 3
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_calls = 0
        self._lock = Lock()

    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args, **kwargs) -> Any:
            return self.call(func, *args, **kwargs)
        return wrapper

    def call(self, func: Callable, *args, **kwargs) -> Any:
        with self._lock:
            self._check_state()

            if self.state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(
                    f"Circuit breaker is OPEN. Retry after {self._time_until_retry()}s"
                )

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise

    def _check_state(self):
        """Check if we should transition states."""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0

    def _on_success(self):
        """Handle successful call."""
        with self._lock:
            if self.state == CircuitState.HALF_OPEN:
                self.half_open_calls += 1
                if self.half_open_calls >= self.half_open_max_calls:
                    # Service recovered
                    self.state = CircuitState.CLOSED
                    self.failure_count = 0
            else:
                self.failure_count = 0

    def _on_failure(self):
        """Handle failed call."""
        with self._lock:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.state == CircuitState.HALF_OPEN:
                # Still failing, back to open
                self.state = CircuitState.OPEN
            elif self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN

    def _time_until_retry(self) -> int:
        if self.last_failure_time is None:
            return 0
        elapsed = time.time() - self.last_failure_time
        return max(0, int(self.recovery_timeout - elapsed))

class CircuitBreakerOpenError(Exception):
    """Raised when circuit breaker is open."""
    pass

# Usage
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

@breaker
def make_api_call(prompt: str):
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
```

---

## 10. Rate Limiting and Throttling

Rate limiting is essential for staying within provider limits and controlling costs.

### Understanding Rate Limits

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     RATE LIMIT TYPES                                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  REQUESTS PER MINUTE (RPM)                                                   ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  How many API calls you can make per minute.                                ║
║  Example: 60 RPM = 1 request per second on average                          ║
║                                                                              ║
║  TOKENS PER MINUTE (TPM)                                                     ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  How many tokens (input + output) you can process per minute.               ║
║  Example: 40,000 TPM with avg 500 tokens/request = 80 requests max          ║
║                                                                              ║
║  TOKENS PER DAY (TPD)                                                        ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Daily token budget (some providers/tiers have this).                       ║
║  Important for cost control in federal applications.                        ║
║                                                                              ║
║  TYPICAL LIMITS (vary by tier/provider):                                    ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Provider      │ Free Tier      │ Paid Tier      │ Enterprise              ║
║  ─────────────────────────────────────────────────────────────────────     ║
║  OpenAI GPT-4o │ 500 RPM/30K TPM│ 5000 RPM/800K  │ Custom                   ║
║  Anthropic     │ 60 RPM/40K TPM │ 1000 RPM/400K  │ Custom                   ║
║  Azure OpenAI  │ N/A            │ Per deployment │ Custom                   ║
║  AWS Bedrock   │ N/A            │ Region-based   │ Custom                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Rate Limiter Implementation

```python
"""
Production-grade rate limiter for LLM APIs.
"""

import time
import threading
from collections import deque
from typing import Optional
from dataclasses import dataclass

@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    requests_per_minute: int = 60
    tokens_per_minute: int = 40000
    tokens_per_day: Optional[int] = None

class TokenBucketLimiter:
    """
    Token bucket rate limiter.

    This implements a smooth rate limiting approach where tokens
    are added to a bucket at a constant rate and consumed by requests.
    """

    def __init__(self, rate: float, capacity: float):
        """
        Args:
            rate: Tokens added per second
            capacity: Maximum bucket size
        """
        self.rate = rate
        self.capacity = capacity
        self.tokens = capacity
        self.last_update = time.time()
        self._lock = threading.Lock()

    def acquire(self, tokens: float = 1.0, blocking: bool = True) -> bool:
        """
        Acquire tokens from the bucket.

        Args:
            tokens: Number of tokens to acquire
            blocking: If True, wait until tokens available

        Returns:
            True if acquired, False if not (only when blocking=False)
        """
        with self._lock:
            self._refill()

            if self.tokens >= tokens:
                self.tokens -= tokens
                return True

            if not blocking:
                return False

            # Calculate wait time
            needed = tokens - self.tokens
            wait_time = needed / self.rate

        # Wait outside lock
        time.sleep(wait_time)

        # Try again
        return self.acquire(tokens, blocking=False)

    def _refill(self):
        """Refill tokens based on elapsed time."""
        now = time.time()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        self.last_update = now

class SlidingWindowLimiter:
    """
    Sliding window rate limiter for both RPM and TPM.

    More accurate than fixed windows and prevents bursts at window boundaries.
    """

    def __init__(self, config: RateLimitConfig):
        self.config = config

        # Track requests in the last minute
        self.request_times = deque()
        self.token_usage = deque()  # (timestamp, tokens)
        self.daily_tokens = 0
        self.daily_reset = time.time()

        self._lock = threading.Lock()

    def check_and_wait(self, estimated_tokens: int = 500) -> float:
        """
        Check rate limits and wait if necessary.

        Args:
            estimated_tokens: Estimated tokens for this request

        Returns:
            Time waited in seconds
        """
        wait_time = 0.0

        with self._lock:
            now = time.time()

            # Clean old entries
            self._clean_old_entries(now)

            # Check RPM
            if len(self.request_times) >= self.config.requests_per_minute:
                oldest = self.request_times[0]
                rpm_wait = 60 - (now - oldest)
                wait_time = max(wait_time, rpm_wait)

            # Check TPM
            current_tpm = sum(tokens for _, tokens in self.token_usage)
            if current_tpm + estimated_tokens > self.config.tokens_per_minute:
                if self.token_usage:
                    oldest_time = self.token_usage[0][0]
                    tpm_wait = 60 - (now - oldest_time)
                    wait_time = max(wait_time, tpm_wait)

            # Check daily limit
            if self.config.tokens_per_day:
                # Reset daily counter if needed
                if now - self.daily_reset >= 86400:
                    self.daily_tokens = 0
                    self.daily_reset = now

                if self.daily_tokens + estimated_tokens > self.config.tokens_per_day:
                    raise DailyLimitExceededError(
                        f"Daily token limit ({self.config.tokens_per_day}) exceeded"
                    )

        if wait_time > 0:
            time.sleep(wait_time)

        return wait_time

    def record_usage(self, tokens: int):
        """Record actual token usage after a request."""
        with self._lock:
            now = time.time()
            self.request_times.append(now)
            self.token_usage.append((now, tokens))

            if self.config.tokens_per_day:
                self.daily_tokens += tokens

    def _clean_old_entries(self, now: float):
        """Remove entries older than 1 minute."""
        cutoff = now - 60

        while self.request_times and self.request_times[0] < cutoff:
            self.request_times.popleft()

        while self.token_usage and self.token_usage[0][0] < cutoff:
            self.token_usage.popleft()

    def get_status(self) -> dict:
        """Get current rate limit status."""
        with self._lock:
            now = time.time()
            self._clean_old_entries(now)

            return {
                "requests_used": len(self.request_times),
                "requests_limit": self.config.requests_per_minute,
                "tokens_used": sum(t for _, t in self.token_usage),
                "tokens_limit": self.config.tokens_per_minute,
                "daily_tokens_used": self.daily_tokens,
                "daily_tokens_limit": self.config.tokens_per_day,
            }

class DailyLimitExceededError(Exception):
    """Raised when daily token limit is exceeded."""
    pass

# Usage example
limiter = SlidingWindowLimiter(RateLimitConfig(
    requests_per_minute=60,
    tokens_per_minute=40000,
    tokens_per_day=1000000
))

def make_request(prompt: str):
    # Estimate tokens (rough: 1 token per 4 chars)
    estimated_tokens = len(prompt) // 4 + 500  # +500 for response

    # Wait if needed
    wait_time = limiter.check_and_wait(estimated_tokens)
    if wait_time > 0:
        print(f"Rate limited, waited {wait_time:.2f}s")

    # Make the actual request
    response = client.chat.completions.create(...)

    # Record actual usage
    actual_tokens = response.usage.total_tokens
    limiter.record_usage(actual_tokens)

    return response
```

---

## 11. Cost Management and Optimization

Cost control is critical for federal applications with fixed budgets.

### Understanding LLM Pricing

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LLM API PRICING (2025)                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  OPENAI                                 (per 1M tokens)                      ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  GPT-4o              │ Input: $2.50    │ Output: $10.00                     ║
║  GPT-4o-mini         │ Input: $0.15    │ Output: $0.60                      ║
║  GPT-4 Turbo         │ Input: $10.00   │ Output: $30.00                     ║
║  o1                  │ Input: $15.00   │ Output: $60.00                     ║
║  o1-mini             │ Input: $3.00    │ Output: $12.00                     ║
║  text-embedding-3-small │ $0.02                                             ║
║  text-embedding-3-large │ $0.13                                             ║
║                                                                              ║
║  ANTHROPIC                              (per 1M tokens)                      ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Claude Sonnet 4     │ Input: $3.00    │ Output: $15.00                     ║
║  Claude 3.5 Sonnet   │ Input: $3.00    │ Output: $15.00                     ║
║  Claude 3 Opus       │ Input: $15.00   │ Output: $75.00                     ║
║  Claude 3 Haiku      │ Input: $0.25    │ Output: $1.25                      ║
║                                                                              ║
║  GOOGLE GEMINI                          (per 1M characters)                  ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  Gemini 1.5 Pro      │ Input: $1.25    │ Output: $5.00                      ║
║  Gemini 1.5 Flash    │ Input: $0.075   │ Output: $0.30                      ║
║                                                                              ║
║  COST EXAMPLE                                                                ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  10,000 requests/day × 1,000 tokens avg × 30 days = 300M tokens/month       ║
║                                                                              ║
║  GPT-4o:     300M × ($2.50 + $10.00)/1M × 0.3 = $1,125/month               ║
║  GPT-4o-mini: 300M × ($0.15 + $0.60)/1M × 0.3 = $67.50/month               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Cost Tracker Implementation

```python
"""
Comprehensive cost tracking for federal budget compliance.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime, date
from collections import defaultdict
import json

@dataclass
class ModelPricing:
    """Pricing for a specific model."""
    input_cost_per_million: float
    output_cost_per_million: float

# Current pricing (update as needed)
PRICING = {
    "gpt-4o": ModelPricing(2.50, 10.00),
    "gpt-4o-mini": ModelPricing(0.15, 0.60),
    "gpt-4-turbo": ModelPricing(10.00, 30.00),
    "o1": ModelPricing(15.00, 60.00),
    "claude-3-5-sonnet": ModelPricing(3.00, 15.00),
    "claude-sonnet-4": ModelPricing(3.00, 15.00),
    "claude-3-opus": ModelPricing(15.00, 75.00),
    "claude-3-haiku": ModelPricing(0.25, 1.25),
    "gemini-1.5-pro": ModelPricing(1.25, 5.00),
    "gemini-1.5-flash": ModelPricing(0.075, 0.30),
}

@dataclass
class UsageRecord:
    """Single usage record."""
    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    cost: float
    user_id: Optional[str] = None
    project_id: Optional[str] = None
    request_id: Optional[str] = None

@dataclass
class CostBudget:
    """Budget configuration."""
    daily_limit: float = 100.0
    monthly_limit: float = 2000.0
    alert_threshold: float = 0.8  # Alert at 80% of budget

class CostTracker:
    """
    Track and manage LLM API costs for federal budget compliance.
    """

    def __init__(self, budget: CostBudget = None):
        self.budget = budget or CostBudget()
        self.records: List[UsageRecord] = []
        self._daily_costs: Dict[date, float] = defaultdict(float)
        self._monthly_costs: Dict[str, float] = defaultdict(float)  # "2025-01" format
        self._model_costs: Dict[str, float] = defaultdict(float)
        self._user_costs: Dict[str, float] = defaultdict(float)
        self._project_costs: Dict[str, float] = defaultdict(float)

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculate cost for a request."""
        # Normalize model name
        model_key = self._normalize_model_name(model)
        pricing = PRICING.get(model_key)

        if not pricing:
            # Unknown model - use conservative estimate
            pricing = ModelPricing(5.00, 15.00)

        input_cost = (input_tokens / 1_000_000) * pricing.input_cost_per_million
        output_cost = (output_tokens / 1_000_000) * pricing.output_cost_per_million

        return input_cost + output_cost

    def record_usage(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        user_id: str = None,
        project_id: str = None,
        request_id: str = None
    ) -> UsageRecord:
        """Record API usage and check budget limits."""

        cost = self.calculate_cost(model, input_tokens, output_tokens)
        now = datetime.utcnow()
        today = now.date()
        month_key = now.strftime("%Y-%m")

        record = UsageRecord(
            timestamp=now,
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=cost,
            user_id=user_id,
            project_id=project_id,
            request_id=request_id
        )

        self.records.append(record)

        # Update aggregations
        self._daily_costs[today] += cost
        self._monthly_costs[month_key] += cost
        self._model_costs[model] += cost

        if user_id:
            self._user_costs[user_id] += cost
        if project_id:
            self._project_costs[project_id] += cost

        # Check budget alerts
        self._check_budget_alerts(today, month_key)

        return record

    def _check_budget_alerts(self, today: date, month_key: str):
        """Check and raise alerts for budget thresholds."""
        daily_usage = self._daily_costs[today]
        monthly_usage = self._monthly_costs[month_key]

        # Daily limit check
        if daily_usage >= self.budget.daily_limit:
            raise DailyBudgetExceededError(
                f"Daily budget exceeded: ${daily_usage:.2f} / ${self.budget.daily_limit:.2f}"
            )
        elif daily_usage >= self.budget.daily_limit * self.budget.alert_threshold:
            print(f"⚠️  Daily budget alert: ${daily_usage:.2f} / ${self.budget.daily_limit:.2f}")

        # Monthly limit check
        if monthly_usage >= self.budget.monthly_limit:
            raise MonthlyBudgetExceededError(
                f"Monthly budget exceeded: ${monthly_usage:.2f} / ${self.budget.monthly_limit:.2f}"
            )
        elif monthly_usage >= self.budget.monthly_limit * self.budget.alert_threshold:
            print(f"⚠️  Monthly budget alert: ${monthly_usage:.2f} / ${self.budget.monthly_limit:.2f}")

    def get_report(self) -> dict:
        """Generate a cost report."""
        today = datetime.utcnow().date()
        month_key = datetime.utcnow().strftime("%Y-%m")

        return {
            "daily_cost": self._daily_costs[today],
            "daily_budget": self.budget.daily_limit,
            "daily_remaining": self.budget.daily_limit - self._daily_costs[today],
            "monthly_cost": self._monthly_costs[month_key],
            "monthly_budget": self.budget.monthly_limit,
            "monthly_remaining": self.budget.monthly_limit - self._monthly_costs[month_key],
            "cost_by_model": dict(self._model_costs),
            "cost_by_user": dict(self._user_costs),
            "cost_by_project": dict(self._project_costs),
            "total_requests": len(self.records),
            "total_tokens": sum(r.input_tokens + r.output_tokens for r in self.records),
        }

    def _normalize_model_name(self, model: str) -> str:
        """Normalize model name for pricing lookup."""
        model = model.lower()

        # Handle version suffixes
        for key in PRICING.keys():
            if model.startswith(key) or key in model:
                return key

        return model

    def export_for_audit(self, filepath: str):
        """Export records for federal audit compliance."""
        export_data = {
            "export_timestamp": datetime.utcnow().isoformat(),
            "summary": self.get_report(),
            "records": [
                {
                    "timestamp": r.timestamp.isoformat(),
                    "model": r.model,
                    "input_tokens": r.input_tokens,
                    "output_tokens": r.output_tokens,
                    "cost": r.cost,
                    "user_id": r.user_id,
                    "project_id": r.project_id,
                    "request_id": r.request_id,
                }
                for r in self.records
            ]
        }

        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)

class DailyBudgetExceededError(Exception):
    pass

class MonthlyBudgetExceededError(Exception):
    pass

# Usage
tracker = CostTracker(CostBudget(
    daily_limit=100.0,
    monthly_limit=2000.0,
    alert_threshold=0.8
))

# After each API call
response = client.chat.completions.create(...)
tracker.record_usage(
    model="gpt-4o",
    input_tokens=response.usage.prompt_tokens,
    output_tokens=response.usage.completion_tokens,
    user_id="analyst-123",
    project_id="compliance-review"
)

# Get report
print(tracker.get_report())
```

### Cost Optimization Strategies

```python
"""
Strategies for optimizing LLM API costs.
"""

from typing import List, Dict, Tuple
import tiktoken

class CostOptimizer:
    """
    Collection of strategies for reducing LLM API costs.
    """

    # ═══════════════════════════════════════════════════════════════════════
    # STRATEGY 1: Model Routing
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def select_model_by_complexity(prompt: str, requires_reasoning: bool = False) -> str:
        """
        Route to appropriate model based on task complexity.

        Cost savings: 50-90% by using cheaper models for simple tasks
        """
        word_count = len(prompt.split())

        if requires_reasoning:
            # Complex reasoning tasks need advanced models
            return "o1" if word_count > 500 else "o1-mini"

        # Simple queries can use cheaper models
        if word_count < 50 and "?" in prompt:
            return "gpt-4o-mini"  # Simple Q&A

        if any(word in prompt.lower() for word in ["summarize", "list", "extract"]):
            return "gpt-4o-mini"  # Structured extraction

        # Default to balanced model
        return "gpt-4o"

    # ═══════════════════════════════════════════════════════════════════════
    # STRATEGY 2: Prompt Compression
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def compress_prompt(prompt: str, max_tokens: int = 2000) -> str:
        """
        Compress a prompt to reduce input tokens.

        Cost savings: 20-50% on input costs
        """
        # Remove extra whitespace
        prompt = " ".join(prompt.split())

        # Remove filler words for factual queries
        filler_words = [
            "please", "kindly", "i would like you to", "could you",
            "i need you to", "i want you to", "basically", "essentially"
        ]
        for filler in filler_words:
            prompt = prompt.lower().replace(filler, "")

        # Truncate if still too long
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(prompt)

        if len(tokens) > max_tokens:
            tokens = tokens[:max_tokens]
            prompt = encoding.decode(tokens)
            prompt += "... [truncated]"

        return prompt.strip()

    # ═══════════════════════════════════════════════════════════════════════
    # STRATEGY 3: Response Caching
    # ═══════════════════════════════════════════════════════════════════════

    def __init__(self):
        self._cache: Dict[str, Tuple[str, float]] = {}  # prompt_hash -> (response, timestamp)
        self._cache_ttl = 3600  # 1 hour

    def get_cached_response(self, prompt: str, system: str = "") -> str | None:
        """
        Check cache for identical prompts.

        Cost savings: 100% for repeated queries
        """
        import hashlib
        import time

        cache_key = hashlib.sha256(f"{system}:{prompt}".encode()).hexdigest()

        if cache_key in self._cache:
            response, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                return response
            else:
                del self._cache[cache_key]

        return None

    def cache_response(self, prompt: str, response: str, system: str = ""):
        """Cache a response for future use."""
        import hashlib
        import time

        cache_key = hashlib.sha256(f"{system}:{prompt}".encode()).hexdigest()
        self._cache[cache_key] = (response, time.time())

    # ═══════════════════════════════════════════════════════════════════════
    # STRATEGY 4: Batching
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def batch_similar_prompts(prompts: List[str], batch_size: int = 5) -> List[str]:
        """
        Combine multiple similar prompts into batched requests.

        Cost savings: 30-50% on overhead
        """
        batched = []
        for i in range(0, len(prompts), batch_size):
            batch = prompts[i:i + batch_size]
            combined = "Process each of the following items separately:\n\n"
            for j, prompt in enumerate(batch, 1):
                combined += f"Item {j}:\n{prompt}\n\n"
            combined += "Provide your response for each item clearly labeled."
            batched.append(combined)
        return batched

    # ═══════════════════════════════════════════════════════════════════════
    # STRATEGY 5: Output Length Control
    # ═══════════════════════════════════════════════════════════════════════

    @staticmethod
    def estimate_max_tokens(task_type: str) -> int:
        """
        Estimate appropriate max_tokens for task type.

        Cost savings: 20-40% by not over-allocating output tokens
        """
        estimates = {
            "classification": 50,
            "yes_no": 10,
            "short_answer": 200,
            "summary": 500,
            "analysis": 1000,
            "detailed_report": 2000,
            "code_generation": 1500,
        }
        return estimates.get(task_type, 500)
```

---

## 12. Production Architecture Patterns

Designing robust architectures for federal production systems.

### Multi-Provider Fallback

```python
"""
Multi-provider client with automatic fallback.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProviderConfig:
    """Configuration for a single provider."""
    name: str
    priority: int  # Lower = higher priority
    enabled: bool = True
    max_retries: int = 2

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(self, messages: List[Dict], **kwargs) -> str:
        pass

    @abstractmethod
    def is_healthy(self) -> bool:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, client):
        self.client = client

    def complete(self, messages: List[Dict], **kwargs) -> str:
        response = self.client.chat.completions.create(
            model=kwargs.get("model", "gpt-4o"),
            messages=messages,
            **{k: v for k, v in kwargs.items() if k != "model"}
        )
        return response.choices[0].message.content

    def is_healthy(self) -> bool:
        try:
            self.client.models.list()
            return True
        except:
            return False

class AnthropicProvider(LLMProvider):
    def __init__(self, client):
        self.client = client

    def complete(self, messages: List[Dict], **kwargs) -> str:
        # Convert OpenAI format to Anthropic format
        anthropic_messages = []
        system = None

        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                anthropic_messages.append(msg)

        response = self.client.messages.create(
            model=kwargs.get("model", "claude-sonnet-4-20250514"),
            max_tokens=kwargs.get("max_tokens", 1024),
            system=system,
            messages=anthropic_messages,
        )
        return response.content[0].text

    def is_healthy(self) -> bool:
        # Anthropic doesn't have a list models endpoint
        # Could do a minimal test request
        return True

class MultiProviderClient:
    """
    Client that routes requests across multiple providers with fallback.

    Usage:
        client = MultiProviderClient()
        client.add_provider("openai", OpenAIProvider(openai_client), priority=1)
        client.add_provider("anthropic", AnthropicProvider(anthropic_client), priority=2)

        # Will try OpenAI first, fall back to Anthropic if it fails
        response = client.complete(messages=[...])
    """

    def __init__(self):
        self.providers: Dict[str, tuple[LLMProvider, ProviderConfig]] = {}

    def add_provider(
        self,
        name: str,
        provider: LLMProvider,
        priority: int = 10,
        enabled: bool = True
    ):
        """Add a provider to the pool."""
        config = ProviderConfig(name=name, priority=priority, enabled=enabled)
        self.providers[name] = (provider, config)

    def complete(self, messages: List[Dict], **kwargs) -> str:
        """
        Complete with automatic fallback.

        Tries providers in priority order until one succeeds.
        """
        # Sort providers by priority
        sorted_providers = sorted(
            self.providers.items(),
            key=lambda x: x[1][1].priority
        )

        last_error = None

        for name, (provider, config) in sorted_providers:
            if not config.enabled:
                continue

            for attempt in range(config.max_retries):
                try:
                    logger.info(f"Trying provider {name} (attempt {attempt + 1})")
                    result = provider.complete(messages, **kwargs)
                    logger.info(f"Success with provider {name}")
                    return result

                except Exception as e:
                    last_error = e
                    logger.warning(
                        f"Provider {name} failed (attempt {attempt + 1}): {e}"
                    )

        raise AllProvidersFailedError(
            f"All providers failed. Last error: {last_error}"
        )

    def health_check(self) -> Dict[str, bool]:
        """Check health of all providers."""
        return {
            name: provider.is_healthy()
            for name, (provider, _) in self.providers.items()
        }

class AllProvidersFailedError(Exception):
    pass
```

### Request Queue with Priority

```python
"""
Priority queue for managing API requests in high-volume federal applications.
"""

import asyncio
from dataclasses import dataclass, field
from typing import Any, Callable, Optional
from enum import IntEnum
import heapq
import uuid

class Priority(IntEnum):
    CRITICAL = 0    # Mission-critical requests
    HIGH = 1        # Important user requests
    NORMAL = 2      # Standard requests
    LOW = 3         # Background/batch requests
    BULK = 4        # Large batch operations

@dataclass(order=True)
class QueuedRequest:
    priority: int
    timestamp: float = field(compare=False)
    request_id: str = field(compare=False)
    coroutine: Any = field(compare=False)
    callback: Optional[Callable] = field(compare=False, default=None)

class PriorityRequestQueue:
    """
    Async priority queue for LLM API requests.

    Features:
    - Priority-based processing
    - Rate limit awareness
    - Request deduplication
    - Timeout handling
    """

    def __init__(self, max_concurrent: int = 10, rate_limiter=None):
        self.max_concurrent = max_concurrent
        self.rate_limiter = rate_limiter

        self._queue: list = []  # Heap queue
        self._pending: dict = {}  # request_id -> QueuedRequest
        self._active = 0
        self._lock = asyncio.Lock()
        self._not_full = asyncio.Condition()

    async def submit(
        self,
        coroutine,
        priority: Priority = Priority.NORMAL,
        callback: Callable = None,
        timeout: float = 60.0
    ) -> str:
        """Submit a request to the queue."""
        import time

        request_id = str(uuid.uuid4())
        request = QueuedRequest(
            priority=priority,
            timestamp=time.time(),
            request_id=request_id,
            coroutine=coroutine,
            callback=callback
        )

        async with self._lock:
            heapq.heappush(self._queue, request)
            self._pending[request_id] = request

        # Start processing if not at capacity
        asyncio.create_task(self._process())

        return request_id

    async def _process(self):
        """Process requests from the queue."""
        async with self._not_full:
            while self._active >= self.max_concurrent:
                await self._not_full.wait()

        async with self._lock:
            if not self._queue:
                return

            request = heapq.heappop(self._queue)
            self._active += 1

        try:
            # Apply rate limiting if configured
            if self.rate_limiter:
                await self.rate_limiter.acquire()

            # Execute the request
            result = await request.coroutine

            # Call callback if provided
            if request.callback:
                request.callback(result, None)

        except Exception as e:
            if request.callback:
                request.callback(None, e)

        finally:
            async with self._lock:
                self._active -= 1
                if request.request_id in self._pending:
                    del self._pending[request.request_id]

            async with self._not_full:
                self._not_full.notify()

    def get_queue_stats(self) -> dict:
        """Get queue statistics."""
        return {
            "queued": len(self._queue),
            "active": self._active,
            "max_concurrent": self.max_concurrent,
            "by_priority": {
                p.name: sum(1 for r in self._queue if r.priority == p)
                for p in Priority
            }
        }
```

---

## 13. Federal Compliance Considerations

Key compliance requirements for federal LLM API integrations.

### Compliance Checklist

```
╔══════════════════════════════════════════════════════════════════════════════╗
║               FEDERAL LLM API COMPLIANCE CHECKLIST                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DATA HANDLING                                                               ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  [ ] Classify data before sending to any API                                ║
║  [ ] Never send CUI/classified data to non-FedRAMP APIs                    ║
║  [ ] Implement data sanitization before API calls                           ║
║  [ ] Log all data sent to external APIs (without logging content)           ║
║  [ ] Implement data retention policies                                      ║
║                                                                              ║
║  AUTHENTICATION & ACCESS                                                     ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  [ ] Store API keys in approved secret management systems                   ║
║  [ ] Implement key rotation (minimum 90 days)                               ║
║  [ ] Use service accounts, not personal accounts                            ║
║  [ ] Implement least-privilege access                                       ║
║  [ ] Enable MFA for API provider accounts                                   ║
║                                                                              ║
║  AUDIT & LOGGING                                                             ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  [ ] Log all API requests (user, timestamp, model, tokens)                  ║
║  [ ] Do NOT log prompt content in production                                ║
║  [ ] Retain logs per agency retention schedule                              ║
║  [ ] Implement audit trail for cost tracking                                ║
║  [ ] Regular access reviews                                                  ║
║                                                                              ║
║  NETWORK SECURITY                                                            ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  [ ] Use TLS 1.2+ for all API communications                               ║
║  [ ] Consider private endpoints where available                             ║
║  [ ] Implement egress filtering                                             ║
║  [ ] Monitor for data exfiltration                                          ║
║                                                                              ║
║  PROCUREMENT                                                                 ║
║  ───────────────────────────────────────────────────────────────────────    ║
║  [ ] Verify FedRAMP authorization status                                    ║
║  [ ] Review provider's System Security Plan                                 ║
║  [ ] Ensure contract includes required clauses (FAR 52.204-21, etc.)       ║
║  [ ] Budget for API costs in advance                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Data Classification Helper

```python
"""
Helper for classifying data before API submission.
"""

from enum import Enum
from typing import List, Tuple
import re

class DataClassification(Enum):
    PUBLIC = "public"           # Can use any API
    INTERNAL = "internal"       # Prefer FedRAMP, avoid direct APIs
    CUI = "cui"                 # FedRAMP Moderate+ only
    CLASSIFIED = "classified"   # Never use commercial APIs

class DataClassifier:
    """
    Classify data to determine appropriate API usage.

    This is a basic implementation - federal agencies should
    customize based on their specific classification guidance.
    """

    # Patterns that indicate sensitive data
    CUI_PATTERNS = [
        r'\b\d{3}-\d{2}-\d{4}\b',              # SSN
        r'\b[A-Z]{2}\d{6,8}\b',                 # Passport
        r'SECRET|CONFIDENTIAL|TOP SECRET',      # Classification markings
        r'CUI|FOUO|SBU',                        # Handling caveats
        r'ITAR|EAR|EXPORT',                     # Export controlled
        r'\b\d{16}\b',                          # Credit card
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}',  # Email
    ]

    # Keywords that suggest internal data
    INTERNAL_KEYWORDS = [
        'internal', 'proprietary', 'draft', 'pre-decisional',
        'budget', 'personnel', 'procurement', 'source selection',
        'bid', 'proposal', 'contract', 'acquisition'
    ]

    @classmethod
    def classify(cls, text: str) -> Tuple[DataClassification, List[str]]:
        """
        Classify text and return classification with reasons.

        Returns:
            Tuple of (classification, list of reasons)
        """
        reasons = []

        # Check for CUI patterns
        for pattern in cls.CUI_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                reasons.append(f"Contains pattern: {pattern[:30]}...")

        if reasons:
            return DataClassification.CUI, reasons

        # Check for internal keywords
        text_lower = text.lower()
        found_keywords = [kw for kw in cls.INTERNAL_KEYWORDS if kw in text_lower]

        if found_keywords:
            return DataClassification.INTERNAL, [f"Contains keywords: {found_keywords}"]

        return DataClassification.PUBLIC, ["No sensitive patterns detected"]

    @classmethod
    def get_allowed_providers(cls, classification: DataClassification) -> List[str]:
        """Get list of allowed providers for a classification level."""

        allowed = {
            DataClassification.PUBLIC: [
                "openai", "anthropic", "google",
                "azure_openai", "aws_bedrock", "gcp_vertex"
            ],
            DataClassification.INTERNAL: [
                "azure_openai", "aws_bedrock", "gcp_vertex"
            ],
            DataClassification.CUI: [
                "azure_openai_gov", "aws_bedrock_govcloud"
            ],
            DataClassification.CLASSIFIED: []  # No commercial APIs
        }

        return allowed.get(classification, [])

# Usage
def safe_api_call(prompt: str, provider: str):
    """Make an API call only if data classification allows."""

    classification, reasons = DataClassifier.classify(prompt)
    allowed = DataClassifier.get_allowed_providers(classification)

    if provider not in allowed:
        raise DataClassificationError(
            f"Cannot use {provider} for {classification.value} data. "
            f"Reasons: {reasons}. Allowed providers: {allowed}"
        )

    # Proceed with API call...

class DataClassificationError(Exception):
    pass
```

---

## 14. Exercises

### Exercise 4.1: Multi-Provider Client

Build a unified client that can switch between OpenAI, Anthropic, and Google APIs.

**Requirements:**
- Single interface for all providers
- Automatic format conversion between providers
- Fallback on provider failure
- Consistent response format

```python
"""
Exercise 4.1 Starter Code

Complete the UnifiedLLMClient class to support multiple providers.
"""

from typing import List, Dict, Optional
from abc import ABC, abstractmethod

class UnifiedLLMClient:
    """
    Your task: Implement a client that provides a unified interface
    to OpenAI, Anthropic, and Google Gemini APIs.
    """

    def __init__(self):
        # TODO: Initialize clients for each provider
        pass

    def complete(
        self,
        prompt: str,
        provider: str = "openai",
        model: Optional[str] = None,
        **kwargs
    ) -> str:
        """
        Generate a completion using the specified provider.

        Args:
            prompt: The user's prompt
            provider: "openai", "anthropic", or "google"
            model: Optional model override
            **kwargs: Additional parameters

        Returns:
            The generated text response
        """
        # TODO: Implement routing logic
        pass

    def complete_with_fallback(
        self,
        prompt: str,
        preferred_order: List[str] = None,
        **kwargs
    ) -> str:
        """
        Try providers in order until one succeeds.

        Args:
            prompt: The user's prompt
            preferred_order: Order to try providers
            **kwargs: Additional parameters

        Returns:
            The generated text response
        """
        # TODO: Implement fallback logic
        pass

# Test your implementation
if __name__ == "__main__":
    client = UnifiedLLMClient()

    # Test each provider
    for provider in ["openai", "anthropic", "google"]:
        response = client.complete(
            "What is FedRAMP?",
            provider=provider
        )
        print(f"{provider}: {response[:100]}...")

    # Test fallback
    response = client.complete_with_fallback(
        "Explain NIST 800-53",
        preferred_order=["openai", "anthropic", "google"]
    )
    print(f"Fallback result: {response[:100]}...")
```

### Exercise 4.2: Rate Limiter with Token Tracking

Implement a rate limiter that tracks both requests and tokens.

```python
"""
Exercise 4.2 Starter Code

Implement a rate limiter that respects both RPM and TPM limits.
"""

class SmartRateLimiter:
    """
    Your task: Implement a rate limiter that:
    1. Tracks requests per minute (RPM)
    2. Tracks tokens per minute (TPM)
    3. Provides wait time estimates
    4. Handles token usage recording
    """

    def __init__(self, rpm_limit: int, tpm_limit: int):
        # TODO: Initialize tracking structures
        pass

    def can_proceed(self, estimated_tokens: int) -> bool:
        """Check if a request can proceed without waiting."""
        # TODO: Implement
        pass

    def wait_time(self, estimated_tokens: int) -> float:
        """Calculate how long to wait before proceeding."""
        # TODO: Implement
        pass

    def record_usage(self, actual_tokens: int):
        """Record actual token usage after a request."""
        # TODO: Implement
        pass

    def get_status(self) -> dict:
        """Get current rate limit status."""
        # TODO: Implement
        pass
```

### Exercise 4.3: Cost Dashboard

Build a cost tracking system that monitors API usage across multiple providers.

```python
"""
Exercise 4.3 Starter Code

Build a comprehensive cost tracking dashboard.
"""

class CostDashboard:
    """
    Your task: Implement a cost tracking system that:
    1. Tracks costs by provider, model, user, and project
    2. Enforces budget limits
    3. Generates reports for audit
    4. Provides cost projections
    """

    def __init__(self, daily_budget: float, monthly_budget: float):
        # TODO: Initialize
        pass

    def record_usage(
        self,
        provider: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        user_id: str = None,
        project_id: str = None
    ):
        """Record API usage."""
        # TODO: Implement
        pass

    def check_budget(self) -> dict:
        """Check current budget status."""
        # TODO: Implement
        pass

    def generate_report(self, period: str = "daily") -> dict:
        """Generate a cost report."""
        # TODO: Implement
        pass

    def project_costs(self, days_ahead: int = 30) -> dict:
        """Project future costs based on current usage."""
        # TODO: Implement
        pass
```

### Exercise 4.4: Streaming Handler

Create a streaming response handler that works with all major providers.

```python
"""
Exercise 4.4 Starter Code

Implement a universal streaming handler.
"""

from typing import Generator, Callable

class UniversalStreamer:
    """
    Your task: Implement a streaming handler that:
    1. Works with OpenAI, Anthropic, and Google
    2. Provides consistent output format
    3. Handles errors gracefully
    4. Supports callbacks for real-time processing
    """

    def stream(
        self,
        prompt: str,
        provider: str,
        on_token: Callable[[str], None] = None,
        on_complete: Callable[[str, dict], None] = None,
        on_error: Callable[[Exception], None] = None,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Stream a response from the specified provider.

        Args:
            prompt: The user's prompt
            provider: "openai", "anthropic", or "google"
            on_token: Called for each token
            on_complete: Called when done with full text and metadata
            on_error: Called on error
            **kwargs: Additional parameters

        Yields:
            Text chunks as they arrive
        """
        # TODO: Implement
        pass
```

---

## 15. Assessment

### Knowledge Check

Answer the following questions to verify your understanding:

1. **API Fundamentals**
   - What HTTP status code indicates rate limiting?
   - What's the difference between synchronous and streaming responses?
   - Why do LLM providers charge differently for input vs output tokens?

2. **Provider Differences**
   - How does Claude's system prompt handling differ from OpenAI's?
   - What is a "deployment" in Azure OpenAI?
   - Which providers have FedRAMP High authorization?

3. **Security & Compliance**
   - What are three methods for securely storing API keys?
   - What data classification level requires FedRAMP Moderate+?
   - Why should you never log prompt content in production?

4. **Error Handling**
   - Which errors should trigger automatic retry?
   - What is a circuit breaker and when should you use it?
   - How do you handle content filter responses?

5. **Cost Management**
   - How do you estimate tokens before making a request?
   - What strategies can reduce API costs by 50% or more?
   - How should you track costs for federal audit compliance?

### Practical Assessment

Complete the following tasks to demonstrate proficiency:

1. **Basic Integration** (30 minutes)
   - Set up authentication for OpenAI and Anthropic
   - Make a successful API call to each
   - Handle a rate limit error gracefully

2. **Production Readiness** (1 hour)
   - Implement retry logic with exponential backoff
   - Add cost tracking to your API calls
   - Create an audit log for compliance

3. **Advanced Patterns** (1.5 hours)
   - Build a multi-provider client with fallback
   - Implement streaming for real-time responses
   - Add rate limiting that respects both RPM and TPM

---

## ➡️ Next Module

[Module 05: Prompt Engineering](../05-prompt-engineering/README.md)

---

<div align="center">

[⬆ Back to Top](#module-04-api-integration) · [📚 Return to Curriculum](../../README.md)

</div>
