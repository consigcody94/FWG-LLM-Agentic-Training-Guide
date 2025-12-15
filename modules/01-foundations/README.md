<div align="center">

# Module 01: LLM Foundations

<img src="https://img.shields.io/badge/Duration-6_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Difficulty-Beginner-green?style=for-the-badge" alt="Difficulty"/>
<img src="https://img.shields.io/badge/Prerequisites-None-gray?style=for-the-badge" alt="Prerequisites"/>

*Understanding the fundamental architecture and principles that power modern AI language models*

</div>

---

## Learning Objectives

By the end of this module, you will be able to:

- [ ] Explain the transformer architecture and understand why it revolutionized NLP
- [ ] Understand tokenization and its critical impact on model behavior and costs
- [ ] Describe attention mechanisms and how they enable context understanding
- [ ] Apply model scaling laws to predict capability requirements for your use cases
- [ ] Identify emergent capabilities and understand their implications for federal applications
- [ ] Compare major model families and select appropriate models for specific tasks

---

## Why This Module Matters

Before diving into practical applications of AI, it's essential to understand **how these systems actually work**. This foundational knowledge will help you:

1. **Make informed decisions** about which models to use for specific tasks
2. **Troubleshoot issues** when AI systems don't behave as expected
3. **Optimize costs** by understanding token economics
4. **Communicate effectively** with technical teams and vendors
5. **Assess risks** by understanding model limitations and failure modes

Think of this module as learning how an engine works before driving a car—you don't need to be a mechanic, but understanding the basics helps you be a better driver and make smarter decisions about maintenance and capabilities.

---

## Table of Contents

