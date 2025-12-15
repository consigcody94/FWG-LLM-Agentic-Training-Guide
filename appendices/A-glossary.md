<div align="center">

# Appendix A: Glossary of Terms

<img src="https://img.shields.io/badge/Reference-Glossary-blue?style=for-the-badge" alt="Glossary"/>

</div>

---

## A

**A2A (Agent-to-Agent) Protocol**
An open standard enabling AI agents to discover, communicate, and collaborate through standardized Agent Cards, JSON-RPC transport, and task state management.

**Agentic AI**
AI systems that can autonomously plan, reason, and execute multi-step tasks with minimal human intervention, often using tools and interacting with external systems.

**Alignment**
The process of ensuring AI systems behave in accordance with human values, intentions, and safety requirements.

**API (Application Programming Interface)**
A set of protocols and tools for building software applications, allowing different systems to communicate.

**Attention Mechanism**
A neural network component that allows models to focus on relevant parts of the input when generating output, enabling context-aware processing.

**Authorization to Operate (ATO)**
Formal approval from an authorizing official permitting a federal information system to operate at an acceptable level of risk.

---

## B

**Batch Processing**
Processing multiple requests together to optimize resource utilization and reduce per-request overhead.

**Baseline (Security)**
A minimum set of security controls required for an information system based on its impact level (Low, Moderate, or High).

**BPE (Byte Pair Encoding)**
A tokenization algorithm that iteratively merges frequent character pairs to create a vocabulary of subword tokens.

---

## C

**Chain-of-Thought (CoT)**
A prompting technique that encourages LLMs to show step-by-step reasoning, improving performance on complex tasks.

**Claude**
Anthropic's family of large language models, known for safety focus and long context windows.

**Claude Code**
Anthropic's CLI tool for AI-assisted software development.

**Compliance**
Adherence to laws, regulations, standards, and policies applicable to federal information systems.

**Constitutional AI**
Anthropic's training approach using AI-generated critiques guided by a set of principles (constitution) to improve safety and helpfulness.

**Context Window**
The maximum number of tokens an LLM can process in a single request, including both input and output.

**CUI (Controlled Unclassified Information)**
Unclassified information requiring safeguarding or dissemination controls pursuant to federal law, regulation, or policy.

---

## D

**Decoder**
The component of a transformer that generates output tokens, typically using autoregressive (one token at a time) generation.

**Dual-Use**
Technology or capabilities that can be used for both beneficial and harmful purposes.

---

## E

**Embedding**
A dense vector representation of text (or other data) that captures semantic meaning, used for similarity search and retrieval.

**Emergent Capability**
An ability that appears suddenly in LLMs at certain scales, not present in smaller models.

**Encoder**
The component of a transformer that processes input and creates contextual representations.

**Executive Order 14110**
Presidential order on Safe, Secure, and Trustworthy Artificial Intelligence (October 2023).

---

## F

**FAR (Federal Acquisition Regulation)**
The primary regulation governing federal government procurement.

**FedRAMP (Federal Risk and Authorization Management Program)**
A government-wide program providing a standardized approach to security assessment, authorization, and continuous monitoring for cloud products and services.

**Few-Shot Learning**
The ability of an LLM to learn tasks from a small number of examples provided in the prompt.

**Fine-Tuning**
Training a pre-trained model on a specific dataset to improve performance on particular tasks.

**FIPS 199**
Federal standard for categorizing information and information systems based on impact levels (Low, Moderate, High).

**FISMA (Federal Information Security Management Act)**
Federal law requiring agencies to develop, document, and implement information security programs.

**Function Calling**
LLM capability to generate structured output that can be used to invoke external functions or APIs.

---

## G

**GGUF (GPT-Generated Unified Format)**
A file format for storing quantized LLM models, commonly used with llama.cpp and Ollama.

**GPT (Generative Pre-trained Transformer)**
OpenAI's family of large language models based on the transformer architecture.

**Grounding**
Connecting LLM outputs to verified facts or sources to reduce hallucination.

---

## H

**Hallucination**
When an LLM generates plausible-sounding but factually incorrect or fabricated information.

**Human-in-the-Loop (HITL)**
A design pattern where human oversight is incorporated into AI system workflows.

---

## I

**Impact Level**
FIPS 199 categorization (Low, Moderate, High) based on potential harm from security breaches.

**Inference**
The process of running input through a trained model to generate predictions or outputs.

