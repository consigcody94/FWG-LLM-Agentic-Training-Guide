# Lab 00: Hello Agent

<div align="center">

**Your First AI Agent Interaction**

⭐ Beginner | ⏱️ 15 minutes | 📚 Module 01

</div>

---

## Learning Objectives

By the end of this lab, you will:

- [ ] Verify your development environment is correctly configured
- [ ] Make your first API call to an LLM
- [ ] Understand the basic request/response structure
- [ ] Run a local LLM with Ollama
- [ ] Compare cloud vs. local model responses

---

## Prerequisites

- Completed [Quick Start](../../README.md#-quick-start) setup
- At least one of: Ollama installed OR API key configured

---

## Part 1: Environment Verification (5 minutes)

### Step 1.1: Run the Verification Script

```bash
cd /path/to/FWG-LLM-Agentic-Training-Guide
python scripts/verify_setup.py
```

**Expected Output:**
```
✅ Python 3.11.x
✅ Node.js 18.x
✅ Ollama installed
...
```

### Step 1.2: Fix Any Issues

If you see ❌ for any component, refer to the Quick Start guide to install missing dependencies.

---

## Part 2: Hello Ollama (Local LLM) (5 minutes)

### Step 2.1: Start Ollama

```bash
# Ensure Ollama is running
ollama serve
```

### Step 2.2: Pull a Model (if not already done)

```bash
ollama pull llama3.2
```

### Step 2.3: Create Your First Agent Script

Create a file called `hello_agent.py`:

```python
"""
Lab 00: Hello Agent
Your first interaction with an AI agent using Ollama.
"""

import ollama

def main():
    print("🤖 Hello Agent - FWG Training Lab 00")
    print("=" * 50)

    # Define the message
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant for Federal Working Group employees learning about AI agents."
        },
        {
            "role": "user",
            "content": "Hello! Please introduce yourself and explain what an AI agent is in 2-3 sentences."
        }
    ]

    print("\n📤 Sending request to Ollama (llama3.2)...")
    print("-" * 50)

    # Make the API call
    response = ollama.chat(
        model="llama3.2",
        messages=messages
    )

    # Extract and display the response
    assistant_message = response["message"]["content"]

    print("\n📥 Response:")
    print("-" * 50)
    print(assistant_message)
    print("-" * 50)

    # Show metadata
    print("\n📊 Response Metadata:")
    print(f"   Model: {response.get('model', 'N/A')}")
    print(f"   Total Duration: {response.get('total_duration', 0) / 1e9:.2f} seconds")
    print(f"   Prompt Eval Count: {response.get('prompt_eval_count', 'N/A')} tokens")
    print(f"   Response Eval Count: {response.get('eval_count', 'N/A')} tokens")

if __name__ == "__main__":
    main()
```

### Step 2.4: Run the Script

```bash
python hello_agent.py
```

### Expected Output

```
🤖 Hello Agent - FWG Training Lab 00
==================================================

📤 Sending request to Ollama (llama3.2)...
--------------------------------------------------

📥 Response:
--------------------------------------------------
Hello! I'm an AI assistant here to help you learn about artificial intelligence
and agent systems. An AI agent is a software program that can perceive its
environment, make decisions, and take actions to achieve specific goals.
Unlike simple chatbots, agents can use tools, access external data, and
operate autonomously to complete complex tasks.
--------------------------------------------------

📊 Response Metadata:
   Model: llama3.2
   Total Duration: 2.34 seconds
   Prompt Eval Count: 45 tokens
   Response Eval Count: 78 tokens
```

---

## Part 3: Hello Cloud API (5 minutes)

### Step 3.1: OpenAI Version

Create `hello_openai.py`:

```python
"""
Lab 00: Hello Agent - OpenAI Version
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🤖 Hello Agent - OpenAI Version")
    print("=" * 50)

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant for Federal Working Group employees."
        },
        {
            "role": "user",
            "content": "Hello! Please introduce yourself and explain what an AI agent is in 2-3 sentences."
        }
    ]

    print("\n📤 Sending request to OpenAI (gpt-4o-mini)...")

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=200
    )

    print("\n📥 Response:")
    print("-" * 50)
    print(response.choices[0].message.content)
    print("-" * 50)

    print("\n📊 Usage:")
    print(f"   Prompt tokens: {response.usage.prompt_tokens}")
    print(f"   Completion tokens: {response.usage.completion_tokens}")
    print(f"   Total tokens: {response.usage.total_tokens}")

if __name__ == "__main__":
    main()
```

### Step 3.2: Anthropic Version

Create `hello_anthropic.py`:

```python
"""
Lab 00: Hello Agent - Anthropic Version
"""

import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🤖 Hello Agent - Anthropic Version")
    print("=" * 50)

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    print("\n📤 Sending request to Anthropic (claude-3-5-sonnet)...")

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=200,
        system="You are a helpful AI assistant for Federal Working Group employees.",
        messages=[
            {
                "role": "user",
                "content": "Hello! Please introduce yourself and explain what an AI agent is in 2-3 sentences."
            }
        ]
    )

    print("\n📥 Response:")
    print("-" * 50)
    print(message.content[0].text)
    print("-" * 50)

    print("\n📊 Usage:")
    print(f"   Input tokens: {message.usage.input_tokens}")
    print(f"   Output tokens: {message.usage.output_tokens}")

if __name__ == "__main__":
    main()
```

### Step 3.3: Run and Compare

```bash
# Run each script
python hello_openai.py
python hello_anthropic.py
python hello_agent.py  # Ollama version for comparison
```

---

## Exercises

### Exercise 1: Modify the Prompt

Change the user message to ask the agent about a specific topic related to federal AI adoption. Observe how the response changes.

### Exercise 2: Compare Models

Modify the Ollama script to try different models:

```python
models = ["llama3.2", "mistral", "codellama"]

for model in models:
    response = ollama.chat(model=model, messages=messages)
    print(f"\n{model}:")
    print(response["message"]["content"][:200])
```

### Exercise 3: Add Streaming

Modify the script to stream the response token by token:

```python
stream = ollama.chat(
    model="llama3.2",
    messages=messages,
    stream=True
)

for chunk in stream:
    print(chunk["message"]["content"], end="", flush=True)
```

---

## Knowledge Check

1. **What is the difference between the `system` and `user` roles in the messages array?**

2. **Why might you choose Ollama (local) over OpenAI API (cloud) for certain tasks?**

3. **What information does the response metadata provide that could be useful for optimization?**

---

## Self-Assessment Rubric

| Criteria | Meets Expectations |
|----------|-------------------|
| Environment verified | All checks pass |
| Ollama script runs | Response received |
| API script runs | At least one cloud API works |
| Understand request structure | Can explain messages array |
| Understand response structure | Can access content and metadata |

---

## Troubleshooting

### Ollama Connection Error

```bash
# Make sure Ollama is running
ollama serve

# Check if models are available
ollama list
```

### API Key Errors

```bash
# Verify .env file exists and has keys
cat .env

# Check environment variable is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY')[:10])"
```

---

## Next Steps

Congratulations! You've completed your first agent lab.

**Next Lab:** [Lab 01: Web GUI Comparison →](../01-web-gui-comparison/README.md)

---

<div align="center">

**Lab 00 Complete!** 🎉

</div>
