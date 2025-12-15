<div align="center">

# Module 11: Fine-Tuning LLMs

<img src="https://img.shields.io/badge/Duration-4_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Advanced-red?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Customizing language models for specialized federal applications*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Understand when fine-tuning is appropriate vs other approaches
- [ ] Prepare datasets for supervised fine-tuning
- [ ] Implement parameter-efficient fine-tuning (LoRA/QLoRA)
- [ ] Evaluate fine-tuned model performance
- [ ] Deploy fine-tuned models securely

---

## 11.1 Fine-Tuning Decision Framework

```
┌─────────────────────────────────────────────────────────────────┐
│              WHEN TO FINE-TUNE VS ALTERNATIVES                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  NEED                          SOLUTION                          │
│  ────                          ────────                          │
│                                                                  │
│  Specific format/style      →  Few-shot prompting               │
│  Current information        →  RAG                               │
│  Domain terminology         →  Fine-tuning (light)              │
│  Specialized task           →  Fine-tuning (full)               │
│  Behavior modification      →  RLHF / Constitutional AI         │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FINE-TUNING IS BEST WHEN:                                      │
│  ✓ You have quality training data (100+ examples)               │
│  ✓ Task requires specialized knowledge                          │
│  ✓ Consistent output format needed                              │
│  ✓ Reducing prompt length is valuable                           │
│  ✓ Base model understands task but needs refinement             │
│                                                                  │
│  FINE-TUNING IS NOT BEST WHEN:                                  │
│  ✗ You need factual accuracy (use RAG)                          │
│  ✗ Information changes frequently (use RAG)                     │
│  ✗ Few examples available (<50)                                 │
│  ✗ Task is simple prompt engineering can solve                  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Cost-Benefit Analysis

| Approach | Setup Cost | Inference Cost | Latency | Customization |
|----------|------------|----------------|---------|---------------|
| Prompting | Low | Higher (long prompts) | Low | Limited |
| RAG | Medium | Medium | Medium | High (docs) |
| Fine-tuning | High | Lower | Low | High (behavior) |
| From Scratch | Very High | Variable | Variable | Complete |

---

## 11.2 Dataset Preparation

### Data Format Standards

```python
from dataclasses import dataclass
from typing import List, Optional
import json

@dataclass
class TrainingExample:
    """Standard format for fine-tuning data."""
    system: Optional[str]  # System prompt
    messages: List[dict]   # Conversation turns

# OpenAI format
openai_format = {
    "messages": [
        {"role": "system", "content": "You are a federal policy expert."},
        {"role": "user", "content": "What is FISMA?"},
        {"role": "assistant", "content": "FISMA (Federal Information Security Management Act)..."}
    ]
}

# Anthropic format
anthropic_format = {
    "prompt": "\n\nHuman: What is FISMA?\n\nAssistant:",
    "completion": " FISMA (Federal Information Security Management Act)..."
}

# Alpaca format (common for open models)
alpaca_format = {
    "instruction": "Explain what FISMA is.",
    "input": "",
    "output": "FISMA (Federal Information Security Management Act)..."
}

# ShareGPT format (multi-turn)
sharegpt_format = {
    "conversations": [
        {"from": "human", "value": "What is FISMA?"},
        {"from": "gpt", "value": "FISMA (Federal Information Security Management Act)..."},
        {"from": "human", "value": "What are its requirements?"},
        {"from": "gpt", "value": "FISMA requires agencies to..."}
    ]
}
```

### Dataset Curation Pipeline

```python
import json
from pathlib import Path
from typing import List, Tuple
import hashlib

