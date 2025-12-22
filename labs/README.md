# Hands-On Labs

<div align="center">

**Practical Exercises for Mastering LLM Agent Development**

*From Hello World to Production-Ready AI Systems*

</div>

---

## Overview

This directory contains 21 comprehensive hands-on labs designed to reinforce concepts from each training module. Labs are organized by difficulty and build upon each other progressively.

---

## Lab Index

| # | Lab Name | Module | Difficulty | Duration | Key Skills |
|:-:|:---------|:------:|:----------:|:--------:|:-----------|
| 00 | [Hello Agent](./00-hello-agent/README.md) | 01 | ⭐ | 15 min | Environment setup, first API call |
| 01 | [Web GUI Comparison](./01-web-gui-comparison/README.md) | 02 | ⭐ | 30 min | ChatGPT, Claude, Gemini evaluation |
| 02 | [Ollama Local Setup](./02-ollama-setup/README.md) | 03 | ⭐⭐ | 45 min | Local LLM installation, model management |
| 03 | [API Authentication](./03-api-authentication/README.md) | 04 | ⭐⭐ | 30 min | Secure API key handling, multi-provider setup |
| 04 | [Prompt Engineering Dojo](./04-prompt-engineering/README.md) | 05 | ⭐⭐ | 60 min | Prompt patterns, optimization techniques |
| 05 | [MCP Server Build](./05-mcp-server/README.md) | 06 | ⭐⭐⭐ | 90 min | MCP protocol implementation |
| 06 | [A2A Agent Card](./06-a2a-agent-card/README.md) | 07 | ⭐⭐⭐ | 60 min | Agent discovery, capability exposure |
| 07 | [LangChain Pipeline](./07-langchain-pipeline/README.md) | 08 | ⭐⭐⭐ | 90 min | Chain construction, agent building |
| 08 | [Claude Code Workflow](./08-claude-code-workflow/README.md) | 09 | ⭐⭐ | 45 min | CLI coding assistant mastery |
| 09 | [RAG Implementation](./09-rag-implementation/README.md) | 10 | ⭐⭐⭐ | 120 min | Vector DB, embeddings, retrieval |
| 10 | [LoRA Fine-Tuning](./10-lora-fine-tuning/README.md) | 11 | ⭐⭐⭐⭐ | 180 min | Model customization, training |
| 11 | [Multi-Agent Debate](./11-multi-agent-debate/README.md) | 12 | ⭐⭐⭐⭐ | 120 min | Agent orchestration, consensus |
| 12 | [Custom Tool Creation](./12-custom-tool-creation/README.md) | 13 | ⭐⭐⭐ | 60 min | Function calling, tool chains |
| 13 | [Memory System Design](./13-memory-system/README.md) | 14 | ⭐⭐⭐ | 90 min | Context management, persistence |
| 14 | [Red Team Exercise](./14-red-team-exercise/README.md) | 15 | ⭐⭐⭐⭐ | 120 min | Security testing, jailbreak prevention |
| 15 | [Evaluation Framework](./15-evaluation-framework/README.md) | 16 | ⭐⭐⭐ | 90 min | Benchmarking, automated testing |
| 16 | [K8s Deployment](./16-k8s-deployment/README.md) | 17 | ⭐⭐⭐⭐ | 150 min | Container orchestration, scaling |
| 17 | [Enterprise Integration](./17-enterprise-integration/README.md) | 18 | ⭐⭐⭐⭐ | 180 min | Multi-tenancy, audit logging |
| 18 | [Security Audit](./18-security-audit/README.md) | 19 | ⭐⭐⭐⭐⭐ | 240 min | FedRAMP compliance, controls |
| 19 | [Cost Analysis](./19-cost-analysis/README.md) | 20 | ⭐⭐⭐ | 60 min | Token optimization, budgeting |
| 20 | [Hybrid Architecture](./20-hybrid-architecture/README.md) | 21 | ⭐⭐⭐⭐ | 150 min | Cloud/local, failover design |

---

## Difficulty Levels

| Level | Description | Prerequisites |
|:-----:|:------------|:--------------|
| ⭐ | Beginner | Basic programming knowledge |
| ⭐⭐ | Intermediate | Completed Tier 1 foundations |
| ⭐⭐⭐ | Advanced | Comfortable with APIs and frameworks |
| ⭐⭐⭐⭐ | Expert | Strong development experience |
| ⭐⭐⭐⭐⭐ | Master | Security/compliance background |

---

## Prerequisites

Before starting labs, ensure you have completed the [Quick Start](../README.md#-quick-start) setup:

```bash
# Verify environment
python scripts/verify_setup.py
```

Required tools:
- [ ] Python 3.11+
- [ ] Node.js 18+
- [ ] Git
- [ ] Ollama
- [ ] Claude Code CLI
- [ ] API keys configured (.env file)

---

## Lab Structure

Each lab follows a consistent structure:

```
lab-XX-name/
├── README.md           # Lab overview and instructions
├── starter/            # Starting code templates
│   └── ...
├── solution/           # Complete solutions (don't peek!)
│   └── ...
├── tests/              # Validation tests
│   └── ...
└── resources/          # Additional resources
    └── ...
```

---

## Learning Paths

### Quick Start Path (3 hours)
Labs: 00 → 02 → 04 → 08

### Developer Path (20 hours)
Labs: 00 → 02 → 03 → 04 → 05 → 07 → 09 → 12 → 13

### Security Path (15 hours)
Labs: 00 → 04 → 14 → 15 → 18

### Architect Path (25 hours)
Labs: 00 → 02 → 05 → 06 → 07 → 09 → 11 → 16 → 17 → 20

---

## Assessment

Each lab includes:

1. **Learning Objectives**: What you'll learn
2. **Exercises**: Step-by-step tasks
3. **Challenges**: Optional advanced exercises
4. **Knowledge Check**: Quiz questions
5. **Rubric**: Self-assessment criteria

---

## Getting Help

- **Documentation**: Each lab has detailed instructions
- **Solutions**: Available in `solution/` directory (try on your own first!)
- **Issues**: Open a GitHub issue with the `lab-help` label
- **Discussion**: Join lab discussion threads

---

## Contributing Labs

See [CONTRIBUTING.md](../CONTRIBUTING.md) for lab contribution guidelines.

---

<div align="center">

**Ready to start?**

[Begin with Lab 00: Hello Agent →](./00-hello-agent/README.md)

</div>
