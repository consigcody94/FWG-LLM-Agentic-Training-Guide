#!/usr/bin/env python3
"""
Module 01: LLM Foundations - Interactive Quiz
Test your understanding of transformer architecture, tokenization, and model fundamentals
"""

from quiz_framework import Quiz, MultipleChoice, TrueFalse, FillInBlank


def create_module01_quiz():
    """Create the Module 01 quiz with comprehensive questions"""

    quiz = Quiz(
        title="Module 01: LLM Foundations - Knowledge Assessment",
        module="01",
        difficulty="beginner",
        time_limit=30,
        passing_score=70
    )

    # Question 1: Transformer Innovation
    quiz.add_question(MultipleChoice(
        question="What is the PRIMARY innovation that the Transformer architecture introduced to NLP?",
        options=[
            "Recurrent connections for better sequential processing",
            "Self-attention mechanism enabling parallel processing",
            "Convolutional layers for pattern recognition",
            "Larger embedding dimensions for more parameters"
        ],
        correct=1,
        explanation="The Transformer's key innovation was the self-attention mechanism, which allows parallel processing of entire sequences rather than sequential token-by-token processing used in RNNs/LSTMs.",
        points=10,
        reference="modules/01-foundations/README.md#transformer-architecture-deep-dive"
    ))

    # Question 2: Tokenization
    quiz.add_question(MultipleChoice(
        question='How many tokens would the text "unhappiness" MOST LIKELY be split into using BPE tokenization?',
        options=[
            "1 token (the whole word)",
            "2 tokens (e.g., 'un' + 'happiness')",
            "11 tokens (one per character)",
            "3 tokens (e.g., 'un' + 'happi' + 'ness')"
        ],
        correct=1,
        explanation="BPE (Byte-Pair Encoding) typically breaks words into subword units. 'unhappiness' would likely split into common pieces like 'un' (common prefix) and 'happiness' (common word), resulting in 2 tokens. The exact split depends on the vocabulary, but 2-3 tokens is most common.",
        points=10,
        reference="modules/01-foundations/README.md#tokenization"
    ))

    # Question 3: Cost Implications
    quiz.add_question(MultipleChoice(
        question="Your agency processes 1,000 documents per month, each ~5,000 tokens. At $0.03 per 1K input tokens, what is the monthly cost?",
        options=[
            "$15",
            "$150",
            "$1,500",
            "$15,000"
        ],
        correct=1,
        explanation="Cost calculation: 1,000 documents × 5,000 tokens = 5,000,000 tokens total. At $0.03 per 1,000 tokens: (5,000,000 / 1,000) × $0.03 = $150/month. This demonstrates why token economics matter for federal budgets!",
        points=15,
        reference="modules/01-foundations/README.md#cost-implications"
    ))

    # Question 4: Attention Mechanism
    quiz.add_question(MultipleChoice(
        question='In the sentence "The employee who submitted the report was promoted," which word should "promoted" pay most attention to?',
        options=[
            "The",
            "employee",
            "submitted",
            "report"
        ],
        correct=1,
        explanation="'Promoted' should attend most strongly to 'employee' because the employee is the subject receiving the action of promotion. While 'submitted' and 'report' provide context, 'employee' is the grammatical subject of 'promoted'.",
        points=10,
        reference="modules/01-foundations/README.md#attention-mechanisms"
    ))

    # Question 5: Scaling Laws
    quiz.add_question(TrueFalse(
        question="According to Chinchilla scaling laws, a model with 70 billion parameters should ideally be trained on approximately 1.4 trillion tokens for optimal performance.",
        correct=True,
        explanation="Chinchilla scaling laws suggest optimal training uses: Parameters ≈ Training Tokens / 20. For 70B parameters: 70B × 20 ≈ 1.4T tokens. This is why modern models like Llama 70B are trained on massive datasets.",
        points=10,
        reference="modules/01-foundations/README.md#scaling-laws"
    ))

    # Question 6: Emergent Capabilities
    quiz.add_question(MultipleChoice(
        question="At approximately what parameter count do models typically develop reliable Chain-of-Thought reasoning capabilities?",
        options=[
            "~1 billion parameters",
            "~10 billion parameters",
            "~60 billion parameters",
            "~500 billion parameters"
        ],
        correct=2,
        explanation="Chain-of-Thought reasoning emerges around 60B parameters. Below this threshold, models struggle to break down complex problems into logical steps. This is why smaller models (7B-13B) often can't explain their reasoning well.",
        points=15,
        reference="modules/01-foundations/README.md#emergent-capabilities"
    ))

    # Question 7: Context Window
    quiz.add_question(MultipleChoice(
        question="GPT-4 with 128K context window can process approximately how many pages of text?",
        options=[
            "~50 pages",
            "~150 pages",
            "~380 pages",
            "~1,000 pages"
        ],
        correct=2,
        explanation="128,000 tokens ≈ 96,000 words ≈ 380 pages (assuming ~250 words/page). This is crucial for processing long federal documents like regulations or policy manuals in a single pass.",
        points=10,
        reference="modules/01-foundations/README.md#context-window-implications"
    ))

    # Question 8: Model Architecture
    quiz.add_question(MultipleChoice(
        question="Which type of model architecture would be BEST for classifying emails as spam or not spam?",
        options=[
            "Decoder-only (like GPT)",
            "Encoder-only (like BERT)",
            "Encoder-decoder (like T5)",
            "All architectures work equally well"
        ],
        correct=1,
        explanation="Encoder-only models (like BERT) are best for classification tasks. They process the entire input bidirectionally to understand it, then output a classification. Decoder models are optimized for generation, not understanding.",
        points=10,
        reference="modules/01-foundations/README.md#encoder-vs-decoder"
    ))

    # Question 9: Practical Application
    quiz.add_question(TrueFalse(
        question="For processing classified documents that cannot leave an air-gapped network, you should use proprietary API-based models like GPT-4 or Claude.",
        correct=False,
        explanation="For air-gapped, classified environments, you MUST use local open-source models (like Llama or Mistral) that can run entirely on your own infrastructure. API-based models send data to external servers, violating security requirements.",
        points=15,
        reference="modules/01-foundations/README.md#model-selection"
    ))

    # Question 10: Token Economics
    quiz.add_question(FillInBlank(
        question="The process of converting text into numerical tokens that LLMs can process is called ________.",
        correct_answers=["tokenization", "tokenisation"],
        explanation="Tokenization is the foundational process of breaking text into tokens (subword units) that get converted to numbers. Understanding tokenization is critical for cost optimization and debugging AI behavior.",
        points=5,
        reference="modules/01-foundations/README.md#tokenization"
    ))

    return quiz


if __name__ == "__main__":
    quiz = create_module01_quiz()
    quiz.run()
