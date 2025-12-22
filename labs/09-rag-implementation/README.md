# Lab 09: RAG Implementation

<div align="center">

**Building a Retrieval-Augmented Generation System**

⭐⭐⭐ Advanced | ⏱️ 120 minutes | 📚 Module 10

</div>

---

## Learning Objectives

By the end of this lab, you will:

- [ ] Understand the RAG architecture and workflow
- [ ] Create document embeddings using sentence transformers
- [ ] Set up a ChromaDB vector database
- [ ] Implement semantic search and retrieval
- [ ] Build a complete RAG pipeline with LangChain
- [ ] Evaluate retrieval quality and optimize parameters

---

## Prerequisites

- Completed Labs 00-07
- Python 3.11+ with required packages
- At least one LLM API key (OpenAI or Anthropic)
- 4GB+ RAM available

---

## Overview

Retrieval-Augmented Generation (RAG) enhances LLM responses by retrieving relevant context from a knowledge base before generation. This is essential for:

- Grounding responses in specific documents
- Reducing hallucinations
- Providing up-to-date information
- Working with private/proprietary data

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           RAG PIPELINE                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   INDEXING PHASE (Offline)                                               │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────────────┐      │
│   │Documents│───▶│ Chunker │───▶│Embedding│───▶│  Vector Store   │      │
│   │         │    │         │    │  Model  │    │   (ChromaDB)    │      │
│   └─────────┘    └─────────┘    └─────────┘    └─────────────────┘      │
│                                                         │                │
│                                                         ▼                │
│   QUERY PHASE (Online)                         ┌─────────────────┐      │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐   │   Indexed       │      │
│   │  User   │───▶│ Query   │───▶│Embedding│──▶│   Embeddings    │      │
│   │  Query  │    │Processor│    │  Model  │   └────────┬────────┘      │
│   └─────────┘    └─────────┘    └─────────┘            │                │
│                                                         │                │
│                                      Similarity Search  │                │
│                                                         ▼                │
│   ┌─────────┐    ┌─────────┐    ┌─────────────────────────────┐        │
│   │Response │◀───│   LLM   │◀───│    Retrieved Chunks +       │        │
│   │         │    │         │    │    Original Query           │        │
│   └─────────┘    └─────────┘    └─────────────────────────────┘        │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## Part 1: Project Setup (15 minutes)

### Step 1.1: Create Project Directory

```bash
mkdir -p ~/fwg-rag-lab/{data,src,tests}
cd ~/fwg-rag-lab
```

### Step 1.2: Install Dependencies

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Create requirements.txt
cat > requirements.txt << 'EOF'
# Vector database
chromadb>=0.4.22

# Embeddings
sentence-transformers>=2.2.2

# LLM frameworks
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.1
langchain-community>=0.0.20

# Document processing
pypdf>=3.17.0
python-docx>=1.1.0
unstructured>=0.12.0

# Utilities
python-dotenv>=1.0.0
rich>=13.7.0
tiktoken>=0.5.2

# Development
pytest>=7.4.0
EOF

pip install -r requirements.txt
```

### Step 1.3: Prepare Sample Documents

Create `data/federal_policies.txt`:

```text
# Federal AI Governance Framework

## Executive Summary
This framework establishes comprehensive guidelines for the responsible
development, deployment, and use of artificial intelligence systems
within federal agencies. It aligns with Executive Order 14110 on Safe,
Secure, and Trustworthy AI.

## Scope
This framework applies to all federal agencies and their contractors
developing or deploying AI systems that:
- Make decisions affecting public rights or safety
- Process sensitive government data
- Interact directly with citizens
- Support critical infrastructure

## Key Principles

### 1. Transparency
AI systems must be explainable. Agencies must document:
- Training data sources and quality controls
- Model architecture and decision logic
- Performance metrics and limitations
- Known biases and mitigation measures

### 2. Accountability
Clear lines of responsibility must be established:
- Designated AI accountability officers
- Regular audits and compliance reviews
- Incident reporting procedures
- Remediation processes

