<div align="center">

# Module 22: Real-Time Streaming

<img src="https://img.shields.io/badge/Duration-3_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Modules_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Building responsive AI applications with streaming responses*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Implement LLM response streaming
- [ ] Build SSE (Server-Sent Events) endpoints
- [ ] Handle streaming in web applications
- [ ] Process streamed responses for agents
- [ ] Optimize streaming for user experience

---

## 22.1 Streaming Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                   STREAMING RESPONSE FLOW                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌────────┐        ┌────────┐        ┌────────┐        ┌────┐ │
│   │ Client │───────▶│  API   │───────▶│  LLM   │───────▶│ AI │ │
│   │        │        │Gateway │        │Provider│        │    │ │
│   └────────┘        └────────┘        └────────┘        └────┘ │
│       ▲                 │                  │                    │
│       │                 │                  │                    │
│       │   ◀─────────────┴──────────────────┘                   │
│       │         Token-by-token streaming                        │
│       │                                                         │
│   ┌───┴────────────────────────────────────────────────┐       │
│   │                                                     │       │
│   │   Token1 ──▶ Token2 ──▶ Token3 ──▶ ... ──▶ [DONE] │       │
│   │                                                     │       │
│   │   "The"    "quick"   "brown"      ...     [END]    │       │
│   │                                                     │       │
│   └─────────────────────────────────────────────────────┘       │
│                                                                  │
│   BENEFITS:                                                      │
│   • Reduced perceived latency (first token in ~200ms)           │
│   • Progressive rendering                                        │
│   • Better user experience                                       │
│   • Memory efficient for long responses                          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Streaming vs Non-Streaming

| Aspect | Non-Streaming | Streaming |
|--------|---------------|-----------|
| **Time to First Token** | Full generation time | ~100-500ms |
| **Memory Usage** | Full response in memory | Incremental |
| **User Experience** | Wait then display | Progressive display |
| **Error Handling** | Simpler | More complex |
| **Tool Use** | Easier | Requires buffering |

---

## 22.2 Server-Side Implementation

### OpenAI Streaming

```python
from openai import OpenAI
import asyncio
from typing import AsyncGenerator

client = OpenAI()

async def stream_chat_completion(
    messages: list,
    model: str = "gpt-4o"
) -> AsyncGenerator[str, None]:
    """Stream chat completion response."""
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    )

    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

        # Check for finish reason
        if chunk.choices[0].finish_reason:
            break


# Async version with httpx
async def stream_async(
    messages: list,
    model: str = "gpt-4o"
) -> AsyncGenerator[str, None]:
    """Async streaming with httpx."""
    from openai import AsyncOpenAI

    client = AsyncOpenAI()

    async with client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True
    ) as response:
        async for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
```

### Anthropic Streaming

```python
import anthropic
from typing import AsyncGenerator

client = anthropic.Anthropic()

async def stream_claude(
    messages: list,
    model: str = "claude-sonnet-4-20250514"
) -> AsyncGenerator[str, None]:
    """Stream Claude response."""
    with client.messages.stream(
        model=model,
        max_tokens=4096,
        messages=messages
    ) as stream:
        for text in stream.text_stream:
            yield text


# With events for tool use
async def stream_with_events(
    messages: list
) -> AsyncGenerator[dict, None]:
    """Stream with full event information."""
    with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        messages=messages
    ) as stream:
        for event in stream:
            if event.type == "content_block_delta":
                yield {
                    "type": "text",
                    "content": event.delta.text
                }
            elif event.type == "message_stop":
                yield {
                    "type": "done",
                    "content": None
                }
```

### FastAPI SSE Endpoint

```python
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import json
import asyncio

app = FastAPI()

@app.post("/v1/chat/stream")
async def stream_chat(request: Request):
    """Stream chat completion via SSE."""
    body = await request.json()
    messages = body.get("messages", [])
    model = body.get("model", "gpt-4o")

    async def generate():
        try:
            async for token in stream_chat_completion(messages, model):
                # Format as SSE
                data = json.dumps({
                    "choices": [{
                        "delta": {"content": token},
                        "finish_reason": None
                    }]
                })
                yield f"data: {data}\n\n"

            # Send done signal
            yield f"data: [DONE]\n\n"

        except Exception as e:
            error_data = json.dumps({"error": str(e)})
            yield f"data: {error_data}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"  # Disable nginx buffering
        }
    )


@app.post("/v1/chat/sse")
async def chat_sse(request: Request):
    """Alternative using sse-starlette."""
    body = await request.json()
    messages = body.get("messages", [])

    async def event_generator():
        async for token in stream_chat_completion(messages):
            yield {
                "event": "message",
                "data": json.dumps({"content": token})
            }

        yield {
            "event": "done",
            "data": json.dumps({"finished": True})
        }

    return EventSourceResponse(event_generator())
```

