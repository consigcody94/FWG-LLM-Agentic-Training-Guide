# Lab 28.3: Custom Rules and Workflows

## Overview

In this lab, you will create custom rules, workflows, and skills to tailor Google Antigravity for your team's development practices. These configurations ensure consistent agent behavior across projects.

**Duration:** 60 minutes
**Difficulty:** Intermediate
**Prerequisites:** Labs 28.1 and 28.2 completed

## Learning Objectives

1. Create project-specific rules in GEMINI.md
2. Build reusable workflows for common tasks
3. Develop custom skills for specialized knowledge
4. Configure security policies for team use

## Part 1: Creating Rules (15 minutes)

Rules are persistent guidelines that govern agent behavior across all tasks.

### Task 1.1: Create Global Rules

Create a global rules file that applies to all your projects:

**File: `~/.gemini/GEMINI.md`**

```markdown
# Global Agent Rules

## Code Style
- Use 4 spaces for indentation (never tabs)
- Maximum line length: 100 characters
- Always include type hints in Python functions
- Use camelCase for JavaScript, snake_case for Python
- Prefer const over let in JavaScript

## Documentation
- All public functions require docstrings/JSDoc comments
- Use Google-style docstrings for Python
- Include @param and @returns in JSDoc

## Git Practices
- Write meaningful commit messages (imperative mood)
- Keep commits focused on single changes
- Never commit directly to main/master

## Security
- Never hardcode credentials or API keys
- Use environment variables for all secrets
- Validate all user inputs
- Sanitize outputs to prevent XSS

## Testing
- Write tests for all new functionality
- Maintain minimum 80% code coverage
- Name tests descriptively: test_should_[expected_behavior]_when_[condition]
```

### Task 1.2: Create Project-Specific Rules

For the task-manager project from Lab 28.2, create project rules:

**File: `~/task-manager-app/.agent/rules/project-rules.md`**

```markdown
# Task Manager Project Rules

## Architecture
- Follow MVC pattern for backend
- Keep API routes in routes.py, business logic in services/
- Frontend uses vanilla JavaScript (no frameworks)

## Database
- Use SQLAlchemy ORM for all database operations
- Always use migrations for schema changes
- Include created_at and updated_at timestamps on all models

## API Design
- Follow REST conventions
- Use proper HTTP status codes
- Return JSON for all endpoints
- Include error messages in response body

## Frontend
- Use BEM naming convention for CSS classes
- Keep JavaScript functions under 30 lines
- Use async/await for API calls

## Specific Patterns
- Task status values: 'todo', 'in-progress', 'done'
- API base URL: /api/v1/
- Date format: ISO 8601
```

### Task 1.3: Test Your Rules

Open the task-manager project in Antigravity and ask:

```
Add a new endpoint to get tasks by status. Follow project conventions.
```

Verify the agent:
- Uses the correct API prefix (`/api/v1/`)
- Returns proper JSON format
- Includes appropriate status codes
- Follows your coding style

## Part 2: Building Workflows (20 minutes)

Workflows are reusable prompts triggered with `/` commands.

### Task 2.1: Create a Test Generation Workflow

**File: `~/.gemini/antigravity/global_workflows/generate-tests.md`**

```markdown
---
name: generate-tests
description: Generate comprehensive unit tests for selected code
trigger: /generate-tests
---

# Generate Unit Tests

Analyze the selected code and generate comprehensive unit tests:

## Requirements

1. **Test Framework**
   - Python: Use pytest with fixtures
   - JavaScript: Use Jest with describe/it blocks

2. **Test Categories**
   Create tests for:
   - Happy path scenarios (expected inputs)
   - Edge cases (empty, null, boundary values)
   - Error conditions (invalid inputs, exceptions)

3. **Coverage Goals**
   - Test all public functions/methods
   - Test all code branches (if/else paths)
   - Test error handling

4. **Test Structure**
   - Group related tests in classes/describe blocks
   - Use descriptive test names
   - Include setup/teardown as needed
   - Mock external dependencies

5. **Documentation**
   - Add docstring/comment explaining what each test verifies

## Output Format

Create test files in the appropriate tests/ directory following project structure.
```

### Task 2.2: Create a Code Review Workflow

**File: `~/.gemini/antigravity/global_workflows/review-code.md`**

