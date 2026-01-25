"""
Semantic Compression Pipeline - Reference Implementation

This module provides a multi-stage compression pipeline that reduces
token count while preserving semantic information. Includes lexical
compression, entity consolidation, and semantic deduplication.

Part of Module 28: Antigravity - Advanced Agent Techniques
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import re
import math


@dataclass
class CompressionResult:
    """Result of compression operation."""
    original_text: str
    compressed_text: str
    original_tokens: int
    compressed_tokens: int
    compression_ratio: float
    entity_registry: Dict[str, str]
    stages_applied: List[str]
    metrics: Dict[str, Any] = field(default_factory=dict)

    @property
    def tokens_saved(self) -> int:
        return self.original_tokens - self.compressed_tokens

    @property
    def savings_percentage(self) -> float:
        if self.original_tokens == 0:
            return 0.0
        return (1 - self.compression_ratio) * 100


class CompressionStage(ABC):
    """Abstract base class for compression stages."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Stage name for logging."""
        pass

    @abstractmethod
    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        """
        Apply compression to text.

        Returns:
            Tuple of (compressed_text, stage_metadata)
        """
        pass


class StructuralCleaningStage(CompressionStage):
    """
    Remove structural noise from text.

    - Normalize whitespace
    - Remove redundant line breaks
    - Clean up formatting artifacts
    """

    @property
    def name(self) -> str:
        return "structural_cleaning"

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        original_len = len(text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove leading/trailing whitespace
        text = text.strip()

        # Remove multiple periods
        text = re.sub(r'\.{2,}', '.', text)

        metadata = {
            "chars_removed": original_len - len(text)
        }

        return text, metadata


class FillerWordRemovalStage(CompressionStage):
    """
    Remove filler words that add no semantic value.

    Preserves sentence structure while removing words
    like "very", "really", "basically", etc.
    """

    FILLER_WORDS = {
        'very', 'really', 'just', 'quite', 'rather', 'somewhat',
        'basically', 'actually', 'literally', 'essentially',
        'definitely', 'certainly', 'probably', 'possibly',
        'simply', 'merely', 'practically', 'virtually',
        'extremely', 'incredibly', 'absolutely', 'totally',
        'completely', 'entirely', 'perfectly', 'utterly'
    }

    @property
    def name(self) -> str:
        return "filler_removal"

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        words = text.split()
        removed_count = 0
        filtered_words = []

        for word in words:
            # Check if word (lowercase, stripped of punctuation) is a filler
            clean_word = re.sub(r'[^\w]', '', word.lower())
            if clean_word in self.FILLER_WORDS:
                removed_count += 1
            else:
                filtered_words.append(word)

        result = ' '.join(filtered_words)

        # Clean up double spaces
        result = re.sub(r'\s+', ' ', result)

        metadata = {
            "words_removed": removed_count,
            "filler_words_found": removed_count
        }

        return result, metadata


class PhraseAbbreviationStage(CompressionStage):
    """
    Replace verbose phrases with concise equivalents.

    Maintains meaning while reducing token count through
    standard abbreviations and condensed phrasing.
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
        'with regard to': 'regarding',
        'in spite of the fact that': 'although',
        'for the purpose of': 'for',
        'in the near future': 'soon',
        'at the present time': 'now',
        'in light of the fact that': 'because',
        'on a regular basis': 'regularly',
        'in a timely manner': 'promptly',
        'prior to': 'before',
        'subsequent to': 'after',
        'in addition to': 'besides',
        'with the exception of': 'except',
        'in the absence of': 'without',
        'in conjunction with': 'with',
        'a majority of': 'most',
        'a minority of': 'few',
        'at all times': 'always',
        'on the occasion of': 'when',
    }

    @property
    def name(self) -> str:
        return "phrase_abbreviation"

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        replacements_made = 0
        result = text

        # Sort by length (longest first) to avoid partial matches
        sorted_phrases = sorted(
            self.ABBREVIATIONS.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )

        for phrase, replacement in sorted_phrases:
            # Case-insensitive replacement
            pattern = re.compile(re.escape(phrase), re.IGNORECASE)
            new_result, count = pattern.subn(replacement, result)
            replacements_made += count
            result = new_result

        metadata = {
            "phrases_replaced": replacements_made
        }

        return result, metadata


class EntityConsolidationStage(CompressionStage):
    """
    Consolidate repeated entity mentions.

    Tracks named entities and replaces subsequent mentions
    with short references, maintaining a registry for
    decompression.
    """

    def __init__(self, min_entity_length: int = 3):
        self.min_entity_length = min_entity_length
        self.entity_registry: Dict[str, str] = {}

    @property
    def name(self) -> str:
        return "entity_consolidation"

    def _extract_entities(self, text: str) -> List[Tuple[str, int, int]]:
        """
        Extract potential entities from text.

        Uses heuristic approach - looks for capitalized phrases,
        quoted terms, and organizational patterns.
        """
        entities = []

        # Pattern for capitalized phrases (2+ words)
        cap_pattern = r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b'
        for match in re.finditer(cap_pattern, text):
            if len(match.group(1)) >= self.min_entity_length:
                entities.append((
                    match.group(1),
                    match.start(),
                    match.end()
                ))

        # Pattern for acronyms followed by full name
        acronym_pattern = r'\b([A-Z]{2,})\b'
        for match in re.finditer(acronym_pattern, text):
            entities.append((
                match.group(1),
                match.start(),
                match.end()
            ))

        return entities

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        self.entity_registry = {}
        entity_counter = {}

        # Extract entities
        entities = self._extract_entities(text)

        # Count occurrences
        entity_counts: Dict[str, int] = {}
        for entity_text, _, _ in entities:
            entity_counts[entity_text] = entity_counts.get(entity_text, 0) + 1

        # Only consolidate entities that appear 2+ times
        repeated_entities = {
            e for e, count in entity_counts.items() if count >= 2
        }

        # Create registry and replace
        result = text
        replaced_count = 0

        for entity in repeated_entities:
            # Generate short reference
            entity_type = self._classify_entity(entity)
            if entity_type not in entity_counter:
                entity_counter[entity_type] = 0
            entity_counter[entity_type] += 1

            ref = f"[{entity_type}:{entity_counter[entity_type]}]"
            self.entity_registry[ref] = entity

            # Replace all but first occurrence
            pattern = re.escape(entity)
            matches = list(re.finditer(pattern, result))

            if len(matches) > 1:
                # Replace from end to preserve positions
                for match in reversed(matches[1:]):
                    result = (
                        result[:match.start()] +
                        ref +
                        result[match.end():]
                    )
                    replaced_count += 1

        metadata = {
            "entities_found": len(repeated_entities),
            "replacements_made": replaced_count,
            "registry": self.entity_registry.copy()
        }

        return result, metadata

    def _classify_entity(self, entity: str) -> str:
        """Classify entity type for reference generation."""
        # Simple heuristics
        if re.match(r'^[A-Z]{2,}$', entity):
            return "ACRONYM"
        elif any(word in entity.lower() for word in
                 ['department', 'agency', 'office', 'bureau', 'commission']):
            return "ORG"
        elif any(word in entity.lower() for word in
                 ['act', 'law', 'regulation', 'policy', 'order']):
            return "LAW"
        else:
            return "ENT"

    def get_registry(self) -> Dict[str, str]:
        """Get the entity registry for decompression."""
        return self.entity_registry.copy()


class SemanticDeduplicationStage(CompressionStage):
    """
    Remove semantically redundant sentences.

    Uses embedding similarity to identify and remove
    sentences that convey the same information.
    """

    def __init__(
        self,
        similarity_threshold: float = 0.85,
        embedding_fn=None
    ):
        self.similarity_threshold = similarity_threshold
        self.embedding_fn = embedding_fn or self._default_embedding

    @property
    def name(self) -> str:
        return "semantic_deduplication"

    def _default_embedding(self, text: str) -> List[float]:
        """
        Default embedding (hash-based for demo).

        In production, use sentence-transformers or similar.
        """
        import hashlib
        hash_bytes = hashlib.sha256(text.lower().encode()).digest()
        return [b / 255.0 for b in hash_bytes[:32]]

    def _cosine_similarity(
        self,
        vec1: List[float],
        vec2: List[float]
    ) -> float:
        """Calculate cosine similarity between vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)

    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        sentences = self._split_sentences(text)

        if len(sentences) <= 1:
            return text, {"sentences_removed": 0}

        # Generate embeddings
        embeddings = [self.embedding_fn(s) for s in sentences]

        # Find redundant sentences
        keep_indices = [0]  # Always keep first sentence

        for i in range(1, len(sentences)):
            is_redundant = False

            for j in keep_indices:
                similarity = self._cosine_similarity(
                    embeddings[i],
                    embeddings[j]
                )

                if similarity >= self.similarity_threshold:
                    is_redundant = True
                    break

            if not is_redundant:
                keep_indices.append(i)

        # Reconstruct text
        kept_sentences = [sentences[i] for i in sorted(keep_indices)]
        result = ' '.join(kept_sentences)

        metadata = {
            "sentences_original": len(sentences),
            "sentences_kept": len(kept_sentences),
            "sentences_removed": len(sentences) - len(kept_sentences)
        }

        return result, metadata