### 3. Fairness and Civil Rights
AI systems must not discriminate:
- Bias testing before deployment
- Disparate impact analysis
- Regular monitoring for emerging biases
- Feedback mechanisms for affected parties

### 4. Security
AI systems must be protected:
- Adversarial attack resistance
- Data poisoning prevention
- Model extraction protection
- Secure deployment practices

### 5. Privacy
Personal information must be protected:
- Minimization of data collection
- Purpose limitation
- Individual rights to access and correction
- Secure data handling and retention

## Implementation Requirements

### Risk Assessment
All AI systems must undergo risk assessment:
- HIGH RISK: Requires senior leadership approval
- MEDIUM RISK: Requires department review
- LOW RISK: Standard development processes

### Documentation
Required documentation includes:
- Algorithm impact assessment
- Data quality report
- Testing and validation results
- Deployment authorization

### Monitoring
Ongoing monitoring requirements:
- Performance dashboards
- Anomaly detection
- User feedback collection
- Quarterly reviews

## Compliance Timeline
- Phase 1 (6 months): High-risk AI inventory
- Phase 2 (12 months): Risk assessments complete
- Phase 3 (18 months): Full compliance required
```

Create `data/security_guidelines.txt`:

```text
# AI Security Guidelines for Federal Systems

## Classification
UNCLASSIFIED // FOR OFFICIAL USE ONLY

## Purpose
These guidelines establish security requirements for AI systems
operating in federal environments.

## Data Security

### Training Data Classification
Training data must be classified according to:
- PUBLIC: Open source, publicly available data
- INTERNAL: Proprietary organizational data
- CONFIDENTIAL: Sensitive business information
- RESTRICTED: Regulated data (PII, PHI, CUI)

### Data Handling Requirements

For PUBLIC data:
- Standard security controls apply
- Can be processed by commercial AI services

For INTERNAL data:
- Must remain within organizational boundaries
- Commercial AI with enterprise agreements permitted

For CONFIDENTIAL data:
- On-premises or FedRAMP High processing only
- Encryption at rest and in transit required

For RESTRICTED data:
- Prohibited from external AI processing
- Air-gapped systems may be required
- Audit logging mandatory

## Model Security

### Supply Chain Security
- Verify model provenance
- Scan for backdoors and trojans
- Use signed model artifacts
- Maintain model inventory

### Adversarial Robustness
- Test for adversarial inputs
- Implement input validation
- Monitor for attack patterns
- Deploy defense mechanisms

### Access Control
- Role-based access to models
- API key rotation
- Rate limiting
- Audit logging

## Deployment Security

### Infrastructure Requirements
- Isolated network segments
- Container security scanning
- Runtime monitoring
- Incident response procedures

### API Security
- Authentication required
- TLS 1.3 minimum
- Input sanitization
- Output filtering

## Incident Response

### Detection
Monitor for:
- Unusual query patterns
- Performance degradation
- Data exfiltration attempts
- Model behavior changes

### Response Procedures
1. Isolate affected systems
2. Preserve evidence
3. Assess impact
4. Notify stakeholders
5. Remediate and recover
6. Post-incident review

## Compliance Requirements
- Annual security assessments
- Penetration testing for high-risk systems
- Continuous monitoring
- Regular training for personnel
```

---

## Part 2: Document Processing (20 minutes)

### Step 2.1: Create the Document Loader

Create `src/loader.py`:

```python
"""
Document loading and chunking for RAG pipeline.
"""

from pathlib import Path
from typing import List
from dataclasses import dataclass

@dataclass
class Document:
    """Represents a document chunk with metadata."""
    content: str
    metadata: dict
    chunk_id: str

