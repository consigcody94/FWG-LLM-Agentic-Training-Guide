<div align="center">

# Module 10: Retrieval-Augmented Generation (RAG)

<img src="https://img.shields.io/badge/Duration-5_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Building knowledge-grounded AI systems with vector databases and semantic search*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand RAG architecture and components
- [ ] Implement document ingestion pipelines
- [ ] Configure and use vector databases
- [ ] Build production RAG applications
- [ ] Optimize retrieval quality and relevance

---

## 10.1 RAG Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG SYSTEM ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INDEXING PHASE                    QUERY PHASE                  │
│  ──────────────                    ───────────                  │
│                                                                  │
│  ┌──────────┐                      ┌──────────┐                 │
│  │Documents │                      │  Query   │                 │
│  │  (PDF,   │                      │          │                 │
│  │  DOCX,   │                      └────┬─────┘                 │
│  │  HTML)   │                           │                       │
│  └────┬─────┘                           ▼                       │
│       │                           ┌──────────┐                  │
│       ▼                           │  Embed   │                  │
│  ┌──────────┐                     │  Query   │                  │
│  │  Chunk   │                     └────┬─────┘                  │
│  │  Split   │                          │                        │
│  └────┬─────┘                          ▼                        │
│       │                           ┌──────────┐    ┌──────────┐ │
│       ▼                           │  Vector  │───▶│ Top-K    │ │
│  ┌──────────┐                     │  Search  │    │ Results  │ │
│  │  Embed   │                     └──────────┘    └────┬─────┘ │
│  │  Chunks  │                                          │        │
│  └────┬─────┘                                          ▼        │
│       │                                          ┌──────────┐   │
│       ▼                                          │ Rerank   │   │
│  ┌──────────┐                                    │(Optional)│   │
│  │  Vector  │                                    └────┬─────┘   │
│  │   DB     │                                         │         │
│  └──────────┘                                         ▼         │
│                                                 ┌──────────┐    │
│                                                 │   LLM    │    │
│                                                 │ Generate │    │
│                                                 └────┬─────┘    │
│                                                      │          │
│                                                      ▼          │
│                                                 ┌──────────┐    │
│                                                 │ Response │    │
│                                                 └──────────┘    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Why RAG?

| Challenge | Without RAG | With RAG |
|-----------|-------------|----------|
| **Knowledge Cutoff** | Limited to training data | Access current information |
| **Hallucination** | Makes up facts | Grounded in sources |
| **Domain Knowledge** | General knowledge only | Organization-specific |
| **Verifiability** | Cannot cite sources | Provides citations |
| **Updates** | Requires retraining | Update documents only |

---

## 10.2 Document Processing Pipeline

### Text Extraction

```python
from pathlib import Path
import fitz  # PyMuPDF
from docx import Document
import markdown
from bs4 import BeautifulSoup

class DocumentExtractor:
    """Extract text from various document formats."""

    def extract(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()

        extractors = {
            '.pdf': self._extract_pdf,
            '.docx': self._extract_docx,
            '.md': self._extract_markdown,
            '.html': self._extract_html,
            '.txt': self._extract_text
        }

        extractor = extractors.get(suffix)
        if not extractor:
            raise ValueError(f"Unsupported format: {suffix}")

        return extractor(file_path)

    def _extract_pdf(self, path: Path) -> str:
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def _extract_docx(self, path: Path) -> str:
        doc = Document(path)
        return "\n".join([para.text for para in doc.paragraphs])

    def _extract_markdown(self, path: Path) -> str:
        with open(path) as f:
            html = markdown.markdown(f.read())
        return BeautifulSoup(html, 'html.parser').get_text()

    def _extract_html(self, path: Path) -> str:
        with open(path) as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        return soup.get_text()

    def _extract_text(self, path: Path) -> str:
        return path.read_text()
```

### Chunking Strategies