1. [The AI Revolution: Historical Context](#1-the-ai-revolution-historical-context)
2. [Transformer Architecture Deep Dive](#2-transformer-architecture-deep-dive)
3. [Tokenization: The Foundation of Understanding](#3-tokenization-the-foundation-of-understanding)
4. [Attention Mechanisms: How Models "Think"](#4-attention-mechanisms-how-models-think)
5. [Model Scaling Laws](#5-model-scaling-laws)
6. [Emergent Capabilities](#6-emergent-capabilities)
7. [Model Families Overview](#7-model-families-overview)
8. [Practical Exercises](#8-practical-exercises)
9. [Assessment](#9-assessment)

---

## 1. The AI Revolution: Historical Context

### Understanding Where We Came From

To appreciate modern Large Language Models (LLMs), it's helpful to understand the journey that brought us here. This context will help you understand why certain architectural decisions were made and what problems they solve.

#### The Evolution of Language AI

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    EVOLUTION OF NATURAL LANGUAGE PROCESSING                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  1950s-1980s: RULE-BASED SYSTEMS                                            ║
║  ───────────────────────────────                                            ║
║  • Hand-coded grammar rules                                                 ║
║  • Limited vocabulary dictionaries                                          ║
║  • Brittle: broke with unexpected inputs                                    ║
║  • Example: ELIZA (1966) - simple pattern matching chatbot                  ║
║                                                                              ║
║  1990s-2000s: STATISTICAL METHODS                                           ║
║  ──────────────────────────────                                             ║
║  • Machine learning from data                                               ║
║  • N-gram language models                                                   ║
║  • Hidden Markov Models                                                     ║
║  • Better but still limited context                                         ║
║                                                                              ║
║  2010-2017: NEURAL NETWORKS                                                 ║
║  ─────────────────────────                                                  ║
║  • Recurrent Neural Networks (RNNs)                                         ║
║  • Long Short-Term Memory (LSTM)                                            ║
║  • Better at sequences but slow and limited                                 ║
║  • Struggled with long documents                                            ║
║                                                                              ║
║  2017-PRESENT: TRANSFORMER ERA                                              ║
║  ─────────────────────────────                                              ║
║  • "Attention Is All You Need" paper (Google, 2017)                         ║
║  • Parallel processing of entire sequences                                  ║
║  • Massive scaling becomes possible                                         ║
║  • GPT, BERT, Claude, Llama, and modern LLMs                               ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

#### Why the Transformer Changed Everything

Before transformers, processing language was like reading a book one word at a time while trying to remember everything you've read. The further you got, the harder it became to remember the beginning.

**The key insight of transformers**: Instead of processing words sequentially, process the entire text at once and let each word "look at" every other word to understand context.

**Real-world analogy**: Imagine you're analyzing a 100-page federal regulation. The old approach was like reading it once, start to finish, trying to remember everything. The transformer approach is like having 100 copies of yourself, each assigned to one page, with instant communication between all of you to discuss how your pages relate to each other.

### What Makes LLMs "Large"?

The term "Large Language Model" refers to three types of scale:

| Dimension | What It Means | Why It Matters |
|:----------|:--------------|:---------------|
| **Parameters** | The adjustable numbers in the model (like dials) | More parameters = more "knowledge storage capacity" |
| **Training Data** | Text the model learned from | More diverse data = broader knowledge |
| **Compute** | Processing power used for training | More compute = better pattern learning |

**Key insight**: These three dimensions work together. A model with 70 billion parameters trained on 2 trillion tokens of text using massive GPU clusters can exhibit capabilities that simply don't exist in smaller models—this is called "emergence," which we'll explore later.

---

## 2. Transformer Architecture Deep Dive

### Overview: The Building Blocks of Modern AI

The transformer architecture is the foundation of every modern LLM, including GPT-4, Claude, Llama, and Gemini. Understanding it helps you grasp why these models behave the way they do.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        TRANSFORMER ARCHITECTURE                              ║
║                    (Simplified for Understanding)                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║    INPUT: "The federal agency requires compliance documentation"             ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                         1. TOKENIZATION                                 │ ║
║  │   Break text into pieces the model can process                         │ ║
║  │   ["The", "federal", "agency", "requires", "compliance", "document..."]│ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                         2. EMBEDDING                                    │ ║
║  │   Convert tokens into numerical vectors (lists of numbers)             │ ║
║  │   "federal" → [0.23, -0.87, 0.45, 0.12, -0.56, ...]  (768+ numbers)   │ ║
║  │   These numbers capture the "meaning" of each word                     │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                    3. POSITIONAL ENCODING                              │ ║
║  │   Add information about WHERE each word appears in the sentence        │ ║
║  │   Without this, "dog bites man" = "man bites dog" (same words!)       │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │               4. ATTENTION LAYERS (x many times)                       │ ║
║  │   Each word "looks at" every other word to understand context          │ ║
║  │   "compliance" pays attention to "requires" and "documentation"        │ ║
║  │   This happens multiple times with different "perspectives"            │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                    5. FEED-FORWARD LAYERS                              │ ║
║  │   Process the attended information to extract patterns                 │ ║
║  │   Think of this as "thinking about what was learned"                   │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                      │                                       ║
║                                      ▼                                       ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                      6. OUTPUT GENERATION                              │ ║
║  │   Predict the most likely next word (repeated for each word)           │ ║
║  │   Output: "that" → "must" → "be" → "submitted" → "by" → ...           │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Understanding Each Component

#### 2.1 Tokenization (Detailed in Section 3)

Before a model can process text, it must convert human-readable text into numbers. This is tokenization—the process of breaking text into "tokens" that the model understands.

**Key point**: Tokenization is not the same as splitting by words. The text "unhappiness" might become ["un", "happiness"] or ["unhapp", "iness"] depending on the tokenizer. This has profound implications for cost, behavior, and capabilities.

#### 2.2 Embeddings: Turning Words into Numbers

An embedding is a list of numbers (called a "vector") that represents a word or token. These numbers capture the **meaning** of the word in a way that allows mathematical operations.

**Why this matters**: In embedding space, similar concepts are numerically close together. This is why the model "understands" that "car" and "automobile" mean similar things—their embedding vectors are similar.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         UNDERSTANDING EMBEDDINGS                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  SIMPLIFIED EXAMPLE (real embeddings have 768-8192 dimensions):             ║
║                                                                              ║
║  Word: "king"     → [0.8, 0.9, 0.2, 0.1]                                    ║
║  Word: "queen"    → [0.8, 0.9, 0.8, 0.1]                                    ║
║  Word: "man"      → [0.2, 0.1, 0.2, 0.1]                                    ║
║  Word: "woman"    → [0.2, 0.1, 0.8, 0.1]                                    ║
║                                                                              ║
║  MATHEMATICAL RELATIONSHIPS:                                                ║
║                                                                              ║
║  king - man + woman ≈ queen                                                 ║
║  [0.8, 0.9, 0.2, 0.1] - [0.2, 0.1, 0.2, 0.1] + [0.2, 0.1, 0.8, 0.1]        ║
║  = [0.8, 0.9, 0.8, 0.1] ≈ queen                                            ║
║                                                                              ║
║  This shows the model has learned:                                          ║
║  • "king" and "queen" share "royalty" features                             ║
║  • "man" and "woman" differ in "gender" features                           ║
║  • These relationships are captured mathematically                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Federal application**: This is why AI can understand that "Executive Order" and "Presidential Directive" are related concepts, even if they weren't explicitly trained on documents explaining this relationship.

#### 2.3 Positional Encoding: Understanding Word Order

Without positional encoding, the model would treat "The agency approved the policy" and "The policy approved the agency" identically—both contain the same words!

Positional encoding adds mathematical patterns to each embedding that tell the model "this token is in position 1, this one is in position 2, etc."

**How it works**: Sine and cosine functions of different frequencies are added to each embedding. Position 1 gets one pattern, position 2 gets a different pattern, and so on. The model learns to use these patterns to understand word order.

#### 2.4 Attention: The Core Innovation (Detailed in Section 4)

Attention is the mechanism that allows each word to "look at" every other word in the input. This is what makes transformers so powerful—they can capture long-range dependencies that previous architectures couldn't handle.

**Example**: In "The compliance officer who reviewed the 500-page document submitted their report," the word "submitted" needs to know that "officer" is the one doing the submitting, not "document." Attention allows this connection across many words.

#### 2.5 Feed-Forward Networks: Processing What Was Learned

After attention determines which words are relevant to each other, feed-forward networks process this information. Think of attention as "gathering information" and feed-forward as "thinking about what was gathered."

Each feed-forward layer:
1. Takes the attended representation
2. Projects it to a higher dimension (expanding)
3. Applies a non-linear function (ReLU or GELU)
4. Projects back down (compressing)

**Analogy**: If attention is like reading and highlighting important parts of a document, feed-forward networks are like reflecting on what you highlighted and forming conclusions.

### Encoder vs. Decoder: Two Architectural Choices

Modern LLMs come in different architectural variants, each optimized for different tasks:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      MODEL ARCHITECTURE COMPARISON                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  ENCODER-ONLY MODELS                                                        ║
║  ───────────────────                                                        ║
║  Examples: BERT, RoBERTa, DeBERTa                                           ║
║                                                                              ║
║  How they work:                                                             ║
║  • Process entire input at once (bidirectional)                             ║
║  • Each word sees ALL other words, before and after                         ║
║  • Output: Understanding of the input                                       ║
║                                                                              ║
║  Best for:                                                                  ║
║  • Classification ("Is this email spam?")                                   ║
║  • Named Entity Recognition ("Find all organization names")                 ║
║  • Semantic search ("Find similar documents")                               ║
║  • Sentiment analysis ("Is this review positive?")                          ║
║                                                                              ║
║  Federal use cases:                                                         ║
║  • Classifying FOIA requests by type                                        ║
║  • Identifying PII in documents                                             ║
║  • Routing correspondence to correct department                             ║
║                                                                              ║
║  ──────────────────────────────────────────────────────────────────────────║
║                                                                              ║
║  DECODER-ONLY MODELS                                                        ║
║  ───────────────────                                                        ║
║  Examples: GPT-4, Claude, Llama, Mistral                                    ║
║                                                                              ║
║  How they work:                                                             ║
║  • Process left-to-right only (autoregressive)                              ║
║  • Each word only sees words that came BEFORE it                            ║
║  • Output: Generate new text, one token at a time                           ║
║                                                                              ║
║  Best for:                                                                  ║
║  • Text generation ("Write a memo about...")                                ║
║  • Conversation ("Answer this question...")                                 ║
║  • Code generation ("Write a Python function that...")                      ║
║  • Reasoning ("Analyze this situation and recommend...")                    ║
║                                                                              ║
║  Federal use cases:                                                         ║
║  • Drafting responses to inquiries                                          ║
║  • Summarizing lengthy reports                                              ║
║  • Generating code for data analysis                                        ║
║  • Answering policy questions                                               ║
║                                                                              ║
║  ──────────────────────────────────────────────────────────────────────────║
║                                                                              ║
║  ENCODER-DECODER MODELS                                                     ║
║  ──────────────────────                                                     ║
║  Examples: T5, BART, mT5                                                    ║
║                                                                              ║
║  How they work:                                                             ║
║  • Encoder processes input (bidirectional understanding)                    ║
║  • Decoder generates output (looking at encoder + previous output)          ║
║  • Best of both worlds for transformation tasks                             ║
║                                                                              ║
║  Best for:                                                                  ║
║  • Translation ("Translate to Spanish...")                                  ║
║  • Summarization ("Summarize this document...")                             ║
║  • Question answering ("Given this context, answer...")                     ║
║                                                                              ║
║  Federal use cases:                                                         ║
║  • Translating citizen communications                                       ║
║  • Creating executive summaries                                             ║
║  • Extracting answers from policy documents                                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Key insight for practitioners**: When you use ChatGPT or Claude, you're using decoder-only models. They generate text one word at a time, with each word informed by everything that came before. This is why they can seem to "change their mind" mid-sentence—they're literally making decisions word by word.

---

## 3. Tokenization: The Foundation of Understanding

### What Is Tokenization?

Tokenization is the process of converting human-readable text into a sequence of numbers that a model can process. This seemingly simple step has profound implications for model behavior, costs, and capabilities.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          TOKENIZATION IN ACTION                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Original text: "The DOD's FY2024 appropriation is $842B"                   ║
║                                                                              ║
║  ┌──────────────────────────────────────────────────────────────────────┐   ║
║  │                      TOKENIZATION PROCESS                             │   ║
║  │                                                                       │   ║
║  │  Step 1: Text enters tokenizer                                       │   ║
║  │          "The DOD's FY2024 appropriation is $842B"                   │   ║
║  │                                                                       │   ║
║  │  Step 2: Split into tokens (subwords)                                │   ║
║  │          ["The", " D", "OD", "'s", " FY", "202", "4",                │   ║
║  │           " approp", "riation", " is", " $", "842", "B"]             │   ║
║  │                                                                       │   ║
║  │  Step 3: Convert to token IDs (numbers)                              │   ║
║  │          [464, 360, 3727, 338, 19446, 2366, 19, ...]                 │   ║
║  │                                                                       │   ║
║  │  Total: 13 tokens (this costs money per token with APIs!)            │   ║
║  └──────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  WHY NOT JUST SPLIT BY WORDS?                                               ║
║  ─────────────────────────────                                              ║
║  • Vocabulary would be infinite (every possible word)                       ║
║  • Rare words wouldn't be represented well                                  ║
║  • Numbers, codes, and acronyms would be problematic                        ║
║  • No way to handle new or misspelled words                                 ║
║                                                                              ║
║  SUBWORD TOKENIZATION SOLVES THIS:                                          ║
║  • Fixed vocabulary (typically 32K-100K tokens)                             ║
║  • Common words = single token: "the" → [464]                              ║
║  • Rare words = multiple tokens: "cryptocurrency" → ["crypt", "ocurrency"] ║
║  • Can handle ANY text, even made-up words                                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### How Tokenization Algorithms Work

Different models use different tokenization algorithms, but they all share the same goal: represent text efficiently with a fixed vocabulary.

#### Byte-Pair Encoding (BPE)

The most common algorithm, used by GPT models and many others.

**How it works (simplified)**:

1. Start with individual characters as the vocabulary
2. Count which pairs of characters appear most frequently
3. Merge the most frequent pair into a single token
4. Repeat until desired vocabulary size is reached

**Example**:
```
Starting text: "low lower lowest"
Initial: l, o, w, l, o, w, e, r, l, o, w, e, s, t

Most common pair: "l" + "o" → merge into "lo"
After merge: lo, w, lo, w, e, r, lo, w, e, s, t

Most common pair: "lo" + "w" → merge into "low"
After merge: low, low, e, r, low, e, s, t

Continue until vocabulary size is reached...
```

**Result**: Common words like "the" become single tokens, while rare words are broken into pieces.

#### WordPiece (BERT-style)

Similar to BPE but uses a slightly different merging criterion based on likelihood rather than pure frequency. Used by BERT and related models.

#### SentencePiece

A language-agnostic tokenizer that treats the input as a raw stream of characters, making it better for languages without clear word boundaries (like Chinese or Japanese).

### Why Tokenization Matters for Federal Applications

#### 1. Cost Implications

API pricing is **per token**, not per word. Understanding tokenization helps you estimate and control costs.

```python
# Example: Estimating costs for document processing
import tiktoken

def estimate_cost(document_text, model="gpt-4", price_per_1k_input=0.03, price_per_1k_output=0.06):
    """
    Estimate the cost of processing a document with an LLM.

    This is critical for federal budget planning. A single large PDF
    can cost dollars to process—multiply by thousands of documents
    and costs become significant.
    """
    # Get the tokenizer for the model
    encoder = tiktoken.encoding_for_model(model)

    # Count tokens
    input_tokens = len(encoder.encode(document_text))

    # Estimate output (rough: assume 1/3 of input for summaries)
    estimated_output_tokens = input_tokens // 3

    # Calculate cost
    input_cost = (input_tokens / 1000) * price_per_1k_input
    output_cost = (estimated_output_tokens / 1000) * price_per_1k_output
    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "estimated_output_tokens": estimated_output_tokens,
        "input_cost": f"${input_cost:.4f}",
        "output_cost": f"${output_cost:.4f}",
        "total_cost": f"${total_cost:.4f}"
    }

# Example with federal document
sample_memo = """
MEMORANDUM FOR: All Agency Personnel
FROM: Chief Information Officer
SUBJECT: Implementation of AI Governance Framework

Effective immediately, all artificial intelligence systems deployed within
the agency must comply with the requirements outlined in OMB Memorandum
M-24-10 and Executive Order 14110. This includes mandatory risk assessments,
documentation of training data sources, and regular bias audits...
"""

# This would output approximately:
# {"input_tokens": 89, "input_cost": "$0.0027", "total_cost": "$0.0044"}
```

**Federal budget consideration**: A 100-page PDF policy document might contain 25,000-40,000 tokens. At current GPT-4 prices, processing one such document costs approximately $1-2. Processing 10,000 documents per month = $10,000-20,000/month just for input processing.

#### 2. Behavior Implications

How text is tokenized affects how the model "sees" and processes it:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                   TOKENIZATION AFFECTS BEHAVIOR                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  EXAMPLE 1: Numbers                                                         ║
║  ──────────────────                                                         ║
║  "12345" might tokenize as ["123", "45"] or ["1", "234", "5"]              ║
║  The model doesn't "see" 12345 as a number—it sees pieces                  ║
║  This is why LLMs often struggle with precise arithmetic                    ║
║                                                                              ║
║  EXAMPLE 2: Code                                                            ║
║  ──────────────────                                                         ║
║  "def calculate_total(items):" tokenizes differently than                   ║
║  "def calculateTotal(items):"                                               ║
║  Coding style affects token count and processing                            ║
║                                                                              ║
║  EXAMPLE 3: Acronyms                                                        ║
║  ──────────────────                                                         ║
║  "FISMA" might be 1 token (common) or 5 tokens (F-I-S-M-A if rare)        ║
║  Common government acronyms are usually single tokens                       ║
║  Obscure ones get split, potentially losing the semantic connection         ║
║                                                                              ║
║  EXAMPLE 4: Languages                                                       ║
║  ──────────────────                                                         ║
║  English: "hello" = 1 token                                                ║
║  Chinese: "你好" might = 2-3 tokens                                         ║
║  Non-English text often uses more tokens per concept                        ║
║  This affects costs and context window usage                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

#### 3. Context Window Implications

Models have a maximum "context window"—the total number of tokens they can process at once. This includes both your input AND the model's output.

| Model | Context Window | Approximate Equivalent |
|:------|:---------------|:-----------------------|
| GPT-4 (standard) | 8,192 tokens | ~6,000 words or ~24 pages |
| GPT-4 (128K) | 128,000 tokens | ~96,000 words or ~380 pages |
| Claude 3.5 | 200,000 tokens | ~150,000 words or ~600 pages |
| Gemini 1.5 | 1,000,000 tokens | ~750,000 words or ~3,000 pages |

**Practical implication**: If you need to analyze a 500-page regulation, you'll need a model with sufficient context window, or you'll need to implement chunking strategies (covered in Module 10: RAG Systems).

---

## 4. Attention Mechanisms: How Models "Think"

### The Core Insight

Attention is the mechanism that allows transformers to understand context. Before attention, models processed text sequentially and struggled to connect information across long distances.

**The key question attention answers**: "When processing this word, which other words should I pay attention to?"

### Self-Attention Explained

Let's walk through how self-attention works with a concrete example:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          SELF-ATTENTION EXAMPLE                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Sentence: "The security clearance that the employee requested was denied"  ║
║                                                                              ║
║  Question: When processing "denied", what should the model focus on?        ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                    ATTENTION SCORES FOR "denied"                       │ ║
║  │                                                                        │ ║
║  │  Token              Attention Score    Why                             │ ║
║  │  ───────────────────────────────────────────────────────────────────  │ ║
║  │  "clearance"        0.35 (HIGH)        What was denied                │ ║
║  │  "was"              0.25 (HIGH)        Grammar: passive voice          │ ║
║  │  "requested"        0.15 (MEDIUM)      Context: denial of request      │ ║
║  │  "employee"         0.10 (MEDIUM)      Who was affected                │ ║
║  │  "security"         0.08 (LOW)         Type of clearance               │ ║
║  │  "The"              0.03 (MINIMAL)     Article, less important         │ ║
║  │  "that"             0.02 (MINIMAL)     Connector word                  │ ║
║  │  "the"              0.02 (MINIMAL)     Article                         │ ║
║  │                                                                        │ ║
║  │  Total: 1.00 (attention scores always sum to 1)                       │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  WHAT THIS MEANS:                                                           ║
║  The model "understands" that "denied" is primarily about "clearance"      ║
║  and knows to connect it to the grammatical structure ("was") and the      ║
║  original action ("requested"). This allows it to correctly interpret      ║
║  that a security clearance was denied—not the employee or the request.     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### The Query-Key-Value Framework

Attention uses three learned transformations for each token: Query (Q), Key (K), and Value (V).

**Analogy**: Think of it like a library search system:

- **Query (Q)**: "What am I looking for?" (The current word asks a question)
- **Key (K)**: "What do I contain?" (Each word advertises its content)
- **Value (V)**: "Here's my actual information" (The content to retrieve)

The attention mechanism compares each Query against all Keys to determine relevance, then retrieves a weighted combination of Values based on that relevance.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         QUERY-KEY-VALUE MECHANISM                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  For the word "denied" in our example:                                      ║
║                                                                              ║
║  STEP 1: Create Query                                                       ║
║  ──────────────────                                                         ║
║  Q_denied = W_query × Embedding("denied")                                   ║
║  This transforms the embedding into a "question" vector                     ║
║  Intuitively: "What grammatical and semantic info do I need?"               ║
║                                                                              ║
║  STEP 2: Compare Query to all Keys                                          ║
║  ────────────────────────────────                                           ║
║  For each word in the sentence:                                             ║
║    K_word = W_key × Embedding(word)                                         ║
║    Score = Q_denied · K_word / √d_k    (dot product, scaled)               ║
║                                                                              ║
║  The dot product measures similarity:                                       ║
║    High score = Query and Key are aligned (relevant)                        ║
║    Low score = Query and Key are orthogonal (irrelevant)                    ║
║                                                                              ║
║  STEP 3: Apply Softmax                                                      ║
║  ────────────────────                                                       ║
║  Convert scores to probabilities (sum to 1):                                ║
║    attention_weights = softmax(scores)                                      ║
║                                                                              ║
║  STEP 4: Retrieve weighted Values                                           ║
║  ────────────────────────────────                                           ║
║  For each word:                                                             ║
║    V_word = W_value × Embedding(word)                                       ║
║                                                                              ║
║  Final output = Σ (attention_weight_i × V_i)                                ║
║                                                                              ║
║  This creates a new representation for "denied" that incorporates           ║
║  contextual information from the most relevant other words.                 ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Multi-Head Attention: Multiple Perspectives

A single attention mechanism can only capture one type of relationship at a time. Multi-head attention runs multiple attention mechanisms in parallel, each learning to focus on different types of relationships.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         MULTI-HEAD ATTENTION                                 ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Input: "The contractor submitted the compliance report yesterday"          ║
║                                                                              ║
║  ┌────────────────────────────────────────────────────────────────────────┐ ║
║  │                                                                        │ ║
║  │                        INPUT EMBEDDING                                 │ ║
║  │                             │                                          │ ║
║  │        ┌──────────┬─────────┼─────────┬──────────┐                    │ ║
║  │        │          │         │         │          │                    │ ║
║  │        ▼          ▼         ▼         ▼          ▼                    │ ║
║  │     ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐   ┌─────┐                  │ ║
║  │     │Head │   │Head │   │Head │   │Head │   │Head │    (8+ heads     │ ║
║  │     │  1  │   │  2  │   │  3  │   │  4  │   │  5  │     typical)     │ ║
║  │     └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘   └──┬──┘                  │ ║
║  │        │          │         │         │          │                    │ ║
║  │     Learns     Learns    Learns    Learns    Learns                   │ ║
║  │     subject-   object-   temporal  adj-noun   verb-                   │ ║
║  │     verb       verb      relations relations  object                  │ ║
║  │     relations  relations                      relations               │ ║
║  │        │          │         │         │          │                    │ ║
║  │        └──────────┴─────────┴─────────┴──────────┘                    │ ║
║  │                             │                                          │ ║
║  │                             ▼                                          │ ║
║  │                    CONCATENATE + PROJECT                               │ ║
║  │                             │                                          │ ║
║  │                             ▼                                          │ ║
║  │                   COMBINED OUTPUT                                      │ ║
║  │                                                                        │ ║
║  └────────────────────────────────────────────────────────────────────────┘ ║
║                                                                              ║
║  WHAT EACH HEAD MIGHT LEARN:                                                ║
║                                                                              ║
║  Head 1: "submitted" pays attention to "contractor" (who did it?)          ║
║  Head 2: "submitted" pays attention to "report" (what was submitted?)      ║
║  Head 3: "submitted" pays attention to "yesterday" (when?)                 ║
║  Head 4: "compliance" pays attention to "report" (what kind?)              ║
║  Head 5: "report" pays attention to "submitted" (what happened to it?)     ║
║                                                                              ║
║  The model doesn't decide these relationships—they emerge from training.    ║
║  Different heads naturally specialize in different linguistic patterns.     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Masked Attention in Decoder Models

In decoder-only models (like GPT and Claude), there's an additional constraint: when generating text, each position can only attend to previous positions, not future ones.

**Why?** During generation, the model predicts one token at a time. When generating the 5th word, it hasn't generated the 6th word yet—so it can't attend to it!

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MASKED vs UNMASKED ATTENTION                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Sentence: "The quick brown fox"                                            ║
║                                                                              ║
║  ENCODER (BERT-style): Bidirectional - sees everything                      ║
║  ─────────────────────────────────────────────────────                      ║
║            The    quick   brown    fox                                      ║
║  The        ✓       ✓       ✓       ✓                                       ║
║  quick      ✓       ✓       ✓       ✓                                       ║
║  brown      ✓       ✓       ✓       ✓                                       ║
║  fox        ✓       ✓       ✓       ✓                                       ║
║                                                                              ║
║  Every word can attend to every other word.                                 ║
║  Good for understanding, not for generation.                                ║
║                                                                              ║
║  DECODER (GPT-style): Masked - only sees past                               ║
║  ─────────────────────────────────────────────                              ║
║            The    quick   brown    fox                                      ║
║  The        ✓       ✗       ✗       ✗                                       ║
║  quick      ✓       ✓       ✗       ✗                                       ║
║  brown      ✓       ✓       ✓       ✗                                       ║
║  fox        ✓       ✓       ✓       ✓                                       ║
║                                                                              ║
║  Each word can only attend to itself and previous words.                    ║
║  ✗ means "masked" - cannot attend to these positions.                       ║
║  This is what allows autoregressive generation.                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Why Attention Matters for Federal Applications

Understanding attention helps explain AI behavior in practical scenarios:

1. **Long Document Analysis**: Models with better attention can maintain connections across 100+ pages—important for policy documents.

2. **Multi-step Reasoning**: When answering complex questions, attention allows the model to gather relevant facts from different parts of the context.

3. **Following Instructions**: Attention allows the model to keep your instructions in mind throughout a long response.

4. **Handling Ambiguity**: Attention patterns help resolve ambiguous references ("it", "they", "this policy") by connecting them to the right antecedents.

---

## 5. Model Scaling Laws

### The Discovery That Changed AI

In 2020, researchers at OpenAI discovered predictable mathematical relationships between model size, training data, compute, and performance. These "scaling laws" explain why bigger models are systematically better and help predict how much resources are needed for specific capabilities.

### Chinchilla Scaling Laws

The Chinchilla paper (DeepMind, 2022) refined these laws and made a crucial discovery: **most models were undertrained for their size**.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         SCALING LAW FUNDAMENTALS                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE CORE RELATIONSHIP:                                                     ║
║  ─────────────────────                                                      ║
║  Performance (Loss) ∝ Parameters^(-0.076) + Data^(-0.095) + Noise           ║
║                                                                              ║
║  In plain English:                                                          ║
║  • Doubling parameters → ~5% improvement                                    ║
║  • Doubling training data → ~6% improvement                                 ║
║  • Both matter, but data matters slightly more                              ║
║                                                                              ║
║  THE CHINCHILLA INSIGHT:                                                    ║
║  ──────────────────────                                                     ║
║  Optimal training: Parameters ≈ Training Tokens / 20                        ║
║                                                                              ║
║  │  Model Size    │  Optimal Training Data  │  Compute Budget              │
║  ├────────────────┼─────────────────────────┼────────────────              │
║  │     1B         │        20B tokens       │     $50K                     │
║  │     7B         │       140B tokens       │    $500K                     │
║  │    70B         │      1.4T tokens        │    $5M                       │
║  │   175B         │      3.5T tokens        │   $15M                       │
║  │   500B         │       10T tokens        │   $50M                       │
║                                                                              ║
║  WHAT THIS MEANS IN PRACTICE:                                               ║
║  ───────────────────────────                                                ║
║  • GPT-3 (175B) was undertrained—could have been smaller and equally good  ║
║  • Llama 2 70B performs like GPT-3 with much less compute                  ║
║  • Smaller, well-trained models often beat larger, undertrained ones       ║
║  • Training data quality matters as much as quantity                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### What This Means for Federal AI Strategy

Understanding scaling laws helps with several practical decisions:

#### 1. Model Selection

Don't assume bigger is always better. A well-trained 7B model might outperform a poorly trained 13B model.

| Use Case | Recommended Size | Why |
|:---------|:-----------------|:----|
| Simple Q&A, classification | 3-7B | Tasks don't require massive knowledge |
| General document work | 7-13B | Good balance of capability and cost |
| Complex reasoning, analysis | 30-70B | More "thinking capacity" needed |
| Cutting-edge capabilities | 70B+ or flagship APIs | Maximum capability |

#### 2. Local vs. Cloud Trade-offs

Scaling laws help you understand what's possible locally:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                     LOCAL DEPLOYMENT CAPABILITIES                            ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HARDWARE                    VIABLE MODELS              CAPABILITY LEVEL    ║
║  ─────────────────────────────────────────────────────────────────────────  ║
║                                                                              ║
║  Laptop (16GB RAM)          3-7B quantized              Basic tasks         ║
║  • Consumer MacBook         • Llama 3.2 3B              • Simple Q&A        ║
║  • Intel with 8GB GPU       • Phi-3 Mini               • Summarization      ║
║                             • Gemma 2B                 • Classification     ║
║                                                                              ║
║  Workstation (32-64GB)      7-13B quantized            Moderate tasks       ║
║  • Mac Studio               • Llama 3.1 8B             • Document analysis  ║
║  • RTX 4070/4080           • Mistral 7B               • Code assistance    ║
║                             • CodeLlama 13B           • Conversation       ║
║                                                                              ║
║  High-end Server            30-70B quantized           Advanced tasks       ║
║  • RTX 4090 or A100        • Llama 3.1 70B            • Complex reasoning   ║
║  • 128GB+ RAM              • Qwen2 72B                • Multi-step analysis║
║                             • Mixtral 8x7B            • Expert-level Q&A   ║
║                                                                              ║
║  Note: "Quantized" means compressed to use less memory, with some           ║
║  quality trade-off. See Module 03 for details.                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

#### 3. Cost-Performance Optimization

Scaling laws help estimate whether investing in a larger model is worth it:

**Rule of thumb**: Doubling model size gives ~5% improvement. If you need dramatically better performance, you might need to:
- Scale 10x for ~15% improvement
- Use a different approach (fine-tuning, RAG, better prompts)
- Accept that the task may be beyond current AI capabilities

---

## 6. Emergent Capabilities

### What Is Emergence?

Emergence refers to capabilities that appear suddenly at certain model scales—capabilities that simply don't exist in smaller models, then appear as if by magic when models get large enough.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                          EMERGENT CAPABILITIES                               ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  VISUALIZING EMERGENCE:                                                     ║
║  ─────────────────────                                                      ║
║                                                                              ║
║  Accuracy                                                                   ║
║     │                                              ┌─────────┐              ║
║ 100%│                                         ▲▲▲▲▲│ EMERGED │              ║
║     │                                    ▲▲▲▲▲     └─────────┘              ║
║  80%│                                ▲▲▲▲                                   ║
║     │                            ▲▲▲▲                                       ║
║  60%│                        ▲▲▲▲      ← Capability "turns on"              ║
║     │                    ▲▲▲▲                                               ║
║  40%│             ───────┘                                                  ║
║     │   ▲─────────                                                          ║
║  20%│  Random baseline (no capability)                                      ║
║     │                                                                       ║
║   0%└────────────────────────────────────────────────────▶                  ║
║         1B      10B     50B    100B   200B   500B                           ║
║                      Model Parameters                                       ║
║                                                                              ║
║  The capability doesn't gradually improve—it suddenly appears!              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Key Emergent Capabilities

| Capability | Emerges Around | Description | Federal Relevance |
|:-----------|:---------------|:------------|:------------------|
| **Few-Shot Learning** | ~10B params | Learn new tasks from a few examples in the prompt | Adapt to agency-specific formats without fine-tuning |
| **Chain-of-Thought** | ~60B params | Break complex problems into steps | Explain reasoning for audit trails |
| **Mathematical Reasoning** | ~100B params | Solve word problems, basic algebra | Budget calculations, data analysis |
| **Code Generation** | ~70B params | Write functional programs | Automate data processing tasks |
| **Theory of Mind** | ~175B params | Understand others' beliefs and intentions | Better citizen interaction understanding |

### Chain-of-Thought: A Critical Capability

Chain-of-Thought (CoT) reasoning is particularly important for federal applications because it enables **transparency and auditability**.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CHAIN-OF-THOUGHT REASONING                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WITHOUT Chain-of-Thought:                                                  ║
║  ────────────────────────                                                   ║
║  User: "Is this contractor eligible for the small business set-aside?"      ║
║  Model: "No."                                                               ║
║                                                                              ║
║  Problem: No explanation, can't verify reasoning, not auditable.            ║
║                                                                              ║
║  ──────────────────────────────────────────────────────────────────────────║
║                                                                              ║
║  WITH Chain-of-Thought:                                                     ║
║  ──────────────────────                                                     ║
║  User: "Is this contractor eligible for the small business set-aside?       ║
║         Please explain your reasoning step by step."                        ║
║                                                                              ║
║  Model: "Let me analyze this step by step:                                  ║
║                                                                              ║
║  1. First, I'll check the size standard for this NAICS code (541330).      ║
║     The size standard is $25.5 million in average annual receipts.         ║
║                                                                              ║
║  2. The contractor's average annual receipts over the past 5 years:        ║
║     ($28M + $31M + $27M + $29M + $30M) / 5 = $29M                          ║
║                                                                              ║
║  3. $29M exceeds the $25.5M threshold.                                     ║
║                                                                              ║
║  4. Therefore, this contractor does NOT qualify as a small business        ║
║     under NAICS code 541330.                                                ║
║                                                                              ║
║  Conclusion: No, the contractor is not eligible for the small business     ║
║  set-aside because their average annual receipts ($29M) exceed the         ║
║  size standard ($25.5M) for this NAICS code."                              ║
║                                                                              ║
║  Benefits:                                                                  ║
║  ✓ Reasoning is visible and verifiable                                     ║
║  ✓ Errors can be identified at specific steps                              ║
║  ✓ Creates documentation for audit trail                                   ║
║  ✓ Humans can catch if the AI used wrong data                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Implications for Federal AI Strategy

Understanding emergence has several practical implications:

1. **Capability Thresholds**: Some tasks simply require minimum model sizes. If you need complex reasoning, a 7B model may never work well no matter how much you optimize.

2. **Future Planning**: As models continue to scale, new capabilities will emerge. Stay informed about what new capabilities are appearing.

3. **Safety Considerations**: Emergent capabilities can be unexpected. Larger models may exhibit behaviors not present in smaller versions—this requires ongoing monitoring.

4. **Evaluation Requirements**: Test capabilities at each scale. Don't assume a capability works just because the model is "big enough."

---

## 7. Model Families Overview

### The Major Players

Understanding the landscape of available models helps you make informed selection decisions.

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                            LLM LANDSCAPE 2024                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  PROPRIETARY MODELS (API Access Only)                                       ║
║  ════════════════════════════════════                                       ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  OPENAI                                                              │   ║
║  │  ─────────                                                           │   ║
║  │  Models: GPT-4o, GPT-4, GPT-4 Turbo, GPT-3.5 Turbo                  │   ║
║  │  Strengths: Broad capabilities, excellent instruction following     │   ║
║  │  Context: Up to 128K tokens                                         │   ║
║  │  Cost: $0.50-30 per 1M tokens (varies by model)                     │   ║
║  │  FedRAMP: In progress (available via Azure Government)              │   ║
║  │                                                                      │   ║
║  │  Best for: General-purpose tasks, code generation, analysis         │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  ANTHROPIC                                                           │   ║
║  │  ──────────                                                          │   ║
║  │  Models: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku           │   ║
║  │  Strengths: Safety focus, nuanced responses, long context           │   ║
║  │  Context: Up to 200K tokens                                         │   ║
║  │  Cost: $0.25-75 per 1M tokens (varies by model)                     │   ║
║  │  FedRAMP: In progress                                               │   ║
║  │                                                                      │   ║
║  │  Best for: Long documents, nuanced analysis, safety-critical tasks  │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  GOOGLE                                                              │   ║
║  │  ────────                                                            │   ║
║  │  Models: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 1.0 Ultra        │   ║
║  │  Strengths: Multimodal (text, image, video), massive context        │   ║
║  │  Context: Up to 1M+ tokens                                          │   ║
║  │  Cost: $1.25-5 per 1M tokens                                        │   ║
║  │  FedRAMP: Authorized (Google Cloud for Government)                  │   ║
║  │                                                                      │   ║
║  │  Best for: Multimodal tasks, very long documents, Google integration│   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  OPEN SOURCE MODELS (Can Run Locally)                                       ║
║  ═════════════════════════════════════                                      ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  META LLAMA                                                          │   ║
║  │  ────────────                                                        │   ║
║  │  Models: Llama 3.2 (1B, 3B), Llama 3.1 (8B, 70B, 405B)             │   ║
║  │  Strengths: Strong performance, permissive license, large community │   ║
║  │  Context: Up to 128K tokens                                         │   ║
║  │  Requirements: 4GB-280GB+ RAM depending on size                     │   ║
║  │  License: Llama Community License (free for most uses)              │   ║
║  │                                                                      │   ║
║  │  Best for: Local deployment, customization, data sovereignty        │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  MISTRAL                                                             │   ║
║  │  ─────────                                                           │   ║
║  │  Models: Mistral 7B, Mixtral 8x7B, Mixtral 8x22B, Codestral        │   ║
║  │  Strengths: Efficient, strong coding, mixture-of-experts design     │   ║
║  │  Context: Up to 32K tokens                                          │   ║
║  │  Requirements: 6GB-90GB+ RAM depending on size                      │   ║
║  │  License: Apache 2.0 (most models)                                  │   ║
║  │                                                                      │   ║
║  │  Best for: Code generation, efficient local deployment              │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
║  ┌─────────────────────────────────────────────────────────────────────┐   ║
║  │  OTHER NOTABLE OPEN SOURCE                                           │   ║
║  │  ─────────────────────────                                           │   ║
║  │  • Qwen2 (Alibaba): Strong multilingual, up to 72B                  │   ║
║  │  • Phi-3 (Microsoft): Very efficient small models                   │   ║
║  │  • Gemma 2 (Google): Open weights, efficient                        │   ║
║  │  • DeepSeek-Coder: Specialized for code                             │   ║
║  │  • Yi (01.AI): Strong reasoning capabilities                        │   ║
║  └─────────────────────────────────────────────────────────────────────┘   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Model Selection Framework

Choosing the right model requires balancing multiple factors:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                        MODEL SELECTION DECISION TREE                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║                           START HERE                                         ║
║                               │                                              ║
║                               ▼                                              ║
║           ┌─────────────────────────────────────┐                           ║
║           │  Does data need to stay on-premise? │                           ║
║           └─────────────────────────────────────┘                           ║
║                     │                    │                                   ║
║                    YES                  NO                                   ║
║                     │                    │                                   ║
║                     ▼                    ▼                                   ║
║       ┌────────────────────┐    ┌────────────────────┐                      ║
║       │   LOCAL MODELS     │    │   API MODELS       │                      ║
║       │  (Llama, Mistral)  │    │  (GPT, Claude)     │                      ║
║       └────────────────────┘    └────────────────────┘                      ║
║                │                         │                                   ║
║                ▼                         ▼                                   ║
║       What's your GPU?          Need FedRAMP?                                ║
║            │                         │                                       ║
║     ┌──────┴──────┐          ┌──────┴──────┐                                ║
║     │             │          │             │                                 ║
║  ≤8GB VRAM   ≥24GB VRAM    YES           NO                                 ║
║     │             │          │             │                                 ║
║     ▼             ▼          ▼             ▼                                 ║
║  ┌───────┐  ┌───────┐  ┌─────────┐  ┌─────────┐                            ║
║  │3-7B   │  │13-70B │  │Gemini   │  │Any major│                            ║
║  │models │  │models │  │Azure    │  │provider │                            ║
║  └───────┘  └───────┘  │OpenAI   │  └─────────┘                            ║
║                        └─────────┘                                          ║
║                                                                              ║
║  ADDITIONAL FACTORS TO CONSIDER:                                            ║
║  ───────────────────────────────                                            ║
║  • Task type: Simple Q&A vs complex reasoning                               ║
║  • Volume: Low usage favors per-token APIs; high usage favors local         ║
║  • Context needs: Long documents need 100K+ context models                  ║
║  • Latency: Real-time needs faster inference                                ║
║  • Multimodal: Image/audio needs specific model capabilities                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

### Detailed Comparison Matrix

| Factor | GPT-4 | Claude 3.5 | Gemini 1.5 | Llama 3.1 70B | Mistral |
|:-------|:-----:|:----------:|:----------:|:-------------:|:-------:|
| **Reasoning** | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★☆ |
| **Coding** | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★★★ |
| **Long Context** | 128K | 200K | 1M+ | 128K | 32K |
| **Local Deploy** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **FedRAMP** | ⏳ (via Azure) | ⏳ | ✅ | N/A | ❌ |
| **Cost/1M tokens** | $10-30 | $3-15 | $1.25-5 | Free* | $0.25-2 |
| **Multimodal** | ✅ | ✅ | ✅ | ✅ | Limited |

*Free for the model weights; requires your own compute infrastructure.

---

## 8. Practical Exercises

### Exercise 1.1: Token Economics Analysis

**Objective**: Understand the cost implications of tokenization for a real federal use case.

**Scenario**: Your agency processes 5,000 FOIA requests per month. Each request averages 2 pages (approximately 500 words). You need to generate a 1-page response for each.

**Tasks**:
1. Use the tiktoken library to count tokens in a sample request
2. Calculate monthly API costs for GPT-4 vs GPT-3.5
3. Analyze potential cost savings from prompt optimization

**Starter Code**:
```python
import tiktoken

def analyze_foia_costs():
    """
    Analyze token costs for FOIA request processing.

    This exercise helps understand the real-world cost implications
    of tokenization in federal AI applications.
    """
    # Sample FOIA request text
    sample_request = """
    Dear FOIA Officer,

    Pursuant to the Freedom of Information Act, 5 U.S.C. § 552,
    I hereby request copies of all records pertaining to the agency's
    implementation of artificial intelligence systems between
    January 1, 2023 and December 31, 2024.

    Specifically, I am requesting:
    1. All contracts or agreements with AI vendors
    2. Risk assessments conducted for AI systems
    3. Training data documentation
    4. Bias audit reports
    5. Internal memos discussing AI policy

    I am willing to pay reasonable duplication fees up to $50.
    Please contact me if costs exceed this amount.

    Sincerely,
    [Requester Name]
    """

    # Initialize tokenizer for GPT-4
    encoder = tiktoken.encoding_for_model("gpt-4")

    # Count tokens in sample
    request_tokens = len(encoder.encode(sample_request))

    print(f"Sample request tokens: {request_tokens}")

    # TODO: Complete the cost analysis
    # 1. Estimate tokens for a typical response
    # 2. Calculate cost per request for different models
    # 3. Project monthly costs at 5,000 requests/month
    # 4. Identify potential optimizations

# Run the analysis
analyze_foia_costs()
```

### Exercise 1.2: Attention Visualization

**Objective**: Visualize attention patterns to understand how models process federal documents.

**Tasks**:
1. Install BertViz library
2. Analyze attention patterns for a security-related sentence
3. Identify which words "attend to" each other
4. Explain the patterns in plain language

### Exercise 1.3: Model Capability Assessment

**Objective**: Evaluate different models for a specific federal task.

**Scenario**: Your agency needs to classify incoming correspondence into 10 categories.

**Tasks**:
1. Design a test set of 20 sample messages
2. Test at least 3 different models (can use free tiers)
3. Measure accuracy, latency, and cost
4. Recommend a model with justification

### Exercise 1.4: Scaling Law Application

**Objective**: Apply scaling law concepts to a resource allocation decision.

**Scenario**: You have $10,000/month budget for AI compute. Should you use:
- Many GPT-3.5 calls?
- Fewer GPT-4 calls?
- Local deployment of open-source models?

**Tasks**:
1. Define specific quality requirements
2. Calculate cost/capability trade-offs
3. Present a recommendation with supporting analysis

---

## 9. Assessment

### Knowledge Check Questions

Answer these questions to verify your understanding:

1. **Architecture**: Explain in your own words why transformers can process text faster than previous architectures (RNNs).

2. **Tokenization**: Why might the phrase "unmistakable" require more tokens in some languages than in English?

3. **Attention**: If a model is answering a question about federal budget allocation, which words in "The Department of Defense's 2024 budget request was approved by Congress" would likely have high attention scores?

4. **Scaling Laws**: A 13B parameter model and a 70B parameter model both achieve 85% accuracy on your task. Which should you use, and why?

5. **Emergence**: Your team asks why the 7B model can't perform chain-of-thought reasoning well. How would you explain this using the concept of emergence?

6. **Model Selection**: For processing classified documents that cannot leave your agency's air-gapped network, which model family would you recommend and why?

### Practical Assessment

**Capstone Exercise**: Deploy Ollama locally and demonstrate:

1. Model download and verification
2. Token counting for a sample document
3. Basic inference with a federal-themed prompt
4. Context window limitation demonstration
5. Comparison of different model sizes

**Deliverables**:
- Written report (2-3 pages) explaining your setup
- Screenshot evidence of working deployment
- Analysis of observed model behavior
- Recommendations for your agency based on your findings

---

## Key Takeaways

1. **Transformers revolutionized NLP** by enabling parallel processing and attention mechanisms that capture context across entire documents.

2. **Tokenization directly impacts costs** and behavior—understanding it helps you budget and optimize AI usage.

3. **Attention mechanisms** allow models to connect relevant information across long distances, enabling sophisticated understanding.

4. **Scaling laws are predictable**—bigger models are systematically better, but with diminishing returns.

5. **Emergent capabilities appear suddenly** at certain scales—don't expect smaller models to gain capabilities they don't have.

6. **Model selection requires balancing** capability, cost, compliance, and deployment constraints.

---

## Additional Resources

### Papers (Foundational)
- "Attention Is All You Need" (Vaswani et al., 2017)
- "Language Models are Few-Shot Learners" (Brown et al., 2020)
- "Training Compute-Optimal Large Language Models" (Hoffmann et al., 2022)

### Documentation
- [OpenAI Tokenizer](https://platform.openai.com/tokenizer)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [Ollama Documentation](https://ollama.ai/docs)

### Federal Guidance
- NIST AI Risk Management Framework
- OMB M-24-10: Advancing Governance, Innovation, and Risk Management for Agency Use of AI
- Executive Order 14110 on Safe, Secure, and Trustworthy AI

---

## Next Module

➡️ [Module 02: Web GUI AI Interfaces](../02-web-gui-ai/README.md)

---

<div align="center">

[⬆ Back to Top](#module-01-llm-foundations) · [📚 Return to Curriculum](../../README.md)

</div>
