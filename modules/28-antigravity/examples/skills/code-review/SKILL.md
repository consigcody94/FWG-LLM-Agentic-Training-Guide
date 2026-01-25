---
name: code-review
description: Comprehensive code review checklist and guidelines
triggers:
  - review
  - code review
  - PR review
  - pull request
---

# Code Review Skill

This skill provides a systematic approach to code reviews.

## When This Skill Applies

- Reviewing pull requests
- Reviewing code changes before commit
- Auditing existing code
- Mentoring through code review

## Review Checklist

### Correctness
- [ ] Logic is correct and handles all expected cases
- [ ] No off-by-one errors in loops or array access
- [ ] Proper null/undefined handling
- [ ] Correct comparison operators (== vs ===, is vs ==)
- [ ] Async operations properly awaited
- [ ] Transactions properly committed/rolled back

### Security
- [ ] All user inputs validated
- [ ] Parameterized queries used (no string concatenation)
- [ ] Output properly escaped (XSS prevention)
- [ ] Authentication required where needed
- [ ] Authorization checks present
- [ ] No sensitive data in logs
- [ ] No hardcoded secrets

### Performance
- [ ] No unnecessary database queries in loops
- [ ] Appropriate indexes exist for queries
- [ ] No memory leaks (listeners removed, resources closed)
- [ ] Pagination used for large datasets
- [ ] Caching considered where appropriate

### Maintainability
- [ ] Code is readable and self-explanatory
- [ ] Functions/methods are focused (single responsibility)
- [ ] Meaningful variable and function names
- [ ] No magic numbers (use named constants)
- [ ] Consistent code style
- [ ] Appropriate error messages

### Testing
- [ ] Tests cover the changes
- [ ] Edge cases tested
- [ ] Error scenarios tested
- [ ] Tests are deterministic (no flaky tests)
- [ ] Mocks used appropriately

### Documentation
- [ ] Public APIs documented
- [ ] Complex logic has comments
- [ ] README updated if needed
- [ ] CHANGELOG updated if applicable

## Common Issues by Language

### Python
- Using mutable default arguments
- Not using context managers for resources
- Bare except clauses
- Using is for value comparison
- Not handling StopIteration

### JavaScript
- Not handling promise rejections
- Using == instead of ===
- Variable hoisting issues
- this binding problems
- Memory leaks in closures

### SQL
- N+1 query problems
- Missing indexes
- Not using transactions
- SQL injection vulnerabilities
- Not handling NULL properly

## Review Process

1. **Understand Context**
   - Read PR description
   - Understand the problem being solved
   - Check related issues/tickets

2. **Review Changes**
   - Go through diff file by file
   - Check against checklist
   - Note issues and suggestions

3. **Test Mentally**
   - Walk through code paths
   - Consider edge cases
   - Think about failure modes

4. **Provide Feedback**
   - Be specific and actionable
   - Explain the "why"
   - Suggest alternatives
   - Acknowledge good work

## Feedback Guidelines

### Be Constructive
- Focus on the code, not the person
- Explain reasoning behind suggestions
- Offer alternatives, not just criticism

### Be Specific
- Reference line numbers
- Provide code examples
- Link to documentation when helpful

### Be Proportionate
- Distinguish critical issues from nitpicks
- Don't block for style preferences
- Focus on what matters most

### Be Kind
- Assume good intent
- Ask questions instead of assuming
- Recognize effort and good patterns
