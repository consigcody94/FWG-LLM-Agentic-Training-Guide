<div align="center">

# Module 09: AI Coding Assistants

<img src="https://img.shields.io/badge/Duration-3_Hours-blue?style=for-the-badge" alt="Duration"/>
<img src="https://img.shields.io/badge/Level-Intermediate-yellow?style=for-the-badge" alt="Level"/>
<img src="https://img.shields.io/badge/Prerequisites-Module_1--5-green?style=for-the-badge" alt="Prerequisites"/>

*Mastering GitHub Copilot, Claude Code, Cursor, and other AI-powered development tools*

</div>

---

## Learning Objectives

Upon completion of this module, participants will be able to:

- [ ] Configure and use GitHub Copilot effectively
- [ ] Master Claude Code CLI for agentic development
- [ ] Leverage Cursor IDE features
- [ ] Implement security-conscious AI-assisted coding
- [ ] Establish coding assistant policies for federal teams

---

## 9.1 AI Coding Assistant Landscape

```
┌─────────────────────────────────────────────────────────────────┐
│                 AI CODING ASSISTANT ECOSYSTEM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   IDE-INTEGRATED           CLI-BASED            STANDALONE      │
│   ──────────────           ─────────            ──────────      │
│                                                                  │
│   ┌───────────┐         ┌───────────┐        ┌───────────┐     │
│   │  GitHub   │         │  Claude   │        │  ChatGPT  │     │
│   │  Copilot  │         │   Code    │        │   Code    │     │
│   │           │         │           │        │Interpreter│     │
│   └───────────┘         └───────────┘        └───────────┘     │
│                                                                  │
│   ┌───────────┐         ┌───────────┐        ┌───────────┐     │
│   │  Cursor   │         │   Aider   │        │  Replit   │     │
│   │   IDE     │         │           │        │   Agent   │     │
│   │           │         │           │        │           │     │
│   └───────────┘         └───────────┘        └───────────┘     │
│                                                                  │
│   ┌───────────┐         ┌───────────┐        ┌───────────┐     │
│   │  Codeium  │         │  Codex    │        │   Devin   │     │
│   │           │         │   CLI     │        │           │     │
│   │           │         │           │        │           │     │
│   └───────────┘         └───────────┘        └───────────┘     │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Feature Comparison

| Feature | Copilot | Claude Code | Cursor | Codeium |
|---------|---------|-------------|--------|---------|
| **Inline Completion** | ✅ | ❌ | ✅ | ✅ |
| **Chat Interface** | ✅ | ✅ | ✅ | ✅ |
| **Multi-File Editing** | Limited | ✅ | ✅ | Limited |
| **Terminal Integration** | ✅ | ✅ | ✅ | ❌ |
| **Agentic Capabilities** | Limited | ✅ | ✅ | Limited |
| **Local Model Support** | ❌ | ❌ | ✅ | ❌ |
| **Enterprise/FedRAMP** | ✅ | In Progress | ❌ | ✅ |
| **Code Privacy** | Configurable | High | Configurable | High |

---

## 9.2 GitHub Copilot

### Installation and Configuration

```bash
# VS Code Extension
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat

# JetBrains Plugin
# Install via Settings → Plugins → Marketplace
```

### VS Code Settings

```json
{
    "github.copilot.enable": {
        "*": true,
        "plaintext": false,
        "markdown": true,
        "yaml": true
    },
    "github.copilot.advanced": {
        "length": 500,
        "temperature": 0.2,
        "top_p": 1,
        "inlineSuggestCount": 3
    },
    "github.copilot.editor.enableAutoCompletions": true
}
```

### Effective Usage Patterns

```python
# Pattern 1: Descriptive function names
def calculate_federal_employee_retirement_benefits(
    years_of_service: int,
    high_3_salary: float,
    retirement_type: str
) -> float:
    # Copilot suggests implementation based on name
    pass

# Pattern 2: Docstring-first development
def process_foia_request(request_id: str) -> dict:
    """
    Process a Freedom of Information Act request.

    Steps:
    1. Validate request ID format
    2. Check for existing processing status
    3. Queue for review if new
    4. Return current status

    Args:
        request_id: FOIA request identifier (format: FOIA-YYYY-NNNNN)

    Returns:
        dict with keys: status, assigned_to, due_date, documents
    """
    # Copilot implements based on docstring
    pass

# Pattern 3: Example-driven completion
# Example input: {"name": "John", "ssn": "123-45-6789"}
# Example output: {"name": "John", "ssn": "***-**-6789"}
def mask_pii(data: dict) -> dict:
    # Copilot understands masking pattern from examples
    pass
```

### Security Considerations

```yaml
# .github/copilot-settings.yml
suggestions:
  # Block suggestions containing sensitive patterns
  block_patterns:
    - "api_key"
    - "secret"
    - "password"
    - "ssn"
    - "social_security"

  # Only suggest from approved libraries
  approved_imports:
    - "cryptography"
    - "bcrypt"
    - "hashlib"

  # Disable for sensitive files
  disabled_files:
    - "*.env*"
    - "*secrets*"
    - "*credentials*"
    - "config/production.py"
