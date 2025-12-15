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

- [ ] Authenticate and connect to major LLM provider APIs
- [ ] Implement proper error handling and retry logic
- [ ] Design rate-limiting strategies for production use
- [ ] Choose appropriate API configurations for federal workloads
- [ ] Build secure API integrations meeting compliance requirements

---

## 📑 Table of Contents

1. [API Landscape Overview](#1-api-landscape-overview)
2. [OpenAI API](#2-openai-api)
3. [Anthropic Claude API](#3-anthropic-claude-api)
4. [Google AI API](#4-google-ai-api)
5. [Azure OpenAI](#5-azure-openai)
6. [AWS Bedrock](#6-aws-bedrock)
7. [API Best Practices](#7-api-best-practices)

---

## 1. API Landscape Overview

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         LLM API ECOSYSTEM                                    ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                      DIRECT PROVIDER APIs                               │║
║  │                                                                          │║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │║
║  │   │   OpenAI     │  │  Anthropic   │  │   Google     │                 │║
║  │   │              │  │              │  │              │                 │║
║  │   │ • GPT-4o     │  │ • Claude 3.5 │  │ • Gemini Pro │                 │║
║  │   │ • GPT-4      │  │ • Claude 3   │  │ • Gemini 1.5 │                 │║
║  │   │ • Embeddings │  │ • Haiku      │  │ • Embeddings │                 │║
║  │   │ • DALL-E     │  │              │  │ • Imagen     │                 │║
║  │   └──────────────┘  └──────────────┘  └──────────────┘                 │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────────┐║
║  │                    CLOUD PROVIDER WRAPPERS                              │║
║  │                                                                          │║
║  │   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │║
║  │   │ Azure OpenAI │  │ AWS Bedrock  │  │  GCP Vertex  │                 │║
║  │   │              │  │              │  │              │                 │║
║  │   │ • GPT Models │  │ • Claude     │  │ • Gemini     │                 │║
║  │   │ • FedRAMP ✓  │  │ • Llama      │  │ • PaLM       │                 │║
║  │   │ • Gov Cloud  │  │ • Titan      │  │ • Codey      │                 │║
║  │   │              │  │ • FedRAMP ✓  │  │ • FedRAMP ✓  │                 │║
║  │   └──────────────┘  └──────────────┘  └──────────────┘                 │║
║  └─────────────────────────────────────────────────────────────────────────┘║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Provider Comparison Matrix

| Feature | OpenAI | Anthropic | Google | Azure | Bedrock |
|:--------|:------:|:---------:|:------:|:-----:|:-------:|
| **FedRAMP** | ⏳ | ⏳ | ✅ | ✅ | ✅ |
| **GovCloud** | ❌ | ❌ | ✅ | ✅ | ✅ |
| **SSO/SAML** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Data Residency** | US | US | Configurable | Configurable | Configurable |
| **SLA** | 99.9% | 99.9% | 99.9% | 99.95% | 99.9% |

---

## 2. OpenAI API

### Authentication Setup

```python
# Method 1: Environment Variable (Recommended)
import os
os.environ["OPENAI_API_KEY"] = "sk-..."

# Method 2: Direct Client Configuration
from openai import OpenAI

client = OpenAI(
    api_key="sk-...",  # Or use environment variable
    organization="org-...",  # Optional
    timeout=60.0,
    max_retries=3
)
```

### Chat Completions

```python
from openai import OpenAI

client = OpenAI()

# Basic completion
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": "You are a federal compliance expert."
        },
        {
            "role": "user",
            "content": "Explain FedRAMP authorization levels."
        }
    ],
    temperature=0.7,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Streaming Responses

```python
# Stream for real-time output
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Explain NIST 800-53"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

### Function Calling

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_regulations",
            "description": "Search federal regulations database",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "regulation_type": {
                        "type": "string",
                        "enum": ["FAR", "DFARS", "NIST", "OMB"],
                        "description": "Type of regulation"
                    }
                },
                "required": ["query"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Find FAR requirements for small business"}],
    tools=tools,
    tool_choice="auto"
)

# Handle tool calls
if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        print(f"Calling {function_name} with {arguments}")
```

---

## 3. Anthropic Claude API

### Authentication Setup

```python
import anthropic

# Using environment variable ANTHROPIC_API_KEY
client = anthropic.Anthropic()

# Or explicit configuration
client = anthropic.Anthropic(
    api_key="sk-ant-...",
    timeout=60.0,
    max_retries=3
)
```

### Messages API

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="You are a federal security analyst specializing in compliance.",
    messages=[
        {
            "role": "user",
            "content": "What are the key differences between FedRAMP Low, Moderate, and High?"
        }
    ]
)

print(message.content[0].text)
print(f"Input tokens: {message.usage.input_tokens}")
print(f"Output tokens: {message.usage.output_tokens}")
```

### Streaming

```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Explain FISMA requirements"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Tool Use

```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[
        {
            "name": "get_control_details",
            "description": "Get details about a NIST 800-53 security control",
            "input_schema": {
                "type": "object",
                "properties": {
                    "control_id": {
                        "type": "string",
                        "description": "Control ID (e.g., AC-2, AU-3)"
                    },
                    "baseline": {
                        "type": "string",
                        "enum": ["low", "moderate", "high"],
                        "description": "Security baseline"
                    }
                },
                "required": ["control_id"]
            }
        }
    ],
    messages=[{"role": "user", "content": "Tell me about control AC-2"}]
)

# Process tool use
for content in response.content:
    if content.type == "tool_use":
        print(f"Tool: {content.name}")
        print(f"Input: {content.input}")
```

### Vision (Image Analysis)

```python
import base64

# Read and encode image
with open("system_diagram.png", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode("utf-8")

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Analyze this system architecture for security concerns."
                }
            ]
        }
    ]
)
```

---

## 4. Google AI API

### Setup

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-pro")
```

### Generate Content

```python
response = model.generate_content(
    "Explain federal cloud security requirements",
    generation_config=genai.GenerationConfig(
        temperature=0.7,
        max_output_tokens=1024,
        top_p=0.9
    )
)

print(response.text)
```

### Chat Sessions

```python
chat = model.start_chat(history=[])

response = chat.send_message("What is FedRAMP?")
print(response.text)

response = chat.send_message("What are the authorization levels?")
print(response.text)

# Access history
for message in chat.history:
    print(f"{message.role}: {message.parts[0].text[:100]}...")
```

---

## 5. Azure OpenAI

### Configuration

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2024-02-01",
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
)
```

### Deployment-Based Calls

```python
# Azure uses deployment names instead of model names
response = client.chat.completions.create(
    model="gpt-4o-deployment",  # Your deployment name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)
```

### Government Cloud Configuration

```python
# Azure Government endpoints
client = AzureOpenAI(
    api_key=os.environ["AZURE_OPENAI_GOV_KEY"],
    api_version="2024-02-01",
    azure_endpoint="https://your-resource.openai.azure.us"  # .azure.us for Gov
)
```

---

## 6. AWS Bedrock

### Setup

```python
import boto3
import json

# Initialize Bedrock client
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1'
)
```

### Invoke Model

```python
# Claude on Bedrock
body = json.dumps({
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 1024,
    "messages": [
        {"role": "user", "content": "Explain AWS GovCloud compliance"}
    ]
})

