# Example 02: RAG System

<div align="center">

**Retrieval-Augmented Generation for Document Q&A**

⭐⭐⭐ Intermediate | Modules: 10, 14

</div>

---

## Overview

This example demonstrates a complete RAG (Retrieval-Augmented Generation) system that can:
- Index documents into a vector database
- Perform semantic search
- Generate answers grounded in document content
- Track sources and citations

## Features

- ChromaDB vector storage
- Multiple embedding model support
- Configurable chunking strategies
- Source attribution
- Caching for repeated queries

---

## Quick Start

```bash
# Index documents
python main.py index ./data

# Query the system
python main.py query "What are the AI governance requirements?"

# Interactive mode
python main.py interactive
```