---

## 22.3 Client-Side Implementation

### JavaScript/TypeScript Client

```typescript
// Fetch with streaming
async function streamChat(messages: Message[]): Promise<void> {
  const response = await fetch('/v1/chat/stream', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ messages }),
  });

  if (!response.body) {
    throw new Error('No response body');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    // Process complete SSE messages
    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6);

        if (data === '[DONE]') {
          return;
        }

        try {
          const parsed = JSON.parse(data);
          const content = parsed.choices?.[0]?.delta?.content;

          if (content) {
            // Update UI with new content
            appendToChat(content);
          }
        } catch (e) {
          console.error('Parse error:', e);
        }
      }
    }
  }
}

// Using EventSource for SSE
function streamWithEventSource(messages: Message[]): void {
  const eventSource = new EventSource(
    `/v1/chat/sse?messages=${encodeURIComponent(JSON.stringify(messages))}`
  );

  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    appendToChat(data.content);
  };

  eventSource.addEventListener('done', () => {
    eventSource.close();
  });

  eventSource.onerror = (error) => {
    console.error('SSE error:', error);
    eventSource.close();
  };
}


// React hook for streaming
function useStreamingChat() {
  const [content, setContent] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async (messages: Message[]) => {
    setIsStreaming(true);
    setContent('');

    try {
      const response = await fetch('/v1/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages }),
      });

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split('\n');

        for (const line of lines) {
          if (line.startsWith('data: ') && line !== 'data: [DONE]') {
            const data = JSON.parse(line.slice(6));
            const token = data.choices?.[0]?.delta?.content;
            if (token) {
              setContent(prev => prev + token);
            }
          }
        }
      }
    } finally {
      setIsStreaming(false);
    }
  };

  return { content, isStreaming, sendMessage };
}
```

### Python Client

```python
import httpx
from typing import AsyncGenerator

async def stream_response(
    url: str,
    messages: list
) -> AsyncGenerator[str, None]:
    """Stream response from API."""
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            url,
            json={"messages": messages},
            headers={"Accept": "text/event-stream"},
            timeout=60.0
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data == "[DONE]":
                        break
                    try:
                        parsed = json.loads(data)
                        content = parsed.get("choices", [{}])[0].get("delta", {}).get("content")
                        if content:
                            yield content
                    except json.JSONDecodeError:
                        continue


# Usage
async def main():
    messages = [{"role": "user", "content": "Explain FISMA in detail"}]

    full_response = ""
    async for token in stream_response("http://localhost:8000/v1/chat/stream", messages):
        print(token, end="", flush=True)
        full_response += token

    print()  # Newline at end
```

---

## 22.4 Streaming for Agents

### Tool Call Streaming

```python
class StreamingAgentExecutor:
    """Execute agent with streaming support."""

    def __init__(self, llm, tools: list):
        self.llm = llm
        self.tools = tools
        self.tool_map = {t.name: t for t in tools}

    async def stream_execute(
        self,
        messages: list
    ) -> AsyncGenerator[dict, None]:
        """Stream agent execution."""
        current_messages = messages.copy()

        while True:
            # Stream LLM response
            full_response = ""
            tool_calls = []

            async for event in self._stream_llm(current_messages):
                if event["type"] == "text":
                    full_response += event["content"]
                    yield {
                        "type": "text",
                        "content": event["content"]
                    }
                elif event["type"] == "tool_call":
                    tool_calls.append(event["tool_call"])
                    yield {
                        "type": "tool_call",
                        "tool": event["tool_call"]["name"]
                    }

            # If no tool calls, we're done
            if not tool_calls:
                yield {"type": "done"}
                break

            # Execute tools
            for tool_call in tool_calls:
                yield {
                    "type": "tool_executing",
                    "tool": tool_call["name"]
                }

                result = await self._execute_tool(tool_call)

                yield {
                    "type": "tool_result",
                    "tool": tool_call["name"],
                    "result": result
                }

                # Add to messages
                current_messages.append({
                    "role": "assistant",
                    "content": full_response,
                    "tool_calls": tool_calls
                })
                current_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": str(result)
                })

    async def _stream_llm(self, messages: list):
        """Stream LLM with tool support."""
        # Implementation depends on provider
        pass

    async def _execute_tool(self, tool_call: dict):
        """Execute a tool."""
        tool = self.tool_map.get(tool_call["name"])
        if not tool:
            return {"error": f"Unknown tool: {tool_call['name']}"}

        return await tool.execute(**tool_call["arguments"])
```