class DocumentLoader:
    """Load and process documents for RAG."""

    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def load_text_file(self, file_path: Path) -> List[Document]:
        """Load a text file and split into chunks."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._chunk_document(
            content=content,
            source=str(file_path),
            file_type="text"
        )

    def load_directory(self, dir_path: Path, pattern: str = "*.txt") -> List[Document]:
        """Load all matching files from a directory."""
        documents = []
        for file_path in Path(dir_path).glob(pattern):
            documents.extend(self.load_text_file(file_path))
        return documents

    def _chunk_document(
        self,
        content: str,
        source: str,
        file_type: str
    ) -> List[Document]:
        """Split document into overlapping chunks."""
        chunks = []

        # Split by paragraphs first, then by size
        paragraphs = content.split('\n\n')
        current_chunk = ""
        chunk_index = 0

        for para in paragraphs:
            # If adding this paragraph exceeds chunk size, save current and start new
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append(Document(
                    content=current_chunk.strip(),
                    metadata={
                        "source": source,
                        "file_type": file_type,
                        "chunk_index": chunk_index
                    },
                    chunk_id=f"{Path(source).stem}_chunk_{chunk_index}"
                ))
                # Keep overlap from end of current chunk
                overlap_text = current_chunk[-self.chunk_overlap:] if len(current_chunk) > self.chunk_overlap else ""
                current_chunk = overlap_text + para + "\n\n"
                chunk_index += 1
            else:
                current_chunk += para + "\n\n"

        # Don't forget the last chunk
        if current_chunk.strip():
            chunks.append(Document(
                content=current_chunk.strip(),
                metadata={
                    "source": source,
                    "file_type": file_type,
                    "chunk_index": chunk_index
                },
                chunk_id=f"{Path(source).stem}_chunk_{chunk_index}"
            ))

        return chunks


def main():
    """Test the document loader."""
    from rich import print
    from rich.table import Table

    loader = DocumentLoader(chunk_size=500, chunk_overlap=50)

    # Load documents
    data_dir = Path(__file__).parent.parent / "data"
    documents = loader.load_directory(data_dir, "*.txt")

    # Display results
    table = Table(title="Loaded Documents")
    table.add_column("Chunk ID", style="cyan")
    table.add_column("Source", style="green")
    table.add_column("Length", style="yellow")
    table.add_column("Preview", style="white")

    for doc in documents:
        table.add_row(
            doc.chunk_id,
            Path(doc.metadata["source"]).name,
            str(len(doc.content)),
            doc.content[:50] + "..."
        )

    print(table)
    print(f"\n[green]Total chunks: {len(documents)}[/green]")


if __name__ == "__main__":
    main()
```

---

## Part 3: Vector Store Setup (25 minutes)

### Step 3.1: Create the Embeddings Manager

Create `src/embeddings.py`:

```python
"""
Embedding generation and vector store management.
"""

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from typing import List, Optional
from pathlib import Path

from src.loader import Document

class EmbeddingManager:
    """Manage embeddings and vector store."""

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        persist_directory: str = "./chroma_db"
    ):
        # Initialize embedding model
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)

        # Initialize ChromaDB
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(anonymized_telemetry=False)
        )

        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="fwg_documents",
            metadata={"hnsw:space": "cosine"}
        )

    def embed_text(self, text: str) -> List[float]:
        """Generate embedding for a single text."""
        return self.model.encode(text).tolist()

    def embed_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if not documents:
            print("No documents to embed")
            return

        # Prepare data for ChromaDB
        ids = [doc.chunk_id for doc in documents]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        # Generate embeddings
        print(f"Generating embeddings for {len(documents)} documents...")
        embeddings = self.model.encode(texts).tolist()

        # Add to collection
        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )
        print(f"Added {len(documents)} documents to vector store")

    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[dict] = None
    ) -> dict:
        """Search for similar documents."""
        query_embedding = self.embed_text(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        return results

    def get_stats(self) -> dict:
        """Get collection statistics."""
        return {
            "collection_name": self.collection.name,
            "document_count": self.collection.count(),
            "persist_directory": str(self.persist_directory)
        }

    def clear(self) -> None:
        """Clear all documents from the collection."""
        # Delete and recreate collection
        self.client.delete_collection("fwg_documents")
        self.collection = self.client.get_or_create_collection(
            name="fwg_documents",
            metadata={"hnsw:space": "cosine"}
        )
        print("Collection cleared")


def main():
    """Test the embedding manager."""
    from rich import print
    from src.loader import DocumentLoader

    # Load documents
    loader = DocumentLoader()
    data_dir = Path(__file__).parent.parent / "data"
    documents = loader.load_directory(data_dir)

    # Initialize embedding manager
    manager = EmbeddingManager()

    # Clear previous data
    manager.clear()

    # Add documents
    manager.embed_documents(documents)

    # Print stats
    print(f"\n[green]Vector Store Stats:[/green]")
    print(manager.get_stats())

    # Test search
    print("\n[cyan]Test Search: 'AI security requirements'[/cyan]")
    results = manager.search("AI security requirements", n_results=3)

    for i, (doc, distance) in enumerate(zip(
        results["documents"][0],
        results["distances"][0]
    )):
        print(f"\n[yellow]Result {i+1} (distance: {distance:.4f}):[/yellow]")
        print(doc[:200] + "...")


if __name__ == "__main__":
    main()
```

---

## Part 4: RAG Pipeline (25 minutes)

### Step 4.1: Create the RAG Engine

Create `src/rag.py`:

```python
"""
Complete RAG pipeline implementation.
"""

import os
from typing import List, Optional
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic

from src.loader import DocumentLoader
from src.embeddings import EmbeddingManager

load_dotenv()

@dataclass
class RAGResponse:
    """Response from the RAG pipeline."""
    answer: str
    sources: List[dict]
    query: str
    model: str

class RAGPipeline:
    """Complete RAG pipeline with retrieval and generation."""

    def __init__(
        self,
        embedding_model: str = "all-MiniLM-L6-v2",
        llm_provider: str = "openai",
        llm_model: str = "gpt-4o-mini",
        persist_directory: str = "./chroma_db"
    ):
        self.embedding_manager = EmbeddingManager(
            model_name=embedding_model,
            persist_directory=persist_directory
        )
        self.llm_provider = llm_provider
        self.llm_model = llm_model

        # Initialize LLM client
        if llm_provider == "openai":
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif llm_provider == "anthropic":
            self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError(f"Unsupported LLM provider: {llm_provider}")

    def index_documents(self, documents_path: Path) -> int:
        """Index documents from a directory."""
        loader = DocumentLoader(chunk_size=500, chunk_overlap=50)
        documents = loader.load_directory(documents_path)
        self.embedding_manager.embed_documents(documents)
        return len(documents)

    def retrieve(
        self,
        query: str,
        n_results: int = 5
    ) -> List[dict]:
        """Retrieve relevant documents for a query."""
        results = self.embedding_manager.search(query, n_results=n_results)

        retrieved = []
        for i in range(len(results["documents"][0])):
            retrieved.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })

        return retrieved

    def generate(
        self,
        query: str,
        context: List[dict],
        system_prompt: Optional[str] = None
    ) -> str:
        """Generate a response using retrieved context."""

        # Build context string
        context_str = "\n\n---\n\n".join([
            f"[Source: {doc['metadata'].get('source', 'Unknown')}]\n{doc['content']}"
            for doc in context
        ])

        # Default system prompt
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant for Federal Working Group employees.
You answer questions based on the provided context documents.
Always cite your sources when providing information.
If the context doesn't contain relevant information, say so clearly.
Be concise but thorough in your responses."""

        # Build user prompt
        user_prompt = f"""Context Documents:
{context_str}

---

Question: {query}

Please answer the question based on the context documents above. Cite specific sources when possible."""

        # Generate response based on provider
        if self.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content

        elif self.llm_provider == "anthropic":
            response = self.client.messages.create(
                model=self.llm_model,
                max_tokens=1000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.content[0].text

    def query(
        self,
        query: str,
        n_results: int = 5,
        system_prompt: Optional[str] = None
    ) -> RAGResponse:
        """Complete RAG query: retrieve and generate."""

        # Retrieve relevant documents
        context = self.retrieve(query, n_results=n_results)

        # Generate response
        answer = self.generate(query, context, system_prompt)

        return RAGResponse(
            answer=answer,
            sources=[
                {
                    "source": doc["metadata"].get("source", "Unknown"),
                    "chunk_index": doc["metadata"].get("chunk_index", 0),
                    "relevance": 1 - doc["distance"]  # Convert distance to similarity
                }
                for doc in context
            ],
            query=query,
            model=self.llm_model
        )


def main():
    """Interactive RAG demo."""
    from rich import print
    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    print("\n[bold cyan]FWG RAG Pipeline Demo[/bold cyan]")
    print("=" * 50)

    # Initialize pipeline
    print("\n[yellow]Initializing RAG pipeline...[/yellow]")
    rag = RAGPipeline(
        llm_provider="openai",
        llm_model="gpt-4o-mini"
    )

    # Index documents
    data_dir = Path(__file__).parent.parent / "data"
    if data_dir.exists():
        print(f"\n[yellow]Indexing documents from {data_dir}...[/yellow]")
        rag.embedding_manager.clear()
        count = rag.index_documents(data_dir)
        print(f"[green]Indexed {count} document chunks[/green]")

    # Interactive query loop
    print("\n[bold]Enter your questions (type 'exit' to quit):[/bold]\n")

    while True:
        query = input("🔍 Query: ").strip()

        if query.lower() == 'exit':
            break

        if not query:
            continue

        print("\n[yellow]Searching and generating response...[/yellow]\n")

        try:
            response = rag.query(query, n_results=3)

            # Display answer
            console.print(Panel(
                response.answer,
                title="[bold green]Answer[/bold green]",
                border_style="green"
            ))

            # Display sources
            print("\n[cyan]Sources:[/cyan]")
            for src in response.sources:
                print(f"  • {Path(src['source']).name} (chunk {src['chunk_index']}, relevance: {src['relevance']:.2f})")

        except Exception as e:
            print(f"[red]Error: {e}[/red]")

        print("\n" + "-" * 50 + "\n")


if __name__ == "__main__":
    main()
```

---

## Part 5: Evaluation (15 minutes)

### Step 5.1: Create Evaluation Script

Create `src/evaluate.py`:

```python
"""
RAG evaluation and quality metrics.
"""

from dataclasses import dataclass
from typing import List
import json

@dataclass
class EvaluationResult:
    """Result of RAG evaluation."""
    query: str
    expected_sources: List[str]
    retrieved_sources: List[str]
    precision: float
    recall: float
    f1_score: float
    answer_contains_expected: bool

class RAGEvaluator:
    """Evaluate RAG pipeline quality."""

    def __init__(self, rag_pipeline):
        self.rag = rag_pipeline

    def evaluate_retrieval(
        self,
        query: str,
        expected_keywords: List[str]
    ) -> dict:
        """Evaluate retrieval quality."""
        results = self.rag.retrieve(query, n_results=5)

        # Check if expected keywords appear in retrieved documents
        retrieved_text = " ".join([r["content"] for r in results])

        keyword_hits = {}
        for keyword in expected_keywords:
            keyword_hits[keyword] = keyword.lower() in retrieved_text.lower()

        hit_rate = sum(keyword_hits.values()) / len(expected_keywords)

        return {
            "query": query,
            "documents_retrieved": len(results),
            "keyword_coverage": hit_rate,
            "keyword_hits": keyword_hits,
            "avg_relevance": sum(1 - r["distance"] for r in results) / len(results)
        }

    def evaluate_answer(
        self,
        query: str,
        expected_content: List[str]
    ) -> dict:
        """Evaluate answer quality."""
        response = self.rag.query(query)

        content_hits = {}
        for content in expected_content:
            content_hits[content] = content.lower() in response.answer.lower()

        accuracy = sum(content_hits.values()) / len(expected_content)

        return {
            "query": query,
            "answer_length": len(response.answer),
            "sources_cited": len(response.sources),
            "content_accuracy": accuracy,
            "content_hits": content_hits
        }

    def run_test_suite(self, test_cases: List[dict]) -> dict:
        """Run a complete test suite."""
        results = []

        for test in test_cases:
            retrieval_eval = self.evaluate_retrieval(
                test["query"],
                test.get("expected_keywords", [])
            )

            answer_eval = self.evaluate_answer(
                test["query"],
                test.get("expected_content", [])
            )

            results.append({
                "test_name": test.get("name", "Unnamed"),
                "query": test["query"],
                "retrieval": retrieval_eval,
                "answer": answer_eval
            })

        # Calculate aggregate metrics
        avg_keyword_coverage = sum(
            r["retrieval"]["keyword_coverage"] for r in results
        ) / len(results)

        avg_content_accuracy = sum(
            r["answer"]["content_accuracy"] for r in results
        ) / len(results)

        return {
            "total_tests": len(results),
            "avg_keyword_coverage": avg_keyword_coverage,
            "avg_content_accuracy": avg_content_accuracy,
            "detailed_results": results
        }


# Test cases
TEST_CASES = [
    {
        "name": "AI Governance Principles",
        "query": "What are the key principles of AI governance?",
        "expected_keywords": ["transparency", "accountability", "fairness", "security", "privacy"],
        "expected_content": ["explainable", "audit", "bias"]
    },
    {
        "name": "Data Classification",
        "query": "How should training data be classified?",
        "expected_keywords": ["public", "internal", "confidential", "restricted"],
        "expected_content": ["classification", "PII", "CUI"]
    },
    {
        "name": "Risk Assessment",
        "query": "What are the risk assessment requirements for AI systems?",
        "expected_keywords": ["high risk", "medium risk", "low risk"],
        "expected_content": ["assessment", "approval", "review"]
    }
]


def main():
    """Run evaluation."""
    from rich import print
    from rich.table import Table
    from pathlib import Path
    from src.rag import RAGPipeline

    print("\n[bold cyan]RAG Evaluation Suite[/bold cyan]")
    print("=" * 50)

    # Initialize pipeline
    rag = RAGPipeline(llm_provider="openai", llm_model="gpt-4o-mini")

    # Ensure documents are indexed
    data_dir = Path(__file__).parent.parent / "data"
    if rag.embedding_manager.collection.count() == 0:
        rag.index_documents(data_dir)

    # Run evaluation
    evaluator = RAGEvaluator(rag)
    results = evaluator.run_test_suite(TEST_CASES)

    # Display results
    table = Table(title="Evaluation Results")
    table.add_column("Test Name", style="cyan")
    table.add_column("Keyword Coverage", style="yellow")
    table.add_column("Content Accuracy", style="green")

    for test in results["detailed_results"]:
        table.add_row(
            test["test_name"],
            f"{test['retrieval']['keyword_coverage']:.2%}",
            f"{test['answer']['content_accuracy']:.2%}"
        )

    print(table)

    print(f"\n[bold]Aggregate Metrics:[/bold]")
    print(f"  Average Keyword Coverage: {results['avg_keyword_coverage']:.2%}")
    print(f"  Average Content Accuracy: {results['avg_content_accuracy']:.2%}")


if __name__ == "__main__":
    main()
```

---

## Exercises

### Exercise 1: Add PDF Support

Extend the `DocumentLoader` to handle PDF files using `pypdf`.

### Exercise 2: Implement Hybrid Search

Combine vector search with keyword search for better retrieval.

### Exercise 3: Add Query Expansion

Implement query expansion using an LLM to improve retrieval.

---

## Challenges

### Challenge A: Multi-Query RAG
Implement RAG-Fusion by generating multiple query variations.

### Challenge B: Reranking
Add a reranking step using a cross-encoder model.

### Challenge C: Streaming Responses
Implement streaming for the generation phase.

---

## Knowledge Check

1. **Why is chunking important in RAG systems?**

2. **What are the trade-offs between chunk size and overlap?**

3. **How does cosine similarity work for document retrieval?**

4. **What metrics can you use to evaluate RAG quality?**

---

## Self-Assessment Rubric

| Criteria | Meets Expectations |
|----------|-------------------|
| Documents load and chunk correctly | ✅ |
| Embeddings are generated | ✅ |
| Vector search returns results | ✅ |
| Complete RAG pipeline works | ✅ |
| Evaluation suite passes | ✅ |
| Understands optimization options | ✅ |

---

## Next Steps

**Next Lab:** [Lab 10: LoRA Fine-Tuning →](../10-lora-fine-tuning/README.md)

---

<div align="center">

**Lab 09 Complete!** 🎉

</div>