class AbstractiveSummaryStage(CompressionStage):
    """
    Abstractive summarization for aggressive compression.

    Uses an LLM to generate a concise summary while
    preserving key information.
    """

    def __init__(
        self,
        summarizer_fn=None,
        target_ratio: float = 0.3
    ):
        self.summarizer_fn = summarizer_fn or self._default_summarize
        self.target_ratio = target_ratio

    @property
    def name(self) -> str:
        return "abstractive_summary"

    def _default_summarize(self, text: str) -> str:
        """Default summarization (truncation). Replace with LLM."""
        target_len = int(len(text) * self.target_ratio)

        if len(text) <= target_len:
            return text

        # Find sentence boundary near target
        sentences = re.split(r'(?<=[.!?])\s+', text)
        result = []
        current_len = 0

        for sentence in sentences:
            if current_len + len(sentence) <= target_len:
                result.append(sentence)
                current_len += len(sentence) + 1
            else:
                break

        if not result:
            return text[:target_len] + "..."

        return ' '.join(result)

    def compress(self, text: str) -> Tuple[str, Dict[str, Any]]:
        original_len = len(text)
        result = self.summarizer_fn(text)

        metadata = {
            "original_length": original_len,
            "summary_length": len(result),
            "compression_achieved": len(result) / original_len
        }

        return result, metadata


