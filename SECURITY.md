# Security Policy

## FWG LLM Agentic Training Guide

<div align="center">

**Security is a shared responsibility**

*Protecting our training materials and community*

</div>

---

## Table of Contents

- [Security Commitment](#security-commitment)
- [Reporting Vulnerabilities](#reporting-vulnerabilities)
- [Classification Guidelines](#classification-guidelines)
- [Secure Development Practices](#secure-development-practices)
- [Dependency Management](#dependency-management)
- [Incident Response](#incident-response)

---

## Security Commitment

Federal Working Group is committed to maintaining the security and integrity of this training guide. We follow federal security standards and best practices to protect our materials and community.

### Supported Versions

| Version | Supported | Security Updates |
|---------|-----------|------------------|
| 1.0.x   | ✅ Yes    | Active           |
| < 1.0   | ❌ No     | None             |

---

## Reporting Vulnerabilities

### How to Report

**DO NOT** report security vulnerabilities through public GitHub issues.

Instead, please report security vulnerabilities through one of these secure channels:

1. **Email**: security@federalworkinggroup.example.com
   - Use encryption if available (PGP key below)
   - Subject line: `[SECURITY] FWG-LLM-Training - Brief Description`

2. **Private Disclosure**: GitHub Security Advisory
   - Navigate to Security tab → Report a vulnerability
   - Provides private communication channel

### What to Include

Please provide the following information:

```markdown
## Vulnerability Report

### Summary
[Brief description of the issue]

### Affected Components
[Which files, modules, or scripts are affected]

### Severity Assessment
[Your assessment: Critical / High / Medium / Low]

### Steps to Reproduce
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Impact
[What could an attacker do with this vulnerability]

### Suggested Fix
[If you have a recommendation]

### Your Information (Optional)
[Name and contact for credit in acknowledgments]
```

### Response Timeline

| Phase | Timeframe |
|-------|-----------|
| Initial Response | Within 24 hours |
| Triage & Assessment | Within 48 hours |
| Fix Development | 1-14 days (severity dependent) |
| Disclosure | After fix deployed |

### What to Expect

1. **Acknowledgment**: We will acknowledge receipt within 24 hours
2. **Communication**: We will keep you informed of progress
3. **Credit**: We will credit you in security advisories (unless you prefer anonymity)
4. **No Retaliation**: We will not take legal action against good-faith security researchers

---

## Classification Guidelines

### Data Handling

This repository contains **UNCLASSIFIED** training materials only.

| Classification | Allowed in Repo | Handling |
|---------------|-----------------|----------|
| UNCLASSIFIED | ✅ Yes | Standard handling |
| CUI | ❌ No | Do not commit |
| CLASSIFIED | ❌ No | Do not commit |

### Prohibited Content

**NEVER** commit the following:

- [ ] API keys, tokens, or secrets
- [ ] Passwords or credentials
- [ ] Personally Identifiable Information (PII)
- [ ] Protected Health Information (PHI)
- [ ] Controlled Unclassified Information (CUI)
- [ ] Classified information of any level
- [ ] Export-controlled technical data
- [ ] Proprietary client information

### Pre-Commit Checks

Before committing, verify:

```bash
# Check for potential secrets
git diff --staged | grep -iE "(api.?key|password|secret|token|credential)"

# Use git-secrets (recommended)
git secrets --scan
```

---

## Secure Development Practices

### Code Security Standards

All code in this repository must follow secure coding practices:

#### Python Code

```python
# DO: Use environment variables for secrets
import os
api_key = os.getenv("API_KEY")

# DON'T: Hardcode secrets
api_key = "sk-abc123..."  # NEVER DO THIS

# DO: Validate input
from pydantic import BaseModel, validator

class UserInput(BaseModel):
    query: str

    @validator('query')
    def sanitize_query(cls, v):
        # Validate and sanitize
        return v.strip()[:1000]

# DO: Use parameterized queries
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))

# DON'T: String concatenation for queries
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")  # SQL INJECTION RISK
```

#### JavaScript Code

```javascript
// DO: Sanitize output
const safeOutput = DOMPurify.sanitize(userInput);

// DON'T: Direct DOM injection
element.innerHTML = userInput;  // XSS RISK

// DO: Use Content Security Policy
// Add to server responses:
// Content-Security-Policy: default-src 'self'
```

### Dependency Security

#### Python Dependencies

```bash
# Check for vulnerable packages
pip install safety
safety check -r requirements.txt

# Keep dependencies updated
pip install pip-audit
pip-audit
```

#### Node.js Dependencies

```bash
# Check for vulnerabilities
npm audit

# Fix automatically where possible
npm audit fix
```

### Secret Scanning

We use multiple layers of secret detection:

1. **Pre-commit hooks**: git-secrets, detect-secrets
2. **CI/CD scanning**: GitHub Secret Scanning
3. **Manual review**: Security team review for PRs

---

## Dependency Management

### Approved Sources

| Package Type | Approved Sources |
|-------------|------------------|
| Python | PyPI (pypi.org) |
| JavaScript | npm (npmjs.com) |
| System | Official OS repositories |

### Version Pinning

All dependencies must be version-pinned:

```txt
# requirements.txt
openai==1.12.0
anthropic==0.18.1
langchain==0.1.0
```

### Vulnerability Monitoring

We monitor dependencies using:
- GitHub Dependabot
- Snyk (for additional scanning)
- Regular manual audits (quarterly)

### Update Process

1. Dependabot creates PR for update
2. Automated tests run
3. Security review for major updates
4. Merge after approval

---

## Incident Response

### Security Incident Categories

| Category | Description | Response Time |
|----------|-------------|---------------|
| **Critical** | Active exploitation, data breach | Immediate |
| **High** | Vulnerability with high impact | 24 hours |
| **Medium** | Vulnerability with limited impact | 72 hours |
| **Low** | Best practice improvement | 1 week |

### Incident Response Process

```
┌─────────────┐
│  Detection  │
└──────┬──────┘
       ▼
┌─────────────┐
│   Triage    │◄── Assess severity
└──────┬──────┘
       ▼
┌─────────────┐
│ Containment │◄── Stop the bleeding
└──────┬──────┘
       ▼
┌─────────────┐
│ Eradication │◄── Remove the threat
└──────┬──────┘
       ▼
┌─────────────┐
│  Recovery   │◄── Restore operations
└──────┬──────┘
       ▼
┌─────────────┐
│   Review    │◄── Learn and improve
└─────────────┘
```

### Communication

During incidents:
- Updates posted to repository Security tab
- Major incidents communicated via email to contributors
- Post-incident report published after resolution

---

## Security Best Practices for Users

### When Using This Training Material

1. **Environment Isolation**
   ```bash
   # Always use virtual environments
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Secure API Key Storage**
   ```bash
   # Use .env files (never commit)
   echo ".env" >> .gitignore

   # Secure file permissions
   chmod 600 .env
   ```

3. **Network Security**
   - Use VPN when working remotely
   - Verify TLS certificates for API connections
   - Monitor for unusual API activity

4. **Regular Updates**
   ```bash
   # Keep dependencies current
   pip install --upgrade -r requirements.txt
   ```

---

## Acknowledgments

We thank the following security researchers for responsible disclosure:

*No vulnerabilities reported yet - be the first to help us improve!*

---

## Contact

For security-related questions that don't involve vulnerabilities:
- Open an issue with the `security-question` label
- Contact the security team

---

<div align="center">

**Security is everyone's responsibility**

*Report • Protect • Improve*

</div>
