# Contributing to FWG LLM Agentic Training Guide

<div align="center">

**Thank you for your interest in improving our training materials!**

*Your contributions help build AI competency across the federal contracting community.*

</div>

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Who Can Contribute](#who-can-contribute)
- [Types of Contributions](#types-of-contributions)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Content Standards](#content-standards)
- [Review Process](#review-process)
- [Style Guide](#style-guide)

---

## Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming, inclusive, and harassment-free environment for all participants.

---

## Who Can Contribute

Contributions are welcome from:

| Contributor Type | Contribution Scope |
|-----------------|-------------------|
| **FWG Employees** | All content areas |
| **Authorized Partners** | Technical content, labs, examples |
| **Federal Agency SMEs** | Compliance guidance, case studies |
| **Open Source Community** | Bug fixes, tool improvements (public sections only) |

### Authorization Requirements

Before contributing, ensure you have:
- [ ] FWG employee ID or partner authorization
- [ ] Signed contributor agreement on file
- [ ] Completed security awareness training
- [ ] Reviewed classification guidelines

---

## Types of Contributions

### Content Contributions

| Type | Description | Priority |
|------|-------------|----------|
| **Module Content** | New lessons, expanded explanations | High |
| **Lab Exercises** | Hands-on practical exercises | High |
| **Code Examples** | Working, tested code samples | High |
| **Case Studies** | Real-world implementation stories | Medium |
| **Cheatsheets** | Quick reference guides | Medium |
| **Diagrams** | Visual aids and architecture diagrams | Medium |
| **Translations** | Accessibility improvements | Low |

### Technical Contributions

| Type | Description | Priority |
|------|-------------|----------|
| **Bug Fixes** | Correct errors in code or documentation | Critical |
| **Template Updates** | Improve reusable templates | High |
| **Script Improvements** | Enhance utility scripts | Medium |
| **CI/CD** | Automated testing and validation | Medium |
| **Accessibility** | Section 508 compliance improvements | High |

---

## Getting Started

### Prerequisites

```bash
# Required tools
- Git 2.30+
- Python 3.11+
- Node.js 18+
- Markdown editor (VS Code recommended)
```

### Fork and Clone

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/FWG-LLM-Agentic-Training-Guide.git
cd FWG-LLM-Agentic-Training-Guide

# 3. Add upstream remote
git remote add upstream https://github.com/consigcody94/FWG-LLM-Agentic-Training-Guide.git

# 4. Create a branch for your work
git checkout -b feature/your-feature-name
```

### Set Up Development Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development tools

# Install pre-commit hooks
pre-commit install
```

---

## Development Workflow

### Branch Naming Convention

```
feature/      - New features or content
fix/          - Bug fixes and corrections
docs/         - Documentation-only changes
lab/          - New or updated labs
cheatsheet/   - Cheatsheet additions
module/       - Module content updates
```

**Examples:**
- `feature/add-kubernetes-lab`
- `fix/correct-api-example-module-04`
- `docs/improve-rag-explanation`
- `lab/multimodal-agent-exercise`

### Commit Message Format

```
type(scope): brief description

[optional body with more details]

[optional footer with references]
```

**Types:**
- `feat`: New feature or content
- `fix`: Bug fix or correction
- `docs`: Documentation changes
- `refactor`: Code restructuring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```bash
feat(module-10): add vector database comparison section

fix(lab-05): correct MCP server initialization code

docs(readme): update quick start instructions for macOS
```

### Pull Request Process

1. **Update your branch**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Run quality checks**
   ```bash
   # Validate markdown
   npm run lint:md

   # Check Python code
   black --check .
   flake8 .
   mypy .

   # Run tests
   pytest

   # Verify setup script
   python scripts/verify_setup.py
   ```

3. **Create Pull Request**
   - Use the PR template
   - Link related issues
   - Request appropriate reviewers
   - Add labels

4. **Address Review Feedback**
   - Respond to all comments
   - Make requested changes
   - Re-request review when ready

---

## Content Standards

### Documentation Requirements

All documentation must:

- [ ] Be technically accurate and tested
- [ ] Follow federal compliance requirements
- [ ] Use clear, accessible language
- [ ] Include practical examples
- [ ] Reference authoritative sources
- [ ] Maintain consistent formatting

### Code Example Requirements

All code examples must:

- [ ] Be complete and runnable
- [ ] Include necessary imports
- [ ] Have comments explaining key sections
- [ ] Follow PEP 8 (Python) or ESLint (JavaScript)
- [ ] Include error handling
- [ ] Use secure practices (no hardcoded secrets)
- [ ] Be tested before submission

### Federal Compliance Requirements

All content must:

- [ ] Avoid classified or sensitive information
- [ ] Comply with NIST guidelines where applicable
- [ ] Reference appropriate FedRAMP/FISMA controls
- [ ] Include security considerations
- [ ] Follow Section 508 accessibility guidelines
- [ ] Use inclusive language

### Security Review Checklist

Before submitting code or examples:

- [ ] No API keys, passwords, or secrets
- [ ] No PII or sensitive data
- [ ] Input validation included
- [ ] Error messages don't expose internals
- [ ] Dependencies are from trusted sources
- [ ] No vulnerable dependency versions

---

## Review Process

### Review Timeline

| Review Type | Expected Turnaround |
|-------------|-------------------|
| Minor Documentation | 2-3 business days |
| Code Examples | 3-5 business days |
| New Modules/Labs | 5-10 business days |
| Security-Related | 5-10 business days |

### Reviewer Assignments

| Content Type | Reviewers |
|-------------|-----------|
| Technical Content | 2 technical reviewers |
| Security Content | 1 security SME + 1 technical |
| Compliance Content | 1 compliance SME + 1 technical |
| All Content | 1 final editor review |

### Approval Requirements

- **Minor changes**: 1 approval
- **New content**: 2 approvals
- **Security/Compliance**: Security SME approval required
- **Module changes**: Curriculum lead approval required

---

## Style Guide

### Markdown Formatting

```markdown
# Module Title (H1 - one per file)

## Major Section (H2)

### Subsection (H3)

#### Minor Heading (H4)

**Bold** for emphasis on key terms
*Italic* for new terms on first use
`code` for inline code and commands
```

### Code Blocks

Always specify language for syntax highlighting:

````markdown
```python
# Python code here
```

```bash
# Shell commands here
```

```json
{
  "json": "data"
}
```
````

### Diagrams

Use ASCII art for diagrams in documentation:

```
┌─────────────────┐     ┌─────────────────┐
│    Component    │────▶│    Component    │
└─────────────────┘     └─────────────────┘
```

### File Organization

```
module-XX-name/
├── README.md           # Module overview and learning objectives
├── lessons/
│   ├── 01-topic.md     # Individual lessons
│   ├── 02-topic.md
│   └── ...
├── exercises/
│   ├── exercise-01.md  # Practice exercises
│   └── solutions/      # Exercise solutions (optional)
├── examples/
│   ├── example-01.py   # Code examples
│   └── example-02.py
└── resources/
    └── references.md   # Additional resources
```

---

## Recognition

Contributors are recognized in:
- Repository contributors list
- Module acknowledgments (for significant contributions)
- Annual FWG training contributor awards

---

## Questions?

- **Technical Questions**: Open an issue with the `question` label
- **Process Questions**: Contact the training curriculum team
- **Security Concerns**: Follow the security reporting process in [SECURITY.md](SECURITY.md)

---

<div align="center">

**Thank you for contributing to federal AI competency!**

*Together, we're building the future of AI in government.*

</div>