### Buffered Processing

```python
class StreamBuffer:
    """Buffer streamed content for processing."""

    def __init__(self, chunk_size: int = 100):
        self.buffer = ""
        self.chunk_size = chunk_size

    def add(self, token: str) -> list[str]:
        """Add token and return any complete chunks."""
        self.buffer += token
        chunks = []

        # Check for sentence boundaries
        while True:
            # Look for sentence endings
            for end in [". ", "? ", "! ", "\n\n"]:
                idx = self.buffer.find(end)
                if idx != -1:
                    chunk = self.buffer[:idx + len(end)]
                    self.buffer = self.buffer[idx + len(end):]
                    chunks.append(chunk)
                    break
            else:
                # No sentence boundary found
                if len(self.buffer) > self.chunk_size:
                    # Force chunk at word boundary
                    space_idx = self.buffer.rfind(" ", 0, self.chunk_size)
                    if space_idx > 0:
                        chunk = self.buffer[:space_idx + 1]
                        self.buffer = self.buffer[space_idx + 1:]
                        chunks.append(chunk)
                    else:
                        break
                else:
                    break

        return chunks

    def flush(self) -> str:
        """Flush remaining buffer."""
        remaining = self.buffer
        self.buffer = ""
        return remaining


# Usage with streaming
async def stream_with_processing(messages: list):
    """Stream with sentence-level processing."""
    buffer = StreamBuffer()

    async for token in stream_chat_completion(messages):
        chunks = buffer.add(token)

        for chunk in chunks:
            # Process complete sentences
            processed = await process_sentence(chunk)
            yield processed

    # Flush remaining
    remaining = buffer.flush()
    if remaining:
        yield await process_sentence(remaining)
```

---

## 22.5 Performance Optimization

```python
class StreamingOptimizer:
    """Optimize streaming performance."""

    def __init__(self):
        self.metrics = {
            "first_token_times": [],
            "total_tokens": 0,
            "total_time": 0
        }

    async def optimized_stream(
        self,
        generator: AsyncGenerator,
        batch_yield: bool = False,
        batch_size: int = 5
    ) -> AsyncGenerator[str, None]:
        """Optimize streaming with batching option."""
        start_time = time.time()
        first_token_time = None
        token_count = 0
        batch = []

        async for token in generator:
            if first_token_time is None:
                first_token_time = time.time() - start_time
                self.metrics["first_token_times"].append(first_token_time)

            token_count += 1

            if batch_yield:
                batch.append(token)
                if len(batch) >= batch_size:
                    yield "".join(batch)
                    batch = []
            else:
                yield token

        # Yield remaining batch
        if batch:
            yield "".join(batch)

        total_time = time.time() - start_time
        self.metrics["total_tokens"] += token_count
        self.metrics["total_time"] += total_time

    def get_metrics(self) -> dict:
        """Get streaming metrics."""
        avg_first_token = (
            sum(self.metrics["first_token_times"]) /
            max(len(self.metrics["first_token_times"]), 1)
        )

        return {
            "avg_first_token_ms": avg_first_token * 1000,
            "total_tokens": self.metrics["total_tokens"],
            "total_time_seconds": self.metrics["total_time"],
            "tokens_per_second": (
                self.metrics["total_tokens"] /
                max(self.metrics["total_time"], 0.001)
            )
        }
```

---

## Hands-On Lab

### Lab 22.1: Build Streaming Chat Application

Create a real-time chat application:
1. Implement SSE endpoint in FastAPI
2. Build React frontend with streaming display
3. Add typing indicators
4. Handle errors gracefully
5. Measure streaming performance

---

## Knowledge Check

1. What are the benefits of streaming vs non-streaming responses?
2. How do you handle tool calls in streaming mode?
3. What's the difference between SSE and WebSockets for LLM streaming?
4. How do you optimize streaming for user experience?

---

<div align="center">

[← Module 21: Hybrid Architectures](../21-hybrid-architectures/README.md) | [Home](../../README.md) | [Module 23: Multimodal Agents →](../23-multimodal-agents/README.md)

</div>
