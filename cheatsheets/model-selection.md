# Model Selection Guide

<div align="center">

**Choosing the Right LLM for Your Federal Use Case**

</div>

---

## Quick Decision Matrix

### By Use Case

| Use Case | Recommended Model(s) | Rationale |
|----------|---------------------|-----------|
| **General Q&A** | GPT-4o-mini, Claude 3.5 Haiku | Cost-effective, fast |
| **Complex Reasoning** | GPT-4o, Claude 3.5 Sonnet | Best reasoning capabilities |
| **Code Generation** | Claude 3.5 Sonnet, GPT-4o | Strong code understanding |
| **Document Analysis** | Claude 3.5 Sonnet (200K) | Largest context window |
| **Multimodal (Vision)** | GPT-4o, Gemini Pro | Native image support |
| **Local/Air-gapped** | Llama 3.1 70B, Mixtral | No external API needed |
| **Cost-Sensitive** | Llama 3.2, Mistral 7B | Open-source, self-hosted |
| **Sensitive Data** | Azure OpenAI, AWS Bedrock | FedRAMP-authorized |

---

## Model Comparison Chart (2025)

### Cloud API Models

| Provider | Model | Context | Input $/1M | Output $/1M | Speed | Quality |
|----------|-------|---------|------------|-------------|-------|---------|
| **OpenAI** | GPT-4o | 128K | $2.50 | $10.00 | Fast | ★★★★★ |
| **OpenAI** | GPT-4o-mini | 128K | $0.15 | $0.60 | V.Fast | ★★★★☆ |
| **OpenAI** | o1 | 200K | $15.00 | $60.00 | Slow | ★★★★★+ |
| **Anthropic** | Claude 3.5 Sonnet | 200K | $3.00 | $15.00 | Fast | ★★★★★ |
| **Anthropic** | Claude 3.5 Haiku | 200K | $0.25 | $1.25 | V.Fast | ★★★★☆ |
| **Google** | Gemini 1.5 Pro | 1M+ | $1.25 | $5.00 | Fast | ★★★★★ |
| **Google** | Gemini 1.5 Flash | 1M+ | $0.075 | $0.30 | V.Fast | ★★★★☆ |

### Local/Open-Source Models

| Model | Parameters | VRAM Needed | Speed | Quality | License |
|-------|------------|-------------|-------|---------|---------|
| **Llama 3.1 405B** | 405B | 200GB+ | Slow | ★★★★★ | Llama 3.1 |
| **Llama 3.1 70B** | 70B | 40-80GB | Medium | ★★★★☆ | Llama 3.1 |
| **Llama 3.2 8B** | 8B | 6-8GB | Fast | ★★★☆☆ | Llama 3.2 |
| **Mixtral 8x7B** | 47B | 24-48GB | Medium | ★★★★☆ | Apache 2.0 |
| **Mistral 7B** | 7B | 6-8GB | Fast | ★★★☆☆ | Apache 2.0 |
| **Phi-3 Medium** | 14B | 8-16GB | Fast | ★★★☆☆ | MIT |
| **Qwen 2.5 72B** | 72B | 40-80GB | Medium | ★★★★☆ | Apache 2.0 |

---

## FedRAMP Availability

### Currently Authorized

| Platform | Authorization | Model Access |
|----------|---------------|--------------|
| **Azure OpenAI** | FedRAMP High | GPT-4, GPT-4o |
| **AWS Bedrock** | FedRAMP High | Claude 3, Llama 2, Titan |
| **Google Cloud Vertex AI** | FedRAMP Moderate | Gemini, PaLM |

### Authorization Status

```
✅ FedRAMP Authorized
⚠️  In Process / Limited
❌ Not Authorized

Azure OpenAI GCC High    ✅
AWS Bedrock GovCloud     ✅
Google Cloud GCC         ✅
Anthropic Direct API     ⚠️  (in process)
OpenAI Direct API        ⚠️  (in process)
```

