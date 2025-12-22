# Troubleshooting Guide

<div align="center">

**Common Issues and Solutions for AI Development**

</div>

---

## Quick Diagnostic Commands

```bash
# Check Python environment
python --version
which python
pip list | grep -E "(openai|anthropic|langchain|ollama)"

# Check Node.js
node --version
npm list -g | grep -E "(mcp|claude)"

# Check Ollama
ollama list
curl http://localhost:11434/api/tags

# Check API connectivity
curl -s https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | head -20
```

---

## API Issues

### Error: 401 Unauthorized

**Symptoms:**
```
Error: Unauthorized
Status: 401
```

**Solutions:**

```bash
# 1. Check if API key is set
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# 2. Verify key format
# OpenAI: sk-... (51 chars)
# Anthropic: sk-ant-... (108 chars)

# 3. Check .env file
cat .env | grep API_KEY

# 4. Reload environment
source .env  # or restart terminal

# 5. Test key directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer YOUR_KEY_HERE"
```

**Python fix:**
```python
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Verify key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found in environment")
```

---

### Error: 429 Rate Limit Exceeded

**Symptoms:**
```
Error: Rate limit exceeded
Status: 429
Retry-After: 60
```

**Solutions:**

```python
import time
from openai import OpenAI, RateLimitError

client = OpenAI()

def query_with_retry(prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError as e:
            wait_time = 2 ** attempt  # Exponential backoff
            print(f"Rate limited. Waiting {wait_time}s...")
            time.sleep(wait_time)
    raise Exception("Max retries exceeded")
```

**Prevention:**
- Implement request queuing
- Use batch API for bulk operations
- Upgrade API tier if needed
- Cache repeated queries

---

### Error: 500/503 Server Error

**Symptoms:**
```
Error: Internal Server Error
Status: 500 or 503
```

**Solutions:**

```python
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def resilient_query(prompt):
    response = client.chat.completions.create(...)
    return response
```

**Check provider status:**
- OpenAI: https://status.openai.com
- Anthropic: https://status.anthropic.com
- Google: https://status.cloud.google.com

---

### Error: Context Length Exceeded

**Symptoms:**
```
Error: maximum context length exceeded
```

**Solutions:**

```python
import tiktoken

def count_tokens(text, model="gpt-4o"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def truncate_to_fit(text, max_tokens=100000):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    tokens = encoding.encode(text)
    if len(tokens) > max_tokens:
        tokens = tokens[:max_tokens]
        text = encoding.decode(tokens)
    return text

# Before sending
tokens = count_tokens(my_prompt)
if tokens > 128000:  # GPT-4o limit
    my_prompt = truncate_to_fit(my_prompt, 100000)
```

---

## Ollama Issues

### Error: Connection Refused

**Symptoms:**
```
httpx.ConnectError: [Errno 111] Connection refused
Error: Failed to connect to localhost:11434
```

**Solutions:**

```bash
# 1. Check if Ollama is running
pgrep ollama

# 2. Start Ollama
ollama serve

# 3. Check port availability
lsof -i :11434

# 4. If port is in use, kill process
kill $(lsof -t -i :11434)

# 5. Restart Ollama
systemctl restart ollama  # Linux with systemd
```

---

### Error: Model Not Found

**Symptoms:**
```
Error: model 'llama3.2' not found
```

**Solutions:**

```bash
# 1. List available models
ollama list

# 2. Pull the model
ollama pull llama3.2

# 3. Check model name (case-sensitive)
ollama show llama3.2

# 4. Use correct format
ollama pull llama3.2:latest
ollama pull llama3.2:7b-instruct-q4_K_M
```

---

### Error: Out of Memory (GPU/RAM)

**Symptoms:**
```
Error: CUDA out of memory
Error: Failed to allocate memory
```

**Solutions:**

```bash
# 1. Check GPU memory
nvidia-smi

# 2. Use smaller model variant
ollama pull llama3.2:3b  # Instead of 8B

# 3. Use quantized model
ollama pull llama3.2:7b-q4_K_M  # 4-bit quantization

# 4. Set memory limits
OLLAMA_MAX_LOADED_MODELS=1 ollama serve

# 5. Offload to CPU (slower)
OLLAMA_NUM_GPU=0 ollama run llama3.2
```

---

## Python Environment Issues

### Error: ModuleNotFoundError

**Symptoms:**
```
ModuleNotFoundError: No module named 'openai'
```

**Solutions:**

```bash
# 1. Check you're in virtual environment
which python
# Should show: /path/to/venv/bin/python

# 2. Activate virtual environment
source .venv/bin/activate

# 3. Install missing package
pip install openai

# 4. Install all requirements
pip install -r requirements.txt

# 5. Verify installation
pip show openai
```

---

### Error: ImportError Version Mismatch

**Symptoms:**
```
ImportError: cannot import name 'X' from 'package'
```

**Solutions:**

```bash
# 1. Check installed version
pip show openai

# 2. Upgrade to latest
pip install --upgrade openai

# 3. Install specific version
pip install openai==1.12.0

# 4. Check compatibility
pip check
```

---

### Error: SSL Certificate

**Symptoms:**
```
ssl.SSLCertVerificationError: certificate verify failed
```

**Solutions:**

```bash
# 1. Update certifi
pip install --upgrade certifi

# 2. Check certificate path
python -c "import certifi; print(certifi.where())"

# 3. Use system certificates (if corporate proxy)
export REQUESTS_CA_BUNDLE=/path/to/corporate/ca-bundle.crt

# 4. For development only (NOT production)
export PYTHONHTTPSVERIFY=0  # INSECURE - dev only!
```

