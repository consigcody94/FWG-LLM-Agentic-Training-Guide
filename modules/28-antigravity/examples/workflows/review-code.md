---
name: review-code
description: Perform thorough code review with actionable feedback
trigger: /review-code
---

# Code Review

Perform a comprehensive code review of the selected code.

## Review Categories

### 1. Correctness

- [ ] Logic is correct and handles all expected cases
- [ ] No off-by-one errors in loops or array access
- [ ] Null/undefined values properly handled
- [ ] Async operations handled correctly (await, promises)
- [ ] Race conditions considered
- [ ] Edge cases handled

### 2. Security

- [ ] Input validation present and sufficient
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No command injection vulnerabilities
- [ ] Secrets not hardcoded
- [ ] Proper authentication checks
- [ ] Proper authorization checks
- [ ] Sensitive data not logged

### 3. Performance

- [ ] No unnecessary loops or iterations
- [ ] Efficient algorithms and data structures
- [ ] No N+1 query problems
- [ ] Appropriate caching considered
- [ ] No memory leaks
- [ ] Resource cleanup handled

### 4. Maintainability

- [ ] Code is readable and self-documenting
- [ ] Functions have single responsibility
- [ ] No magic numbers (use named constants)
- [ ] Appropriate comments for complex logic
- [ ] Consistent naming conventions
- [ ] DRY principle followed

### 5. Error Handling

- [ ] Errors are caught and handled appropriately
- [ ] Error messages are meaningful
- [ ] Errors are logged with context
- [ ] User-facing errors are friendly
- [ ] Errors don't expose sensitive information

### 6. Testing

- [ ] Tests exist for new code
- [ ] Edge cases are tested
- [ ] Error conditions are tested
- [ ] Tests are meaningful (not just for coverage)
- [ ] Mocks are used appropriately

## Output Format

Provide feedback organized as:

### Critical Issues
Must fix before merge. These are bugs, security issues, or major problems.

```
🔴 [Line X] Issue description
   Problem: Explain the issue
   Solution: Suggest fix with code example
```

### Suggestions
Recommended improvements for code quality.

```
🟡 [Line X] Suggestion title
   Current: How it is now
   Suggested: How it could be better
   Reason: Why this improves the code
```

### Nitpicks
Minor style issues or preferences.

```
🟢 [Line X] Nitpick description
   Consider: Alternative approach
```

### Praise
What was done well - reinforce good practices.

```
✨ [Line X] Praise description
   This is a good example of [pattern/practice]
```

## Example Review

```
🔴 [Line 15] SQL Injection Vulnerability
   Problem: User input directly concatenated into SQL query
   Solution: Use parameterized query
   ```python
   # Instead of:
   cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

   # Use:
   cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
   ```

🟡 [Line 42] Consider extracting to function
   Current: Complex logic inline
   Suggested: Extract to named function
   Reason: Improves readability and testability

🟢 [Line 67] Naming convention
   Consider: Using `user_count` instead of `cnt` for clarity

✨ [Line 89] Great error handling
   This is a good example of catching specific exceptions
   and providing meaningful error messages.
```

## Summary

End with a brief summary:
- Overall assessment (approve/request changes)
- Key points to address
- Positive aspects of the code
