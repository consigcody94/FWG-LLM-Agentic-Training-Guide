<div align="center">

# Module 01: LLM Foundations

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-None-gray?style=for-the-badge" alt="Prerequisites"/>

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Explain the transformer architecture and its key components
- [ ] Understand tokenization and its impact on model behavior
- [ ] Describe attention mechanisms and their role in context processing
- [ ] Apply model scaling laws to predict capability requirements
- [ ] Identify emergent capabilities and their implications
- [ ] Compare major model families and their strengths

---

## Table of Contents

1. [Transformer Architecture](#1-transformer-architecture)
2. [Tokenization Deep Dive](#2-tokenization-deep-dive)
3. [Attention Mechanisms](#3-attention-mechanisms)
4. [Model Scaling Laws](#4-model-scaling-laws)
5. [Emergent Capabilities](#5-emergent-capabilities)
6. [Model Families Overview](#6-model-families-overview)
7. [Exercises](#exercises)
8. [Assessment](#assessment)

---

## 1. Transformer Architecture

### Overview

The transformer architecture, introduced in "Attention Is All You Need" (2017), revolutionized natural language processing by enabling parallel processing of sequences.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        TRANSFORMER ARCHITECTURE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    Input Sequence                           Output Sequence                  ║
║         │                                         ▲                          ║
║         ▼                                         │                          ║
║  ┌─────────────┐                          ┌─────────────┐                   ║
║  │  Embedding  │                          │   Linear    │                   ║
║  │   + Pos     │                          │  + Softmax  │                   ║
║  └─────────────┘                          └─────────────┘                   ║
║         │                                         ▲                          ║
║         ▼                                         │                          ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │                         ENCODER STACK                           │        ║
║  │  ┌─────────────────────────────────────────────────────────┐   │        ║
║  │  │  Multi-Head Self-Attention                               │   │        ║
║  │  └─────────────────────────────────────────────────────────┘   │        ║
║  │                           │                                     │        ║
║  │                    Add & Normalize                              │        ║
║  │                           │                                     │        ║
║  │  ┌─────────────────────────────────────────────────────────┐   │        ║
║  │  │  Feed-Forward Neural Network                            │   │        ║
║  │  └─────────────────────────────────────────────────────────┘   │        ║
║  │                           │                                     │        ║
║  │                    Add & Normalize                              │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                              │                                               ║
║                              ▼                                               ║
║  ┌─────────────────────────────────────────────────────────────────┐        ║
║  │                         DECODER STACK                           │        ║
║  │  ┌─────────────────────────────────────────────────────────┐   │        ║
║  │  │  Masked Multi-Head Self-Attention                       │   │        ║
║  │  └─────────────────────────────────────────────────────────┘   │        ║
║  │                           │                                     │        ║
║  │                    Add & Normalize                              │        ║
║  │                           │                                     │        ║
║  │  ┌─────────────────────────────────────────────────────────┐   │        ║
║  │  │  Multi-Head Cross-Attention (Encoder Output)            │   │        ║
║  │  └─────────────────────────────────────────────────────────┘   │        ║
║  │                           │                                     │        ║
║  │                    Add & Normalize                              │        ║
║  │                           │                                     │        ║
║  │  ┌─────────────────────────────────────────────────────────┐   │        ║
║  │  │  Feed-Forward Neural Network                            │   │        ║
║  │  └─────────────────────────────────────────────────────────┘   │        ║
║  │                           │                                     │        ║
║  │                    Add & Normalize                              │        ║
║  └─────────────────────────────────────────────────────────────────┘        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Key Components

| Component | Function | Federal Application |
|:----------|:---------|:--------------------|
| **Embedding Layer** | Converts tokens to dense vectors | Document representation |
| **Positional Encoding** | Adds sequence position information | Maintaining document order |
| **Multi-Head Attention** | Parallel attention computations | Multi-aspect analysis |
| **Feed-Forward Network** | Non-linear transformations | Pattern extraction |
| **Layer Normalization** | Stabilizes training | Consistent outputs |

### Encoder vs Decoder Models

```
┌────────────────────────────────────────────────────────────────────────────┐
│                         MODEL ARCHITECTURE TYPES                           │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  ENCODER-ONLY              DECODER-ONLY             ENCODER-DECODER        │
│  (Bidirectional)           (Autoregressive)         (Seq2Seq)              │
│                                                                            │
│  ┌──────────────┐          ┌──────────────┐         ┌──────────────┐      │
│  │    BERT      │          │    GPT       │         │     T5       │      │
│  │   RoBERTa    │          │   Claude     │         │    BART      │      │
│  │   DeBERTa    │          │   Llama      │         │    mT5       │      │
│  └──────────────┘          └──────────────┘         └──────────────┘      │
│                                                                            │
│  Best For:                 Best For:                Best For:              │
│  • Classification          • Text Generation        • Translation          │
│  • NER                      • Chat/Dialog            • Summarization        │
│  • Embeddings               • Code Generation        • Q&A                  │
│  • Semantic Search          • Reasoning              • Document Processing  │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Tokenization Deep Dive

### What is Tokenization?

Tokenization is the process of converting text into numerical representations (tokens) that the model can process.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          TOKENIZATION PROCESS                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Input Text: "The federal agency deployed an AI system."                     ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                      TOKENIZATION                                    │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║                                                                              ║
║  Word-Level:    ["The", "federal", "agency", "deployed", "an", "AI",        ║
║                  "system", "."]                                              ║
║                                                                              ║
║  BPE/WordPiece: ["The", "Ġfederal", "Ġagency", "Ġdeployed", "Ġan",         ║
║                  "ĠAI", "Ġsystem", "."]                                      ║
║                                                                              ║
║  Token IDs:     [464, 5765, 4086, 12435, 281, 9552, 1080, 13]               ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                       EMBEDDING                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                              │                                               ║
║                              ▼                                               ║
║                                                                              ║
║  Dense Vectors: [[0.123, -0.456, ...], [0.789, 0.012, ...], ...]            ║
║                  (d_model dimensions, typically 768-8192)                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Tokenization Algorithms

| Algorithm | Used By | Vocabulary Size | Strengths |
|:----------|:--------|:----------------|:----------|
| **BPE** | GPT, Llama | 50K-100K | Handles rare words well |
| **WordPiece** | BERT, DistilBERT | 30K-50K | Efficient subword splits |
| **SentencePiece** | T5, Llama 2 | Variable | Language-agnostic |
| **Tiktoken** | GPT-4, Claude | 100K+ | Optimized for code |

### Token Counting Implications

```python
# Example: Token counting for federal budget planning
import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4")

# Government document excerpt
document = """
The Department of Defense (DoD) requests an appropriation of
$842 billion for fiscal year 2025, representing a 3.4% increase
from the previous fiscal year's enacted budget.
"""

tokens = encoder.encode(document)
print(f"Token count: {len(tokens)}")  # ~45 tokens
print(f"Estimated cost at $0.03/1K: ${len(tokens) * 0.03 / 1000:.4f}")
```

> **Federal Consideration:** Token costs directly impact API budgets. A 100-page PDF may contain 25,000+ tokens.

---

## 3. Attention Mechanisms

### Self-Attention Explained

Self-attention allows each token to "attend to" every other token in the sequence, capturing contextual relationships.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          SELF-ATTENTION MECHANISM                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Input: "The classified document requires security clearance"                ║
║                                                                              ║
║  Query (Q), Key (K), Value (V) projections for each token:                  ║
║                                                                              ║
║  Token: "document"                                                           ║
║         │                                                                    ║
║         ├──▶ Q_doc = W_q × embed("document")                                ║
║         ├──▶ K_doc = W_k × embed("document")                                ║
║         └──▶ V_doc = W_v × embed("document")                                ║
║                                                                              ║
║  Attention Scores (for "document"):                                          ║
║  ┌───────────────────────────────────────────────────────────────────┐      ║
║  │ Token          │ Score │ Interpretation                          │      ║
║  ├───────────────────────────────────────────────────────────────────┤      ║
║  │ "classified"   │ 0.42  │ Strong: modifier of document             │      ║
║  │ "security"     │ 0.31  │ Related: security context                │      ║
║  │ "requires"     │ 0.15  │ Medium: action relationship              │      ║
║  │ "clearance"    │ 0.08  │ Lower: indirect relationship             │      ║
║  │ "The"          │ 0.04  │ Minimal: article                         │      ║
║  └───────────────────────────────────────────────────────────────────┘      ║
║                                                                              ║
║  Attention Formula: Attention(Q,K,V) = softmax(QK^T / √d_k) × V             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Multi-Head Attention

Multiple attention heads allow the model to attend to different aspects simultaneously.

```
┌────────────────────────────────────────────────────────────────────────────┐
│                        MULTI-HEAD ATTENTION                                │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                            │
│  Input                                                                     │
│    │                                                                       │
│    ├───────────┬───────────┬───────────┬───────────┐                      │
│    │           │           │           │           │                      │
│    ▼           ▼           ▼           ▼           ▼                      │
│  ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐    ┌─────┐                     │
│  │Head1│    │Head2│    │Head3│    │Head4│    │Head8│   (8+ heads)        │
│  │     │    │     │    │     │    │     │    │     │                     │
│  │Syntax│   │Seman│    │Coref│    │Named│    │Sent │                     │
│  │     │    │tic  │    │erence│   │Entity│   │iment│                     │
│  └─────┘    └─────┘    └─────┘    └─────┘    └─────┘                     │
│    │           │           │           │           │                      │
│    └───────────┴───────────┴─────┬─────┴───────────┘                      │
│                                  │                                         │
│                                  ▼                                         │
│                          ┌─────────────┐                                   │
│                          │  Concatenate │                                   │
│                          │  + Project   │                                   │
│                          └─────────────┘                                   │
│                                  │                                         │
│                                  ▼                                         │
│                              Output                                        │
│                                                                            │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Model Scaling Laws

### Chinchilla Scaling Laws

Research has shown predictable relationships between model size, training data, and performance.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SCALING LAW RELATIONSHIPS                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Loss ∝ (Parameters)^(-0.076) + (Data)^(-0.095) + (Compute)^(-0.050)        ║
║                                                                              ║
║  Optimal Ratio: Parameters ≈ Data tokens / 20                                ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────┐     ║
║  │  Model Size    │  Optimal Training Data  │  Compute (FLOPs)       │     ║
║  ├────────────────────────────────────────────────────────────────────┤     ║
║  │  1B params     │  20B tokens             │  10^20                  │     ║
║  │  7B params     │  140B tokens            │  10^21                  │     ║
║  │  70B params    │  1.4T tokens            │  10^22                  │     ║
║  │  400B params   │  8T tokens              │  10^23                  │     ║
║  └────────────────────────────────────────────────────────────────────┘     ║
║                                                                              ║
║  Performance vs Scale:                                                       ║
║                                                                              ║
║  Capability │                                           ▲                   ║
║             │                                      ▲▲▲▲                     ║
║             │                                 ▲▲▲▲                          ║
║             │                            ▲▲▲▲                               ║
║             │                       ▲▲▲▲                                    ║
║             │                  ▲▲▲▲                                         ║
║             │             ▲▲▲▲                                              ║
║             │        ▲▲▲▲                                                   ║
║             │   ▲▲▲▲                                                        ║
║             └───────────────────────────────────────────────▶               ║
║                              log(Parameters)                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Practical Implications for Federal Use

| Use Case | Recommended Size | Reasoning |
|:---------|:-----------------|:----------|
| Basic Q&A | 7-13B | Cost-effective for simple queries |
| Document Analysis | 30-70B | Better reasoning for complex docs |
| Code Generation | 34B+ | Needs extensive code training |
| Multi-domain Expert | 70B+ | Broad knowledge required |
| Sensitive Classification | 7-13B (local) | Data residency requirements |

---

## 5. Emergent Capabilities

### Definition

Emergent capabilities are abilities that appear suddenly at certain model scales, not present in smaller versions.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          EMERGENT CAPABILITIES                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Capability         │ Emerges At    │ Example                               ║
║  ───────────────────┼───────────────┼─────────────────────────────────────  ║
║  Basic Reasoning    │ ~1B params    │ Simple math, basic logic              ║
║  Few-Shot Learning  │ ~10B params   │ Learn from examples in context        ║
║  Chain-of-Thought   │ ~60B params   │ Step-by-step reasoning                ║
║  Code Generation    │ ~70B params   │ Complex programming tasks             ║
║  Multi-step Math    │ ~100B params  │ Word problems, algebra                ║
║  Theory of Mind     │ ~175B params  │ Understanding others' beliefs         ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────┐     ║
║  │                     EMERGENCE VISUALIZATION                        │     ║
║  │                                                                     │     ║
║  │  Accuracy                                                          │     ║
║  │     │                                              ┌───────────┐   │     ║
║  │ 100%│                                              │ EMERGENT  │   │     ║
║  │     │                                         ▲▲▲▲▲│ CAPABILITY│   │     ║
║  │  75%│                                    ▲▲▲▲▲     └───────────┘   │     ║
║  │     │                                ▲▲▲▲                          │     ║
║  │  50%│                            ▲▲▲▲                              │     ║
║  │     │                         ▲▲▲                                  │     ║
║  │  25%│  ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲  (random baseline)                │     ║
║  │     │                                                              │     ║
║  │   0%└────────────────────────────────────────────────▶             │     ║
║  │        1B      10B     100B    500B                                │     ║
║  │                 Model Parameters                                   │     ║
║  └────────────────────────────────────────────────────────────────────┘     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Federal Implications

- **Capability Thresholds:** Certain federal tasks may require minimum model sizes
- **Safety Considerations:** Larger models may exhibit unexpected behaviors
- **Testing Requirements:** Each scale jump requires new evaluation protocols

---

## 6. Model Families Overview

### Major LLM Families

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                            LLM FAMILY TREE                                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                         PROPRIETARY MODELS                          │    ║
║  ├─────────────────────────────────────────────────────────────────────┤    ║
║  │                                                                      │    ║
║  │  OpenAI                    Anthropic               Google            │    ║
║  │  ┌──────────┐              ┌──────────┐           ┌──────────┐      │    ║
║  │  │ GPT-4o   │              │Claude 3.5│           │Gemini Pro│      │    ║
║  │  │ GPT-4    │              │Claude 3  │           │Gemini 1.5│      │    ║
║  │  │ GPT-3.5  │              │Claude 2  │           │  Ultra   │      │    ║
║  │  └──────────┘              └──────────┘           └──────────┘      │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐    ║
║  │                         OPEN SOURCE MODELS                          │    ║
║  ├─────────────────────────────────────────────────────────────────────┤    ║
║  │                                                                      │    ║
║  │  Meta                      Mistral                 Others            │    ║
║  │  ┌──────────┐              ┌──────────┐           ┌──────────┐      │    ║
║  │  │Llama 3.2 │              │Mixtral 8x│           │  Qwen2   │      │    ║
║  │  │Llama 3.1 │              │Mistral 7B│           │  Phi-3   │      │    ║
║  │  │Llama 2   │              │  Codestral│          │  Falcon  │      │    ║
║  │  └──────────┘              └──────────┘           └──────────┘      │    ║
║  │                                                                      │    ║
║  └─────────────────────────────────────────────────────────────────────┘    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Selection Matrix

| Criteria | GPT-4 | Claude 3.5 | Gemini | Llama 3 | Mistral |
|:---------|:-----:|:----------:|:------:|:-------:|:-------:|
| **Reasoning** | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| **Coding** | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| **Context Length** | 128K | 200K | 1M+ | 128K | 32K |
| **Local Deployment** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **FedRAMP Ready** | ⏳ | ⏳ | ✅ | N/A | ❌ |
| **Cost (per 1M tokens)** | $30 | $15 | $7 | Free | $2 |

---

## Exercises

### Exercise 1.1: Token Analysis
Analyze tokenization differences across models for a sample federal document.

### Exercise 1.2: Attention Visualization
Use BertViz to visualize attention patterns in a security-focused text.

### Exercise 1.3: Scaling Estimation
Calculate required compute and data for a hypothetical federal LLM.

### Exercise 1.4: Model Selection
Given a federal use case, recommend an appropriate model with justification.

---

## Assessment

### Knowledge Check (10 Questions)

1. What are the three main components of the attention mechanism?
2. Explain the difference between encoder-only and decoder-only architectures.
3. How does tokenization affect model cost calculations?
4. What is an emergent capability? Give two examples.
5. What does the Chinchilla scaling law recommend for optimal training?
6. Compare the context windows of GPT-4, Claude 3.5, and Gemini.
7. Why might a federal agency choose a smaller, local model over a larger API model?
8. What is multi-head attention and why is it useful?
9. How do BPE and WordPiece tokenization differ?
10. What federal compliance considerations affect model selection?

### Practical Assessment

Deploy an Ollama model locally and demonstrate understanding of token counting, context window limitations, and basic inference.

---

## Next Module

➡️ [Module 02: Web GUI AI](../02-web-gui-ai/README.md)

---

<div align="center">

[⬆ Back to Top](#module-01-llm-foundations) · [📚 Return to Curriculum](../../README.md)

</div>
