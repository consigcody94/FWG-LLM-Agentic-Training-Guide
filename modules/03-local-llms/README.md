<div align="center">

# Module 03: Local LLMs

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_01-orange?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Install and configure Ollama for local LLM deployment
- [ ] Select appropriate models based on hardware and use case
- [ ] Deploy LM Studio, LocalAI, and alternative local solutions
- [ ] Understand quantization and its impact on performance
- [ ] Configure local deployments for federal compliance requirements
- [ ] Troubleshoot common local deployment issues

---

## Table of Contents

1. [Why Local LLMs?](#1-why-local-llms)
2. [Ollama Deep Dive](#2-ollama-deep-dive)
3. [LM Studio](#3-lm-studio)
4. [LocalAI](#4-localai)
5. [llama.cpp](#5-llamacpp)
6. [Hardware Requirements](#6-hardware-requirements)
7. [Model Selection Guide](#7-model-selection-guide)
8. [Federal Deployment Patterns](#8-federal-deployment-patterns)

---

## 1. Why Local LLMs?

### Benefits for Federal Use

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     LOCAL LLM ADVANTAGES                                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  🔒 DATA SOVEREIGNTY                                                         ║
║  ├── Data never leaves agency network                                        ║
║  ├── No third-party data processing                                          ║
║  ├── Complete audit trail control                                            ║
║  └── Meets air-gap requirements                                              ║
║                                                                              ║
║  💰 COST CONTROL                                                             ║
║  ├── No per-token API charges                                                ║
║  ├── Predictable infrastructure costs                                        ║
║  ├── No usage-based billing surprises                                        ║
║  └── Capital expense vs. operational expense                                 ║
║                                                                              ║
║  ⚡ LATENCY & AVAILABILITY                                                   ║
║  ├── No network round-trip to cloud                                          ║
║  ├── Works offline / air-gapped                                              ║
║  ├── No external service dependencies                                        ║
║  └── Consistent response times                                               ║
║                                                                              ║
║  🎯 CUSTOMIZATION                                                            ║
║  ├── Fine-tune on agency-specific data                                       ║
║  ├── Custom vocabulary and terminology                                       ║
║  ├── Specialized domain knowledge                                            ║
║  └── Full control over system prompts                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Trade-offs

| Aspect | Local LLM | Cloud API |
|:-------|:----------|:----------|
| **Capability** | 7-70B params typical | 100B+ params |
| **Setup Complexity** | Higher | Lower |
| **Maintenance** | Self-managed | Provider-managed |
| **Cost Model** | CapEx + power | OpEx per token |
| **Data Privacy** | Complete control | Provider dependent |
| **Availability** | Self-managed | Provider SLA |
| **Updates** | Manual | Automatic |

---

## 2. Ollama Deep Dive

### What is Ollama?

Ollama is a streamlined tool for running large language models locally with minimal configuration.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                           OLLAMA ARCHITECTURE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                    ┌────────────────────────────────────────┐                ║
║                    │           YOUR APPLICATION             │                ║
║                    │  (Python, CLI, Web App, Agent, etc.)   │                ║
║                    └────────────────────────────────────────┘                ║
║                                     │                                        ║
║                                     │ HTTP API (localhost:11434)             ║
║                                     ▼                                        ║
║                    ┌────────────────────────────────────────┐                ║
║                    │           OLLAMA SERVER                │                ║
║                    │                                        │                ║
║                    │  ┌──────────────────────────────────┐  │                ║
║                    │  │         Model Manager            │  │                ║
║                    │  │  • Pull models from registry     │  │                ║
║                    │  │  • Cache management              │  │                ║
║                    │  │  • Model switching               │  │                ║
║                    │  └──────────────────────────────────┘  │                ║
║                    │                                        │                ║
║                    │  ┌──────────────────────────────────┐  │                ║
║                    │  │       Inference Engine           │  │                ║
║                    │  │  • llama.cpp backend             │  │                ║
║                    │  │  • GPU acceleration (CUDA/Metal) │  │                ║
║                    │  │  • Quantization support          │  │                ║
║                    │  └──────────────────────────────────┘  │                ║
║                    │                                        │                ║
║                    └────────────────────────────────────────┘                ║
║                                     │                                        ║
║                    ┌────────────────┼────────────────┐                       ║
║                    │                │                │                       ║
║                    ▼                ▼                ▼                       ║
║              ┌──────────┐    ┌──────────┐    ┌──────────┐                   ║
║              │ llama3.2 │    │ mistral  │    │ codestral│                   ║
║              │   8B     │    │   7B     │    │   22B    │                   ║
║              └──────────┘    └──────────┘    └──────────┘                   ║
║                                                                              ║
║                           ~/.ollama/models/                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Installation

#### Linux
```bash
# One-line install
curl -fsSL https://ollama.ai/install.sh | sh

# Verify installation
ollama --version
```

#### macOS
```bash
# Download from ollama.ai or use Homebrew
brew install ollama

# Start the service
ollama serve
```

#### Windows
```powershell
# Download installer from ollama.ai
# Or use winget
winget install Ollama.Ollama
```

### Essential Commands

```bash
# Pull a model
ollama pull llama3.2

# List installed models
ollama list

# Run interactive chat
ollama run llama3.2

# Run with specific prompt
ollama run llama3.2 "Explain the FISMA compliance framework"

# Show model details
ollama show llama3.2

# Remove a model
ollama rm llama3.2

# Copy/create custom model
ollama create mymodel -f Modelfile
```

### API Usage

```python
# Python with ollama library
import ollama

# Simple chat
response = ollama.chat(
    model='llama3.2',
    messages=[
        {
            'role': 'system',
            'content': 'You are a federal compliance assistant.'
        },
        {
            'role': 'user',
            'content': 'What are the key requirements of FedRAMP?'
        }
    ]
)
print(response['message']['content'])

# Streaming response
for chunk in ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Explain NIST 800-53'}],
    stream=True
):
    print(chunk['message']['content'], end='', flush=True)
```

```bash
# Direct HTTP API usage
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}'
```

### Custom Modelfiles

```dockerfile
# Modelfile for federal compliance assistant
FROM llama3.2

# Set system prompt
SYSTEM """
You are a Federal Compliance Assistant specializing in:
- FedRAMP authorization
- FISMA requirements
- NIST frameworks (800-53, AI RMF)
- OMB memoranda and directives

Always cite specific control numbers and document references.
Be precise and avoid speculation on compliance matters.
"""

# Adjust parameters
PARAMETER temperature 0.3
PARAMETER top_p 0.9
PARAMETER num_ctx 8192

# Set stop tokens
PARAMETER stop "<|end|>"
PARAMETER stop "Human:"
```

```bash
# Create the custom model
ollama create federal-assistant -f Modelfile

# Run the custom model
ollama run federal-assistant
```

### Popular Ollama Models

| Model | Params | RAM Required | Best For |
|:------|:------:|:------------:|:---------|
| **llama3.2** | 3B | 4GB | Quick tasks, chat |
| **llama3.2** | 8B | 8GB | General purpose |
| **llama3.1** | 70B | 48GB+ | Complex reasoning |
| **mistral** | 7B | 6GB | Fast, efficient |
| **mixtral** | 8x7B | 26GB | Multi-expert tasks |
| **codestral** | 22B | 16GB | Code generation |
| **qwen2.5** | 7B-72B | 6-48GB | Multilingual |
| **phi3** | 3.8B | 4GB | Lightweight tasks |
| **gemma2** | 9B-27B | 8-20GB | Google quality |

---

## 3. LM Studio

### Overview

LM Studio provides a user-friendly GUI for running local models with easy model discovery and management.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          LM STUDIO INTERFACE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │  🔍 Discover    💬 Chat    🖥️ Local Server    ⚙️ Settings           │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌─────────────────────┬────────────────────────────────────────────────┐   ║
║  │                     │                                                 │   ║
║  │  MODEL BROWSER      │              CHAT INTERFACE                     │   ║
║  │                     │                                                 │   ║
║  │  Search models...   │  Model: Llama-3.2-8B-Instruct-Q4_K_M           │   ║
║  │                     │                                                 │   ║
║  │  📦 Downloaded      │  ┌─────────────────────────────────────────┐   │   ║
║  │  ├─ Llama 3.2 8B   │  │ User: Explain federal AI governance     │   │   ║
║  │  ├─ Mistral 7B     │  └─────────────────────────────────────────┘   │   ║
║  │  └─ CodeLlama 13B  │                                                 │   ║
║  │                     │  ┌─────────────────────────────────────────┐   │   ║
║  │  🌐 Available       │  │ Assistant: Federal AI governance is     │   │   ║
║  │  ├─ Mixtral 8x7B   │  │ guided by Executive Order 14110...      │   │   ║
║  │  ├─ Qwen2 72B      │  └─────────────────────────────────────────┘   │   ║
║  │  └─ DeepSeek       │                                                 │   ║
║  │                     │  ┌─────────────────────────────────────────┐   │   ║
║  │  PARAMETERS         │  │ Type your message...                    │   │   ║
║  │  Temperature: 0.7   │  └─────────────────────────────────────────┘   │   ║
║  │  Top P: 0.9         │                                                 │   ║
║  │  Context: 4096      │  [GPU: 95%] [RAM: 12.4GB] [Tokens/s: 42]       │   ║
║  │                     │                                                 │   ║
║  └─────────────────────┴────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Key Features

- **Model Discovery:** Browse and download from Hugging Face
- **Quantization Selection:** Choose GGUF quantization levels
- **Local Server:** OpenAI-compatible API server
- **GPU Layers:** Fine-grained GPU memory control
- **Chat Presets:** Save conversation templates

### Local Server Mode

```bash
# Start server (GUI or command line)
# Default: http://localhost:1234/v1

# Use with OpenAI library
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # Not required, but needed for library
)

response = client.chat.completions.create(
    model="local-model",  # Model loaded in LM Studio
    messages=[
        {"role": "user", "content": "Hello!"}
    ]
)
```

---

## 4. LocalAI

### Overview

LocalAI is an OpenAI-compatible API server that supports multiple model formats and backends.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          LOCALAI ARCHITECTURE                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────┐     ║
║  │                     LOCALAI SERVER                                  │     ║
║  │                                                                     │     ║
║  │  OpenAI-Compatible API Endpoints:                                  │     ║
║  │  ├── /v1/chat/completions                                          │     ║
║  │  ├── /v1/completions                                               │     ║
║  │  ├── /v1/embeddings                                                │     ║
║  │  ├── /v1/images/generations                                        │     ║
║  │  ├── /v1/audio/transcriptions                                      │     ║
║  │  └── /v1/audio/speech                                              │     ║
║  │                                                                     │     ║
║  │  ┌───────────────────────────────────────────────────────────────┐ │     ║
║  │  │                    BACKEND SUPPORT                            │ │     ║
║  │  │                                                                │ │     ║
║  │  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐│ │     ║
║  │  │  │llama.cpp│ │ GPT4All │ │  RWKV   │ │Whisper  │ │Stable   ││ │     ║
║  │  │  │         │ │         │ │         │ │         │ │Diffusion││ │     ║
║  │  │  │  Text   │ │  Text   │ │  Text   │ │  Audio  │ │ Image   ││ │     ║
║  │  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘│ │     ║
║  │  │                                                                │ │     ║
║  │  └───────────────────────────────────────────────────────────────┘ │     ║
║  │                                                                     │     ║
║  └────────────────────────────────────────────────────────────────────┘     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Docker Deployment

```yaml
# docker-compose.yml
version: '3.8'
services:
  localai:
    image: localai/localai:latest-aio-cpu
    # For GPU: localai/localai:latest-aio-gpu-nvidia-cuda-12
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    environment:
      - THREADS=4
      - CONTEXT_SIZE=4096

# Run
# docker-compose up -d
```

### Model Configuration

```yaml
# models/llama3.yaml
name: llama3
backend: llama-cpp
parameters:
  model: llama-3-8b-instruct.Q4_K_M.gguf
  temperature: 0.7
  top_p: 0.9
  context_size: 8192

template:
  chat_message: |
    <|start_header_id|>{{.RoleName}}<|end_header_id|>

    {{.Content}}<|eot_id|>
  chat: |
    {{.Input}}
    <|start_header_id|>assistant<|end_header_id|>
```

---

## 5. llama.cpp

### Overview

llama.cpp is the foundational C++ library that powers most local LLM tools, including Ollama and LM Studio.

### Direct Usage

```bash
# Clone and build
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
make -j

# With CUDA support
make LLAMA_CUDA=1 -j

# Run inference
./llama-cli -m models/llama-3-8b.Q4_K_M.gguf \
  -p "Explain federal procurement regulations" \
  -n 512 \
  --ctx-size 4096

# Start server
./llama-server -m models/llama-3-8b.Q4_K_M.gguf \
  --host 0.0.0.0 --port 8080
```

### Python Bindings

```python
from llama_cpp import Llama

llm = Llama(
    model_path="models/llama-3-8b.Q4_K_M.gguf",
    n_ctx=8192,
    n_gpu_layers=35  # Offload layers to GPU
)

output = llm(
    "Q: What is FedRAMP? A:",
    max_tokens=256,
    stop=["Q:", "\n\n"],
    echo=True
)
print(output["choices"][0]["text"])
```

---

## 6. Hardware Requirements

### GPU Memory Requirements

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                       VRAM REQUIREMENTS BY MODEL SIZE                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Model Size    │ FP16  │  Q8   │  Q4   │ Recommended GPU                    ║
║  ──────────────┼───────┼───────┼───────┼─────────────────────────────────   ║
║     3B         │  6GB  │  4GB  │  2GB  │ GTX 1660 / RTX 3060                ║
║     7B         │ 14GB  │  8GB  │  4GB  │ RTX 3060 12GB / RTX 4060           ║
║    13B         │ 26GB  │ 14GB  │  8GB  │ RTX 3090 / RTX 4070 Ti             ║
║    34B         │ 68GB  │ 36GB  │ 20GB  │ 2x RTX 3090 / RTX 4090             ║
║    70B         │140GB  │ 75GB  │ 40GB  │ 2x RTX 4090 / A100 40GB            ║
║                                                                              ║
║  Note: Q4 = 4-bit quantization, Q8 = 8-bit quantization                     ║
║        FP16 = Full precision (rarely used locally)                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### System RAM Requirements

| Model (Q4) | Minimum RAM | Recommended RAM |
|:-----------|:-----------:|:---------------:|
| 3B | 8GB | 16GB |
| 7B | 16GB | 32GB |
| 13B | 32GB | 64GB |
| 34B | 64GB | 128GB |
| 70B | 128GB | 256GB |

### Recommended Configurations

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    RECOMMENDED FEDERAL CONFIGURATIONS                        ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TIER 1: DEVELOPMENT WORKSTATION ($2,000-3,000)                             ║
║  ├── CPU: AMD Ryzen 9 / Intel i9                                             ║
║  ├── RAM: 64GB DDR5                                                          ║
║  ├── GPU: NVIDIA RTX 4070 Ti (16GB)                                          ║
║  ├── Storage: 2TB NVMe SSD                                                   ║
║  └── Capable Models: Up to 13B Q4, 7B Q8                                     ║
║                                                                              ║
║  TIER 2: POWER WORKSTATION ($5,000-8,000)                                   ║
║  ├── CPU: AMD Threadripper / Intel Xeon                                      ║
║  ├── RAM: 128GB DDR5                                                         ║
║  ├── GPU: NVIDIA RTX 4090 (24GB)                                             ║
║  ├── Storage: 4TB NVMe SSD                                                   ║
║  └── Capable Models: Up to 34B Q4, 13B Q8                                    ║
║                                                                              ║
║  TIER 3: SERVER DEPLOYMENT ($15,000-30,000)                                 ║
║  ├── CPU: Dual AMD EPYC / Intel Xeon                                         ║
║  ├── RAM: 256GB+ DDR5                                                        ║
║  ├── GPU: 2x NVIDIA A100 (80GB) or 4x RTX 4090                               ║
║  ├── Storage: 8TB NVMe RAID                                                  ║
║  └── Capable Models: 70B+ Q4, 34B+ Q8                                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 7. Model Selection Guide

### Decision Framework

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        MODEL SELECTION DECISION TREE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                              START HERE                                      ║
║                                  │                                           ║
║                                  ▼                                           ║
║                    ┌─────────────────────────────┐                          ║
║                    │   What's your VRAM budget?  │                          ║
║                    └─────────────────────────────┘                          ║
║                         │              │                                     ║
║              ≤8GB       │              │      >16GB                          ║
║                         ▼              ▼                                     ║
║            ┌──────────────────┐  ┌──────────────────┐                       ║
║            │  3B-7B Models    │  │  13B-70B Models  │                       ║
║            │  • Llama 3.2 3B  │  │  • Llama 3.1 70B │                       ║
║            │  • Phi-3 3.8B    │  │  • Qwen2 72B     │                       ║
║            │  • Gemma 2B      │  │  • Mixtral 8x7B  │                       ║
║            └──────────────────┘  └──────────────────┘                       ║
║                         │              │                                     ║
║                         ▼              ▼                                     ║
║                    ┌─────────────────────────────┐                          ║
║                    │   What's your primary task? │                          ║
║                    └─────────────────────────────┘                          ║
║                    /        |        |        \                              ║
║                   /         |        |         \                             ║
║              General     Code    Reasoning   Multi-                          ║
║               Chat      Gen      Tasks      lingual                          ║
║                 │         │        │           │                             ║
║                 ▼         ▼        ▼           ▼                             ║
║            ┌───────┐ ┌────────┐ ┌───────┐ ┌────────┐                        ║
║            │Llama 3│ │Codestral│ │Mixtral│ │ Qwen2  │                        ║
║            │Mistral│ │DeepSeek │ │Llama  │ │Command │                        ║
║            └───────┘ └────────┘ └───────┘ └────────┘                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Model Comparison by Task

| Task | Best Models | Alternative |
|:-----|:------------|:------------|
| **General Chat** | Llama 3.2, Mistral | Qwen2, Gemma2 |
| **Code Generation** | Codestral, DeepSeek-Coder | CodeLlama, Starcoder |
| **Document Analysis** | Llama 3.1 70B, Qwen2 | Mixtral 8x7B |
| **Reasoning** | Mixtral, Llama 3.1 | Qwen2-Math |
| **Multilingual** | Qwen2, Aya | Llama 3.1 |
| **Fast Responses** | Phi-3, Gemma 2B | Llama 3.2 3B |

---

## 8. Federal Deployment Patterns

### Air-Gapped Deployment

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      AIR-GAPPED DEPLOYMENT PATTERN                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  INTERNET                         │ AIR-GAP │    SECURE NETWORK             ║
║                                   │         │                                ║
║  ┌─────────────────┐             │         │    ┌─────────────────┐        ║
║  │ Model Registry  │             │         │    │ Transfer        │        ║
║  │ (Hugging Face)  │─────────────┤ DIODE   ├───▶│ Station         │        ║
║  └─────────────────┘   Download  │         │    └────────┬────────┘        ║
║                        Models    │         │             │                  ║
║  ┌─────────────────┐             │         │             │ USB/DVD          ║
║  │ Ollama Registry │─────────────┤         ├───▶        │ Transfer         ║
║  └─────────────────┘             │         │             ▼                  ║
║                                   │         │    ┌─────────────────┐        ║
║                                   │         │    │ Local Ollama    │        ║
║                                   │         │    │ Server          │        ║
║                                   │         │    │                 │        ║
║                                   │         │    │ • No internet   │        ║
║                                   │         │    │ • Local models  │        ║
║                                   │         │    │ • Audit logs    │        ║
║                                   │         │    └─────────────────┘        ║
║                                   │         │             │                  ║
║                                   │         │             ▼                  ║
║                                   │         │    ┌─────────────────┐        ║
║                                   │         │    │ Client Apps     │        ║
║                                   │         │    └─────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Containerized Deployment

```yaml
# docker-compose.yml for Federal Deployment
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    restart: unless-stopped
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
      - ./audit_logs:/var/log/ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

  # Audit logging sidecar
  fluentd:
    image: fluent/fluentd:v1.16
    volumes:
      - ./audit_logs:/var/log/ollama:ro
      - ./fluentd.conf:/fluentd/etc/fluent.conf

volumes:
  ollama_data:
```

### Kubernetes Deployment

```yaml
# ollama-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ai-services
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      containers:
      - name: ollama
        image: ollama/ollama:latest
        ports:
        - containerPort: 11434
        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
          requests:
            memory: "16Gi"
        volumeMounts:
        - name: models
          mountPath: /root/.ollama
      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: ai-services
spec:
  selector:
    app: ollama
  ports:
  - port: 11434
    targetPort: 11434
  type: ClusterIP
```

---

## Exercises

### Exercise 3.1: Ollama Setup
Install Ollama and run your first local model. Test with federal-themed prompts.

### Exercise 3.2: Custom Modelfile
Create a custom Modelfile for a federal compliance assistant with appropriate system prompts.

### Exercise 3.3: Performance Benchmarking
Compare response times and quality across different model sizes and quantization levels.

### Exercise 3.4: API Integration
Build a simple Python application that uses the Ollama API for document summarization.

---

## Assessment

### Knowledge Check

1. What are the primary advantages of local LLMs for federal use?
2. Explain the difference between Q4 and Q8 quantization.
3. How much VRAM is typically needed for a 13B parameter model at Q4?
4. What is the purpose of a Modelfile in Ollama?
5. Describe an air-gapped deployment pattern for local LLMs.

### Practical Assessment

Deploy Ollama with a custom Modelfile, configure appropriate system prompts for federal use, and demonstrate API integration with a client application.

---

## Next Module

➡️ [Module 04: API Integration](../04-api-integration/README.md)

---

<div align="center">

[⬆ Back to Top](#module-03-local-llms) · [📚 Return to Curriculum](../../README.md)

</div>