---

## J

**JSON-RPC**
A remote procedure call protocol encoded in JSON, used as the transport mechanism for MCP and A2A.

---

## L

**LangChain**
A framework for developing applications powered by language models, providing tools for chains, agents, and retrieval.

**LangGraph**
LangChain's library for building stateful, multi-actor applications with LLMs.

**LLM (Large Language Model)**
A neural network trained on vast text data to understand and generate human language.

**llama.cpp**
A C++ library for efficient inference of Llama-family models, enabling local deployment.

**Local LLM**
Running LLM inference on local hardware rather than cloud APIs, enabling data sovereignty and offline operation.

**LoRA (Low-Rank Adaptation)**
A parameter-efficient fine-tuning technique that trains small adapter layers instead of full model weights.

---

## M

**MCP (Model Context Protocol)**
Anthropic's open standard for connecting LLM applications to external data sources, tools, and services.

**Multi-Agent System**
An AI system where multiple agents collaborate or compete to accomplish complex tasks.

**Multimodal**
Models or systems capable of processing multiple types of input (text, images, audio, etc.).

---

## N

**NIST (National Institute of Standards and Technology)**
Federal agency responsible for developing cybersecurity standards and guidelines.

**NIST 800-53**
Comprehensive catalog of security and privacy controls for federal information systems.

**NIST AI RMF**
NIST Artificial Intelligence Risk Management Framework for managing AI-related risks.

---

## O

**OCSF (Open Cybersecurity Schema Framework)**
A standard for security event data normalization.

**Ollama**
A tool for running large language models locally with minimal configuration.

**OMB (Office of Management and Budget)**
Federal agency that issues government-wide policy memoranda, including AI guidance.

**OSCAL (Open Security Controls Assessment Language)**
NIST standard for expressing security control information in machine-readable formats.

---

## P

**PII (Personally Identifiable Information)**
Information that can identify or trace an individual's identity.

**POA&M (Plan of Action and Milestones)**
Document identifying remediation tasks for security findings, with responsible parties and deadlines.

**Prompt Engineering**
The practice of designing effective prompts to guide LLM behavior and outputs.

**Provider**
A company or organization offering LLM services (e.g., OpenAI, Anthropic, Google).

---

## Q

**QLoRA (Quantized Low-Rank Adaptation)**
A memory-efficient fine-tuning technique combining quantization with LoRA.

**Quantization**
Reducing model precision (e.g., from 32-bit to 4-bit) to decrease memory requirements and increase inference speed.

---

## R

**RAG (Retrieval-Augmented Generation)**
A technique combining LLMs with external knowledge retrieval to improve accuracy and reduce hallucination.

**Rate Limiting**
Controlling the frequency of API requests to prevent overload and ensure fair usage.

**ReAct (Reasoning + Acting)**
A prompting framework combining chain-of-thought reasoning with action execution.

**RLHF (Reinforcement Learning from Human Feedback)**
Training technique using human preferences to improve LLM behavior.

---

## S

**Scaling Laws**
Empirical relationships between model size, training data, compute, and performance.

**SSE (Server-Sent Events)**
A standard for pushing real-time updates from server to client over HTTP.

**SSP (System Security Plan)**
Document describing how security controls are implemented for a specific system.

**System Prompt**
Initial instructions provided to an LLM that set its behavior, role, and constraints.

---

## T

**Task (A2A)**
A unit of work in the A2A protocol with a defined lifecycle (submitted, working, completed, etc.).

**Temperature**
A parameter controlling randomness in LLM outputs; lower values produce more deterministic responses.

**Token**
The basic unit of text processing for LLMs; typically subwords, words, or characters.

**Tokenization**
The process of converting text into tokens for LLM processing.

**Tool (MCP)**
A function that an LLM can invoke through MCP to perform actions or retrieve information.

**Transformer**
The neural network architecture underlying modern LLMs, based on self-attention mechanisms.

---

## V

**Vector Database**
A database optimized for storing and searching embedding vectors, used in RAG systems.

**VRAM (Video RAM)**
GPU memory used for model weights and activations during inference.

---

## W

**Worktree**
A Git feature allowing multiple working directories for the same repository.

---

## Z

**Zero-Shot Learning**
The ability of an LLM to perform tasks without explicit examples in the prompt.

---

<div align="center">

[📚 Return to Curriculum](../README.md)

</div>