class DatasetCurator:
    """Prepare and validate fine-tuning datasets."""

    def __init__(self, min_length: int = 10, max_length: int = 4096):
        self.min_length = min_length
        self.max_length = max_length
        self.seen_hashes = set()

    def load_raw_data(self, path: Path) -> List[dict]:
        """Load raw data from various sources."""
        data = []

        if path.suffix == '.jsonl':
            with open(path) as f:
                for line in f:
                    data.append(json.loads(line))
        elif path.suffix == '.json':
            with open(path) as f:
                data = json.load(f)

        return data

    def validate_example(self, example: dict) -> Tuple[bool, str]:
        """Validate a single training example."""
        # Check required fields
        if 'messages' not in example:
            return False, "Missing 'messages' field"

        messages = example['messages']
        if len(messages) < 2:
            return False, "Need at least user and assistant messages"

        # Check message structure
        for msg in messages:
            if 'role' not in msg or 'content' not in msg:
                return False, "Invalid message structure"
            if msg['role'] not in ['system', 'user', 'assistant']:
                return False, f"Invalid role: {msg['role']}"

        # Check lengths
        total_length = sum(len(m['content']) for m in messages)
        if total_length < self.min_length:
            return False, "Content too short"
        if total_length > self.max_length:
            return False, "Content too long"

        # Check for duplicates
        content_hash = hashlib.md5(
            json.dumps(messages, sort_keys=True).encode()
        ).hexdigest()

        if content_hash in self.seen_hashes:
            return False, "Duplicate example"
        self.seen_hashes.add(content_hash)

        return True, "Valid"

    def clean_content(self, text: str) -> str:
        """Clean and normalize text content."""
        # Remove excess whitespace
        text = ' '.join(text.split())

        # Remove PII patterns (basic)
        import re
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', text)
        text = re.sub(r'\b\d{9}\b', '[SSN REDACTED]', text)

        return text

    def prepare_dataset(
        self,
        raw_data: List[dict],
        train_split: float = 0.9
    ) -> Tuple[List[dict], List[dict]]:
        """Prepare train/validation split."""
        valid_data = []

        for example in raw_data:
            # Clean content
            if 'messages' in example:
                for msg in example['messages']:
                    msg['content'] = self.clean_content(msg['content'])

            # Validate
            is_valid, reason = self.validate_example(example)
            if is_valid:
                valid_data.append(example)
            else:
                print(f"Skipped: {reason}")

        # Split
        import random
        random.shuffle(valid_data)
        split_idx = int(len(valid_data) * train_split)

        return valid_data[:split_idx], valid_data[split_idx:]

    def save_dataset(
        self,
        data: List[dict],
        output_path: Path,
        format: str = 'jsonl'
    ):
        """Save dataset in specified format."""
        if format == 'jsonl':
            with open(output_path, 'w') as f:
                for example in data:
                    f.write(json.dumps(example) + '\n')
        elif format == 'json':
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2)
```

### Data Augmentation

```python
class DataAugmenter:
    """Augment training data for better coverage."""

    def __init__(self, llm_client):
        self.llm = llm_client

    async def paraphrase(self, text: str) -> str:
        """Generate paraphrased version."""
        prompt = f"""Paraphrase the following text while keeping the same meaning:

Original: {text}

Paraphrased:"""
        return await self.llm.generate(prompt)

    async def generate_variations(
        self,
        example: dict,
        num_variations: int = 3
    ) -> List[dict]:
        """Generate variations of a training example."""
        variations = [example]

        for _ in range(num_variations):
            new_example = example.copy()
            new_example['messages'] = []

            for msg in example['messages']:
                if msg['role'] == 'user':
                    # Paraphrase user queries
                    new_content = await self.paraphrase(msg['content'])
                    new_example['messages'].append({
                        'role': 'user',
                        'content': new_content
                    })
                else:
                    new_example['messages'].append(msg)

            variations.append(new_example)

        return variations
```

---

## 11.3 OpenAI Fine-Tuning

### API-Based Fine-Tuning

```python
from openai import OpenAI
import json

client = OpenAI()

# Upload training file
with open("train.jsonl", "rb") as f:
    training_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

# Upload validation file
with open("valid.jsonl", "rb") as f:
    validation_file = client.files.create(
        file=f,
        purpose="fine-tune"
    )

# Create fine-tuning job
job = client.fine_tuning.jobs.create(
    training_file=training_file.id,
    validation_file=validation_file.id,
    model="gpt-4o-mini-2024-07-18",
    hyperparameters={
        "n_epochs": 3,
        "batch_size": "auto",
        "learning_rate_multiplier": "auto"
    },
    suffix="federal-policy-expert"
)

