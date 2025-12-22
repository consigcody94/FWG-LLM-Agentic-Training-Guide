#!/usr/bin/env python3
"""
Example 02: RAG System
A Retrieval-Augmented Generation system for document Q&A.
"""

import os
import sys
import argparse
import logging
from pathlib import Path
from typing import List, Optional
from dataclasses import dataclass

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class RAGConfig:
    """RAG system configuration."""
    embedding_model: str = "all-MiniLM-L6-v2"
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k: int = 5
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o-mini"
    persist_directory: str = "./chroma_db"


# =============================================================================
# Document Processing
# =============================================================================

@dataclass
class Document:
    """A document chunk with metadata."""
    content: str
    metadata: dict
    chunk_id: str


class DocumentProcessor:
    """Process documents into chunks."""

    def __init__(self, config: RAGConfig):
        self.config = config

    def load_file(self, file_path: Path) -> List[Document]:
        """Load and chunk a single file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return self._chunk_document(
            content=content,
            source=str(file_path)
        )

    def load_directory(self, dir_path: Path, pattern: str = "*.txt") -> List[Document]:
        """Load all matching files from a directory."""
        documents = []
        for file_path in Path(dir_path).glob(pattern):
            documents.extend(self.load_file(file_path))
        return documents

    def _chunk_document(self, content: str, source: str) -> List[Document]:
        """Split document into overlapping chunks."""
        chunks = []
        paragraphs = content.split('\n\n')
        current_chunk = ""
        chunk_index = 0

        for para in paragraphs:
            if len(current_chunk) + len(para) > self.config.chunk_size and current_chunk:
                chunks.append(Document(
                    content=current_chunk.strip(),
                    metadata={"source": source, "chunk_index": chunk_index},
                    chunk_id=f"{Path(source).stem}_chunk_{chunk_index}"
                ))
                overlap = current_chunk[-self.config.chunk_overlap:] if len(current_chunk) > self.config.chunk_overlap else ""
                current_chunk = overlap + para + "\n\n"
                chunk_index += 1
            else:
                current_chunk += para + "\n\n"

        if current_chunk.strip():
            chunks.append(Document(
                content=current_chunk.strip(),
                metadata={"source": source, "chunk_index": chunk_index},
                chunk_id=f"{Path(source).stem}_chunk_{chunk_index}"
            ))

        return chunks


# =============================================================================
# Vector Store
# =============================================================================

class VectorStore:
    """ChromaDB vector store wrapper."""

    def __init__(self, config: RAGConfig):
        self.config = config

        # Initialize embedding model
        logger.info(f"Loading embedding model: {config.embedding_model}")
        self.embedder = SentenceTransformer(config.embedding_model)

        # Initialize ChromaDB
        persist_path = Path(config.persist_directory)
        persist_path.mkdir(exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=str(persist_path),
            settings=Settings(anonymized_telemetry=False)
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, documents: List[Document]) -> int:
        """Add documents to the vector store."""
        if not documents:
            return 0

        ids = [doc.chunk_id for doc in documents]
        texts = [doc.content for doc in documents]
        metadatas = [doc.metadata for doc in documents]

        logger.info(f"Generating embeddings for {len(documents)} documents...")
        embeddings = self.embedder.encode(texts).tolist()

        self.collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas
        )

        return len(documents)

    def search(self, query: str, n_results: int = 5) -> List[dict]:
        """Search for similar documents."""
        query_embedding = self.embedder.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )

        retrieved = []
        for i in range(len(results["documents"][0])):
            retrieved.append({
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i],
                "relevance": 1 - results["distances"][0][i]
            })

        return retrieved

    def clear(self):
        """Clear all documents."""
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def count(self) -> int:
        """Get document count."""
        return self.collection.count()


# =============================================================================
# LLM Generation
# =============================================================================

class LLMGenerator:
    """Generate answers using an LLM."""

    def __init__(self, config: RAGConfig):
        self.config = config

        if config.llm_provider == "openai":
            from openai import OpenAI
            self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif config.llm_provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def generate(self, query: str, context: List[dict]) -> str:
        """Generate an answer based on retrieved context."""
        context_str = "\n\n---\n\n".join([
            f"[Source: {doc['metadata'].get('source', 'Unknown')}]\n{doc['content']}"
            for doc in context
        ])

        system_prompt = """You are a helpful assistant that answers questions based on provided context.
Always cite your sources when providing information.
If the context doesn't contain relevant information, say so clearly.
Be concise but thorough."""

        user_prompt = f"""Context Documents:
{context_str}

---

Question: {query}

Please answer based on the context above, citing specific sources."""

        if self.config.llm_provider == "openai":
            response = self.client.chat.completions.create(
                model=self.config.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=1000,
                temperature=0.3
            )
            return response.choices[0].message.content

        elif self.config.llm_provider == "anthropic":
            response = self.client.messages.create(
                model=self.config.llm_model or "claude-3-5-sonnet-20241022",
                max_tokens=1000,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
            return response.content[0].text


# =============================================================================
# RAG Pipeline
# =============================================================================

class RAGPipeline:
    """Complete RAG pipeline."""

    def __init__(self, config: RAGConfig = None):
        self.config = config or RAGConfig()
        self.processor = DocumentProcessor(self.config)
        self.vector_store = VectorStore(self.config)
        self.generator = LLMGenerator(self.config)

    def index(self, path: Path) -> int:
        """Index documents from a path."""
        if path.is_file():
            documents = self.processor.load_file(path)
        else:
            documents = self.processor.load_directory(path)

        return self.vector_store.add_documents(documents)

    def query(self, question: str) -> dict:
        """Query the RAG system."""
        # Retrieve relevant documents
        context = self.vector_store.search(question, n_results=self.config.top_k)

        if not context:
            return {
                "answer": "No relevant documents found.",
                "sources": [],
                "query": question
            }

        # Generate answer
        answer = self.generator.generate(question, context)

        return {
            "answer": answer,
            "sources": [
                {"source": doc["metadata"]["source"], "relevance": doc["relevance"]}
                for doc in context
            ],
            "query": question
        }


# =============================================================================
# Main Application
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="RAG System Example")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Index command
    index_parser = subparsers.add_parser("index", help="Index documents")
    index_parser.add_argument("path", type=Path, help="Path to documents")
    index_parser.add_argument("--clear", action="store_true", help="Clear existing index")

    # Query command
    query_parser = subparsers.add_parser("query", help="Query the system")
    query_parser.add_argument("question", type=str, help="Question to ask")

    # Interactive command
    subparsers.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()

    # Initialize pipeline
    rag = RAGPipeline()

    if args.command == "index":
        if args.clear:
            rag.vector_store.clear()
            print("Index cleared.")

        count = rag.index(args.path)
        print(f"Indexed {count} document chunks.")
        print(f"Total documents in store: {rag.vector_store.count()}")

    elif args.command == "query":
        result = rag.query(args.question)
        print(f"\n📝 Question: {result['query']}\n")
        print(f"📖 Answer:\n{result['answer']}\n")
        print("📚 Sources:")
        for src in result['sources']:
            print(f"  • {Path(src['source']).name} (relevance: {src['relevance']:.2f})")

    elif args.command == "interactive":
        print("\n🔍 RAG System Interactive Mode")
        print("Type 'exit' to quit\n")

        while True:
            try:
                question = input("❓ Question: ").strip()
                if question.lower() == "exit":
                    break
                if not question:
                    continue

                result = rag.query(question)
                print(f"\n📖 Answer:\n{result['answer']}\n")

            except KeyboardInterrupt:
                break

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
