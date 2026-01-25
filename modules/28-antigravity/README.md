# Module 28: Google Antigravity IDE

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   MODULE 28: GOOGLE ANTIGRAVITY IDE                                          ║
║                                                                              ║
║   Google's agent-first development platform for autonomous AI-driven         ║
║   software development. Learn to orchestrate AI agents that plan,           ║
║   execute, and verify complex engineering tasks.                            ║
║                                                                              ║
║   Duration: 4 hours                                                          ║
║   Prerequisites: Module 12 (Multi-Agent Systems)                            ║
║   Difficulty: Intermediate                                                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

## Table of Contents

1. [Overview](#overview)
2. [Learning Objectives](#learning-objectives)
3. [28.1 Introduction to Antigravity](#281-introduction-to-antigravity)
4. [28.2 Installation & Setup](#282-installation--setup)
5. [28.3 Core Interface](#283-core-interface)
6. [28.4 The Artifacts System](#284-the-artifacts-system)
7. [28.5 Security & Autonomy Policies](#285-security--autonomy-policies)
8. [28.6 Rules, Workflows & Skills](#286-rules-workflows--skills)
9. [28.7 Supported Models](#287-supported-models)
10. [28.8 Practical Workflows](#288-practical-workflows)
11. [28.9 Browser Integration](#289-browser-integration)
12. [28.10 Best Practices](#2810-best-practices)
13. [Hands-On Labs](#hands-on-labs)
14. [Summary](#summary)
15. [References](#references)

---

## Overview

Google Antigravity is Google's agentic development platform, announced in November 2025 alongside Gemini 3. Unlike traditional IDEs with AI assistance bolted on, Antigravity is built from the ground up as an **agent-first platform** where autonomous AI agents plan, execute, and iterate on engineering tasks with minimal human oversight.

### Why Antigravity Matters

Traditional AI coding assistants operate in a synchronous, human-driven workflow: you write code, the AI suggests completions. Antigravity inverts this model:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                  TRADITIONAL IDE VS ANTIGRAVITY                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   TRADITIONAL AI IDE                    GOOGLE ANTIGRAVITY                  │
│   ══════════════════                    ══════════════════                  │
│                                                                             │
│   Human drives workflow                 Agent drives workflow               │
│         │                                     │                             │
│         ▼                                     ▼                             │
│   ┌───────────┐                         ┌───────────┐                       │
│   │  Human    │───write──▶ code         │   Human   │───describe──▶ task   │
│   │  writes   │                         │  reviews  │                       │
│   └───────────┘                         └───────────┘                       │
│         │                                     │                             │
│         ▼                                     ▼                             │
│   ┌───────────┐                         ┌───────────┐                       │
│   │    AI     │───suggests──▶ completion│   Agent   │───produces──▶ artifacts│
│   │  assists  │                         │ executes  │                       │
│   └───────────┘                         └───────────┘                       │
│         │                                     │                             │
│         ▼                                     ▼                             │
│   Human accepts/rejects                 Human reviews/comments              │
│                                         Agent iterates autonomously         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Module Architecture

```
modules/28-antigravity/
├── README.md                      # This file
├── labs/
│   ├── lab-01-getting-started.md  # Installation and basic usage
│   ├── lab-02-building-with-agents.md  # Complete application workflow
│   └── lab-03-customization.md    # Rules, workflows, skills
├── examples/
│   ├── rules/                     # Sample GEMINI.md configurations
│   ├── workflows/                 # Reusable workflow templates
│   └── skills/                    # Skill packages
```

---

## Learning Objectives

By the end of this module, participants will be able to:

| # | Objective | Assessment Method |
|---|-----------|-------------------|
| 1 | **Install and configure** Google Antigravity with appropriate security policies | Lab 1 |
| 2 | **Navigate both interfaces** (Editor View and Manager View) effectively | Practical exercise |
| 3 | **Work with artifacts** to review, comment on, and iterate with agents | Lab 2 |
| 4 | **Configure security policies** appropriate for different risk environments | Configuration review |
| 5 | **Create rules, workflows, and skills** to customize agent behavior | Lab 3 |
| 6 | **Orchestrate multiple agents** working in parallel on complex tasks | Lab 2 |

---

## 28.1 Introduction to Antigravity

### What is Google Antigravity?

Google Antigravity represents a paradigm shift in development environments. Rather than functioning as a conventional code editor with AI chat assistance, it operates as an agent-first platform where autonomous AI agents:

- **Plan** complex tasks by creating implementation strategies
- **Execute** code changes across editor, terminal, and browser
- **Verify** their own work through testing and screenshots
- **Iterate** based on feedback without stopping execution

### Platform Origins

Antigravity is a heavily modified fork of Visual Studio Code. Google acquired **Windsurf** (an AI-oriented code editor) and its team for $2.4 billion to lead development of the platform.

### Key Differentiators

| Feature | Traditional AI IDE | Google Antigravity |
|---------|-------------------|-------------------|
| **Workflow** | Human drives, AI assists | Agent drives, human reviews |
| **Execution** | Synchronous, step-by-step | Asynchronous, parallel agents |
| **Output** | Code suggestions | Verified artifacts |
| **Context** | Single conversation | Persistent knowledge base |
| **Scope** | Code editing | Editor + Terminal + Browser |
| **Verification** | Manual testing | Agent-generated screenshots, recordings |

### Two Primary Interfaces

Antigravity combines two distinct interfaces:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GOOGLE ANTIGRAVITY                                   │
├─────────────────────────────────┬───────────────────────────────────────────┤
│          EDITOR VIEW            │              MANAGER VIEW                  │
│                                 │                                           │
│  • VS Code-familiar IDE         │  • Agent orchestration dashboard          │
│  • Tab completions              │  • Multiple agents in parallel            │
│  • Inline commands (Cmd+I)      │  • Asynchronous task execution            │
│  • Synchronous workflow         │  • Cross-workspace management             │
│  • Agent sidebar (Cmd+L)        │  • Inbox for all conversations            │
│                                 │                                           │
│  Best for: Focused coding,      │  Best for: Complex features,              │
│  quick edits, synchronous work  │  parallel tasks, delegation               │
│                                 │                                           │
└─────────────────────────────────┴───────────────────────────────────────────┘
```

---

## 28.2 Installation & Setup

### System Requirements

- **Operating Systems**: macOS, Windows, or supported Linux distributions
- **Browser**: Chrome (required for browser agent features)
- **Account**: Personal Gmail account (currently in preview)
- **Cost**: Free during public preview with generous rate limits

### Installation Steps

**Step 1: Download**
```
Visit: https://antigravity.google/download
Select your operating system (macOS, Windows, or Linux)
```

**Step 2: Run Setup Flow**

The installer guides you through:
1. Import existing VS Code/Cursor settings OR start fresh
2. Select theme (dark or light mode)
3. **Configure agent autonomy levels** (critical step - see below)

**Step 3: Verify Installation**
```bash
# Launch from terminal
antigravity --version

# Open a project
antigravity /path/to/your/project
```

### Initial Autonomy Configuration

During first launch, you must configure security policies across three dimensions:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    AUTONOMY CONFIGURATION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  TERMINAL EXECUTION                                                         │
│  ══════════════════                                                         │
│  Controls whether agents auto-execute shell commands                        │
│  Options: [Auto-execute] [Request approval]                                 │
│                                                                             │
│  REVIEW POLICY                                                              │
│  ═════════════                                                              │
│  Determines artifact review requirements before proceeding                  │
│  Options: [Always review] [Sometimes review] [Never review]                 │
│                                                                             │
│  JAVASCRIPT EXECUTION                                                       │
│  ════════════════════                                                       │
│  Governs browser automation capabilities                                    │
│  Options: [Always Proceed] [Request review] [Disabled]                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Preset Configurations

| Preset | Description | Recommended For |
|--------|-------------|-----------------|
| **Secure Mode** | Enhanced restrictions on external resources | Production systems, sensitive data |
| **Review-driven** | Balanced with frequent user checkpoints | **Most users (recommended)** |
| **Agent-driven** | Minimal interruptions, maximum autonomy | Experienced users, trusted environments |
| **Custom** | Full control over each policy | Advanced users |

> **Recommendation**: Start with **Review-driven development** until you're comfortable with agent behavior.

---

## 28.3 Core Interface

### Editor View

The Editor View retains VS Code familiarity while adding agent capabilities:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  File  Edit  View  Agent  Help                                              │
├──────────────┬──────────────────────────────────────┬───────────────────────┤
│              │                                      │                       │
│  EXPLORER    │       CODE EDITOR                    │    AGENT PANEL        │
│              │                                      │                       │
│  📁 src      │  1  def process_data():              │  ┌─────────────────┐  │
│  📁 tests    │  2      """Process the input"""     │  │  Gemini 3 Pro   │  │
│  📄 main.py  │  3      data = load_data()          │  └─────────────────┘  │
│  📄 utils.py │  4      validated = validate(data)  │                       │
│              │  5      return transform(validated) │  Ask anything...      │
│              │  6                                   │                       │
│              │                                      │  ─────────────────    │
│              │  # Cmd+I for inline edits           │  Recent:              │
│              │  # Cmd+L to toggle this panel       │  • Add error handling │
│              │                                      │  • Write unit tests   │
│              │                                      │                       │
├──────────────┴──────────────────────────────────────┴───────────────────────┤
│  TERMINAL                                                                    │
│  $ python main.py                                                           │
│  Processing complete. 247 records transformed.                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Essential Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Cmd + I` | Trigger inline natural language commands |
| `Cmd + L` | Toggle agent side panel |
| `Cmd + `` ` | Open/close terminal |
| `Cmd + E` | Switch between Editor and Manager views |
| `Cmd + Shift + P` | Command palette |

### Manager View (Mission Control)

The Manager View is where Antigravity differentiates itself—a dashboard for orchestrating multiple autonomous agents simultaneously:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           AGENT MANAGER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  INBOX                               ACTIVE AGENTS                          │
│  ─────                               ─────────────                          │
│  ✓ Build authentication system       [Agent 1] Building auth module         │
│  ✓ Fix payment processing bug         └─ Status: Writing tests...          │
│  ● Add dashboard visualizations                                             │
│  ○ Refactor API layer                [Agent 2] Creating dashboard           │
│  ○ Update documentation               └─ Status: Generating charts...       │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  NEW TASK                                                            │   │
│  │                                                                      │   │
│  │  Mode: [Planning ▼]        Model: [Gemini 3 Pro ▼]                  │   │
│  │                                                                      │   │
│  │  Describe your task...                                               │   │
│  │  ________________________________________________________________   │   │
│  │                                                                      │   │
│  │                                                   [Start Agent]     │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Manager View Features

| Feature | Description |
|---------|-------------|
| **Inbox** | Centralized conversation history, revisit previous tasks, monitor status |
| **Workspace Management** | Work across multiple project folders with persistent context |
| **Model Selection** | Choose AI model for each agent instance |
| **Planning Modes** | "Planning" for detailed task lists, "Fast" for simple tasks |

---

## 28.4 The Artifacts System

### What Are Artifacts?

Rather than displaying raw tool calls or streaming code, Antigravity agents produce structured, verifiable deliverables called **Artifacts**. This builds trust by making agent work transparent and reviewable.

### Artifact Types

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           ARTIFACT TYPES                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📋 TASK LISTS              Concrete execution steps before coding begins   │
│                                                                             │
│  📐 IMPLEMENTATION PLANS    Technical architecture for proposed changes     │
│                                                                             │
│  📝 CODE DIFFS              Side-by-side change visualization               │
│                                                                             │
│  📸 SCREENSHOTS             UI state before/after modifications             │
│                                                                             │
│  🎥 BROWSER RECORDINGS      Video documentation of dynamic interactions     │
│                                                                             │
│  📖 WALKTHROUGHS            Post-completion summaries with verification     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Providing Feedback on Artifacts

Users interact with artifacts using **Google Docs-style comments**:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION PLAN                                                [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  1. Create User model with fields:                                          │
│     - id, email, password_hash, created_at        ◄─── [💬 Comment]        │
│                                                        "Add a 'role'       │
│  2. Implement authentication endpoints:                 field for RBAC"    │
│     - POST /auth/register                                                   │
│     - POST /auth/login                                                      │
│     - POST /auth/logout                                                     │
│                                                                             │
│  3. Add JWT token generation and validation                                 │
│                                                                             │
│  4. Create authentication middleware              ◄─── [💬 Comment]        │
│                                                        "Also add rate      │
│  5. Write comprehensive tests                           limiting here"     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key Point**: The agent incorporates your feedback **without stopping its execution flow**. You can comment asynchronously while the agent continues working.

### Artifact Workflow

```
User Request
     │
     ▼
┌─────────────┐
│ Task List   │◄──── Review & Comment
└─────────────┘
     │
     ▼
┌─────────────┐
│ Impl. Plan  │◄──── Review & Comment
└─────────────┘
     │
     ▼
┌─────────────┐
│ Code Diffs  │◄──── Accept / Reject / Comment
└─────────────┘
     │
     ▼
┌─────────────┐
│ Screenshots │◄──── Verify UI
└─────────────┘
     │
     ▼
┌─────────────┐
│ Walkthrough │◄──── Final Review
└─────────────┘
```

### Undoing Changes

At any point during the workflow:

```
┌─────────────────────────────────────────────────────┐
│  [↩ Undo changes up to this point]                  │
└─────────────────────────────────────────────────────┘
```

This restarts from a previous checkpoint.

---

## 28.5 Security & Autonomy Policies

### Terminal Command Control

Three policy modes manage shell execution:

| Mode | Behavior | Risk Level |
|------|----------|------------|
| **Off** | Explicit allowlisting; everything blocked except specified commands | Lowest |
| **Auto** | Agent decides; requests approval for suspicious operations | Medium |
| **Turbo** | Implicit allowing; explicit denylisting blocks dangerous commands | Highest |

**Example Allowlist** (`~/.gemini/antigravity/terminalAllowlist.txt`):
```bash
# Safe commands - always allowed
npm install
npm run build
npm run test
python -m pytest
git status
git diff
git add
git commit
```

**Example Denylist** (`~/.gemini/antigravity/terminalDenylist.txt`):
```bash
# Dangerous commands - always blocked
rm -rf /
rm -rf ~
sudo rm -rf
chmod 777 /
:(){ :|:& };:
```

### Browser URL Allowlist

Restrict agent web access to trusted domains to mitigate prompt injection attacks:

**Configuration** (`~/.gemini/antigravity/browserAllowlist.txt`):
```
# Trusted documentation sites
docs.python.org
developer.mozilla.org
react.dev
stackoverflow.com
github.com

# Your internal documentation
docs.yourcompany.com
wiki.internal.com
```

### JavaScript Execution Policy

| Setting | Behavior | Use Case |
|---------|----------|----------|
| **Always Proceed** | Maximum autonomy, executes JS without approval | Trusted environments only |
| **Request Review** | Each browser action needs approval | **Recommended** |
| **Disabled** | No browser automation allowed | High-security environments |

---

## 28.6 Rules, Workflows & Skills

### Rules

Rules are **system-level guidelines** governing agent behavior persistently across all tasks.

**Storage Locations:**
- Global: `~/.gemini/GEMINI.md`
- Workspace: `your-workspace/.agent/rules/`

**Example `GEMINI.md`:**
```markdown
# Agent Rules

## Code Style
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Always include type hints in Python functions
- Use descriptive variable names (no single letters except loop counters)

## Documentation
- All public functions require docstrings
- Use Google-style docstring format
- Include usage examples for complex functions

## Testing
- Write unit tests for all new functions
- Maintain >80% code coverage
- Use pytest as the test framework
- Include edge case tests

## Security
- Never hardcode credentials or API keys
- Use environment variables for all secrets
- Validate and sanitize all user inputs
- Log security-relevant events
```

### Workflows

Workflows are **user-triggered saved prompts** invoked with `/` prefix. They're applied on-demand rather than continuously.

**Storage Locations:**
- Global: `~/.gemini/antigravity/global_workflows/`
- Workspace: `your-workspace/.agent/workflows/`

**Example Workflow** (`generate-tests.md`):
```markdown
---
name: generate-tests
description: Generate comprehensive unit tests for selected code
trigger: /generate-tests
---

# Generate Unit Tests

Analyze the selected code and generate comprehensive unit tests:

1. Identify all public functions and methods
2. For each function, create tests for:
   - Happy path scenarios
   - Edge cases (empty inputs, null values, boundaries)
   - Error conditions and exceptions
3. Use pytest framework with fixtures where appropriate
4. Include docstrings explaining each test's purpose
5. Aim for >90% code coverage
6. Mock external dependencies appropriately
```

**Usage:**
```
> /generate-tests
```

### Skills

Skills are **specialized knowledge packages** loaded only when contextually relevant. This prevents "tool bloat" and reduces latency.

**Skill Structure:**
```
skills/
└── code-review/
    ├── SKILL.md           # Required: metadata + instructions
    ├── scripts/           # Optional: automation scripts
    ├── references/        # Optional: reference documents
    └── assets/            # Optional: templates, examples
```

**Example `SKILL.md`:**
```markdown
---
name: code-review
description: Comprehensive code review checklist and guidelines
triggers:
  - review
  - code review
  - PR review
---

# Code Review Skill

When performing code reviews, systematically check:

## Correctness
- [ ] Logic is correct and handles all expected cases
- [ ] No off-by-one errors in loops or array access
- [ ] Proper null/undefined handling

## Edge Cases
- [ ] Empty inputs handled gracefully
- [ ] Boundary conditions tested
- [ ] Concurrent access considered (if applicable)

## Style
- [ ] Follows project conventions
- [ ] Meaningful, descriptive names
- [ ] No magic numbers (use named constants)

## Performance
- [ ] No unnecessary loops or iterations
- [ ] Efficient data structures used
- [ ] No memory leaks (cleanup handled)

## Security
- [ ] Input validation present
- [ ] No injection vulnerabilities (SQL, XSS, command)
- [ ] Secrets not exposed in code or logs
```

**Skill Scopes:**
- Global: `~/.gemini/antigravity/skills/` — Available in all projects
- Workspace: `.agent/skills/` — Available only in that project

---

## 28.7 Supported Models

Google Antigravity supports multiple AI models from different providers:

| Model | Provider | Best For |
|-------|----------|----------|
| **Gemini 3 Pro** | Google | Complex reasoning, planning (default) |
| **Gemini 3 Deep Think** | Google | Deep analysis, research tasks |
| **Gemini 3 Flash** | Google | Fast, simple tasks |
| **Claude Sonnet 4.5** | Anthropic | Detailed coding, thorough explanations |
| **Claude Opus 4.5** | Anthropic | Complex multi-step tasks |
| **GPT-OSS-120B** | OpenAI (OSS) | General purpose |

### Benchmark Performance

| Benchmark | Gemini 3 Pro | Claude Sonnet 4.5 | GPT-5.1 |
|-----------|--------------|-------------------|---------|
| **SWE-bench Verified** | 76.2% | 77.2% | 73.1% |
| **Terminal-Bench 2.0** | 54.2% | 51.8% | 47.6% |

*SWE-bench measures whether an AI can resolve real GitHub issues in production codebases.*

### Selecting Models

In Manager View, select the model before starting a task:

```
┌─────────────────────────────────────────────────────┐
│  Model: [Gemini 3 Pro                         ▼]   │
│         ───────────────────────────────────────    │
│         Gemini 3 Pro      (default)                │
│         Gemini 3 Flash    (fast)                   │
│         Gemini 3 Deep Think (research)             │
│         Claude Sonnet 4.5                          │
│         Claude Opus 4.5                            │
│         GPT-OSS-120B                               │
└─────────────────────────────────────────────────────┘
```

---

## 28.8 Practical Workflows

### Example: Building a Todo Application

**Step 1: Start in Manager View with Planning Mode**

```
Mode: Planning
Model: Gemini 3 Pro
Task: "Create a todo list web app using Python Flask with a React frontend"
```

**Step 2: Review Implementation Plan Artifact**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION PLAN                                               [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Backend (Flask):                                                           │
│  ════════════════                                                           │
│  1. Create Flask application structure                                      │
│  2. Define Todo model with SQLAlchemy                                       │
│  3. Implement REST API endpoints:                                           │
│     - GET /api/todos                                                        │
│     - POST /api/todos                                                       │
│     - PUT /api/todos/:id                                                    │
│     - DELETE /api/todos/:id                                                 │
│                                                                             │
│  Frontend (React):                                                          │
│  ════════════════                                                           │
│  1. Initialize React app with Vite                                          │
│  2. Create TodoList component                                               │
│  3. Create TodoItem component with edit/delete                              │
│  4. Implement API integration with fetch                                    │
│                                                                             │
│  [💬 Add comment: "Include user authentication"]                            │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Step 3: Review Task List Artifact**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TASK LIST                                                         [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ☑ Create project structure                                                 │
│  ☑ Set up Flask backend with SQLAlchemy                                     │
│  ☑ Define database models                                                   │
│  ☐ Implement API endpoints                                     [In Progress]│
│  ☐ Initialize React frontend                                                │
│  ☐ Create UI components                                                     │
│  ☐ Connect frontend to backend                                              │
│  ☐ Add user authentication (per feedback)                                   │
│  ☐ Write unit and integration tests                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Step 4: Review Code Diff Artifacts**

```diff
+ # app.py
+ from flask import Flask, jsonify, request
+ from flask_sqlalchemy import SQLAlchemy
+ from flask_cors import CORS
+
+ app = Flask(__name__)
+ app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
+ CORS(app)
+ db = SQLAlchemy(app)
+
+ class Todo(db.Model):
+     id = db.Column(db.Integer, primary_key=True)
+     title = db.Column(db.String(100), nullable=False)
+     completed = db.Column(db.Boolean, default=False)
+     created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

**Step 5: Verify with Screenshots**

Agent provides screenshot artifacts showing:
- Running application at localhost:3000
- Todo list UI with sample items
- Add/edit/delete functionality working

**Step 6: Iterate Based on Feedback**

Comment on screenshot: *"The checkbox styling doesn't match our design system—use filled checkboxes"*

Agent automatically updates CSS and provides new screenshot.

**Step 7: Trigger Workflow for Tests**

```
> /generate-tests
```

Agent creates comprehensive test suite based on your workflow definition.

---

## 28.9 Browser Integration

### Browser Agent Capabilities

Antigravity includes a specialized browser subagent for web interaction:

| Capability | Description |
|------------|-------------|
| **Navigation** | Visit URLs, handle redirects, manage tabs |
| **Reading** | Extract page content, capture DOM structure |
| **Interaction** | Click, scroll, type, fill forms, select options |
| **Recording** | Video documentation of browser actions |
| **Screenshots** | Capture UI states at any point |

### Setup

On first use requiring browser interaction:

1. Agent requests browser extension installation
2. Install **Antigravity Browser Extension** from Chrome Web Store
3. Grant necessary permissions for automation

### Browser Agent Tools

| Tool | Description |
|------|-------------|
| `navigate(url)` | Go to specified URL |
| `click(selector)` | Click element matching CSS selector |
| `type(selector, text)` | Enter text into input element |
| `scroll(direction, amount)` | Scroll page or element |
| `screenshot()` | Capture current viewport |
| `record_start()` / `record_stop()` | Video recording |
| `extract(selector)` | Get text/data from elements |

### Example: Testing a Web Application

```
Task: "Test the login flow of our application at localhost:3000"

Agent Actions:
1. Navigate to localhost:3000/login
2. Screenshot: Initial login page state
3. Type test credentials into form fields
4. Click login button
5. Screenshot: Post-login dashboard
6. Record video of complete flow
7. Generate test report artifact with findings
```

---

## 28.10 Best Practices

### 1. Start with Review-Driven Mode

Until comfortable with agent behavior, use frequent checkpoints:
```
Security Policy: Review-driven development
```

### 2. Define Comprehensive Rules

Create detailed `GEMINI.md` for consistent agent behavior:
```markdown
# Project Rules

## Code Standards
- All code must pass linting (eslint/pylint)
- Tests required for all new features
- No console.log/print statements in production code
- Use meaningful commit messages

## Architecture
- Follow existing project patterns
- Don't introduce new dependencies without approval
- Keep functions under 50 lines
```

### 3. Create Workflows for Repetitive Tasks

Save time with reusable workflows:
- `/generate-tests` — Create unit tests
- `/review-code` — Code review checklist
- `/document-api` — Generate API documentation
- `/refactor` — Systematic refactoring
- `/security-audit` — Security review

### 4. Leverage Skills for Domain Knowledge

Create skills for specialized tasks:
- Database migration procedures
- Security audit checklists
- Performance optimization guidelines
- Accessibility compliance checks

### 5. Use Multiple Agents Wisely

In Manager View:
- Assign **independent tasks** to separate agents
- Use **Planning mode** for complex features
- Use **Fast mode** for simple bug fixes
- Monitor all agents via the **Inbox**

### 6. Review Artifacts Thoroughly

Artifacts exist to build trust:
- **Read implementation plans** before approving
- **Check code diffs** for security issues
- **Verify screenshots** match expectations
- **Watch browser recordings** for edge cases

### 7. Configure Browser Allowlist

Limit agent web access to trusted sources:
```
# ~/.gemini/antigravity/browserAllowlist.txt
docs.python.org
react.dev
developer.mozilla.org
your-internal-docs.com
```

### 8. Use the Knowledge Base

Save useful context for future tasks:
```
Agent: "Save to Knowledge Base: Our API uses JWT tokens stored in httpOnly
cookies with 24-hour expiration. Refresh tokens are stored in the database."
```

---

## Hands-On Labs

### [Lab 28.1: Getting Started with Antigravity](labs/lab-01-getting-started.md)

Installation, configuration, and basic navigation.

- Install Antigravity on your system
- Configure security policies
- Navigate Editor and Manager views
- Complete a simple task with agent assistance

**Duration:** 45 minutes

### [Lab 28.2: Building with Agents](labs/lab-02-building-with-agents.md)

Complete application development workflow using agents.

- Use Planning mode for a multi-component application
- Work with artifacts (plans, diffs, screenshots)
- Provide feedback and iterate with agents
- Orchestrate multiple agents in parallel

**Duration:** 90 minutes

### [Lab 28.3: Custom Rules and Workflows](labs/lab-03-customization.md)

Advanced customization for team environments.

- Create project-specific rules
- Build reusable workflows
- Develop custom skills
- Configure security policies for team use

**Duration:** 60 minutes

---

## Summary

Google Antigravity represents a fundamental shift from AI-assisted coding to **agent-driven development**. Key concepts:

| Concept | Description |
|---------|-------------|
| **Agent-First Architecture** | Autonomous agents that plan, execute, and verify |
| **Two Views** | Editor for synchronous work, Manager for parallel agents |
| **Artifacts** | Verifiable deliverables (plans, diffs, screenshots, recordings) |
| **Security Policies** | Configurable autonomy levels for different risk environments |
| **Customization** | Rules, Workflows, and Skills for tailored behavior |

Mastering Antigravity means learning to **orchestrate agents effectively** rather than writing every line of code yourself.

---

## References

### Official Resources

- [Google Antigravity Documentation](https://antigravity.google/docs)
- [Google Developers Blog Announcement](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
- [Getting Started Codelab](https://codelabs.developers.google.com/getting-started-google-antigravity)
- [Antigravity Download](https://antigravity.google/download)

### Related Articles

- [Google Antigravity: AI-First Development with This New IDE](https://www.kdnuggets.com/google-antigravity-ai-first-development-with-this-new-ide) - KDnuggets
- [A First Look at Google's New Antigravity IDE](https://www.infoworld.com/article/4096113/a-first-look-at-googles-new-antigravity-ide.html) - InfoWorld
- [Google Antigravity: The Agentic IDE Changing Development Work](https://www.index.dev/blog/google-antigravity-agentic-ide) - Index.dev

### Prerequisite Modules

- [Module 12: Multi-Agent Systems](../12-multi-agent/README.md)

---

<div align="center">

**Module 28: Google Antigravity IDE** | FWG LLM Agentic Training Guide

[Previous: Module 27](../27-case-studies/README.md) | [Back to Main](../../README.md)

</div>