response = bedrock.invoke_model(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=body,
    contentType="application/json",
    accept="application/json"
)

result = json.loads(response["body"].read())
print(result["content"][0]["text"])
```

### Streaming

```python
response = bedrock.invoke_model_with_response_stream(
    modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
    body=body,
    contentType="application/json"
)

for event in response["body"]:
    chunk = json.loads(event["chunk"]["bytes"])
    if chunk["type"] == "content_block_delta":
        print(chunk["delta"]["text"], end="", flush=True)
```

---

## 7. API Best Practices

### Error Handling

```python
from openai import OpenAI, APIError, RateLimitError, APIConnectionError
from tenacity import retry, stop_after_attempt, wait_exponential

client = OpenAI()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=60),
    retry=lambda e: isinstance(e, (RateLimitError, APIConnectionError))
)
def call_api_with_retry(messages):
    try:
        return client.chat.completions.create(
            model="gpt-4o",
            messages=messages
        )
    except RateLimitError as e:
        print(f"Rate limited, retrying: {e}")
        raise
    except APIConnectionError as e:
        print(f"Connection error, retrying: {e}")
        raise
    except APIError as e:
        print(f"API error: {e}")
        raise
```

### Rate Limiting

```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.timestamps = deque()

    def wait_if_needed(self):
        now = time.time()
        # Remove timestamps older than 1 minute
        while self.timestamps and now - self.timestamps[0] > 60:
            self.timestamps.popleft()

        if len(self.timestamps) >= self.rpm:
            sleep_time = 60 - (now - self.timestamps[0])
            if sleep_time > 0:
                time.sleep(sleep_time)

        self.timestamps.append(time.time())