```python
from typing import List
from dataclasses import dataclass
import tiktoken

@dataclass
class Chunk:
    text: str
    metadata: dict
    start_idx: int
    end_idx: int

class ChunkingStrategy:
    """Various text chunking strategies."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        model: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.tokenizer = tiktoken.get_encoding(model)

    def chunk_by_tokens(self, text: str, metadata: dict = None) -> List[Chunk]:
        """Split text by token count."""
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + self.chunk_size
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens)

            chunks.append(Chunk(
                text=chunk_text,
                metadata=metadata or {},
                start_idx=start,
                end_idx=end
            ))

            start = end - self.chunk_overlap

        return chunks

    def chunk_by_sentences(self, text: str, metadata: dict = None) -> List[Chunk]:
        """Split text preserving sentence boundaries."""
        import nltk
        sentences = nltk.sent_tokenize(text)

        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = len(self.tokenizer.encode(sentence))

            if current_tokens + sentence_tokens > self.chunk_size:
                if current_chunk:
                    chunks.append(Chunk(
                        text=" ".join(current_chunk),
                        metadata=metadata or {},
                        start_idx=0,
                        end_idx=0
                    ))
                current_chunk = [sentence]
                current_tokens = sentence_tokens
            else:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens

        if current_chunk:
            chunks.append(Chunk(
                text=" ".join(current_chunk),
                metadata=metadata or {},
                start_idx=0,
                end_idx=0
            ))

        return chunks

    def chunk_by_sections(
        self,
        text: str,
        section_markers: List[str] = None
    ) -> List[Chunk]:
        """Split by document sections (headers, etc.)."""
        import re

        markers = section_markers or [
            r'^#{1,6}\s+',  # Markdown headers
            r'^(?:SECTION|CHAPTER)\s+\d+',  # Document sections
            r'^\d+\.\s+[A-Z]',  # Numbered sections
        ]

        pattern = '|'.join(f'({m})' for m in markers)
        sections = re.split(pattern, text, flags=re.MULTILINE)

        chunks = []
        for section in sections:
            if section and section.strip():
                # Further split large sections
                if len(self.tokenizer.encode(section)) > self.chunk_size:
                    chunks.extend(self.chunk_by_sentences(section))
                else:
                    chunks.append(Chunk(
                        text=section.strip(),
                        metadata={},
                        start_idx=0,
                        end_idx=0
                    ))

        return chunks
```

---

## 10.3 Embedding Models

### Embedding Comparison

| Model | Dimensions | Speed | Quality | Use Case |
|-------|------------|-------|---------|----------|
| **OpenAI ada-002** | 1536 | Fast | Excellent | General purpose |
| **OpenAI 3-large** | 3072 | Medium | Best | High accuracy needs |
| **Cohere embed-v3** | 1024 | Fast | Excellent | Multilingual |
| **BGE-large** | 1024 | Medium | Very Good | Local/air-gapped |
| **all-MiniLM-L6** | 384 | Very Fast | Good | Low latency |

### Implementation

```python
from abc import ABC, abstractmethod
from typing import List
import numpy as np

class EmbeddingModel(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> np.ndarray:
        pass

class OpenAIEmbedding(EmbeddingModel):
    def __init__(self, model: str = "text-embedding-3-small"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = model

    def embed(self, texts: List[str]) -> np.ndarray:
        response = self.client.embeddings.create(
            input=texts,
            model=self.model
        )
        return np.array([e.embedding for e in response.data])

class LocalEmbedding(EmbeddingModel):
    """For air-gapped federal deployments."""

    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True)

class CohereEmbedding(EmbeddingModel):
    def __init__(self, model: str = "embed-english-v3.0"):
        import cohere
        self.client = cohere.Client()
        self.model = model

    def embed(self, texts: List[str]) -> np.ndarray:
        response = self.client.embed(
            texts=texts,
            model=self.model,
            input_type="search_document"
        )
        return np.array(response.embeddings)
```

---

## 10.4 Vector Databases

### Database Comparison

