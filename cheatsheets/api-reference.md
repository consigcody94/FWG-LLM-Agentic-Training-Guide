<div align="center">

# LLM API Quick Reference

<img src="https://img.shields.io/badge/Quick_Reference-API_Cheatsheet-blue?style=for-the-badge" alt="API Reference"/>

</div>

---

## OpenAI API

### Authentication
```bash
export OPENAI_API_KEY="sk-..."
```

### Chat Completion
```python
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
```

### Streaming
```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Function Calling
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {"type": "string"}
                },
                "required": ["location"]
            }
        }
    }]
)
```

### Key Parameters
| Parameter | Type | Description |
|:----------|:-----|:------------|
| `model` | string | Model ID (gpt-4o, gpt-4, gpt-3.5-turbo) |
| `messages` | array | Conversation messages |
| `temperature` | float | Randomness (0-2, default 1) |
| `max_tokens` | int | Max response tokens |
| `top_p` | float | Nucleus sampling (0-1) |
| `frequency_penalty` | float | Reduce repetition (0-2) |
| `presence_penalty` | float | Encourage new topics (0-2) |

---

## Anthropic Claude API

### Authentication
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Messages API
```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

print(message.content[0].text)
```

### Streaming
```python
with client.messages.stream(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="")
```

### Tool Use
```python
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a location",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string"}
            },
            "required": ["location"]
        }
    }],
    messages=[{"role": "user", "content": "Weather in DC?"}]
)
```

### Key Parameters
| Parameter | Type | Description |
|:----------|:-----|:------------|
| `model` | string | Model ID (claude-3-5-sonnet-20241022) |
| `max_tokens` | int | Required: max response tokens |
| `messages` | array | Conversation messages |
| `system` | string | System prompt |
| `temperature` | float | Randomness (0-1, default 1) |
| `top_k` | int | Top-k sampling |
| `top_p` | float | Nucleus sampling |

---

## Google Gemini API

### Authentication
```bash
export GOOGLE_API_KEY="..."
```

### Generate Content
```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

response = model.generate_content("Hello!")
print(response.text)
```

### Chat
```python
chat = model.start_chat(history=[])
response = chat.send_message("Hello!")
print(response.text)
```

### Streaming
```python
response = model.generate_content("Hello!", stream=True)
for chunk in response:
    print(chunk.text, end="")
```

---

## Ollama API

### Local Endpoint
```
http://localhost:11434
```

### Chat Completion
```python
import ollama

response = ollama.chat(
    model='llama3.2',
    messages=[
        {'role': 'user', 'content': 'Hello!'}
    ]
)
print(response['message']['content'])
```

### Streaming
```python
for chunk in ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Hello!'}],
    stream=True
):
    print(chunk['message']['content'], end='')
```

### HTTP API
```bash
curl http://localhost:11434/api/chat -d '{
  "model": "llama3.2",
  "messages": [{"role": "user", "content": "Hello!"}]
}'
```

---

## Model Comparison

| Provider | Model | Context | Input Cost | Output Cost |
|:---------|:------|--------:|:-----------|:------------|
| OpenAI | gpt-4o | 128K | $2.50/1M | $10.00/1M |
| OpenAI | gpt-4o-mini | 128K | $0.15/1M | $0.60/1M |
| Anthropic | claude-3-5-sonnet | 200K | $3.00/1M | $15.00/1M |
| Anthropic | claude-3-5-haiku | 200K | $0.25/1M | $1.25/1M |
| Google | gemini-1.5-pro | 1M | $1.25/1M | $5.00/1M |
| Ollama | llama3.2 | 128K | Free | Free |

*Prices as of 2025; verify current rates*

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Action |
|:-----|:--------|:-------|
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Verify API key |
| 403 | Forbidden | Check permissions |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry with backoff |
| 503 | Overloaded | Retry later |

### Retry Pattern
```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_api_with_retry():
    return client.chat.completions.create(...)
```

---

## Rate Limits

### OpenAI (Tier 1)
- RPM: 500 requests/minute
- TPM: 30,000 tokens/minute

### Anthropic
- RPM: 50 requests/minute (varies by tier)
- TPM: 40,000 tokens/minute

### Ollama (Local)
- No rate limits
- Limited by hardware

---

<div align="center">

[📚 Return to Curriculum](../README.md)

</div>
