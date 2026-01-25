---
name: generate-tests
description: Generate comprehensive unit tests for selected code
trigger: /generate-tests
---

# Generate Unit Tests

Analyze the selected code and generate comprehensive unit tests.

## Test Framework Selection

- **Python**: Use pytest with fixtures
- **JavaScript**: Use Jest with describe/it blocks
- **TypeScript**: Use Jest with type-safe mocks

## Test Categories

For each function/method, create tests for:

### 1. Happy Path
- Expected inputs produce expected outputs
- Normal use cases work correctly

### 2. Edge Cases
- Empty inputs (empty strings, empty arrays, None/null)
- Boundary values (0, -1, MAX_INT, empty collections)
- Single element collections
- Unicode and special characters

### 3. Error Conditions
- Invalid inputs (wrong types, out of range)
- Missing required parameters
- Exception handling verification

## Test Structure

### Python (pytest)
```python
import pytest
from module import function_under_test

class TestFunctionUnderTest:
    """Tests for function_under_test."""

    @pytest.fixture
    def sample_data(self):
        """Provide sample test data."""
        return {"key": "value"}

    def test_should_return_expected_when_valid_input(self, sample_data):
        """Verify normal operation with valid input."""
        result = function_under_test(sample_data)
        assert result == expected_value

    def test_should_raise_error_when_invalid_input(self):
        """Verify error handling for invalid input."""
        with pytest.raises(ValueError, match="Invalid input"):
            function_under_test(None)

    @pytest.mark.parametrize("input_val,expected", [
        ("a", 1),
        ("b", 2),
        ("c", 3),
    ])
    def test_should_handle_multiple_cases(self, input_val, expected):
        """Verify handling of various inputs."""
        assert function_under_test(input_val) == expected
```

### JavaScript (Jest)
```javascript
describe('functionUnderTest', () => {
  let mockDependency;

  beforeEach(() => {
    mockDependency = jest.fn();
  });

  it('should return expected result for valid input', () => {
    const result = functionUnderTest('valid');
    expect(result).toBe(expectedValue);
  });

  it('should throw error for invalid input', () => {
    expect(() => functionUnderTest(null)).toThrow('Invalid input');
  });

  it.each([
    ['a', 1],
    ['b', 2],
    ['c', 3],
  ])('should handle input %s and return %d', (input, expected) => {
    expect(functionUnderTest(input)).toBe(expected);
  });
});
```

## Coverage Goals

- Aim for >90% code coverage
- Test all public functions/methods
- Test all code branches (if/else paths)
- Test all error handling paths

## Mock Guidelines

- Mock external API calls
- Mock database operations
- Mock file system operations
- Mock time-dependent functions
- Use dependency injection to facilitate mocking

## Output

- Create test file in appropriate tests/ directory
- Follow naming convention: `test_<module_name>.py` or `<module_name>.test.js`
- Include setup/teardown as needed
- Add docstrings/comments explaining complex tests