```
┌─────────────────────────────────────────────────────────────────┐
│                   VECTOR DATABASE LANDSCAPE                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  MANAGED SERVICES              SELF-HOSTED                      │
│  ────────────────              ───────────                      │
│                                                                  │
│  ┌───────────┐                 ┌───────────┐                    │
│  │  Pinecone │                 │  Chroma   │  ← Simple, local   │
│  └───────────┘                 └───────────┘                    │
│                                                                  │
│  ┌───────────┐                 ┌───────────┐                    │
│  │  Weaviate │                 │  Milvus   │  ← Enterprise      │
│  │   Cloud   │                 │           │                    │
│  └───────────┘                 └───────────┘                    │
│                                                                  │
│  ┌───────────┐                 ┌───────────┐                    │
│  │   Qdrant  │                 │   pgvector│  ← PostgreSQL      │
│  │   Cloud   │                 │           │    extension       │
│  └───────────┘                 └───────────┘                    │
│                                                                  │
│  ┌───────────┐                 ┌───────────┐                    │
│  │  MongoDB  │                 │   FAISS   │  ← In-memory       │
│  │   Atlas   │                 │           │                    │
│  └───────────┘                 └───────────┘                    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### ChromaDB Implementation

```python
import chromadb
from chromadb.config import Settings

# Initialize client
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",
    persist_directory="./chroma_db",
    anonymized_telemetry=False  # Important for federal
))

# Create collection
collection = client.create_collection(
    name="federal_documents",
    metadata={"hnsw:space": "cosine"}
)

# Add documents
collection.add(
    documents=["Document text 1", "Document text 2"],
    metadatas=[
        {"source": "policy.pdf", "classification": "CUI"},
        {"source": "memo.docx", "classification": "UNCLASSIFIED"}
    ],
    ids=["doc1", "doc2"]
)

# Query
results = collection.query(
    query_texts=["security requirements"],
    n_results=5,
    where={"classification": "UNCLASSIFIED"}  # Filter by metadata
)
```

### pgvector with PostgreSQL

```python
import psycopg2
from pgvector.psycopg2 import register_vector

# Connect
conn = psycopg2.connect(
    host="localhost",
    database="federal_rag",
    user="rag_user"
)
register_vector(conn)

# Create table with vector column
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id SERIAL PRIMARY KEY,
        content TEXT,
        embedding vector(1536),
        source VARCHAR(255),
        classification VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# Create index for fast similarity search
cur.execute("""
    CREATE INDEX ON documents
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100)
""")

# Insert document
cur.execute("""
    INSERT INTO documents (content, embedding, source, classification)
    VALUES (%s, %s, %s, %s)
""", (content, embedding.tolist(), source, classification))

# Query similar documents
cur.execute("""
    SELECT content, source, 1 - (embedding <=> %s) as similarity
    FROM documents
    WHERE classification = %s
    ORDER BY embedding <=> %s
    LIMIT 5
""", (query_embedding.tolist(), 'UNCLASSIFIED', query_embedding.tolist()))
```

---

## 10.5 Complete RAG Pipeline

```python
from typing import List, Optional
from dataclasses import dataclass
import asyncio

@dataclass
class RAGResponse:
    answer: str
    sources: List[dict]
    confidence: float

