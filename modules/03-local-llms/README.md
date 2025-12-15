<div align="center">

# Module 03: Local LLMs

<img src="https://img.shields.io/badge/Duration-6_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Intermediate-yellow?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_01-orange?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Install and configure Ollama for local LLM deployment
- [ ] Select appropriate models based on hardware and use case
- [ ] Deploy LM Studio, LocalAI, and alternative local solutions
- [ ] Understand quantization techniques and their impact on model quality
- [ ] Configure local deployments for federal compliance requirements
- [ ] Troubleshoot common local deployment issues
- [ ] Build production-ready local AI infrastructure

---

## Table of Contents

1. [Why Local LLMs?](#1-why-local-llms)
2. [Understanding Local LLM Infrastructure](#2-understanding-local-llm-infrastructure)
3. [Ollama Deep Dive](#3-ollama-deep-dive)
4. [LM Studio](#4-lm-studio)
5. [LocalAI](#5-localai)
6. [llama.cpp: The Engine Behind Local LLMs](#6-llamacpp-the-engine-behind-local-llms)
7. [Quantization: Making Models Fit Your Hardware](#7-quantization-making-models-fit-your-hardware)
8. [Hardware Requirements and Optimization](#8-hardware-requirements-and-optimization)
9. [Model Selection Guide](#9-model-selection-guide)
10. [Federal Deployment Patterns](#10-federal-deployment-patterns)
11. [Troubleshooting Guide](#11-troubleshooting-guide)

---

## 1. Why Local LLMs?

### The Fundamental Question: Cloud vs Local

Before diving into technical implementation, we need to understand **why** an organization would choose to run AI models locally instead of using cloud APIs like OpenAI or Anthropic. This decision involves weighing several critical factors that directly impact federal operations.

### Understanding the Trade-offs

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     LOCAL LLM vs CLOUD API: THE COMPLETE PICTURE             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  CLOUD APIs (OpenAI, Anthropic, etc.)                                       ║
║  ─────────────────────────────────────                                       ║
║  ✅ Largest, most capable models (GPT-4, Claude)                            ║
║  ✅ No infrastructure management                                             ║
║  ✅ Automatic updates and improvements                                       ║
║  ✅ Enterprise support available                                             ║
║  ❌ Data leaves your network                                                 ║
║  ❌ Per-token costs (can scale rapidly)                                      ║
║  ❌ Internet dependency                                                      ║
║  ❌ Third-party data processing                                              ║
║  ❌ Limited customization                                                    ║
║                                                                              ║
║  LOCAL LLMs (Ollama, LM Studio, etc.)                                       ║
║  ─────────────────────────────────────                                       ║
║  ✅ Complete data sovereignty                                                ║
║  ✅ Works offline/air-gapped                                                 ║
║  ✅ Predictable infrastructure costs                                         ║
║  ✅ Full customization and fine-tuning                                       ║
║  ✅ No per-token charges                                                     ║
║  ❌ Smaller models (typically 7B-70B)                                        ║
║  ❌ Hardware investment required                                             ║
║  ❌ Self-managed infrastructure                                              ║
║  ❌ Requires technical expertise                                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Benefits for Federal Use: A Deep Dive

#### 1. Data Sovereignty

For federal agencies, data sovereignty isn't just a preference—it's often a legal requirement. When you use a cloud API:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        CLOUD API DATA FLOW                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   Your Agency Network                Cloud Provider                         ║
║   ═══════════════════                ══════════════                         ║
║                                                                              ║
║   ┌─────────────────┐     HTTPS      ┌─────────────────┐                   ║
║   │                 │────────────────▶│                 │                   ║
║   │  Your Prompt    │                │  API Endpoint   │                   ║
║   │  (Contains      │◀───────────────│                 │                   ║
║   │   Your Data)    │    Response    │  - Logs stored  │                   ║
║   │                 │                │  - May train    │                   ║
║   └─────────────────┘                │    models       │                   ║
║                                      │  - Third-party  │                   ║
║                                      │    processing   │                   ║
║                                      └─────────────────┘                   ║
║                                                                              ║
║   CONCERN: Your data traverses networks you don't control                   ║
║            and is processed on systems you don't own.                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

With local LLMs:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        LOCAL LLM DATA FLOW                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   Your Agency Network (EVERYTHING STAYS HERE)                               ║
║   ═══════════════════════════════════════════                               ║
║                                                                              ║
║   ┌─────────────────┐    Localhost   ┌─────────────────┐                   ║
║   │                 │────────────────▶│                 │                   ║
║   │  Your Prompt    │                │  Ollama Server  │                   ║
║   │  (Contains      │◀───────────────│                 │                   ║
║   │   Your Data)    │    Response    │  - Your logs    │                   ║
║   │                 │                │  - Your control │                   ║
║   └─────────────────┘                │  - Your data    │                   ║
║                                      └─────────────────┘                   ║
║                                                                              ║
║   ✅ Data NEVER leaves your network                                         ║
║   ✅ Complete audit trail under your control                                ║
║   ✅ No third-party access to your information                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Why This Matters for Federal Agencies:**

- **FISMA Compliance**: The Federal Information Security Modernization Act requires agencies to protect federal information systems. When data leaves your network, you introduce additional attack surfaces and compliance requirements.

- **Controlled Unclassified Information (CUI)**: Many federal documents contain CUI that cannot be processed by third parties without specific agreements and controls.

- **Privacy Act Data**: Personal information protected under the Privacy Act has strict handling requirements that cloud APIs may not satisfy.

- **Mission-Critical Operations**: For defense, intelligence, and law enforcement, the ability to function without internet connectivity is essential.

#### 2. Cost Control and Predictability

Understanding the cost dynamics helps justify local LLM investments:

**Cloud API Cost Model:**
```
Per-Token Pricing Example (approximate):
─────────────────────────────────────────
GPT-4: ~$30/million input tokens, ~$60/million output tokens
Claude 3 Opus: ~$15/million input, ~$75/million output

Example Usage Scenario:
─────────────────────────────────────────
• 100 employees
• 50 prompts per employee per day
• Average 1,000 tokens per prompt
• 500 tokens average response

Daily token usage:
- Input: 100 × 50 × 1,000 = 5,000,000 tokens
- Output: 100 × 50 × 500 = 2,500,000 tokens

Daily cost (GPT-4): ~$150 input + ~$150 output = ~$300/day
Monthly cost: ~$6,600
Annual cost: ~$79,200

And this scales linearly with usage!
```

**Local LLM Cost Model:**
```
Capital Investment:
─────────────────────────────────────────
• Development workstation: $3,000-5,000 (one-time)
• Server deployment: $15,000-30,000 (one-time)
• Power and cooling: ~$50-200/month
• IT staff time: Variable (existing staff can often manage)

Key Difference: Costs are FIXED, not usage-based
─────────────────────────────────────────
• 10 queries or 10,000 queries = same infrastructure cost
• Unlimited users once deployed
• 3-5 year hardware lifecycle
```

#### 3. Latency and Availability

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      LATENCY COMPARISON                                      ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Cloud API Request Path:                                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  User → Agency Firewall → Internet → Cloud Firewall → Load Balancer →      ║
║  API Gateway → Inference Server → ... reverse path back                     ║
║                                                                              ║
║  Typical latency: 200ms - 2000ms (depends on model and load)               ║
║  Additional concerns:                                                        ║
║  • Internet outages = service unavailable                                   ║
║  • Cloud provider issues = service unavailable                              ║
║  • Rate limiting during high demand                                         ║
║  • Unpredictable queue times                                                ║
║                                                                              ║
║  Local LLM Request Path:                                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  User → Local Server → Response                                             ║
║                                                                              ║
║  Typical latency: 50ms - 500ms (depends on model and hardware)             ║
║  Advantages:                                                                 ║
║  • Works offline                                                             ║
║  • No external dependencies                                                  ║
║  • Consistent performance                                                    ║
║  • No rate limits                                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### The Trade-off Reality: Model Capability

The most significant trade-off with local LLMs is model capability. Let's be honest about this:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MODEL CAPABILITY COMPARISON                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Cloud Models (Frontier Capabilities)                                       ║
║  ────────────────────────────────────                                        ║
║  • GPT-4: ~1.8 trillion parameters (estimated)                              ║
║  • Claude 3 Opus: Unknown size, but massive                                 ║
║  • Gemini Ultra: Massive multimodal model                                   ║
║                                                                              ║
║  These models excel at:                                                      ║
║  ✓ Complex reasoning chains                                                  ║
║  ✓ Nuanced understanding                                                     ║
║  ✓ Creative writing                                                          ║
║  ✓ Multi-step problem solving                                                ║
║  ✓ Handling ambiguous queries                                                ║
║                                                                              ║
║  Local Models (Practical for most hardware)                                 ║
║  ────────────────────────────────────────                                    ║
║  • 7B parameters: Good for basic tasks                                       ║
║  • 13B parameters: Solid general purpose                                     ║
║  • 34B parameters: Near-frontier on specific tasks                          ║
║  • 70B parameters: Excellent (requires significant hardware)                ║
║                                                                              ║
║  Local models excel at:                                                      ║
║  ✓ Straightforward Q&A                                                       ║
║  ✓ Text summarization                                                        ║
║  ✓ Code completion (especially specialized code models)                     ║
║  ✓ Classification tasks                                                      ║
║  ✓ Document processing with clear structure                                 ║
║                                                                              ║
║  REALITY CHECK:                                                              ║
║  A well-chosen 13B local model can handle 80% of typical use cases.        ║
║  For the remaining 20%, you may still need cloud APIs (through secure      ║
║  channels) or accept reduced quality.                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### When to Use Local vs Cloud

**Choose Local LLMs When:**
- Processing CUI or sensitive federal data
- Operating in air-gapped environments
- Cost predictability is essential
- Tasks are well-defined (summarization, classification, code assistance)
- 24/7 availability without internet is required
- You need complete audit trails
- Fine-tuning on agency-specific terminology is beneficial

**Consider Cloud APIs When:**
- Maximum capability is required for complex reasoning
- Tasks require frontier model capabilities
- Data is publicly available or properly authorized for cloud processing
- Quick experimentation without infrastructure investment
- Scale varies dramatically and unpredictably

---

## 2. Understanding Local LLM Infrastructure

Before installing tools, let's understand what makes local LLM inference possible.

### The Inference Pipeline

When you send a prompt to a local LLM, here's what happens:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LOCAL LLM INFERENCE PIPELINE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Step 1: TOKENIZATION                                                       ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Your prompt: "Explain federal procurement regulations"                     ║
║       │                                                                      ║
║       ▼                                                                      ║
║  Tokenizer converts to token IDs: [78234, 9823, 45891, 2341]               ║
║                                                                              ║
║  Why: Neural networks can't process text directly.                          ║
║       They need numerical representations.                                   ║
║                                                                              ║
║  Step 2: EMBEDDING LOOKUP                                                   ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Token IDs → Embedding vectors (high-dimensional representations)           ║
║  Each token becomes a vector of ~4096 numbers                               ║
║                                                                              ║
║  Why: Embeddings capture semantic meaning.                                  ║
║       "King" and "Queen" have similar embeddings.                           ║
║                                                                              ║
║  Step 3: TRANSFORMER LAYERS                                                 ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Embeddings flow through transformer layers (32-80+ layers):               ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  For each layer:                                                     │   ║
║  │  1. Self-Attention: Tokens "look at" each other                     │   ║
║  │     - "regulations" attends to "federal" and "procurement"          │   ║
║  │     - This is the O(n²) computation that's expensive                │   ║
║  │                                                                      │   ║
║  │  2. Feed-Forward Network: Process each position                     │   ║
║  │     - Large matrix multiplications                                   │   ║
║  │     - This is where most parameters live                            │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  Step 4: PREDICTION                                                         ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Final layer output → Probability distribution over vocabulary              ║
║  Model predicts most likely next token                                      ║
║                                                                              ║
║  Step 5: SAMPLING                                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Temperature and top_p parameters control how we select from               ║
║  the probability distribution:                                              ║
║  - Temperature 0.0: Always pick most likely (deterministic)                ║
║  - Temperature 1.0: Sample according to probabilities (creative)           ║
║                                                                              ║
║  Step 6: ITERATION                                                          ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Predicted token appended to input, repeat from Step 2                     ║
║  Continue until stop token or max length reached                           ║
║                                                                              ║
║  This "autoregressive" generation is why LLMs seem slow:                   ║
║  Each token requires a full forward pass through the model!                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Why Hardware Matters

Understanding the pipeline reveals why hardware specifications matter:

**GPU VRAM (Video RAM):**
- Model parameters must be loaded into memory
- Larger models = more VRAM needed
- Quantization reduces memory requirements

**GPU Compute:**
- Matrix multiplications happen in parallel on GPU cores
- More CUDA/Tensor cores = faster inference
- Memory bandwidth often the bottleneck

**System RAM:**
- Model can run in CPU mode if GPU VRAM insufficient
- Much slower than GPU (10-100x)
- Useful for testing or when GPU unavailable

**Storage:**
- Models range from 2GB to 100GB+
- Fast SSD reduces model loading time
- Loading from HDD can take minutes

---

## 3. Ollama Deep Dive

### What is Ollama?

Ollama is a streamlined tool for running large language models locally. Think of it as "Docker for LLMs"—it handles the complexity of model management, serving, and API compatibility so you can focus on using the models.

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
║                    │  │  • Version management            │  │                ║
║                    │  │  • Cache optimization            │  │                ║
║                    │  │  • Hot-swapping between models   │  │                ║
║                    │  └──────────────────────────────────┘  │                ║
║                    │                                        │                ║
║                    │  ┌──────────────────────────────────┐  │                ║
║                    │  │       Inference Engine           │  │                ║
║                    │  │  • llama.cpp backend             │  │                ║
║                    │  │  • GPU acceleration (CUDA/Metal) │  │                ║
║                    │  │  • Quantization support          │  │                ║
║                    │  │  • KV-cache management           │  │                ║
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

### Installation: Step-by-Step

#### Linux Installation

```bash
# Method 1: Official install script (recommended)
# This script:
# - Detects your system architecture
# - Downloads the appropriate binary
# - Sets up systemd service
# - Configures GPU support if available

curl -fsSL https://ollama.ai/install.sh | sh

# Method 2: Manual installation (for controlled environments)
# Download from: https://github.com/ollama/ollama/releases

# For Ubuntu/Debian:
wget https://github.com/ollama/ollama/releases/download/v0.1.xx/ollama-linux-amd64
chmod +x ollama-linux-amd64
sudo mv ollama-linux-amd64 /usr/local/bin/ollama

# Create systemd service for background running
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
ExecStart=/usr/local/bin/ollama serve
User=ollama
Group=ollama
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama

# Verify installation
ollama --version
```

#### macOS Installation

```bash
# Method 1: Homebrew (easiest)
brew install ollama

# Method 2: Direct download
# Download .dmg from https://ollama.ai
# Drag to Applications folder

# Start Ollama (runs in menu bar)
ollama serve

# Or start manually in terminal
open -a Ollama

# Verify
ollama --version
```

#### Windows Installation

```powershell
# Method 1: Winget (Windows Package Manager)
winget install Ollama.Ollama

# Method 2: Direct download
# Download from https://ollama.ai
# Run installer
# Ollama runs as a service automatically

# Verify (in PowerShell or CMD)
ollama --version
```

### Understanding Ollama Commands

Let's explore each command with detailed explanations:

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# PULLING MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# Pull a model from Ollama's registry
ollama pull llama3.2

# What happens when you pull:
# 1. Ollama contacts registry.ollama.ai
# 2. Downloads model manifest (describes layers)
# 3. Downloads each layer (model weights, tokenizer, config)
# 4. Verifies checksums
# 5. Stores in ~/.ollama/models/

# Pull specific size variant
ollama pull llama3.2:3b      # 3 billion parameters
ollama pull llama3.2:8b      # 8 billion parameters (default)

# Pull specific quantization
ollama pull llama3.2:8b-q4_0   # 4-bit quantized
ollama pull llama3.2:8b-q8_0   # 8-bit quantized

# ═══════════════════════════════════════════════════════════════════════════════
# LISTING AND INSPECTING MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# List all downloaded models
ollama list

# Example output:
# NAME                    ID              SIZE    MODIFIED
# llama3.2:latest         abc123def456    4.7 GB  2 hours ago
# mistral:latest          789xyz012345    4.1 GB  1 day ago
# codestral:latest        456uvw789012    12 GB   3 days ago

# Show detailed model information
ollama show llama3.2

# This displays:
# - Model architecture (Llama, Mistral, etc.)
# - Parameter count
# - Quantization level
# - Context window size
# - License information
# - System prompt template

# Show just the Modelfile (configuration)
ollama show llama3.2 --modelfile

# ═══════════════════════════════════════════════════════════════════════════════
# RUNNING MODELS
# ═══════════════════════════════════════════════════════════════════════════════

# Start interactive chat
ollama run llama3.2

# This:
# 1. Loads model into GPU memory (takes a few seconds)
# 2. Starts an interactive prompt
# 3. Type your message, press Enter
# 4. Use /bye to exit

# Run with a specific prompt (non-interactive)
ollama run llama3.2 "What is FISMA?"

# Run with multiline prompt
ollama run llama3.2 """
Analyze the following policy excerpt and identify
key compliance requirements:

[Your policy text here]
"""

# Run with system prompt override
ollama run llama3.2 --system "You are a federal compliance expert"

# ═══════════════════════════════════════════════════════════════════════════════
# MODEL MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

# Remove a model (free disk space)
ollama rm llama3.2

# Copy a model (useful for creating variants)
ollama cp llama3.2 my-federal-assistant

# Create a custom model from Modelfile
ollama create federal-assistant -f Modelfile

# Push model to registry (requires account)
ollama push username/my-model

# ═══════════════════════════════════════════════════════════════════════════════
# SERVER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════════════

# Start the server (usually runs automatically)
ollama serve

# The server listens on localhost:11434 by default
# Environment variables for configuration:
# OLLAMA_HOST=0.0.0.0           # Listen on all interfaces
# OLLAMA_MODELS=/path/to/models # Custom model directory
# OLLAMA_NUM_PARALLEL=2         # Concurrent requests
# OLLAMA_MAX_LOADED_MODELS=3    # Models in memory
```

### API Usage: Comprehensive Guide

Ollama provides a REST API that's compatible with many existing tools:

```python
# ═══════════════════════════════════════════════════════════════════════════════
# PYTHON: Using the official ollama library
# ═══════════════════════════════════════════════════════════════════════════════

# Install: pip install ollama

import ollama

# Basic chat completion
response = ollama.chat(
    model='llama3.2',
    messages=[
        {
            'role': 'system',
            'content': '''You are a Federal Compliance Assistant.
            Your role is to help federal employees understand
            compliance requirements. Always cite specific
            regulations and control numbers when applicable.'''
        },
        {
            'role': 'user',
            'content': 'What are the key requirements of FedRAMP?'
        }
    ]
)

# Access the response
print(response['message']['content'])

# The response object contains:
# {
#     'model': 'llama3.2',
#     'created_at': '2024-01-15T10:30:00Z',
#     'message': {
#         'role': 'assistant',
#         'content': 'FedRAMP (Federal Risk and Authorization...'
#     },
#     'done': True,
#     'total_duration': 1234567890,  # nanoseconds
#     'load_duration': 12345678,
#     'prompt_eval_count': 50,
#     'prompt_eval_duration': 123456789,
#     'eval_count': 200,
#     'eval_duration': 1111111111
# }

# ═══════════════════════════════════════════════════════════════════════════════
# STREAMING RESPONSES
# ═══════════════════════════════════════════════════════════════════════════════

# For real-time output (better UX for long responses)
for chunk in ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': 'Explain the NIST AI Risk Management Framework'}
    ],
    stream=True
):
    # Each chunk contains a partial response
    print(chunk['message']['content'], end='', flush=True)
print()  # Newline at end

# ═══════════════════════════════════════════════════════════════════════════════
# CONVERSATION HISTORY (Multi-turn chat)
# ═══════════════════════════════════════════════════════════════════════════════

messages = [
    {'role': 'system', 'content': 'You are a helpful federal IT assistant.'}
]

def chat(user_message):
    """Send a message and get a response, maintaining conversation history."""
    messages.append({'role': 'user', 'content': user_message})

    response = ollama.chat(
        model='llama3.2',
        messages=messages
    )

    assistant_message = response['message']['content']
    messages.append({'role': 'assistant', 'content': assistant_message})

    return assistant_message

# Use in conversation
print(chat("What is ATO?"))
print(chat("How long does it typically take?"))  # Knows context from previous Q
print(chat("What documentation is required?"))   # Continues the conversation

# ═══════════════════════════════════════════════════════════════════════════════
# EMBEDDINGS (for semantic search, RAG applications)
# ═══════════════════════════════════════════════════════════════════════════════

# Generate embeddings for text
embedding = ollama.embeddings(
    model='llama3.2',
    prompt='Federal acquisition regulations'
)

# Returns a vector of floats
vector = embedding['embedding']  # List of ~4096 floats
print(f"Embedding dimension: {len(vector)}")

# Use for similarity search, clustering, RAG pipelines

# ═══════════════════════════════════════════════════════════════════════════════
# GENERATION PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

response = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Draft a policy statement'}],
    options={
        'temperature': 0.3,      # Lower = more deterministic (0.0-2.0)
        'top_p': 0.9,            # Nucleus sampling threshold
        'top_k': 40,             # Consider top K tokens
        'num_ctx': 8192,         # Context window size
        'num_predict': 500,      # Max tokens to generate
        'stop': ['---', 'END'], # Stop sequences
        'seed': 42,              # For reproducibility
    }
)

# Parameter explanations:
#
# temperature: Controls randomness
#   0.0 = Always pick the most likely token (deterministic)
#   0.7 = Balanced creativity (good default)
#   1.5+ = Very creative, potentially incoherent
#
# top_p (nucleus sampling):
#   Consider tokens whose cumulative probability exceeds this
#   0.9 = Consider top 90% of probability mass
#   Lower = more focused, Higher = more diverse
#
# top_k:
#   Only consider top K most likely tokens
#   40 = Good balance
#   Lower = more focused, Higher = more options
#
# num_ctx:
#   Context window size (prompt + response)
#   Larger = more context but more memory
#
# seed:
#   Set for reproducible outputs (same prompt = same response)
```

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# DIRECT HTTP API USAGE (curl, any HTTP client)
# ═══════════════════════════════════════════════════════════════════════════════

# Chat endpoint
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello!"}
  ]
}'

# Generate endpoint (simple completion)
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "The Federal Risk and Authorization Management Program is"
}'

# Streaming (add stream: true)
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Explain FedRAMP"}],
  "stream": true
}'

# Check loaded models
curl http://localhost:11434/api/tags

# Pull model via API
curl http://localhost:11434/api/pull -d '{
  "name": "llama3.2"
}'
```

### Custom Modelfiles: Creating Specialized Assistants

Modelfiles let you create customized versions of models with specific behaviors:

```dockerfile
# ═══════════════════════════════════════════════════════════════════════════════
# Modelfile: Federal Compliance Assistant
# Save as: Modelfile.federal-compliance
# ═══════════════════════════════════════════════════════════════════════════════

# Base model to build upon
FROM llama3.2

# ───────────────────────────────────────────────────────────────────────────────
# SYSTEM PROMPT
# This shapes the model's persona and behavior
# ───────────────────────────────────────────────────────────────────────────────

SYSTEM """
You are a Federal Compliance Assistant specializing in information security
and technology governance. Your expertise includes:

FRAMEWORKS AND STANDARDS:
- FedRAMP (Federal Risk and Authorization Management Program)
- FISMA (Federal Information Security Modernization Act)
- NIST frameworks (800-53, 800-171, AI RMF, CSF)
- OMB memoranda and circulars
- FAR/DFARS regulations

COMMUNICATION STYLE:
- Always cite specific control numbers and document references
- Use precise language appropriate for federal documentation
- When uncertain, acknowledge limitations and recommend official sources
- Provide practical implementation guidance, not just theoretical knowledge

CONSTRAINTS:
- Never provide legal advice - recommend consulting legal counsel
- Do not speculate on classified information or procedures
- Always recommend verifying current versions of regulations
- Acknowledge that requirements may vary by agency

When responding:
1. First, identify the relevant framework(s)
2. Cite specific sections/controls
3. Provide practical implementation guidance
4. Note any agency-specific considerations
5. Recommend next steps or additional resources
"""

# ───────────────────────────────────────────────────────────────────────────────
# MODEL PARAMETERS
# Tune behavior for compliance-focused responses
# ───────────────────────────────────────────────────────────────────────────────

# Temperature: Lower for more consistent, factual responses
PARAMETER temperature 0.3

# Top_p: Slightly restricted for more focused output
PARAMETER top_p 0.9

# Context window: Larger to handle policy documents
PARAMETER num_ctx 8192

# Repeat penalty: Prevent repetitive citations
PARAMETER repeat_penalty 1.1

# Stop tokens: Ensure clean endings
PARAMETER stop "<|end|>"
PARAMETER stop "Human:"
PARAMETER stop "User:"

# ───────────────────────────────────────────────────────────────────────────────
# TEMPLATE (optional, for specific prompt formats)
# ───────────────────────────────────────────────────────────────────────────────

TEMPLATE """
{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>
"""

# ───────────────────────────────────────────────────────────────────────────────
# LICENSE (for documentation purposes)
# ───────────────────────────────────────────────────────────────────────────────

LICENSE """
Federal Compliance Assistant - Custom Configuration
Based on Llama 3.2 - See Meta AI license terms
Custom system prompt and parameters by [Your Agency]
"""
```

Create and use the custom model:

```bash
# Create the model
ollama create federal-compliance -f Modelfile.federal-compliance

# Run it
ollama run federal-compliance

# Test with compliance question
ollama run federal-compliance "What controls address access management in NIST 800-53?"
```

### Popular Ollama Models for Federal Use

| Model | Parameters | VRAM Needed | Best Use Cases | Federal Relevance |
|:------|:----------:|:-----------:|:---------------|:------------------|
| **llama3.2** | 3B | 4GB | Quick tasks, simple Q&A | Basic queries, mobile deployment |
| **llama3.2** | 8B | 8GB | General purpose | Document analysis, policy questions |
| **llama3.1** | 70B | 48GB+ | Complex reasoning | Legal analysis, complex compliance |
| **mistral** | 7B | 6GB | Fast, efficient | High-throughput workloads |
| **mixtral** | 8x7B | 26GB | Expert tasks | Multi-domain analysis |
| **codestral** | 22B | 16GB | Code generation | Automation scripting, code review |
| **qwen2.5** | 7B-72B | 6-48GB | Multilingual | International policy documents |
| **phi3** | 3.8B | 4GB | Edge deployment | Mobile/tablet applications |
| **gemma2** | 9B-27B | 8-20GB | Quality outputs | Documentation generation |

---

## 4. LM Studio

### Understanding LM Studio's Role

LM Studio provides a graphical interface for local LLM operations, making it accessible to users who prefer not to work with command lines. It's particularly valuable for:

- **Evaluation and Testing**: Quickly try different models side-by-side
- **Non-technical Users**: Enable staff without CLI experience to use local LLMs
- **Model Discovery**: Browse and download from Hugging Face directly
- **Parameter Tuning**: Visual controls for adjusting model behavior

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          LM STUDIO INTERFACE                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │  🔍 Discover    💬 Chat    🖥️ Local Server    ⚙️ Settings           │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  DISCOVER TAB:                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Search Hugging Face models directly                                      ║
║  • Filter by size, type, quantization                                       ║
║  • See download sizes before downloading                                    ║
║  • Compare model specifications                                             ║
║                                                                              ║
║  CHAT TAB:                                                                  ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Interactive conversation interface                                       ║
║  • Visual parameter sliders (temperature, top_p, etc.)                     ║
║  • System prompt editor                                                     ║
║  • Conversation history management                                          ║
║  • Token count and generation speed display                                 ║
║                                                                              ║
║  LOCAL SERVER TAB:                                                          ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • OpenAI-compatible API server                                             ║
║  • One-click server start/stop                                              ║
║  • API endpoint display                                                     ║
║  • Request logging                                                          ║
║                                                                              ║
║  SETTINGS TAB:                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • GPU layer configuration                                                  ║
║  • Memory allocation                                                        ║
║  • Model download location                                                  ║
║  • Interface preferences                                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Installation and Setup

1. **Download**: Visit https://lmstudio.ai and download for your platform
2. **Install**: Run the installer (standard installation process)
3. **First Run**: LM Studio will guide you through initial setup

### Using LM Studio's Local Server

One of LM Studio's most powerful features is its OpenAI-compatible API server:

```python
# ═══════════════════════════════════════════════════════════════════════════════
# Using LM Studio with OpenAI library
# ═══════════════════════════════════════════════════════════════════════════════

from openai import OpenAI

# Point to LM Studio's local server
# Default port is 1234
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"  # Required by library but not actually used
)

# Now use exactly like OpenAI API
response = client.chat.completions.create(
    model="local-model",  # LM Studio ignores this, uses loaded model
    messages=[
        {
            "role": "system",
            "content": "You are a helpful federal IT assistant."
        },
        {
            "role": "user",
            "content": "What is an Authority to Operate?"
        }
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)

# ═══════════════════════════════════════════════════════════════════════════════
# Streaming responses
# ═══════════════════════════════════════════════════════════════════════════════

stream = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "user", "content": "Explain FedRAMP authorization levels"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print()
```

### LM Studio vs Ollama: When to Use Which

| Aspect | LM Studio | Ollama |
|:-------|:----------|:-------|
| **Interface** | GUI-first | CLI-first |
| **Model Source** | Hugging Face GGUF | Ollama Registry |
| **API Compatibility** | OpenAI | Native + OpenAI |
| **Best For** | Evaluation, non-technical users | Production, automation |
| **Server Mode** | Manual start | Runs as service |
| **Customization** | Limited | Modelfiles |
| **Resource Usage** | Higher (Electron app) | Lower (native binary) |

**Recommendation**: Use LM Studio for model discovery and testing, Ollama for production deployments.

---

## 5. LocalAI

### Understanding LocalAI

LocalAI is a comprehensive, self-hosted AI platform that provides OpenAI-compatible APIs for multiple AI capabilities—not just text, but also images, audio, and embeddings.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          LOCALAI CAPABILITIES                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                     LOCALAI SERVER                                   │    ║
║  │                                                                      │    ║
║  │  OpenAI-Compatible Endpoints:                                        │    ║
║  │                                                                      │    ║
║  │  /v1/chat/completions      ──▶  Text generation (like ChatGPT)     │    ║
║  │  /v1/completions           ──▶  Text completion                     │    ║
║  │  /v1/embeddings            ──▶  Text embeddings (for RAG)          │    ║
║  │  /v1/images/generations    ──▶  Image generation (Stable Diffusion)│    ║
║  │  /v1/audio/transcriptions  ──▶  Speech-to-text (Whisper)           │    ║
║  │  /v1/audio/speech          ──▶  Text-to-speech                     │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                     │                                        ║
║                                     │                                        ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                     BACKEND SUPPORT                                  │    ║
║  │                                                                      │    ║
║  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐       │    ║
║  │  │llama.cpp│ │ GPT4All │ │  RWKV   │ │Whisper  │ │Diffusers│       │    ║
║  │  │         │ │         │ │         │ │         │ │         │       │    ║
║  │  │  LLMs   │ │  LLMs   │ │  LLMs   │ │  Audio  │ │ Images  │       │    ║
║  │  └─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘       │    ║
║  │                                                                      │    ║
║  │  Supports: GGUF, GGML, PyTorch, ONNX, Safetensors formats          │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Docker Deployment

LocalAI is best deployed via Docker for consistency and isolation:

```yaml
# docker-compose.yml for LocalAI
version: '3.8'

services:
  localai:
    # Choose the appropriate image:
    # CPU only:
    image: localai/localai:latest-aio-cpu

    # NVIDIA GPU (CUDA 11):
    # image: localai/localai:latest-aio-gpu-nvidia-cuda-11

    # NVIDIA GPU (CUDA 12):
    # image: localai/localai:latest-aio-gpu-nvidia-cuda-12

    container_name: localai

    ports:
      - "8080:8080"  # API endpoint

    volumes:
      # Model storage
      - ./models:/models

      # Persistent data
      - ./data:/data

    environment:
      # Number of CPU threads (adjust based on your CPU)
      - THREADS=8

      # Default context size
      - CONTEXT_SIZE=4096

      # Enable debug logging (optional)
      - DEBUG=false

      # Gallery for model discovery
      - GALLERIES=[{"name":"model-gallery", "url":"github:go-skynet/model-gallery/index.yaml"}]

    # GPU support (uncomment for NVIDIA)
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: all
    #           capabilities: [gpu]

    restart: unless-stopped

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/readyz"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
# Deploy LocalAI
docker-compose up -d

# Check status
docker-compose logs -f localai

# Test the API
curl http://localhost:8080/v1/models
```

### Model Configuration

LocalAI uses YAML files to configure models:

```yaml
# models/llama3.yaml
# Place in the models directory mounted to container

name: llama3
backend: llama-cpp

parameters:
  # Model file (must be in models directory)
  model: llama-3-8b-instruct.Q4_K_M.gguf

  # Generation parameters
  temperature: 0.7
  top_p: 0.9
  top_k: 40

  # Context size
  context_size: 8192

  # Number of GPU layers (0 for CPU only)
  # gpu_layers: 35

  # Threads for CPU inference
  threads: 8

# Chat template (Llama 3 specific)
template:
  chat_message: |
    <|start_header_id|>{{.RoleName}}<|end_header_id|>

    {{.Content}}<|eot_id|>

  chat: |
    <|begin_of_text|>{{.Input}}
    <|start_header_id|>assistant<|end_header_id|>

# Stop tokens
stopwords:
  - "<|eot_id|>"
  - "<|end_of_text|>"
```

### Using LocalAI

```python
# LocalAI is fully OpenAI-compatible
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # LocalAI doesn't require auth by default
)

# Text generation
response = client.chat.completions.create(
    model="llama3",  # Must match name in YAML config
    messages=[
        {"role": "user", "content": "Explain NIST 800-53"}
    ]
)
print(response.choices[0].message.content)

# Embeddings (if configured)
embedding = client.embeddings.create(
    model="text-embedding-ada-002",  # Or your configured embedding model
    input="Federal compliance framework"
)
print(f"Embedding dimension: {len(embedding.data[0].embedding)}")

# Audio transcription (if Whisper configured)
with open("meeting.mp3", "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
print(transcript.text)
```

---

## 6. llama.cpp: The Engine Behind Local LLMs

### Understanding llama.cpp

llama.cpp is the foundational C++ library that powers most local LLM tools. Ollama, LM Studio, and LocalAI all use llama.cpp under the hood. Understanding it helps you troubleshoot issues and optimize performance.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        llama.cpp ECOSYSTEM                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                           llama.cpp (Core Library)                          ║
║                    ┌─────────────────────────────────────┐                  ║
║                    │  • Pure C/C++ implementation        │                  ║
║                    │  • No Python dependencies           │                  ║
║                    │  • GGUF model format                │                  ║
║                    │  • Quantization support             │                  ║
║                    │  • Multi-platform                   │                  ║
║                    └────────────────┬────────────────────┘                  ║
║                                     │                                        ║
║         ┌───────────────────────────┼───────────────────────────┐           ║
║         │                           │                           │           ║
║         ▼                           ▼                           ▼           ║
║   ┌───────────┐              ┌───────────┐              ┌───────────┐      ║
║   │  Ollama   │              │ LM Studio │              │  LocalAI  │      ║
║   │           │              │           │              │           │      ║
║   │ • CLI     │              │ • GUI     │              │ • Docker  │      ║
║   │ • REST API│              │ • OpenAI  │              │ • Multi-  │      ║
║   │ • Model   │              │   compat  │              │   modal   │      ║
║   │   registry│              │ • HF      │              │           │      ║
║   └───────────┘              │   browser │              └───────────┘      ║
║                              └───────────┘                                  ║
║                                                                              ║
║   Backend Acceleration:                                                     ║
║   ───────────────────────────────────────────────────────────────────────  ║
║   • CUDA (NVIDIA GPUs) - Fastest for supported cards                       ║
║   • Metal (Apple Silicon) - Excellent performance on Mac                   ║
║   • OpenCL - AMD GPUs and others                                           ║
║   • BLAS (CPU) - Optimized CPU math operations                             ║
║   • Vulkan - Cross-platform GPU support                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Why llama.cpp Matters

Georgi Gerganov created llama.cpp in March 2023, just days after Meta released the original LLaMA weights. His key innovations:

1. **4-bit Quantization**: Made large models run on consumer hardware
2. **Pure C++**: No Python/PyTorch dependencies—runs anywhere
3. **GGML/GGUF Format**: Efficient model storage and loading
4. **CPU Optimization**: Runs on machines without GPUs

### Direct Usage of llama.cpp

For advanced users or specialized deployments:

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# Building llama.cpp from source
# ═══════════════════════════════════════════════════════════════════════════════

# Clone the repository
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp

# Basic build (CPU only)
make -j$(nproc)

# Build with CUDA support (NVIDIA GPUs)
make LLAMA_CUDA=1 -j$(nproc)

# Build with Metal support (Apple Silicon)
make LLAMA_METAL=1 -j$(nproc)

# Build with OpenBLAS (optimized CPU)
make LLAMA_OPENBLAS=1 -j$(nproc)

# ═══════════════════════════════════════════════════════════════════════════════
# Running inference
# ═══════════════════════════════════════════════════════════════════════════════

# Basic inference
./llama-cli \
  -m models/llama-3-8b-instruct.Q4_K_M.gguf \
  -p "Explain the Federal Acquisition Regulation" \
  -n 512 \              # Generate up to 512 tokens
  --ctx-size 4096 \     # Context window size
  --temp 0.7 \          # Temperature
  --top-p 0.9 \         # Top-p sampling
  --threads 8           # CPU threads

# Interactive mode
./llama-cli \
  -m models/llama-3-8b-instruct.Q4_K_M.gguf \
  --interactive \
  --color \
  --ctx-size 8192

# With GPU layers (CUDA)
./llama-cli \
  -m models/llama-3-8b-instruct.Q4_K_M.gguf \
  -p "Your prompt" \
  --n-gpu-layers 35 \   # Offload 35 layers to GPU
  --threads 4           # CPU threads for remaining work

# ═══════════════════════════════════════════════════════════════════════════════
# Running the server (OpenAI-compatible API)
# ═══════════════════════════════════════════════════════════════════════════════

./llama-server \
  -m models/llama-3-8b-instruct.Q4_K_M.gguf \
  --host 0.0.0.0 \
  --port 8080 \
  --ctx-size 8192 \
  --n-gpu-layers 35 \
  --parallel 2          # Handle 2 concurrent requests

# Server provides:
# - /v1/chat/completions
# - /v1/completions
# - /v1/embeddings
# - /health
```

### Python Bindings (llama-cpp-python)

```python
# ═══════════════════════════════════════════════════════════════════════════════
# Using llama-cpp-python directly
# Install: pip install llama-cpp-python
# With CUDA: CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python
# ═══════════════════════════════════════════════════════════════════════════════

from llama_cpp import Llama

# Initialize the model
llm = Llama(
    model_path="models/llama-3-8b-instruct.Q4_K_M.gguf",

    # Context window
    n_ctx=8192,

    # GPU layers to offload (0 = CPU only)
    n_gpu_layers=35,

    # CPU threads
    n_threads=8,

    # Batch size for prompt processing
    n_batch=512,

    # Use memory-mapped files (faster loading)
    use_mmap=True,

    # Verbose output
    verbose=False
)

# Simple completion
output = llm(
    "The Federal Risk and Authorization Management Program, commonly known as FedRAMP, is",
    max_tokens=256,
    stop=[".", "\n\n"],
    echo=True  # Include prompt in output
)
print(output["choices"][0]["text"])

# Chat completion (if model supports chat format)
output = llm.create_chat_completion(
    messages=[
        {
            "role": "system",
            "content": "You are a federal compliance assistant."
        },
        {
            "role": "user",
            "content": "What is an ATO?"
        }
    ],
    max_tokens=500,
    temperature=0.7
)
print(output["choices"][0]["message"]["content"])

# Streaming
for token in llm(
    "Explain NIST 800-53 controls:",
    max_tokens=256,
    stream=True
):
    print(token["choices"][0]["text"], end="", flush=True)
print()

# Embeddings
embeddings = llm.create_embedding("Federal acquisition regulations")
print(f"Embedding dimension: {len(embeddings['data'][0]['embedding'])}")
```

---

## 7. Quantization: Making Models Fit Your Hardware

### What is Quantization?

Quantization is the process of reducing the precision of a model's weights to use less memory and compute faster, with minimal impact on quality.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     UNDERSTANDING QUANTIZATION                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Original Model (FP16 - 16-bit floating point)                             ║
║  ─────────────────────────────────────────────                              ║
║  Each weight stored as 16-bit number                                        ║
║  Example: 3.14159265... stored with high precision                          ║
║                                                                              ║
║  7B parameter model at FP16:                                                ║
║  7,000,000,000 × 16 bits = 112,000,000,000 bits = 14 GB                    ║
║                                                                              ║
║                                                                              ║
║  Quantized Model (Q4_K_M - 4-bit with mixed precision)                     ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Most weights stored as 4-bit numbers                                       ║
║  Example: 3.14159265... rounded to nearest of 16 possible values           ║
║                                                                              ║
║  7B parameter model at Q4:                                                  ║
║  ~7,000,000,000 × 4 bits = ~28,000,000,000 bits = ~3.5 GB                  ║
║  (Actual size ~4GB due to metadata and critical layers kept at higher      ║
║   precision)                                                                ║
║                                                                              ║
║                                                                              ║
║  THE KEY INSIGHT:                                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Neural networks are surprisingly robust to reduced precision.              ║
║  A well-quantized 4-bit model retains 95-99% of the original quality!      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Quantization Levels Explained

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    QUANTIZATION LEVELS COMPARISON                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Level    │ Bits │ Size (7B) │ Quality    │ Speed    │ Use Case             ║
║  ─────────┼──────┼───────────┼────────────┼──────────┼────────────────────  ║
║  FP16     │ 16   │ ~14 GB    │ Baseline   │ Baseline │ Reference only       ║
║  Q8_0     │ 8    │ ~7 GB     │ 99%+       │ Fast     │ Quality-critical     ║
║  Q6_K     │ 6    │ ~5.5 GB   │ 98%+       │ Fast     │ Good balance         ║
║  Q5_K_M   │ 5    │ ~5 GB     │ 97%+       │ Fast     │ Recommended          ║
║  Q4_K_M   │ 4    │ ~4 GB     │ 95-97%     │ Fastest  │ Most popular         ║
║  Q4_K_S   │ 4    │ ~3.8 GB   │ 94-96%     │ Fastest  │ Smaller variant      ║
║  Q3_K_M   │ 3    │ ~3 GB     │ 92-95%     │ Fastest  │ Memory constrained   ║
║  Q2_K     │ 2    │ ~2.5 GB   │ 85-92%     │ Fastest  │ Extreme compression  ║
║                                                                              ║
║  Naming convention:                                                         ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Q4_K_M = 4-bit quantization, K-quant method, Medium variant               ║
║                                                                              ║
║  • Q = Quantization level (bits)                                            ║
║  • K = K-quant method (more sophisticated than original GGML)               ║
║  • _S = Small (more aggressive compression)                                 ║
║  • _M = Medium (balanced)                                                   ║
║  • _L = Large (higher quality)                                              ║
║                                                                              ║
║  RECOMMENDATION FOR FEDERAL USE:                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Q4_K_M: Best balance of quality and efficiency for most tasks           ║
║  • Q5_K_M: When slightly higher quality needed                              ║
║  • Q8_0:   When processing sensitive documents requiring accuracy          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Quality Impact by Task Type

Not all tasks are equally affected by quantization:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   QUANTIZATION IMPACT BY TASK TYPE                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  MINIMAL IMPACT (Q4 works great):                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  ✅ Text summarization                                                       ║
║  ✅ Classification tasks                                                     ║
║  ✅ Simple Q&A                                                               ║
║  ✅ Format conversion                                                        ║
║  ✅ Entity extraction                                                        ║
║  ✅ Sentiment analysis                                                       ║
║                                                                              ║
║  MODERATE IMPACT (Q5 or Q6 recommended):                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  ⚠️ Complex reasoning chains                                                 ║
║  ⚠️ Mathematical calculations                                                ║
║  ⚠️ Code generation (syntax sensitivity)                                    ║
║  ⚠️ Multi-step instructions                                                  ║
║                                                                              ║
║  HIGHER IMPACT (Q8 or larger model preferred):                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  ❗ Legal document analysis                                                  ║
║  ❗ Precise numerical extraction                                             ║
║  ❗ Nuanced language understanding                                           ║
║  ❗ Rare/technical vocabulary                                                ║
║  ❗ Low-resource languages                                                   ║
║                                                                              ║
║  PRACTICAL GUIDELINE:                                                       ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Start with Q4_K_M. If results seem degraded for your specific task,       ║
║  try Q5_K_M or Q8. The difference is often imperceptible.                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Choosing the Right Quantization

```python
# Example: Selecting quantization based on your hardware and needs

def recommend_quantization(
    model_size_b: int,       # Model size in billions of parameters
    available_vram_gb: int,  # Your GPU VRAM
    task_type: str           # 'general', 'coding', 'reasoning', 'legal'
):
    """
    Recommend quantization level based on constraints.
    """

    # Rough VRAM requirements per billion parameters
    vram_per_b = {
        'Q2_K': 0.35,
        'Q3_K_M': 0.45,
        'Q4_K_M': 0.55,
        'Q5_K_M': 0.65,
        'Q6_K': 0.75,
        'Q8_0': 1.0,
        'FP16': 2.0
    }

    # Task-specific minimum recommendations
    task_minimums = {
        'general': 'Q4_K_M',
        'coding': 'Q4_K_M',
        'reasoning': 'Q5_K_M',
        'legal': 'Q5_K_M'
    }

    # Find largest quantization that fits
    suitable_quants = []
    for quant, vram_factor in vram_per_b.items():
        estimated_vram = model_size_b * vram_factor
        if estimated_vram <= available_vram_gb * 0.85:  # Leave 15% buffer
            suitable_quants.append(quant)

    if not suitable_quants:
        return "Model too large for available VRAM. Consider smaller model."

    # Get minimum quality for task
    min_quant = task_minimums.get(task_type, 'Q4_K_M')

    # Return best suitable option that meets minimum
    # (Implementation would rank and compare)
    return f"Recommended: {suitable_quants[-1]} (meets requirements)"

# Example usage:
# 13B model, 12GB VRAM, coding task
# recommend_quantization(13, 12, 'coding')
# → "Recommended: Q4_K_M"
```

---

## 8. Hardware Requirements and Optimization

### Understanding Hardware Bottlenecks

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    LLM INFERENCE BOTTLENECKS                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  BOTTLENECK #1: MEMORY BANDWIDTH                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  During generation, the model must read ALL parameters for EACH token.      ║
║                                                                              ║
║  7B model at Q4 (~4GB):                                                     ║
║  • Generating at 30 tokens/second                                           ║
║  • Must read 4GB × 30 = 120 GB/second from memory!                         ║
║                                                                              ║
║  GPU Memory Bandwidth Comparison:                                           ║
║  • RTX 3060 12GB:  360 GB/s  →  ~90 tokens/sec theoretical max             ║
║  • RTX 4090 24GB:  1000 GB/s →  ~250 tokens/sec theoretical max            ║
║  • A100 80GB:      2000 GB/s →  ~500 tokens/sec theoretical max            ║
║                                                                              ║
║  BOTTLENECK #2: COMPUTE                                                     ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Matrix multiplications in attention and feed-forward layers.               ║
║  Less often the bottleneck with quantized models.                          ║
║                                                                              ║
║  BOTTLENECK #3: PROMPT PROCESSING                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  Long prompts require O(n²) attention computation.                         ║
║  Time to process prompt can exceed generation time for long contexts.      ║
║                                                                              ║
║  Example: 4096 token prompt vs 32 token prompt                             ║
║  • 4096 tokens: ~128x more attention computation                           ║
║  • Noticeable delay before first token generated                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### GPU VRAM Requirements Table

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    DETAILED VRAM REQUIREMENTS                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Model     │ Q4_K_M │ Q5_K_M │ Q6_K  │ Q8_0  │ FP16   │ Context Overhead    ║
║  ──────────┼────────┼────────┼───────┼───────┼────────┼──────────────────   ║
║  3B        │ 2 GB   │ 2.5 GB │ 3 GB  │ 4 GB  │ 6 GB   │ +0.5-1 GB per 4K   ║
║  7B        │ 4 GB   │ 5 GB   │ 6 GB  │ 8 GB  │ 14 GB  │ +1-2 GB per 4K     ║
║  8B        │ 5 GB   │ 6 GB   │ 7 GB  │ 9 GB  │ 16 GB  │ +1-2 GB per 4K     ║
║  13B       │ 8 GB   │ 9 GB   │ 11 GB │ 14 GB │ 26 GB  │ +2-3 GB per 4K     ║
║  34B       │ 20 GB  │ 24 GB  │ 28 GB │ 36 GB │ 68 GB  │ +4-6 GB per 4K     ║
║  70B       │ 40 GB  │ 48 GB  │ 56 GB │ 75 GB │ 140 GB │ +6-8 GB per 4K     ║
║                                                                              ║
║  Note: "per 4K" means per 4096 context window tokens                        ║
║                                                                              ║
║  Example: Running Llama 3.1 8B Q4_K_M with 8K context                       ║
║  • Base model: ~5 GB                                                        ║
║  • Context (8K): ~2-3 GB                                                    ║
║  • Total: ~7-8 GB VRAM needed                                               ║
║                                                                              ║
║  PRACTICAL MAPPINGS:                                                        ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  GPU                  │ VRAM   │ Comfortable Models                         ║
║  ─────────────────────┼────────┼──────────────────────────────────────────  ║
║  GTX 1660 Super       │ 6 GB   │ 3B Q4, 7B Q2 (tight)                       ║
║  RTX 3060             │ 12 GB  │ 7B Q4-Q6, 13B Q4 (tight)                   ║
║  RTX 3080             │ 10 GB  │ 7B Q6-Q8, 13B Q4                           ║
║  RTX 3090/4090        │ 24 GB  │ 13B Q8, 34B Q4, 70B Q2 (tight)            ║
║  2× RTX 4090          │ 48 GB  │ 34B Q8, 70B Q4                             ║
║  A100 40GB            │ 40 GB  │ 34B Q6, 70B Q4 (tight)                     ║
║  A100 80GB            │ 80 GB  │ 70B Q6-Q8                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Recommended Federal Configurations

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FEDERAL DEPLOYMENT CONFIGURATIONS                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TIER 1: INDIVIDUAL WORKSTATION                                             ║
║  Budget: $2,000 - $3,500                                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Components:                                                                 ║
║  • CPU: AMD Ryzen 7/9 or Intel Core i7/i9 (8+ cores)                       ║
║  • RAM: 32-64 GB DDR5                                                       ║
║  • GPU: NVIDIA RTX 4070 Ti (12GB) or RTX 4070 Super (16GB)                 ║
║  • Storage: 1-2 TB NVMe SSD                                                 ║
║                                                                              ║
║  Capabilities:                                                               ║
║  • Models up to 13B Q4 comfortably                                          ║
║  • 7B Q8 with good context                                                  ║
║  • 20-40 tokens/second generation                                           ║
║                                                                              ║
║  Best For:                                                                   ║
║  • Individual analyst workstations                                          ║
║  • Development and testing                                                  ║
║  • Small team shared resource                                               ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  TIER 2: POWER WORKSTATION                                                  ║
║  Budget: $5,000 - $8,000                                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Components:                                                                 ║
║  • CPU: AMD Threadripper or Intel Xeon (16+ cores)                         ║
║  • RAM: 128 GB DDR5 ECC                                                     ║
║  • GPU: NVIDIA RTX 4090 (24GB)                                              ║
║  • Storage: 4 TB NVMe SSD RAID                                              ║
║                                                                              ║
║  Capabilities:                                                               ║
║  • Models up to 34B Q4 comfortably                                          ║
║  • 13B Q8 with large context                                                ║
║  • 40-70 tokens/second generation                                           ║
║                                                                              ║
║  Best For:                                                                   ║
║  • Division-level shared resource                                           ║
║  • Production development                                                   ║
║  • Multi-user with request queuing                                          ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  TIER 3: SERVER DEPLOYMENT                                                  ║
║  Budget: $15,000 - $40,000                                                  ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Components:                                                                 ║
║  • CPU: Dual AMD EPYC or Intel Xeon Scalable                               ║
║  • RAM: 256-512 GB DDR5 ECC                                                 ║
║  • GPU: 2-4× NVIDIA RTX 4090 or 1-2× A100                                  ║
║  • Storage: 8+ TB NVMe SSD with RAID                                        ║
║  • Networking: 10 GbE minimum                                               ║
║                                                                              ║
║  Capabilities:                                                               ║
║  • Models up to 70B Q4-Q6                                                   ║
║  • Multiple concurrent users                                                ║
║  • High throughput (100+ requests/minute)                                   ║
║                                                                              ║
║  Best For:                                                                   ║
║  • Agency-wide deployment                                                   ║
║  • Production services                                                       ║
║  • API endpoint for applications                                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Optimization Techniques

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# OLLAMA OPTIMIZATION
# ═══════════════════════════════════════════════════════════════════════════════

# Set environment variables before starting Ollama

# Number of parallel requests (memory vs throughput tradeoff)
export OLLAMA_NUM_PARALLEL=2

# Max models to keep loaded (memory management)
export OLLAMA_MAX_LOADED_MODELS=1

# Custom model directory (use fast SSD)
export OLLAMA_MODELS=/fast-ssd/ollama/models

# Listen on all interfaces (for server deployment)
export OLLAMA_HOST=0.0.0.0

# Start with optimizations
ollama serve
```

```python
# ═══════════════════════════════════════════════════════════════════════════════
# LLAMA.CPP OPTIMIZATION PARAMETERS
# ═══════════════════════════════════════════════════════════════════════════════

from llama_cpp import Llama

llm = Llama(
    model_path="model.gguf",

    # GPU OPTIMIZATION
    n_gpu_layers=35,        # Adjust based on your VRAM
                            # More layers = more GPU usage = faster
                            # Start with all layers, reduce if OOM

    # MEMORY OPTIMIZATION
    use_mmap=True,          # Memory-map model file
                            # Faster loading, shared across processes

    use_mlock=False,        # Lock model in RAM (requires permissions)
                            # Prevents swapping, improves consistency

    # CONTEXT OPTIMIZATION
    n_ctx=4096,             # Only as large as needed
                            # Larger = more memory per request

    # BATCH OPTIMIZATION
    n_batch=512,            # Prompt processing batch size
                            # Larger = faster prompt processing
                            # But uses more memory

    # CPU OPTIMIZATION (when using CPU)
    n_threads=8,            # Match physical cores, not hyperthreads
                            # Too many threads = cache thrashing

    # QUANTIZATION AWARENESS
    # Already set by model file, but affects performance
)

# Generation optimization
output = llm(
    "Your prompt",
    max_tokens=256,         # Don't generate more than needed

    # Sampling optimization
    temperature=0.7,        # 0 = greedy (fastest)
    top_k=40,              # Limit vocabulary considered

    # Stopping
    stop=["\n\n", "###"],  # Stop early when possible
)
```

---

## 9. Model Selection Guide

### Decision Framework

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MODEL SELECTION DECISION PROCESS                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                           START: What's your task?                          ║
║                                    │                                         ║
║              ┌─────────────────────┼─────────────────────┐                  ║
║              │                     │                     │                  ║
║              ▼                     ▼                     ▼                  ║
║         ┌────────┐           ┌────────┐           ┌────────┐               ║
║         │ SIMPLE │           │ MEDIUM │           │COMPLEX │               ║
║         └────────┘           └────────┘           └────────┘               ║
║              │                     │                     │                  ║
║              │                     │                     │                  ║
║     Chat, Q&A,          Code assist,        Analysis,                       ║
║     Summarize,          Reasoning,          Legal,                          ║
║     Classify            Multi-turn          Multi-doc                       ║
║              │                     │                     │                  ║
║              ▼                     ▼                     ▼                  ║
║         ┌────────┐           ┌────────┐           ┌────────┐               ║
║         │ 3B-7B  │           │ 7B-13B │           │13B-70B │               ║
║         │ model  │           │ model  │           │ model  │               ║
║         └────────┘           └────────┘           └────────┘               ║
║              │                     │                     │                  ║
║              ▼                     ▼                     ▼                  ║
║     ┌──────────────┐    ┌──────────────┐    ┌──────────────┐              ║
║     │ Llama 3.2 3B │    │ Llama 3.2 8B │    │ Llama 3.1 70B│              ║
║     │ Phi-3 3.8B   │    │ Mistral 7B   │    │ Mixtral 8x7B │              ║
║     │ Gemma 2B     │    │ Qwen2 7B     │    │ Qwen2 72B    │              ║
║     └──────────────┘    └──────────────┘    └──────────────┘              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Model Recommendations by Use Case

| Use Case | Primary Recommendation | Alternative | Why |
|:---------|:----------------------|:------------|:----|
| **Policy Q&A** | Llama 3.2 8B | Mistral 7B | Good instruction following, factual |
| **Document Summarization** | Llama 3.2 8B | Qwen2 7B | Strong at compression, coherent |
| **Code Generation** | Codestral 22B | DeepSeek-Coder 33B | Specialized training, low hallucination |
| **Code Review** | Codestral 22B | CodeLlama 13B | Understands patterns, explains issues |
| **Legal Analysis** | Llama 3.1 70B | Mixtral 8x7B | Complex reasoning, nuance |
| **Multilingual** | Qwen2 72B | Aya 35B | Extensive language coverage |
| **Compliance Checking** | Llama 3.2 8B + RAG | Mistral 7B + RAG | Combined with document retrieval |
| **Real-time Chat** | Llama 3.2 3B | Phi-3 3.8B | Low latency, fast response |
| **Air-gapped Systems** | Phi-3 3.8B | Gemma 2B | Runs on minimal hardware |

### Model Family Deep Dive

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         MODEL FAMILIES OVERVIEW                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  LLAMA (Meta)                                                               ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Llama 3.2: 1B, 3B - Great for edge/mobile                               ║
║  • Llama 3.2: 8B - Sweet spot for general tasks                            ║
║  • Llama 3.1: 70B, 405B - Frontier local capabilities                      ║
║                                                                              ║
║  Strengths: Instruction following, reasoning, coding                        ║
║  License: Permissive for most federal uses                                  ║
║  Ollama: ollama pull llama3.2                                               ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  MISTRAL (Mistral AI)                                                       ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Mistral 7B - Excellent efficiency, fast                                  ║
║  • Mixtral 8x7B - Mixture of Experts, great for varied tasks               ║
║  • Codestral 22B - Purpose-built for code                                  ║
║                                                                              ║
║  Strengths: Speed, code generation, European language support              ║
║  License: Apache 2.0                                                        ║
║  Ollama: ollama pull mistral                                                ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  QWEN (Alibaba)                                                             ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Qwen2: 0.5B to 72B range                                                 ║
║  • Qwen2.5: Latest, improved reasoning                                      ║
║  • Qwen2.5-Coder: Specialized for code                                     ║
║                                                                              ║
║  Strengths: Multilingual (esp. CJK), math, long context                    ║
║  License: Apache 2.0 for most sizes                                         ║
║  Ollama: ollama pull qwen2.5                                                ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  PHI (Microsoft)                                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Phi-3 Mini: 3.8B - Punches above weight class                           ║
║  • Phi-3 Medium: 14B - Strong reasoning                                     ║
║                                                                              ║
║  Strengths: Small size, reasoning, coding for its size                     ║
║  License: MIT                                                                ║
║  Ollama: ollama pull phi3                                                   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  GEMMA (Google)                                                             ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  • Gemma 2B, 7B - Original release                                         ║
║  • Gemma 2: 9B, 27B - Significantly improved                               ║
║                                                                              ║
║  Strengths: Quality outputs, safety tuning, efficient                      ║
║  License: Gemma license (permissive with restrictions)                     ║
║  Ollama: ollama pull gemma2                                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 10. Federal Deployment Patterns

### Pattern 1: Air-Gapped Deployment

For classified networks or environments without internet connectivity:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      AIR-GAPPED DEPLOYMENT PATTERN                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PHASE 1: MODEL PREPARATION (Internet-Connected Environment)                ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Download models on approved internet-connected system                   ║
║     ollama pull llama3.2:8b                                                 ║
║     ollama pull codestral:22b                                               ║
║                                                                              ║
║  2. Export models to transferable format                                    ║
║     # Models stored in ~/.ollama/models/                                    ║
║     tar -cvf ollama-models.tar ~/.ollama/models/                           ║
║                                                                              ║
║  3. Verify checksums                                                        ║
║     sha256sum ollama-models.tar > checksums.txt                            ║
║                                                                              ║
║  4. Scan for malware (per agency policy)                                   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  PHASE 2: TRANSFER (Data Diode / Approved Media)                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║           Internet                    │           Air-Gapped Network        ║
║           Connected                   │                                      ║
║                                       │                                      ║
║       ┌─────────────┐                │         ┌─────────────┐              ║
║       │   Models    │═══ DATA ═══════│═════════│   Transfer  │              ║
║       │   Archive   │    DIODE       │         │   Station   │              ║
║       └─────────────┘                │         └──────┬──────┘              ║
║                                       │                │                     ║
║       ┌─────────────┐                │                │                     ║
║       │  Checksums  │═══════════════════════════════════════════            ║
║       └─────────────┘                │                │                     ║
║                                       │                ▼                     ║
║                                       │         ┌─────────────┐              ║
║       OR: Write to approved          │         │  Verify &   │              ║
║       media (DVD, USB per policy)    │         │  Deploy     │              ║
║                                       │         └─────────────┘              ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  PHASE 3: DEPLOYMENT (Air-Gapped Network)                                  ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Verify checksums match                                                  ║
║     sha256sum -c checksums.txt                                              ║
║                                                                              ║
║  2. Install Ollama (from approved media/package)                           ║
║     # Pre-download installer or use local package repository               ║
║                                                                              ║
║  3. Extract models to Ollama directory                                      ║
║     tar -xvf ollama-models.tar -C /                                        ║
║                                                                              ║
║  4. Start Ollama service (no internet required)                            ║
║     ollama serve                                                            ║
║                                                                              ║
║  5. Verify models work                                                      ║
║     ollama list                                                             ║
║     ollama run llama3.2 "Test prompt"                                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Pattern 2: Containerized Production Deployment

```yaml
# docker-compose.yml for production federal deployment
version: '3.8'

services:
  # ═══════════════════════════════════════════════════════════════════════════
  # Ollama LLM Server
  # ═══════════════════════════════════════════════════════════════════════════
  ollama:
    image: ollama/ollama:latest
    container_name: ollama-server
    restart: unless-stopped

    ports:
      - "11434:11434"

    volumes:
      # Model storage (persistent)
      - ollama_models:/root/.ollama

      # Audit logs (mount to secure storage)
      - ./logs/ollama:/var/log/ollama

    environment:
      # Listen on all interfaces (for internal network access)
      - OLLAMA_HOST=0.0.0.0

      # Concurrent request handling
      - OLLAMA_NUM_PARALLEL=2

      # Keep one model loaded (memory management)
      - OLLAMA_MAX_LOADED_MODELS=1

    # GPU access (NVIDIA)
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

    # Resource limits
    mem_limit: 32g

    # Health check
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s

    # Security
    security_opt:
      - no-new-privileges:true
    read_only: false  # Ollama needs write access for model management

    networks:
      - llm-network

  # ═══════════════════════════════════════════════════════════════════════════
  # API Gateway / Reverse Proxy
  # ═══════════════════════════════════════════════════════════════════════════
  nginx:
    image: nginx:alpine
    container_name: llm-gateway
    restart: unless-stopped

    ports:
      - "443:443"
      - "80:80"

    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/certs:/etc/nginx/certs:ro
      - ./logs/nginx:/var/log/nginx

    depends_on:
      - ollama

    networks:
      - llm-network

  # ═══════════════════════════════════════════════════════════════════════════
  # Log Aggregation (for audit compliance)
  # ═══════════════════════════════════════════════════════════════════════════
  fluentd:
    image: fluent/fluentd:v1.16
    container_name: log-aggregator
    restart: unless-stopped

    volumes:
      - ./fluentd/fluent.conf:/fluentd/etc/fluent.conf:ro
      - ./logs:/var/log/apps:ro
      - ./audit_logs:/var/log/audit

    networks:
      - llm-network

volumes:
  ollama_models:
    driver: local

networks:
  llm-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16
```

### Pattern 3: Kubernetes Deployment

```yaml
# ollama-kubernetes.yaml
# Complete Kubernetes deployment for federal environments

---
# Namespace for isolation
apiVersion: v1
kind: Namespace
metadata:
  name: ai-services
  labels:
    name: ai-services
    environment: production

---
# PersistentVolumeClaim for model storage
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: ollama-models-pvc
  namespace: ai-services
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: fast-ssd  # Use your fast storage class
  resources:
    requests:
      storage: 100Gi  # Adjust based on model needs

---
# ConfigMap for Ollama configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: ollama-config
  namespace: ai-services
data:
  OLLAMA_HOST: "0.0.0.0"
  OLLAMA_NUM_PARALLEL: "2"
  OLLAMA_MAX_LOADED_MODELS: "1"

---
# Deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ollama
  namespace: ai-services
  labels:
    app: ollama
spec:
  replicas: 1  # Single replica with GPU
  selector:
    matchLabels:
      app: ollama
  template:
    metadata:
      labels:
        app: ollama
    spec:
      # Node selector for GPU nodes
      nodeSelector:
        nvidia.com/gpu: "true"

      containers:
      - name: ollama
        image: ollama/ollama:latest

        ports:
        - containerPort: 11434
          name: api

        envFrom:
        - configMapRef:
            name: ollama-config

        resources:
          limits:
            nvidia.com/gpu: 1
            memory: "32Gi"
            cpu: "8"
          requests:
            nvidia.com/gpu: 1
            memory: "16Gi"
            cpu: "4"

        volumeMounts:
        - name: models
          mountPath: /root/.ollama

        livenessProbe:
          httpGet:
            path: /api/tags
            port: 11434
          initialDelaySeconds: 60
          periodSeconds: 30

        readinessProbe:
          httpGet:
            path: /api/tags
            port: 11434
          initialDelaySeconds: 30
          periodSeconds: 10

        # Security context
        securityContext:
          allowPrivilegeEscalation: false
          capabilities:
            drop:
              - ALL

      volumes:
      - name: models
        persistentVolumeClaim:
          claimName: ollama-models-pvc

---
# Service
apiVersion: v1
kind: Service
metadata:
  name: ollama-service
  namespace: ai-services
spec:
  selector:
    app: ollama
  ports:
  - name: api
    port: 11434
    targetPort: 11434
  type: ClusterIP

---
# NetworkPolicy for security
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ollama-network-policy
  namespace: ai-services
spec:
  podSelector:
    matchLabels:
      app: ollama
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: trusted-apps
    ports:
    - protocol: TCP
      port: 11434
  egress:
  - to: []  # Deny all egress (air-gap compliant)
```

### Security Considerations for Federal Deployment

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FEDERAL SECURITY CHECKLIST                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ACCESS CONTROL                                                             ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  □ Authentication required for API access                                   ║
║  □ Role-based access control implemented                                    ║
║  □ API keys rotated regularly                                               ║
║  □ Network segmentation enforced                                            ║
║                                                                              ║
║  AUDIT LOGGING                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  □ All API requests logged with timestamps                                  ║
║  □ User identification captured                                             ║
║  □ Input prompts logged (consider sensitivity)                              ║
║  □ Output responses logged                                                  ║
║  □ Logs stored in tamper-evident storage                                    ║
║  □ Log retention per agency policy                                          ║
║                                                                              ║
║  DATA PROTECTION                                                            ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  □ TLS/HTTPS for all API communications                                     ║
║  □ Encryption at rest for model storage                                     ║
║  □ No sensitive data in model prompts without authorization                ║
║  □ Output filtering for PII/sensitive data                                  ║
║                                                                              ║
║  SYSTEM HARDENING                                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  □ Containers run as non-root                                               ║
║  □ Read-only file systems where possible                                    ║
║  □ Security patches applied regularly                                       ║
║  □ Vulnerability scanning performed                                         ║
║  □ STIG compliance verified                                                 ║
║                                                                              ║
║  AVAILABILITY                                                               ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║  □ Health monitoring configured                                             ║
║  □ Automatic restart on failure                                             ║
║  □ Resource limits prevent runaway processes                                ║
║  □ Backup and recovery procedures documented                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

---

## 11. Troubleshooting Guide

### Common Issues and Solutions

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    TROUBLESHOOTING DECISION TREE                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ISSUE: Model won't load / Out of memory                                    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Check available VRAM:                                                   ║
║     nvidia-smi  # Linux/Windows with NVIDIA                                 ║
║                                                                              ║
║  2. If VRAM insufficient:                                                   ║
║     • Use smaller quantization (Q4 instead of Q8)                          ║
║     • Use smaller model (7B instead of 13B)                                ║
║     • Reduce context size in Modelfile                                     ║
║     • Close other GPU applications                                          ║
║                                                                              ║
║  3. For CPU-only systems:                                                   ║
║     • Ensure sufficient RAM (model size + overhead)                         ║
║     • Use smallest practical quantization                                   ║
║     • Be patient - CPU inference is slow                                   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  ISSUE: Very slow generation                                                ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Verify GPU is being used:                                               ║
║     • Watch nvidia-smi during generation                                    ║
║     • GPU utilization should spike                                          ║
║                                                                              ║
║  2. If GPU not used:                                                        ║
║     • Reinstall Ollama with GPU support                                    ║
║     • Check CUDA/ROCm drivers                                              ║
║     • For llama.cpp: ensure compiled with CUDA                             ║
║                                                                              ║
║  3. If GPU is used but still slow:                                         ║
║     • Model may be too large (swapping between GPU/CPU)                    ║
║     • Reduce model size or quantization                                    ║
║     • Check for thermal throttling                                         ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  ISSUE: Poor quality outputs                                                ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Check model selection:                                                  ║
║     • Is model appropriate for task?                                        ║
║     • Try larger model if available                                        ║
║     • Use Q5 or Q8 instead of Q4 for quality-sensitive tasks              ║
║                                                                              ║
║  2. Check prompting:                                                        ║
║     • Include clear system prompt                                          ║
║     • Provide examples (few-shot)                                          ║
║     • Be specific about desired output format                              ║
║                                                                              ║
║  3. Check parameters:                                                       ║
║     • Temperature too high? Try 0.3-0.5 for factual tasks                 ║
║     • Context too small? Important info may be truncated                   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  ISSUE: Ollama server won't start                                           ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Check if already running:                                               ║
║     ps aux | grep ollama                                                    ║
║     # Or: systemctl status ollama                                           ║
║                                                                              ║
║  2. Check port availability:                                                ║
║     netstat -tulpn | grep 11434                                            ║
║     # Kill conflicting process or change port                              ║
║                                                                              ║
║  3. Check logs:                                                             ║
║     journalctl -u ollama -f  # systemd                                      ║
║     # Or: ~/.ollama/logs/                                                   ║
║                                                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  ISSUE: API connection refused                                              ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  1. Verify server is running:                                               ║
║     curl http://localhost:11434/api/tags                                    ║
║                                                                              ║
║  2. If accessing remotely:                                                  ║
║     • Set OLLAMA_HOST=0.0.0.0 before starting                              ║
║     • Check firewall rules                                                  ║
║     • Verify correct IP/hostname                                           ║
║                                                                              ║
║  3. For Docker:                                                             ║
║     • Ensure port mapping correct (-p 11434:11434)                         ║
║     • Check container is running: docker ps                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Diagnostic Commands

```bash
# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════

# Check GPU status (NVIDIA)
nvidia-smi

# Watch GPU usage in real-time
watch -n 1 nvidia-smi

# Check system memory
free -h

# Check disk space (for model storage)
df -h ~/.ollama

# ═══════════════════════════════════════════════════════════════════════════════
# OLLAMA DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════

# Check Ollama version
ollama --version

# List installed models
ollama list

# Show model details
ollama show llama3.2

# Check server status
curl http://localhost:11434/api/tags | jq

# Test simple generation
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2",
  "prompt": "Hello",
  "stream": false
}' | jq

# ═══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE TESTING
# ═══════════════════════════════════════════════════════════════════════════════

# Simple benchmark: measure time for generation
time ollama run llama3.2 "Write a 100-word summary of federal IT policy" --verbose

# The verbose flag shows:
# - Load time
# - Prompt evaluation time
# - Generation time
# - Tokens per second
```

---

## Exercises

### Exercise 3.1: Complete Ollama Setup

**Objective**: Install Ollama, pull a model, and verify it works.

**Steps**:
1. Install Ollama for your platform
2. Pull the Llama 3.2 8B model
3. Start an interactive session
4. Ask it to explain a federal regulation
5. Document the response time and quality

**Expected Output**: Working Ollama installation with verified model response.

### Exercise 3.2: Custom Federal Compliance Assistant

**Objective**: Create a customized model for federal compliance work.

**Steps**:
1. Create a Modelfile with appropriate system prompt for federal compliance
2. Set temperature and other parameters for factual responses
3. Create the custom model using `ollama create`
4. Test with compliance-related questions
5. Compare outputs with default model

**Deliverable**: Modelfile and comparison notes.

### Exercise 3.3: Performance Benchmarking

**Objective**: Understand performance characteristics across different configurations.

**Steps**:
1. Test same prompt with different model sizes (3B, 7B, 13B if available)
2. Compare different quantizations (Q4, Q5, Q8) of the same model
3. Measure: tokens/second, time to first token, memory usage
4. Document findings in a comparison table

**Deliverable**: Benchmark results with analysis.

### Exercise 3.4: API Integration Application

**Objective**: Build a practical application using Ollama's API.

**Steps**:
1. Create a Python script that:
   - Connects to Ollama API
   - Implements a multi-turn conversation
   - Includes error handling
   - Logs all interactions
2. Test with a document summarization task
3. Add streaming response handling

**Deliverable**: Working Python application with documentation.

### Exercise 3.5: Deployment Planning

**Objective**: Design a deployment for your environment.

**Steps**:
1. Assess your hardware resources
2. Determine appropriate models and quantizations
3. Choose deployment pattern (Docker, Kubernetes, direct)
4. Document security considerations
5. Create deployment configuration files

**Deliverable**: Deployment plan document with configuration files.

---

## Assessment

### Knowledge Check

1. What are the three primary benefits of local LLMs for federal agencies?

2. Explain the difference between Q4_K_M and Q8_0 quantization. When would you use each?

3. A 13B parameter model at Q4 quantization needs approximately how much VRAM?

4. What is the purpose of a Modelfile in Ollama? What key elements does it contain?

5. Describe the data flow in an air-gapped deployment pattern for local LLMs.

6. Why is memory bandwidth often the bottleneck for LLM inference rather than compute?

7. What is llama.cpp and why is it significant for the local LLM ecosystem?

8. When would you choose LocalAI over Ollama? What additional capabilities does it offer?

### Practical Assessment

**Scenario**: Your agency needs to deploy a local LLM solution for processing CUI documents. The requirements are:
- Air-gapped network (no internet)
- Must handle document summarization and Q&A
- Available hardware: Server with RTX 4090 (24GB VRAM)
- Need to support 10 concurrent users

**Task**:
1. Select appropriate model(s) and justify your choice
2. Design the deployment architecture
3. Create necessary configuration files
4. Document security controls
5. Provide a troubleshooting guide for common issues

---

## Next Module

➡️ [Module 04: API Integration](../04-api-integration/README.md)

---

<div align="center">

[⬆ Back to Top](#module-03-local-llms) · [📚 Return to Curriculum](../../README.md)

</div>