```markdown
---
name: review-code
description: Perform thorough code review with actionable feedback
trigger: /review-code
---

# Code Review

Perform a comprehensive code review of the selected code:

## Review Checklist

### Correctness
- [ ] Logic is correct for all cases
- [ ] No off-by-one errors
- [ ] Null/undefined properly handled
- [ ] Async operations handled correctly

### Security
- [ ] Input validation present
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Secrets not hardcoded
- [ ] Proper authentication/authorization

### Performance
- [ ] No unnecessary loops
- [ ] Efficient algorithms used
- [ ] No N+1 query problems
- [ ] Appropriate caching

### Maintainability
- [ ] Code is readable
- [ ] Functions are focused (single responsibility)
- [ ] No magic numbers
- [ ] Appropriate comments

### Testing
- [ ] Tests exist for new code
- [ ] Edge cases covered
- [ ] Tests are meaningful (not just coverage)

## Output Format

Provide feedback as:
1. **Critical Issues** - Must fix before merge
2. **Suggestions** - Recommended improvements
3. **Nitpicks** - Minor style issues
4. **Praise** - What was done well

Include specific line references and code examples for suggested fixes.
```

### Task 2.3: Create a Documentation Workflow

**File: `~/task-manager-app/.agent/workflows/document-api.md`**

```markdown
---
name: document-api
description: Generate API documentation for Flask endpoints
trigger: /document-api
---

# Generate API Documentation

Create comprehensive API documentation for all Flask endpoints.

## Documentation Format

For each endpoint, include:

### Endpoint Header
- HTTP Method and Path
- Brief description
- Authentication requirements

### Request
- URL parameters
- Query parameters
- Request body schema (with examples)
- Headers required

### Response
- Success response (status code, body schema, example)
- Error responses (possible error codes and messages)

### Example
```
curl -X POST http://localhost:5000/api/v1/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Example task", "description": "Details"}'
```

## Output

Create/update API.md in the project root with full documentation.
```

### Task 2.4: Test Your Workflows

In Antigravity, test each workflow:

```
/generate-tests
```

Select some code and verify the tests are generated according to your specifications.

```
/review-code
```

Select code and verify you get structured feedback.

## Part 3: Developing Skills (15 minutes)

Skills are specialized knowledge packages loaded on-demand.

### Task 3.1: Create a Database Migration Skill

**Directory: `~/.gemini/antigravity/skills/db-migration/`**

**File: `SKILL.md`**

```markdown
---
name: db-migration
description: Database migration procedures for SQLAlchemy/Flask-Migrate
triggers:
  - migration
  - database change
  - schema change
  - add column
  - alter table
---

# Database Migration Skill

## When to Use
This skill applies when:
- Adding new tables
- Modifying existing tables
- Adding/removing columns
- Changing column types
- Adding indexes

## Migration Procedure

### 1. Create Migration
```bash
flask db migrate -m "Description of changes"
```

### 2. Review Generated Migration
- Check `migrations/versions/` for the new file
- Verify upgrade() and downgrade() functions
- Ensure data migrations are included if needed

### 3. Apply Migration
```bash
# Development
flask db upgrade

# Production (with backup)
# 1. Backup database first
# 2. Apply migration
# 3. Verify data integrity
```

### 4. Rollback if Needed
```bash
flask db downgrade
```

## Best Practices

1. **One migration per logical change**
   - Don't combine unrelated schema changes

2. **Always write downgrade**
   - Ensure migrations are reversible

3. **Handle data migrations**
   - If changing column types, migrate data explicitly

4. **Test migrations**
   - Test upgrade and downgrade on copy of production data

## Common Patterns

### Adding a Column with Default
```python
def upgrade():
    op.add_column('tasks', sa.Column('priority', sa.Integer, default=0))
    # Backfill existing rows
    op.execute("UPDATE tasks SET priority = 0 WHERE priority IS NULL")

def downgrade():
    op.drop_column('tasks', 'priority')
```

### Renaming a Column
```python
def upgrade():
    op.alter_column('tasks', 'desc', new_column_name='description')

def downgrade():
    op.alter_column('tasks', 'description', new_column_name='desc')
```
```

### Task 3.2: Create a Security Audit Skill

**Directory: `~/.gemini/antigravity/skills/security-audit/`**

**File: `SKILL.md`**

```markdown
---
name: security-audit
description: Security audit checklist for web applications
triggers:
  - security
  - audit
  - vulnerability
  - penetration test
---

# Security Audit Skill

## OWASP Top 10 Checklist

### A01: Broken Access Control
- [ ] Enforce server-side access control
- [ ] Deny by default
- [ ] Implement proper CORS
- [ ] Disable directory listing

### A02: Cryptographic Failures
- [ ] Use TLS for all connections
- [ ] Don't store sensitive data unnecessarily
- [ ] Encrypt data at rest
- [ ] Use strong algorithms (AES-256, SHA-256+)

### A03: Injection
- [ ] Use parameterized queries (SQLAlchemy ORM)
- [ ] Validate and sanitize all inputs
- [ ] Use safe APIs that avoid interpreters

### A04: Insecure Design
- [ ] Threat modeling performed
- [ ] Security requirements defined
- [ ] Secure design patterns used

### A05: Security Misconfiguration
- [ ] Remove default credentials
- [ ] Disable unnecessary features
- [ ] Error messages don't leak info
- [ ] Security headers configured

### A06: Vulnerable Components
- [ ] Inventory all dependencies
- [ ] Remove unused dependencies
- [ ] Check for known vulnerabilities (safety, npm audit)

### A07: Authentication Failures
- [ ] Strong password requirements
- [ ] Rate limiting on auth endpoints
- [ ] Secure session management
- [ ] MFA where appropriate

### A08: Data Integrity Failures
- [ ] Verify data integrity
- [ ] Use signed/encrypted tokens
- [ ] Validate CI/CD pipeline

### A09: Logging Failures
- [ ] Log authentication attempts
- [ ] Log access control failures
- [ ] Ensure logs don't contain sensitive data

### A10: SSRF
- [ ] Sanitize user-supplied URLs
- [ ] Use allowlists for external requests
- [ ] Don't follow redirects blindly

## Flask-Specific Checks
- [ ] SECRET_KEY is strong and not in code
- [ ] Debug mode disabled in production
- [ ] CSRF protection enabled
- [ ] Session cookies are secure and httpOnly
```