print(f"Fine-tuning job created: {job.id}")

# Monitor progress
import time

while True:
    job_status = client.fine_tuning.jobs.retrieve(job.id)
    print(f"Status: {job_status.status}")

    if job_status.status in ['succeeded', 'failed', 'cancelled']:
        break

    time.sleep(60)

# Use fine-tuned model
if job_status.status == 'succeeded':
    model_id = job_status.fine_tuned_model

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "user", "content": "What are the FISMA requirements?"}
        ]
    )
    print(response.choices[0].message.content)
```

---

## 11.4 Parameter-Efficient Fine-Tuning (PEFT)

### LoRA Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     LoRA ARCHITECTURE                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Original Weight Matrix W (frozen)                              │
│   ┌─────────────────────────┐                                   │
│   │                         │                                   │
│   │    d × k dimensions     │  → Large, expensive to train      │
│   │                         │                                   │
│   └─────────────────────────┘                                   │
│                                                                  │
│   LoRA Decomposition (trainable)                                │
│   ┌─────┐        ┌─────────────────────┐                        │
│   │  A  │   ×    │          B          │                        │
│   │ d×r │        │        r×k          │  → Small, efficient    │
│   └─────┘        └─────────────────────┘                        │
│                                                                  │
│   W' = W + BA (only A and B are trained)                        │
│                                                                  │
│   Rank r << min(d, k)                                           │
│   Typical r = 8, 16, 32, 64                                     │
│                                                                  │
│   Memory savings: ~10-100x fewer parameters                     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### LoRA Implementation with PEFT

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch

# Load base model
model_name = "meta-llama/Llama-3.2-3B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Configure LoRA
lora_config = LoraConfig(
    r=16,                          # Rank
    lora_alpha=32,                 # Scaling factor
    target_modules=[               # Which layers to adapt
        "q_proj",
        "k_proj",
        "v_proj",
        "o_proj",
        "gate_proj",
        "up_proj",
        "down_proj"
    ],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM
)

# Apply LoRA
model = get_peft_model(model, lora_config)

# Check trainable parameters
model.print_trainable_parameters()
# Output: trainable params: 8,388,608 || all params: 3,213,004,800 || trainable%: 0.2611
```

### QLoRA (4-bit Quantization + LoRA)

```python
from transformers import BitsAndBytesConfig
import torch

# Quantization config for 4-bit
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)

# Apply LoRA to quantized model
from peft import prepare_model_for_kbit_training

model = prepare_model_for_kbit_training(model)
model = get_peft_model(model, lora_config)
```

### Training with Transformers

```python
from transformers import TrainingArguments, Trainer
from datasets import load_dataset

# Load dataset
dataset = load_dataset('json', data_files={
    'train': 'train.jsonl',
    'validation': 'valid.jsonl'
})

# Tokenize
def tokenize_function(examples):
    # Format as chat
    texts = []
    for messages in examples['messages']:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False
        )
        texts.append(text)

    return tokenizer(
        texts,
        truncation=True,
        max_length=2048,
        padding='max_length'
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=dataset['train'].column_names
)

# Training arguments
training_args = TrainingArguments(
    output_dir="./federal-policy-lora",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    weight_decay=0.01,
    warmup_ratio=0.03,
    lr_scheduler_type="cosine",
    logging_steps=10,
    eval_strategy="steps",
    eval_steps=100,
    save_strategy="steps",
    save_steps=100,
    load_best_model_at_end=True,
    bf16=True,
    report_to="none"  # Disable external logging for security
)

# Create trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset['train'],
    eval_dataset=tokenized_dataset['validation'],
    tokenizer=tokenizer
)

# Train
trainer.train()

# Save adapter
model.save_pretrained("./federal-policy-lora")
```

---

## 11.5 Evaluation

### Evaluation Metrics

