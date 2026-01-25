# Lab 28.2: Implement Semantic Compression Pipeline

## Overview

In this lab, you will build a multi-stage semantic compression pipeline that reduces token count while preserving information fidelity. The goal is to achieve 50% compression with >95% information retention.

**Duration:** 60 minutes
**Difficulty:** Intermediate
**Prerequisites:** Module 10 (RAG Systems)

## Learning Objectives

1. Implement lexical compression techniques
2. Build entity consolidation system
3. Create semantic deduplication using embeddings
4. Measure compression fidelity

## Requirements

```bash
pip install spacy sentence-transformers numpy
python -m spacy download en_core_web_sm
```

## Part 1: Lexical Compression (20 minutes)

### Task 1.1: Filler Word Removal

```python
"""
Task: Implement filler word removal.

Filler words add no semantic value and can be safely removed.
"""

FILLER_WORDS = {
    'very', 'really', 'just', 'quite', 'rather', 'somewhat',
    'basically', 'actually', 'literally', 'essentially',
    'definitely', 'certainly', 'probably', 'possibly',
    'simply', 'merely', 'practically', 'virtually'
}

def remove_filler_words(text: str) -> str:
    """
    Remove filler words from text.

    Example:
        Input: "This is really very important and essentially critical"
        Output: "This is important and critical"
    """
    # TODO: Implement
    pass
```

### Task 1.2: Phrase Abbreviation

```python
"""
Task: Implement phrase abbreviation.

Replace verbose phrases with concise equivalents.
"""

ABBREVIATIONS = {
    'for example': 'e.g.',
    'that is': 'i.e.',
    'in order to': 'to',
    'due to the fact that': 'because',
    'at this point in time': 'now',
    'in the event that': 'if',
    'a large number of': 'many',
    'in close proximity to': 'near',
}

def abbreviate_phrases(text: str) -> str:
    """
    Replace verbose phrases with abbreviations.

    Example:
        Input: "In order to succeed, due to the fact that..."
        Output: "To succeed, because..."
    """
    # TODO: Implement (case-insensitive)
    pass
```

## Part 2: Entity Consolidation (15 minutes)

### Task 2.1: Named Entity Reference System

```python
"""
Task: Implement entity consolidation.

Replace repeated entity mentions with short references.
Keep first mention, replace subsequent.
"""

import spacy

nlp = spacy.load("en_core_web_sm")

def consolidate_entities(text: str) -> tuple[str, dict]:
    """
    Consolidate repeated entity mentions.

    Example:
        Input: "The Department of Defense issued a memo.
                The Department of Defense requires compliance."
        Output: "The Department of Defense issued a memo.
                [ORG:1] requires compliance."

    Returns:
        tuple: (compressed_text, entity_registry)
    """
    # TODO: Implement
    pass
```

## Part 3: Semantic Deduplication (15 minutes)

### Task 3.1: Remove Redundant Sentences

```python
"""
Task: Implement semantic deduplication.

Remove sentences that are semantically similar to others.
"""

from sentence_transformers import SentenceTransformer
import numpy as np

embedder = SentenceTransformer("all-MiniLM-L6-v2")

def deduplicate_sentences(
    text: str,
    similarity_threshold: float = 0.85
) -> str:
    """
    Remove semantically redundant sentences.

    Example:
        Input: "AI systems must be tested. Testing of AI is required.
                Documentation should be maintained."
        Output: "AI systems must be tested.
                Documentation should be maintained."
    """
    # TODO: Implement
    pass
```

## Part 4: Complete Pipeline (10 minutes)

### Task 4.1: Combine All Stages

```python
"""
Task: Build the complete compression pipeline.
"""

from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class CompressionResult:
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    entity_registry: Dict[str, str]
    stages_applied: list

class CompressionPipeline:
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold

    def compress(self, text: str) -> CompressionResult:
        """
        Apply full compression pipeline:
        1. Structural cleaning
        2. Filler word removal
        3. Phrase abbreviation
        4. Entity consolidation
        5. Semantic deduplication
        """
        original_tokens = len(text.split())
        stages = []

        # Stage 1: Structural cleaning
        text = ' '.join(text.split())
        stages.append("structural")

        # Stage 2: Filler words
        text = remove_filler_words(text)
        stages.append("filler_removal")

        # Stage 3: Abbreviations
        text = abbreviate_phrases(text)
        stages.append("abbreviation")

        # Stage 4: Entity consolidation
        text, entities = consolidate_entities(text)
        stages.append("entity_consolidation")

        # Stage 5: Deduplication
        text = deduplicate_sentences(text, self.similarity_threshold)
        stages.append("deduplication")

        compressed_tokens = len(text.split())

        return CompressionResult(
            original_text=text,
            compressed_text=text,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / original_tokens,
            entity_registry=entities,
            stages_applied=stages
        )
```

## Testing

### Fidelity Test

```python
"""
Test compression fidelity using Q&A accuracy.
"""

TEST_DOCUMENT = """
The Federal Artificial Intelligence Risk Management Act requires all federal
agencies to conduct comprehensive risk assessments for artificial intelligence
systems. The Federal Artificial Intelligence Risk Management Act mandates that
these assessments be completed annually. Due to the fact that AI systems can
have significant impacts, agencies must really carefully document all potential
risks. In order to comply with the requirements, agencies should establish
dedicated AI governance committees. The AI governance committees are responsible
for oversight. It is essentially important that agencies maintain detailed
records of all AI system deployments.
"""

TEST_QUESTIONS = [
    ("What does the Act require?", "risk assessments"),
    ("How often are assessments needed?", "annually"),
    ("What must agencies establish?", "committees"),
]

def test_fidelity(original: str, compressed: str, questions: list) -> float:
    """
    Test if compressed text preserves key information.

    Returns accuracy score (0.0 to 1.0)
    """
    # Simple keyword presence check
    correct = 0
    for question, expected_keyword in questions:
        if expected_keyword.lower() in compressed.lower():
            correct += 1
    return correct / len(questions)

# Run test
pipeline = CompressionPipeline()
result = pipeline.compress(TEST_DOCUMENT)

print(f"Original tokens: {result.original_tokens}")
print(f"Compressed tokens: {result.compressed_tokens}")
print(f"Compression ratio: {result.compression_ratio:.1%}")
print(f"Fidelity score: {test_fidelity(TEST_DOCUMENT, result.compressed_text, TEST_QUESTIONS):.1%}")
```

## Deliverables

1. Working compression pipeline implementation
2. Test results showing:
   - Compression ratio achieved
   - Fidelity score
   - Example compressed output

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Achieves >40% compression | 25 |
| Maintains >90% fidelity | 25 |
| Entity registry is accurate | 20 |
| Deduplication works correctly | 20 |
| Code quality | 10 |
| **Total** | **100** |