```

---

## 9.3 Claude Code CLI

### Installation

```bash
# Install Claude Code
npm install -g @anthropic-ai/claude-code

# Authenticate
claude auth login

# Verify installation
claude --version
```

### Configuration

```bash
# Initialize in project
claude init

# Configure settings
claude config set model claude-sonnet-4-20250514
claude config set max-turns 50
claude config set auto-approve-safe-commands true
```

### CLAUDE.md Project Instructions

```markdown
# CLAUDE.md

## Project Context
This is a federal agency case management system built with Python/FastAPI.
Security classification: CUI (Controlled Unclassified Information)

## Coding Standards
- Follow PEP 8 and federal secure coding guidelines
- All database queries must use parameterized statements
- Implement comprehensive audit logging
- Never log PII or sensitive data

## Architecture
- Backend: FastAPI with SQLAlchemy
- Database: PostgreSQL with row-level security
- Auth: OAuth 2.0 with PIV/CAC support
- Deployment: AWS GovCloud

## Testing Requirements
- Minimum 80% code coverage
- All security controls must have unit tests
- Integration tests for all API endpoints

## Off-Limits
- Do not modify authentication/authorization code without review
- Do not change database schema without migration plan
- Never commit secrets or credentials
```

### Effective Commands

```bash
# Start interactive session
claude

# Ask specific questions
claude "How should I implement RBAC for this FastAPI app?"

# Generate code
claude "Create a SQLAlchemy model for audit logs with:
  - timestamp
  - user_id
  - action_type
  - resource_type
  - resource_id
  - ip_address
  - user_agent
  - before/after state (JSON)"

# Review code
claude "Review src/auth/permissions.py for security issues"

# Refactor
claude "Refactor this function to handle errors properly" < src/api/users.py

# Run with specific context
claude --context "FISMA compliance" "Audit this endpoint for security"
```

### MCP Integration

```json
// .claude/mcp.json
{
  "servers": {
    "federal-docs": {
      "command": "npx",
      "args": ["-y", "@federal/mcp-regulations"],
      "env": {
        "REGULATIONS_API_KEY": "${REGULATIONS_API_KEY}"
      }
    },
    "security-scanner": {
      "command": "python",
      "args": ["-m", "security_mcp_server"],
      "cwd": "./tools"
    }
  }
}
```

---

## 9.4 Cursor IDE

### Installation and Setup

```bash
# Download from cursor.sh
# Or using brew
brew install --cask cursor
```

### Key Features

```
┌─────────────────────────────────────────────────────────────────┐
│                      CURSOR IDE FEATURES                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   CMD+K Edit    │  │   CMD+L Chat    │  │  Composer Mode  │ │
│  │                 │  │                 │  │                 │ │
│  │  Inline code    │  │  Context-aware  │  │  Multi-file     │ │
│  │  generation     │  │  conversation   │  │  editing        │ │
│  │  and editing    │  │  with codebase  │  │  with agent     │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                  │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │  @ References   │  │   .cursorrules  │  │ Privacy Mode    │ │
│  │                 │  │                 │  │                 │ │
│  │  @file @folder  │  │  Project-level  │  │  Code never     │ │
│  │  @docs @web     │  │  AI behavior    │  │  leaves machine │ │
│  │  @codebase      │  │  customization  │  │  (local models) │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Cursor Rules File

```markdown
# .cursorrules

## Project Overview
Federal workforce management system - handle all code as CUI

## Code Style
- Python 3.11+ with type hints on all functions
- Use dataclasses or Pydantic for data structures
- Async/await for all I/O operations
- Comprehensive error handling with custom exceptions

## Security Requirements
- Never hardcode credentials or secrets
- Use parameterized queries exclusively
- Implement input validation on all endpoints
- Add audit logging for all data modifications

## Architecture Patterns
- Repository pattern for data access
- Service layer for business logic
- Dependency injection for testability
- Event sourcing for sensitive operations

## Testing
- pytest with async support
- Mock external services
- Test edge cases and error paths
- Security-focused test cases

## Documentation
- Docstrings for all public functions
- OpenAPI annotations for endpoints
- Architecture decision records for significant changes

## Prohibited
- No print statements (use logging)
- No global mutable state
- No direct database connections (use connection pool)
- No storing PII in logs
```

### Context References

```
# In Cursor chat, use @ to reference context:

@file:src/auth/oauth.py - Reference specific file
@folder:src/api - Reference entire folder
@docs - Search indexed documentation
@web - Search web for current info
@codebase - Search entire codebase
@git - Reference git history

# Example prompts:
"@file:models/user.py Add field validation for email"
"@codebase Find all places where we query users"
"@docs How does FastAPI handle authentication?"
```

---

## 9.5 Security-Conscious AI Coding

### Code Review Checklist