# Usage
limiter = RateLimiter(requests_per_minute=50)

for request in requests:
    limiter.wait_if_needed()
    response = client.chat.completions.create(...)
```

### Cost Tracking

```python
from dataclasses import dataclass
from typing import Dict

@dataclass
class TokenUsage:
    input_tokens: int = 0
    output_tokens: int = 0

    def add(self, usage):
        self.input_tokens += usage.prompt_tokens
        self.output_tokens += usage.completion_tokens

    def cost(self, model: str) -> float:
        # Pricing per 1M tokens (as of 2025)
        pricing = {
            "gpt-4o": {"input": 2.50, "output": 10.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
        }
        rates = pricing.get(model, {"input": 0, "output": 0})
        return (
            (self.input_tokens / 1_000_000) * rates["input"] +
            (self.output_tokens / 1_000_000) * rates["output"]
        )

# Usage
tracker = TokenUsage()
response = client.chat.completions.create(...)
tracker.add(response.usage)
print(f"Total cost: ${tracker.cost('gpt-4o'):.4f}")
```

### Secure Configuration

```python
# NEVER hardcode API keys
# Use environment variables or secret management

import os
from pathlib import Path

def get_api_key(provider: str) -> str:
    """Get API key from environment or secure store."""
    env_var = f"{provider.upper()}_API_KEY"

    # Try environment variable first
    key = os.environ.get(env_var)
    if key:
        return key

    # Try .env file (for development only)
    env_file = Path.home() / ".env"
    if env_file.exists():
        for line in env_file.read_text().splitlines():
            if line.startswith(f"{env_var}="):
                return line.split("=", 1)[1].strip()

    raise ValueError(f"API key not found for {provider}")
```

---

## 🧪 Exercises

### Exercise 4.1: Multi-Provider Client
Build a unified client that can switch between OpenAI, Anthropic, and Google APIs.

### Exercise 4.2: Retry Logic
Implement robust retry logic with exponential backoff for a production API client.

### Exercise 4.3: Cost Calculator
Build a cost tracking system that monitors API usage across multiple providers.

### Exercise 4.4: Streaming Handler
Create a streaming response handler that works with all major providers.

---

## 📝 Assessment

### Knowledge Check

1. What are the authentication methods for each major API provider?
2. How do you implement proper rate limiting for federal workloads?
3. What error handling strategies should be used for production systems?
4. Which providers have FedRAMP authorization?
5. How do you track and optimize API costs?

---

## ➡️ Next Module

[Module 05: Prompt Engineering](../05-prompt-engineering/README.md)

---

<div align="center">

[⬆ Back to Top](#module-04-api-integration) · [📚 Return to Curriculum](../../README.md)

</div>