**File: `references/security-headers.md`**

```markdown
# Security Headers Reference

## Required Headers

```python
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response
```
```

### Task 3.3: Test Skills

The skills will automatically load when you mention relevant topics:

```
I need to add a 'priority' column to the tasks table. Help me create a migration.
```

The agent should use the db-migration skill's procedures.

```
Perform a security audit of the task-manager backend
```

The agent should use the security-audit checklist.

## Part 4: Team Security Configuration (10 minutes)

### Task 4.1: Create Team Security Policy

**File: `~/task-manager-app/.agent/security-policy.md`**

```markdown
# Team Security Policy

## Terminal Commands

### Allowed Commands
```
# Development
npm install
npm run *
pip install -r requirements.txt
python -m pytest
flask run
flask db *

# Git (non-destructive)
git status
git diff
git add
git commit
git pull
git push

# Database
sqlite3 *.db ".tables"
sqlite3 *.db ".schema *"
```

### Blocked Commands
```
# Destructive
rm -rf
git reset --hard
git push --force
drop table
delete from

# Sensitive
curl (to non-allowlisted URLs)
wget
ssh
scp
```

## Browser Access

### Allowed Domains
```
localhost
127.0.0.1
docs.python.org
developer.mozilla.org
flask.palletsprojects.com
```

### Blocked Domains
```
*  # Default deny all external
```

## File Access

### Protected Paths
```
.env
.env.*
secrets/
credentials/
*.pem
*.key
```
```

### Task 4.2: Create Onboarding Workflow for New Team Members

**File: `~/task-manager-app/.agent/workflows/onboard-developer.md`**

```markdown
---
name: onboard-developer
description: Set up development environment for new team members
trigger: /onboard
---

# Developer Onboarding

Welcome to the Task Manager project! Let me help you set up your environment.

## Steps

1. **Verify Prerequisites**
   - Python 3.10+ installed
   - Node.js 18+ installed (for any tooling)
   - Git configured

2. **Clone and Setup**
   ```bash
   git clone <repo-url>
   cd task-manager-app
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r backend/requirements.txt
   ```

3. **Environment Configuration**
   - Copy .env.example to .env
   - Generate a new SECRET_KEY
   - Configure database path

4. **Initialize Database**
   ```bash
   cd backend
   flask db upgrade
   ```

5. **Run Tests**
   ```bash
   python -m pytest
   ```

6. **Start Development Server**
   ```bash
   flask run
   ```

7. **Verify Setup**
   - Open http://localhost:5000
   - You should see the task board

## Project Structure Overview

[Explain key directories and files]

## Development Guidelines

[Link to GEMINI.md and other relevant docs]
```

## Deliverables

By the end of this lab, you should have:

1. ✅ Global rules file (`~/.gemini/GEMINI.md`)
2. ✅ Project-specific rules
3. ✅ At least 3 reusable workflows
4. ✅ At least 2 custom skills
5. ✅ Team security configuration

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Created comprehensive global rules | 20 |
| Created project-specific rules | 15 |
| Built working workflows | 25 |
| Developed useful skills | 25 |
| Configured security policies | 15 |
| **Total** | **100** |

## Sharing Configurations

To share your configurations with your team:

1. **Version control workspace configs**
   - Add `.agent/` directory to your repo
   - Team members get configs when they clone

2. **Global configs**
   - Document in team wiki
   - Or create a shared setup script

3. **Skills repository**
   - Create a shared repo for team skills
   - Symlink to `~/.gemini/antigravity/skills/`

## Next Steps

You've completed the Google Antigravity IDE module! You now know how to:

- Install and configure Antigravity
- Work with agents in Editor and Manager views
- Review and iterate on artifacts
- Orchestrate multiple agents
- Customize behavior with rules, workflows, and skills

Continue exploring the platform and building your library of reusable configurations!
