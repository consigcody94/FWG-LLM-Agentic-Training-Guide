# Example Projects

<div align="center">

**Complete, Working AI Applications for Learning and Reference**

</div>

---

## Overview

This directory contains fully functional example applications demonstrating key concepts from the training modules. Each example is self-contained and can be run independently.

---

## Example Index

| # | Project | Description | Modules | Difficulty |
|:-:|---------|-------------|---------|:----------:|
| 01 | [Simple Chatbot](./01-simple-chatbot/) | Basic conversational AI with multiple providers | 01-04 | ⭐ |
| 02 | [RAG System](./02-rag-system/) | Document Q&A with vector search | 10, 14 | ⭐⭐⭐ |
| 03 | [MCP Server](./03-mcp-server/) | Custom MCP server with tools and resources | 06 | ⭐⭐⭐ |
| 04 | [Multi-Agent](./04-multi-agent/) | Collaborative agents solving complex tasks | 08, 12 | ⭐⭐⭐⭐ |
| 05 | [Document Assistant](./05-document-assistant/) | Full-featured document analysis system | 10, 13, 23 | ⭐⭐⭐⭐ |

---

## Quick Start

### Prerequisites

```bash
# Ensure you're in the repository root
cd FWG-LLM-Agentic-Training-Guide

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys
```

### Running an Example

```bash
# Navigate to example directory
cd examples/01-simple-chatbot

# Read the README for specific instructions
cat README.md

# Run the example
python main.py
```

---

## Project Structure

Each example follows a consistent structure:

```
example-name/
├── README.md           # Project documentation
├── requirements.txt    # Project-specific dependencies (if any)
├── main.py            # Entry point
├── src/               # Source code
│   └── ...
├── tests/             # Test files
│   └── ...
├── config/            # Configuration files
│   └── ...
└── data/              # Sample data (if needed)
    └── ...
```

---

## Best Practices Demonstrated

Each example demonstrates key best practices:

### Security
- Environment variable usage for secrets
- Input validation
- Error handling without information leakage

### Code Quality
- Type hints throughout
- Comprehensive docstrings
- Modular architecture

### Operations
- Logging configuration
- Health checks
- Configuration management

---

## Customization

These examples are designed to be extended:

1. **Change the LLM provider**: Most examples support OpenAI, Anthropic, and Ollama
2. **Modify prompts**: System prompts are clearly marked for customization
3. **Add features**: Examples include extension points with comments

---

## Federal Considerations

All examples include:
- Data handling best practices
- Audit logging patterns
- Security-conscious design
- Comments noting compliance considerations

---

<div align="center">

**Learn by doing. Modify freely. Build confidently.**

</div>
