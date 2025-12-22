# Example 01: Simple Chatbot

<div align="center">

**A Multi-Provider Conversational AI Application**

⭐ Beginner | Modules: 01-04

</div>

---

## Overview

This example demonstrates how to build a simple but production-ready chatbot that can use multiple LLM providers (OpenAI, Anthropic, Ollama).

## Features

- Multi-provider support (easily switch between providers)
- Conversation memory
- Streaming responses
- Proper error handling
- Configuration management
- Logging

---

## Quick Start

```bash
# From this directory
python main.py

# Or specify a provider
python main.py --provider ollama
python main.py --provider anthropic
```

---

## Files

```
01-simple-chatbot/
├── README.md
├── main.py              # Entry point
└── src/
    ├── __init__.py
    ├── providers.py     # LLM provider implementations
    ├── chat.py          # Chat logic
    └── config.py        # Configuration
```