class FederalRAGPipeline:
    """Production RAG pipeline for federal applications."""

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        llm: LLMClient,
        reranker: Optional[Reranker] = None
    ):
        self.embedding = embedding_model
        self.vector_store = vector_store
        self.llm = llm
        self.reranker = reranker

    async def ingest_document(
        self,
        content: str,
        metadata: dict,
        chunking_strategy: str = "sentences"
    ):
        """Ingest and index a document."""
        # Validate classification
        classification = metadata.get("classification", "UNCLASSIFIED")
        if classification not in ["UNCLASSIFIED", "CUI"]:
            raise ValueError(f"Cannot process {classification} documents")

        # Chunk document
        chunker = ChunkingStrategy(chunk_size=512, chunk_overlap=50)
        if chunking_strategy == "sentences":
            chunks = chunker.chunk_by_sentences(content, metadata)
        else:
            chunks = chunker.chunk_by_tokens(content, metadata)

        # Generate embeddings
        texts = [c.text for c in chunks]
        embeddings = self.embedding.embed(texts)

        # Store in vector database
        for chunk, embedding in zip(chunks, embeddings):
            await self.vector_store.insert(
                text=chunk.text,
                embedding=embedding,
                metadata=chunk.metadata
            )

    async def query(
        self,
        question: str,
        user_clearance: str = "UNCLASSIFIED",
        top_k: int = 5,
        rerank: bool = True
    ) -> RAGResponse:
        """Query the RAG system."""

        # Embed query
        query_embedding = self.embedding.embed([question])[0]

        # Retrieve relevant chunks
        results = await self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k * 2 if rerank else top_k,
            filter={"classification": {"$in": self._allowed_classifications(user_clearance)}}
        )

        # Rerank if enabled
        if rerank and self.reranker:
            results = self.reranker.rerank(question, results)[:top_k]

        # Build context
        context = self._build_context(results)

        # Generate response
        prompt = self._build_prompt(question, context)
        response = await self.llm.generate(prompt)

        # Extract citations
        sources = [
            {
                "source": r.metadata.get("source"),
                "excerpt": r.text[:200],
                "relevance": r.score
            }
            for r in results
        ]

        return RAGResponse(
            answer=response,
            sources=sources,
            confidence=self._calculate_confidence(results)
        )

    def _allowed_classifications(self, clearance: str) -> List[str]:
        """Return classifications user can access."""
        hierarchy = ["UNCLASSIFIED", "CUI", "CONFIDENTIAL", "SECRET", "TOP_SECRET"]
        idx = hierarchy.index(clearance) if clearance in hierarchy else 0
        return hierarchy[:idx + 1]

    def _build_context(self, results: List) -> str:
        """Build context from retrieved documents."""
        context_parts = []
        for i, result in enumerate(results, 1):
            context_parts.append(f"[{i}] {result.text}\nSource: {result.metadata.get('source', 'Unknown')}")
        return "\n\n".join(context_parts)

    def _build_prompt(self, question: str, context: str) -> str:
        return f"""You are a federal knowledge assistant. Answer the question based ONLY on the provided context. If the context doesn't contain enough information, say so.

Context:
{context}

Question: {question}

Instructions:
1. Answer based only on the provided context
2. Cite sources using [1], [2], etc.
3. If unsure, indicate uncertainty
4. Never make up information

Answer:"""

    def _calculate_confidence(self, results: List) -> float:
        """Calculate confidence based on retrieval scores."""
        if not results:
            return 0.0
        avg_score = sum(r.score for r in results) / len(results)
        return min(avg_score, 1.0)
```

---

## 10.6 Advanced RAG Techniques

### Hybrid Search

```python
from rank_bm25 import BM25Okapi
import numpy as np

class HybridRetriever:
    """Combine semantic and keyword search."""

    def __init__(
        self,
        vector_store: VectorStore,
        documents: List[str],
        alpha: float = 0.7  # Weight for semantic search
    ):
        self.vector_store = vector_store
        self.alpha = alpha

        # Build BM25 index
        tokenized = [doc.lower().split() for doc in documents]
        self.bm25 = BM25Okapi(tokenized)
        self.documents = documents

    async def search(
        self,
        query: str,
        query_embedding: np.ndarray,
        top_k: int = 10
    ) -> List[dict]:
        # Semantic search
        semantic_results = await self.vector_store.search(
            embedding=query_embedding,
            top_k=top_k * 2
        )

        # Keyword search
        tokenized_query = query.lower().split()
        bm25_scores = self.bm25.get_scores(tokenized_query)
        keyword_indices = np.argsort(bm25_scores)[::-1][:top_k * 2]

        # Combine scores with RRF (Reciprocal Rank Fusion)
        combined_scores = {}

        for rank, result in enumerate(semantic_results):
            doc_id = result.id
            combined_scores[doc_id] = combined_scores.get(doc_id, 0) + \
                self.alpha / (60 + rank)

        for rank, idx in enumerate(keyword_indices):
            doc_id = str(idx)
            combined_scores[doc_id] = combined_scores.get(doc_id, 0) + \
                (1 - self.alpha) / (60 + rank)

        # Sort by combined score
        sorted_ids = sorted(combined_scores.keys(),
                          key=lambda x: combined_scores[x],
                          reverse=True)[:top_k]

        return [{"id": doc_id, "score": combined_scores[doc_id]}
                for doc_id in sorted_ids]