class CompressionPipeline:
    """
    Multi-stage compression pipeline.

    Orchestrates multiple compression stages to achieve
    maximum compression while preserving semantic content.
    """

    def __init__(
        self,
        stages: List[CompressionStage] = None,
        chars_per_token: float = 4.0
    ):
        self.stages = stages or self._default_stages()
        self.chars_per_token = chars_per_token

    def _default_stages(self) -> List[CompressionStage]:
        """Create default compression stages."""
        return [
            StructuralCleaningStage(),
            FillerWordRemovalStage(),
            PhraseAbbreviationStage(),
            EntityConsolidationStage(),
            SemanticDeduplicationStage(similarity_threshold=0.85),
        ]

    def _count_tokens(self, text: str) -> int:
        """Estimate token count."""
        return int(len(text) / self.chars_per_token)

    def compress(
        self,
        text: str,
        target_ratio: Optional[float] = None
    ) -> CompressionResult:
        """
        Apply compression pipeline to text.

        Args:
            text: Input text to compress
            target_ratio: Optional target compression ratio

        Returns:
            CompressionResult with compressed text and metrics
        """
        original_text = text
        original_tokens = self._count_tokens(text)

        current_text = text
        stages_applied = []
        all_metrics = {}
        entity_registry = {}

        for stage in self.stages:
            compressed, metadata = stage.compress(current_text)

            stages_applied.append(stage.name)
            all_metrics[stage.name] = metadata

            # Track entity registry
            if 'registry' in metadata:
                entity_registry.update(metadata['registry'])

            current_text = compressed

            # Check if target ratio achieved
            if target_ratio:
                current_ratio = (
                    self._count_tokens(current_text) / original_tokens
                )
                if current_ratio <= target_ratio:
                    break

        compressed_tokens = self._count_tokens(current_text)

        return CompressionResult(
            original_text=original_text,
            compressed_text=current_text,
            original_tokens=original_tokens,
            compressed_tokens=compressed_tokens,
            compression_ratio=compressed_tokens / original_tokens,
            entity_registry=entity_registry,
            stages_applied=stages_applied,
            metrics=all_metrics
        )

    def decompress(
        self,
        compressed_text: str,
        entity_registry: Dict[str, str]
    ) -> str:
        """
        Decompress text by restoring entity references.

        Note: Some compression stages (filler removal, deduplication)
        are not reversible. This only restores entity references.
        """
        result = compressed_text

        for ref, original in entity_registry.items():
            result = result.replace(ref, original)

        return result