```python
from typing import List, Dict
import numpy as np

class FineTuneEvaluator:
    """Evaluate fine-tuned model quality."""

    def __init__(self, model, tokenizer, reference_model=None):
        self.model = model
        self.tokenizer = tokenizer
        self.reference_model = reference_model

    def compute_perplexity(self, texts: List[str]) -> float:
        """Compute perplexity on test set."""
        total_loss = 0
        total_tokens = 0

        for text in texts:
            inputs = self.tokenizer(text, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs, labels=inputs['input_ids'])
                total_loss += outputs.loss.item() * inputs['input_ids'].shape[1]
                total_tokens += inputs['input_ids'].shape[1]

        return np.exp(total_loss / total_tokens)

    def evaluate_task_accuracy(
        self,
        test_cases: List[Dict]
    ) -> Dict:
        """Evaluate on specific task test cases."""
        correct = 0
        total = len(test_cases)
        results = []

        for case in test_cases:
            # Generate response
            inputs = self.tokenizer(
                case['input'],
                return_tensors="pt"
            )

            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=256,
                    temperature=0.1
                )

            response = self.tokenizer.decode(
                outputs[0],
                skip_special_tokens=True
            )

            # Check against expected
            is_correct = self._check_response(
                response,
                case['expected']
            )

            if is_correct:
                correct += 1

            results.append({
                'input': case['input'],
                'expected': case['expected'],
                'actual': response,
                'correct': is_correct
            })

        return {
            'accuracy': correct / total,
            'correct': correct,
            'total': total,
            'results': results
        }

    def _check_response(self, actual: str, expected: str) -> bool:
        """Check if response matches expected (flexible matching)."""
        # Normalize
        actual = actual.lower().strip()
        expected = expected.lower().strip()

        # Exact match
        if expected in actual:
            return True

        # Key phrase match
        key_phrases = expected.split(',')
        matches = sum(1 for phrase in key_phrases if phrase.strip() in actual)
        return matches >= len(key_phrases) * 0.8

    def compare_to_baseline(
        self,
        prompts: List[str]
    ) -> Dict:
        """Compare fine-tuned model to baseline."""
        if not self.reference_model:
            raise ValueError("Reference model required for comparison")

        comparisons = []

        for prompt in prompts:
            # Fine-tuned response
            ft_response = self._generate(self.model, prompt)

            # Baseline response
            baseline_response = self._generate(self.reference_model, prompt)

            comparisons.append({
                'prompt': prompt,
                'fine_tuned': ft_response,
                'baseline': baseline_response
            })

        return {'comparisons': comparisons}
```

---

## 11.6 Deployment

### Merging LoRA Weights

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B-Instruct",
    torch_dtype=torch.bfloat16
)

# Load and merge LoRA
model = PeftModel.from_pretrained(base_model, "./federal-policy-lora")
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./federal-policy-merged")
tokenizer.save_pretrained("./federal-policy-merged")
```

### Ollama Deployment

```bash
# Create Modelfile
cat > Modelfile << EOF
FROM ./federal-policy-merged

TEMPLATE """{{ if .System }}<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>

{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>

{{ .Response }}<|eot_id|>"""

PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER stop "<|eot_id|>"

SYSTEM "You are a federal policy expert assistant."
EOF

# Create Ollama model
ollama create federal-policy -f Modelfile

# Test
ollama run federal-policy "What are FISMA requirements?"
```

---

## Hands-On Lab

### Lab 11.1: Fine-Tune a Federal Policy Assistant

Create a fine-tuned model for federal policy Q&A:
1. Prepare dataset from policy documents
2. Fine-tune using QLoRA
3. Evaluate against baseline
4. Deploy with Ollama

**Requirements:**
- Minimum 200 training examples
- Include NIST, FISMA, FedRAMP content
- Measure improvement over base model

---

## Knowledge Check

1. When should you choose fine-tuning over RAG?
2. What is the benefit of LoRA over full fine-tuning?
3. How do you validate fine-tuned model quality?
4. What security considerations apply to fine-tuned models?

---

<div align="center">

[← Module 10: RAG Systems](../10-rag-systems/README.md) | [Home](../../README.md) | [Module 12: Multi-Agent Systems →](../12-multi-agent-systems/README.md)

</div>