---

## Context Window Guide

### What Fits in Each Context Size

| Context | Approximate Capacity |
|---------|---------------------|
| **4K tokens** | ~3,000 words, ~6 pages |
| **8K tokens** | ~6,000 words, ~12 pages |
| **32K tokens** | ~24,000 words, ~48 pages |
| **128K tokens** | ~96,000 words, ~200 pages |
| **200K tokens** | ~150,000 words, ~300 pages |
| **1M+ tokens** | ~750,000 words, book-length |

### Context Utilization Tips

```python
# Estimate tokens (rough approximation)
def estimate_tokens(text):
    words = len(text.split())
    return int(words * 1.3)

# Check if content fits
def will_fit(content, model_context, buffer=0.1):
    tokens = estimate_tokens(content)
    usable = model_context * (1 - buffer)  # Leave room for response
    return tokens < usable
```

---

## Cost Optimization Strategies

### 1. Model Tiering

```
Simple queries     → GPT-4o-mini / Claude Haiku
                     Cost: ~$0.15-0.25 per 1M tokens

Standard queries   → GPT-4o / Claude Sonnet
                     Cost: ~$3-5 per 1M tokens

Complex reasoning  → o1 / Claude Opus
                     Cost: ~$15-60 per 1M tokens
```

### 2. Token Reduction

```python
# Before: 150 tokens
prompt = """Please analyze the following document and
provide a comprehensive summary highlighting all the
key points, main arguments, and conclusions that
can be drawn from the text provided below."""

# After: 20 tokens
prompt = "Summarize key points from this document:"
```

### 3. Caching Strategies

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_query(prompt_hash: str, model: str) -> str:
    # Cache identical queries
    return api.complete(prompt, model=model)

def query_with_cache(prompt: str, model: str) -> str:
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()
    return cached_query(prompt_hash, model)
```

### 4. Prompt Engineering for Efficiency

```
✗ Long-winded: "I would like you to please help me by..."
✓ Efficient: "Help me..."

✗ Repetitive context in each message
✓ Use system prompts for stable context

✗ Requesting verbose explanations always
✓ "Be concise" when detail isn't needed
```

---

## Performance Benchmarks

### Speed Comparison (Tokens/Second)

```
Fastest                              Slowest
├────────────────────────────────────────────┤
│ Gemini Flash    ████████████████████  500+ │
│ GPT-4o-mini     ██████████████████    450  │
│ Claude Haiku    █████████████████     400  │
│ GPT-4o          ████████████          250  │
│ Claude Sonnet   ███████████           280  │
│ Gemini Pro      █████████             200  │
│ Claude Opus     █████                 100  │
│ o1 (reasoning)  ██                    50   │
└────────────────────────────────────────────┘
```

### Quality Benchmarks (MMLU)

```
Most Capable                    Baseline
├────────────────────────────────────────┤
│ o1              ████████████████  92%  │
│ Claude 3 Opus   ███████████████   88%  │
│ GPT-4o          ██████████████    87%  │
│ Claude Sonnet   █████████████     85%  │
│ Gemini Pro      ████████████      84%  │
│ Llama 3.1 405B  ███████████       83%  │
│ GPT-4o-mini     ██████████        80%  │
│ Llama 3.1 70B   █████████         79%  │
│ Claude Haiku    ████████          77%  │
│ Mixtral 8x7B    ███████           75%  │
└────────────────────────────────────────┘
```

---

## Capability Matrix

### Feature Support

| Feature | GPT-4o | Claude 3.5 | Gemini | Llama 3.1 |
|---------|--------|------------|--------|-----------|
| Function Calling | ✅ | ✅ | ✅ | ✅ |
| Vision/Images | ✅ | ✅ | ✅ | ❌ |
| Streaming | ✅ | ✅ | ✅ | ✅ |
| JSON Mode | ✅ | ✅ | ✅ | Varies |
| System Prompts | ✅ | ✅ | ✅ | ✅ |
| MCP Support | ❌ | ✅ | ✅ | ❌ |
| Tool Use | ✅ | ✅ | ✅ | ✅ |
| Batch API | ✅ | ✅ | ❌ | N/A |

### Special Capabilities

```
Code Generation Excellence:
  1. Claude 3.5 Sonnet (best overall)
  2. GPT-4o
  3. Llama 3.1 70B