---

## MCP Issues

### Error: MCP Server Won't Start

**Symptoms:**
```
Error: Failed to start MCP server
Error: ENOENT: no such file or directory
```

**Solutions:**

```bash
# 1. Check server file exists
ls -la src/server.py

# 2. Check Python path
which python
python -c "import mcp"

# 3. Check syntax errors
python -m py_compile src/server.py

# 4. Run with verbose output
python -m src.server 2>&1 | head -50

# 5. Check MCP Inspector logs
mcp-inspector --debug
```

---

### Error: MCP Client Can't Connect

**Solutions:**

```bash
# 1. Check Claude Desktop config location
# macOS/Linux:
cat ~/.config/claude/claude_desktop_config.json

# Windows:
cat %APPDATA%\Claude\claude_desktop_config.json

# 2. Validate JSON
python -m json.tool ~/.config/claude/claude_desktop_config.json

# 3. Check paths are absolute
# ✗ "cwd": "./my-server"
# ✓ "cwd": "/Users/name/my-server"

# 4. Restart Claude Desktop completely
```

---

## LangChain Issues

### Error: Chain Not Returning Expected Output

**Solutions:**

```python
# 1. Enable verbose mode
from langchain.globals import set_verbose
set_verbose(True)

# 2. Use callbacks for debugging
from langchain.callbacks import StdOutCallbackHandler

chain.invoke(
    {"input": "test"},
    config={"callbacks": [StdOutCallbackHandler()]}
)

# 3. Check prompt template
print(chain.get_prompts())

# 4. Trace with LangSmith
import langchain
langchain.debug = True
```

---

### Error: Memory Not Persisting

**Solutions:**

```python
# 1. Ensure same memory instance
memory = ConversationBufferMemory()

chain1 = LLMChain(..., memory=memory)
chain2 = LLMChain(..., memory=memory)  # Same instance!

# 2. Check memory contents
print(memory.chat_memory.messages)

# 3. For persistence across runs
from langchain.memory import FileChatMessageHistory

history = FileChatMessageHistory("chat_history.json")
memory = ConversationBufferMemory(chat_memory=history)
```

---

## RAG Issues

### Error: ChromaDB Collection Empty

**Solutions:**

```python
# 1. Check collection exists
print(collection.count())

# 2. Verify embeddings were added
collection.peek()

# 3. Check for silent failures
try:
    collection.add(...)
except Exception as e:
    print(f"Add failed: {e}")

# 4. Clear and rebuild
client.delete_collection("my_collection")
collection = client.create_collection("my_collection")
```

---

### Error: Poor Retrieval Quality

**Solutions:**

```python
# 1. Check chunk size (smaller often better)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,  # Try smaller
    chunk_overlap=50
)

# 2. Try different embedding models
from sentence_transformers import SentenceTransformer

# Default (fast, less accurate)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Better quality (slower)
model = SentenceTransformer('all-mpnet-base-v2')

# 3. Increase results and rerank
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=20  # Get more, filter later
)

# 4. Use hybrid search
# Combine semantic search with BM25 keyword search
```

---

## Performance Issues

### Slow Response Times

```python
# 1. Use streaming
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")

# 2. Reduce max_tokens
response = client.chat.completions.create(
    max_tokens=500  # Limit output length
)

# 3. Use faster models
# gpt-4o-mini instead of gpt-4o
# claude-3-haiku instead of sonnet

# 4. Implement caching
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_query(prompt_hash):
    return api.query(prompt)
```

---

### High Token Usage

```python
# 1. Monitor usage
response = client.chat.completions.create(...)
print(f"Tokens used: {response.usage.total_tokens}")

# 2. Compress prompts
prompt = prompt.replace("  ", " ").strip()

# 3. Use system prompts wisely
# Put stable content in system prompt (cached)
# Put variable content in user prompt

# 4. Summarize conversation history
if len(messages) > 10:
    summary = summarize(messages[:-3])
    messages = [{"role": "system", "content": summary}] + messages[-3:]
```

---

## Debug Checklist

```
□ Environment
  □ Correct Python version?
  □ Virtual environment active?
  □ Dependencies installed?

□ API
  □ API key set correctly?
  □ Key has sufficient credits?
  □ Using correct endpoint?

□ Local Models
  □ Ollama running?
  □ Model downloaded?
  □ Sufficient resources?

□ Code
  □ No syntax errors?
  □ Correct parameter names?
  □ Proper error handling?

□ Network
  □ Internet connected?
  □ Firewall/proxy issues?
  □ SSL certificates valid?
```

---

## Getting Help

### Before Asking for Help

1. Read the error message completely
2. Check this troubleshooting guide
3. Search provider documentation
4. Search GitHub issues
5. Create minimal reproducible example

### Information to Include

```markdown
**Environment:**
- OS: [e.g., macOS 14.0]
- Python: [e.g., 3.11.7]
- Package versions: [pip list output]

**Error:**
```
[Full error message]
```

**Code:**
```python
[Minimal code that reproduces issue]
```

**Expected vs Actual:**
- Expected: [what should happen]
- Actual: [what actually happened]

**Already Tried:**
- [Solution 1]
- [Solution 2]
```

---

<div align="center">

**When in doubt, restart everything and try again.**

</div>