```

### Query Expansion

```python
class QueryExpander:
    """Expand queries for better retrieval."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    async def expand(self, query: str, num_variations: int = 3) -> List[str]:
        prompt = f"""Generate {num_variations} alternative phrasings of this question that might help find relevant documents. Include the original query.

Original query: {query}

Alternative phrasings (one per line):"""

        response = await self.llm.generate(prompt)
        variations = [query] + [
            line.strip() for line in response.split('\n')
            if line.strip()
        ]
        return variations[:num_variations + 1]

    async def decompose(self, query: str) -> List[str]:
        """Break complex query into sub-questions."""
        prompt = f"""Break this complex question into simpler sub-questions that can be answered independently:

Question: {query}

Sub-questions (one per line):"""

        response = await self.llm.generate(prompt)
        return [line.strip() for line in response.split('\n') if line.strip()]
```

### Reranking

```python
class CrossEncoderReranker:
    """Rerank results using cross-encoder model."""

    def __init__(self, model_name: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"):
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)

    def rerank(
        self,
        query: str,
        results: List[dict],
        top_k: int = 5
    ) -> List[dict]:
        # Score each query-document pair
        pairs = [(query, r['text']) for r in results]
        scores = self.model.predict(pairs)

        # Sort by score
        scored_results = list(zip(results, scores))
        scored_results.sort(key=lambda x: x[1], reverse=True)

        return [
            {**r, 'rerank_score': float(s)}
            for r, s in scored_results[:top_k]
        ]
```

---

## 10.7 Evaluation Metrics

```python
from typing import List, Tuple

class RAGEvaluator:
    """Evaluate RAG system quality."""

    def __init__(self, llm: LLMClient):
        self.llm = llm

    def precision_at_k(
        self,
        retrieved: List[str],
        relevant: List[str],
        k: int
    ) -> float:
        """Precision of top-k retrieved documents."""
        retrieved_k = set(retrieved[:k])
        relevant_set = set(relevant)
        return len(retrieved_k & relevant_set) / k

    def recall_at_k(
        self,
        retrieved: List[str],
        relevant: List[str],
        k: int
    ) -> float:
        """Recall of top-k retrieved documents."""
        retrieved_k = set(retrieved[:k])
        relevant_set = set(relevant)
        if not relevant_set:
            return 0.0
        return len(retrieved_k & relevant_set) / len(relevant_set)

    def mrr(self, retrieved: List[str], relevant: List[str]) -> float:
        """Mean Reciprocal Rank."""
        for i, doc in enumerate(retrieved):
            if doc in relevant:
                return 1 / (i + 1)
        return 0.0

    async def faithfulness(
        self,
        question: str,
        context: str,
        answer: str
    ) -> float:
        """Measure if answer is faithful to context."""
        prompt = f"""Evaluate if the answer is faithful to the provided context (only uses information from context, no hallucination).

Context: {context}

Question: {question}

Answer: {answer}

Score from 0-1 (1 = completely faithful):"""

        response = await self.llm.generate(prompt)
        try:
            return float(response.strip())
        except:
            return 0.5

    async def relevance(
        self,
        question: str,
        answer: str
    ) -> float:
        """Measure if answer is relevant to question."""
        prompt = f"""Evaluate if the answer is relevant and addresses the question.

Question: {question}

Answer: {answer}

Score from 0-1 (1 = completely relevant):"""

        response = await self.llm.generate(prompt)
        try:
            return float(response.strip())
        except:
            return 0.5
```

---

## Hands-On Lab

### Lab 10.1: Build Federal Document RAG

Create a RAG system for federal policy documents:
1. Ingest NIST 800-53 controls
2. Implement semantic search
3. Add metadata filtering
4. Build Q&A interface

**Requirements:**
- Handle CUI classification
- Provide source citations
- Support hybrid search
- Include evaluation metrics

---

## Knowledge Check

1. What are the key components of a RAG system?
2. How does chunking strategy affect retrieval quality?
3. When should you use hybrid search vs pure semantic search?
4. How do you evaluate RAG system performance?

---

<div align="center">

[← Module 09: Coding Assistants](../09-coding-assistants/README.md) | [Home](../../README.md) | [Module 11: Fine-Tuning →](../11-fine-tuning/README.md)

</div>
