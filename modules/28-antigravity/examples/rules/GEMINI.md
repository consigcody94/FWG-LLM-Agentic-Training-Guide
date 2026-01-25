# Example GEMINI.md - Global Agent Rules

This file should be placed at `~/.gemini/GEMINI.md` to apply to all projects.

---

## Code Style

### Python
- Use 4 spaces for indentation (never tabs)
- Maximum line length: 100 characters
- Always include type hints for function parameters and return values
- Use snake_case for variables and functions
- Use PascalCase for classes
- Follow PEP 8 guidelines

### JavaScript/TypeScript
- Use 2 spaces for indentation
- Use semicolons
- Prefer const over let, avoid var
- Use camelCase for variables and functions
- Use PascalCase for classes and React components
- Use single quotes for strings

### General
- One blank line between functions
- Two blank lines between classes
- No trailing whitespace
- Files should end with a newline

## Documentation

### Python
- All public functions require docstrings
- Use Google-style docstring format:
  ```python
  def function(param1: str, param2: int) -> bool:
      """Brief description.

      Longer description if needed.

      Args:
          param1: Description of param1.
          param2: Description of param2.

      Returns:
          Description of return value.

      Raises:
          ValueError: When param1 is empty.
      """
  ```

### JavaScript
- Use JSDoc for public functions:
  ```javascript
  /**
   * Brief description.
   * @param {string} param1 - Description
   * @param {number} param2 - Description
   * @returns {boolean} Description
   */
  ```

## Git Practices

- Write meaningful commit messages in imperative mood
- Format: `<type>: <description>`
- Types: feat, fix, docs, style, refactor, test, chore
- Keep commits focused on single logical changes
- Never commit directly to main/master branch
- Always create feature branches

## Security

- Never hardcode credentials, API keys, or secrets
- Use environment variables for all sensitive configuration
- Never commit .env files (use .env.example as template)
- Validate and sanitize all user inputs
- Use parameterized queries for database operations
- Escape output to prevent XSS
- Log security-relevant events without sensitive data

## Testing

- Write tests for all new functionality
- Maintain minimum 80% code coverage
- Name tests descriptively: `test_should_[expected]_when_[condition]`
- Include tests for edge cases and error conditions
- Mock external dependencies
- Keep tests independent (no test should depend on another)

## Error Handling

- Use specific exception types, not generic Exception
- Always include meaningful error messages
- Log errors with appropriate context
- Don't swallow exceptions silently
- Provide user-friendly error messages in APIs

## Performance

- Avoid N+1 query problems
- Use pagination for list endpoints
- Consider caching for frequently accessed data
- Profile before optimizing
- Document any performance-critical code