def create_pipeline(
    include_deduplication: bool = True,
    include_abstractive: bool = False,
    similarity_threshold: float = 0.85
) -> CompressionPipeline:
    """
    Create a customized compression pipeline.

    Args:
        include_deduplication: Include semantic deduplication
        include_abstractive: Include abstractive summarization
        similarity_threshold: Threshold for deduplication

    Returns:
        Configured CompressionPipeline
    """
    stages = [
        StructuralCleaningStage(),
        FillerWordRemovalStage(),
        PhraseAbbreviationStage(),
        EntityConsolidationStage(),
    ]

    if include_deduplication:
        stages.append(
            SemanticDeduplicationStage(
                similarity_threshold=similarity_threshold
            )
        )

    if include_abstractive:
        stages.append(AbstractiveSummaryStage())

    return CompressionPipeline(stages=stages)


# Example usage
if __name__ == "__main__":
    TEST_DOCUMENT = """
    The Federal Artificial Intelligence Risk Management Act requires all federal
    agencies to conduct comprehensive risk assessments for artificial intelligence
    systems. The Federal Artificial Intelligence Risk Management Act mandates that
    these assessments be completed annually. Due to the fact that AI systems can
    have significant impacts, agencies must really carefully document all potential
    risks. In order to comply with the requirements, agencies should establish
    dedicated AI governance committees. The AI governance committees are responsible
    for oversight. It is essentially important that agencies maintain detailed
    records of all AI system deployments. At this point in time, a large number of
    agencies are working to implement these requirements.
    """

    # Create pipeline
    pipeline = create_pipeline(
        include_deduplication=True,
        similarity_threshold=0.85
    )

    # Compress
    result = pipeline.compress(TEST_DOCUMENT)

    print("=== Compression Results ===")
    print(f"Original tokens: {result.original_tokens}")
    print(f"Compressed tokens: {result.compressed_tokens}")
    print(f"Compression ratio: {result.compression_ratio:.1%}")
    print(f"Tokens saved: {result.tokens_saved}")
    print(f"Savings: {result.savings_percentage:.1f}%")

    print(f"\nStages applied: {result.stages_applied}")

    print("\n=== Entity Registry ===")
    for ref, original in result.entity_registry.items():
        print(f"  {ref} -> {original}")

    print("\n=== Compressed Text ===")
    print(result.compressed_text)

    print("\n=== Stage Metrics ===")
    for stage, metrics in result.metrics.items():
        print(f"\n{stage}:")
        for key, value in metrics.items():
            if key != 'registry':
                print(f"  {key}: {value}")