```markdown
## AI-Generated Code Review Checklist

### Input Validation
- [ ] All user inputs validated
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] Path traversal prevention

### Authentication/Authorization
- [ ] Proper authentication checks
- [ ] Authorization verified for each operation
- [ ] Session management secure
- [ ] No hardcoded credentials

### Data Protection
- [ ] PII properly handled
- [ ] Encryption used appropriately
- [ ] Secure key management
- [ ] Audit logging implemented

### Error Handling
- [ ] No sensitive data in error messages
- [ ] Proper exception handling
- [ ] Graceful degradation
- [ ] Error logging (without secrets)

### Dependencies
- [ ] No vulnerable packages introduced
- [ ] Packages from trusted sources
- [ ] Minimal necessary permissions
```

### Safe Patterns

```python
# SAFE: Parameterized query
async def get_user(db: AsyncSession, user_id: str) -> User:
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    return result.scalar_one_or_none()

# UNSAFE: String interpolation (AI might suggest this!)
# cursor.execute(f"SELECT * FROM users WHERE id = '{user_id}'")

# SAFE: Input validation
from pydantic import BaseModel, Field, validator
import re

class UserCreate(BaseModel):
    email: str = Field(..., max_length=254)
    name: str = Field(..., min_length=1, max_length=100)

    @validator('email')
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise ValueError('Invalid email format')
        return v.lower()

# SAFE: Secure password handling
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)
```

---

## 9.6 Federal Team Policies

### Acceptable Use Policy Template

```markdown
# AI Coding Assistant Acceptable Use Policy

## Approved Tools
- GitHub Copilot Enterprise (with telemetry disabled)
- Claude Code (with approved configuration)

## Prohibited Uses
1. Processing classified information
2. Generating code for weapons systems
3. Bypassing security controls
4. Creating malicious code

## Required Practices
1. Review all AI-generated code before commit
2. Run security scans on AI-generated code
3. Document AI assistance in commit messages
4. Report suspicious AI suggestions

## Data Handling
1. Never paste sensitive data into AI prompts
2. Use sanitized/synthetic data for examples
3. Disable telemetry and code sharing
4. Use air-gapped solutions for sensitive projects

## Code Review Requirements
1. AI-generated code requires peer review
2. Security-critical code requires security review
3. Infrastructure code requires DevSecOps review
```

### Git Hooks for AI Code

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Check for AI-generated code markers
if git diff --cached | grep -q "AI-GENERATED"; then
    echo "⚠️  AI-generated code detected"
    echo "Ensure code has been reviewed per policy"

    # Check for required reviewer comment
    if ! git diff --cached | grep -q "Reviewed-By:"; then
        echo "❌ Missing Reviewed-By annotation"
        exit 1
    fi
fi

# Run security scanner on changed files
changed_files=$(git diff --cached --name-only --diff-filter=ACM | grep "\.py$")
if [ -n "$changed_files" ]; then
    echo "Running security scan..."
    bandit -r $changed_files
    if [ $? -ne 0 ]; then
        echo "❌ Security issues found"
        exit 1
    fi
fi
```

---

## 9.7 Productivity Patterns

### Effective Prompting for Code Generation

```python
# Pattern 1: Specification-First
"""
Create a FastAPI endpoint that:
- Path: POST /api/v1/documents
- Accepts: multipart file upload
- Validates: file size < 10MB, allowed types [pdf, docx]
- Stores: S3 with encryption
- Returns: document ID, upload timestamp
- Audit logs: user, action, document_id, timestamp
- Error handling: proper HTTP status codes
"""

# Pattern 2: Test-First
"""
Write a function that passes these tests:

def test_mask_ssn():
    assert mask_ssn("123-45-6789") == "***-**-6789"
    assert mask_ssn("123456789") == "*****6789"
    assert mask_ssn(None) == None
    assert mask_ssn("invalid") == "invalid"
"""

# Pattern 3: Interface-First
"""
Implement this interface:

class DocumentRepository(Protocol):
    async def create(self, doc: Document) -> str: ...
    async def get(self, doc_id: str) -> Optional[Document]: ...
    async def update(self, doc_id: str, doc: Document) -> bool: ...
    async def delete(self, doc_id: str) -> bool: ...
    async def list(self, filters: Dict) -> List[Document]: ...

Use SQLAlchemy async with PostgreSQL.
"""
```

---

## Hands-On Lab

### Lab 9.1: Configure Secure AI Coding Environment

Set up a security-compliant AI coding environment:
1. Configure GitHub Copilot with privacy settings
2. Set up Claude Code with MCP servers
3. Create project-specific rules files
4. Implement pre-commit security hooks

**Deliverables:**
- Configuration files for all tools
- Security scanning pipeline
- Team usage policy document

---

## Knowledge Check

1. What configuration options help protect sensitive code in GitHub Copilot?
2. How does Claude Code's CLAUDE.md file influence AI behavior?
3. What security checks should be performed on AI-generated code?
4. How should AI-assisted code be documented in federal projects?

---

<div align="center">

[← Module 08: Agent Frameworks](../08-agent-frameworks/README.md) | [Home](../../README.md) | [Module 10: RAG Systems →](../10-rag-systems/README.md)

</div>