Long Context Processing:
  1. Gemini 1.5 Pro (1M+)
  2. Claude 3.5 (200K)
  3. GPT-4o (128K)

Reasoning/Analysis:
  1. o1 (dedicated reasoning)
  2. Claude 3 Opus
  3. GPT-4o

Multimodal (Vision):
  1. GPT-4o (best vision)
  2. Gemini Pro
  3. Claude 3.5 Sonnet
```

---

## Selection Flowchart

```
                        START
                          │
                          ▼
          ┌───────────────────────────┐
          │ Is data classification    │
          │ above PUBLIC?             │
          └───────────────┬───────────┘
                          │
              ┌───────────┴───────────┐
              ▼ Yes                   ▼ No
    ┌─────────────────────┐   ┌─────────────────────┐
    │ Use FedRAMP-        │   │ Any cloud provider  │
    │ authorized platform │   │ acceptable          │
    │ (Azure, AWS, GCP)   │   └─────────┬───────────┘
    └─────────┬───────────┘             │
              │                         │
              ▼                         ▼
    ┌─────────────────────┐   ┌─────────────────────┐
    │ Air-gapped/         │   │ Need complex        │
    │ on-premises needed? │   │ reasoning?          │
    └─────────┬───────────┘   └─────────┬───────────┘
              │                         │
    ┌─────────┴─────────┐     ┌─────────┴─────────┐
    ▼ Yes               ▼ No  ▼ Yes               ▼ No
┌───────────┐    ┌───────────┐ ┌───────────┐    ┌───────────┐
│ Llama 3.1 │    │ Azure     │ │ o1 or     │    │ Check     │
│ or        │    │ OpenAI,   │ │ Claude    │    │ cost vs   │
│ Mixtral   │    │ Bedrock   │ │ Opus      │    │ speed     │
│ (local)   │    │           │ │           │    │ needs     │
└───────────┘    └───────────┘ └───────────┘    └─────┬─────┘
                                                      │
                              ┌────────────────┬──────┴──────┐
                              ▼                ▼             ▼
                        ┌──────────┐    ┌──────────┐  ┌──────────┐
                        │ Cost:    │    │ Speed:   │  │ Balance: │
                        │ GPT-4o-  │    │ Gemini   │  │ GPT-4o   │
                        │ mini,    │    │ Flash,   │  │ Claude   │
                        │ Haiku    │    │ Haiku    │  │ Sonnet   │
                        └──────────┘    └──────────┘  └──────────┘
```

---

## Quick Reference Commands

### Check Model Availability (Ollama)

```bash
# List available models
ollama list

# Search for models
ollama search llama

# Pull a specific model
ollama pull llama3.2:latest
```

### Compare Models in Code

```python
models = [
    {"name": "gpt-4o-mini", "provider": "openai"},
    {"name": "claude-3-5-sonnet-20241022", "provider": "anthropic"},
]

for model in models:
    response = query(prompt, model=model["name"])
    print(f"{model['name']}: {len(response)} chars, {response[:100]}...")
```

---

## Model Versioning Note

```
⚠️ Always pin model versions in production

✗ model="gpt-4"           # Can change unexpectedly
✓ model="gpt-4-0613"      # Specific version

✗ model="claude-3-sonnet" # Generic
✓ model="claude-3-5-sonnet-20241022" # Specific
```

---

<div align="center">

**Choose wisely. Evaluate thoroughly. Iterate continuously.**

</div>
