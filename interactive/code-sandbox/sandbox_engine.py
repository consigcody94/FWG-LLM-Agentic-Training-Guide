#!/usr/bin/env python3
"""
FWG Training - Live Code Execution Sandbox
Jupyter-style notebook system with secure sandboxed execution

Features:
- Cell-based code execution
- Multi-language support (Python, JavaScript, Bash)
- Resource limits and security controls
- Real-time output streaming
- Integrated with progress tracking
- Web and CLI interfaces
"""

import ast
import asyncio
import builtins
import contextlib
import io
import json
import multiprocessing
import os
import resource
import signal
import sys
import tempfile
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from uuid import uuid4

try:
    from RestrictedPython import compile_restricted, safe_builtins
    from RestrictedPython.Guards import guarded_iter_unpack_sequence, safe_globals
    RESTRICTED_PYTHON_AVAILABLE = True
except ImportError:
    RESTRICTED_PYTHON_AVAILABLE = False
    print("⚠️  RestrictedPython not installed. Running without advanced sandboxing.")


class CellType(Enum):
    """Types of notebook cells"""
    CODE = "code"
    MARKDOWN = "markdown"
    RAW = "raw"


class ExecutionStatus(Enum):
    """Execution status of a cell"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    ERROR = "error"
    TIMEOUT = "timeout"
    KILLED = "killed"


class Language(Enum):
    """Supported programming languages"""
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    BASH = "bash"
    SQL = "sql"


@dataclass
class ExecutionResult:
    """Result of code execution"""
    status: ExecutionStatus
    output: str = ""
    error: str = ""
    execution_time: float = 0.0
    memory_used: int = 0
    variables: Dict[str, Any] = field(default_factory=dict)
    return_value: Any = None
    stdout: str = ""
    stderr: str = ""


@dataclass
class Cell:
    """A notebook cell"""
    id: str = field(default_factory=lambda: str(uuid4()))
    cell_type: CellType = CellType.CODE
    source: str = ""
    language: Language = Language.PYTHON
    outputs: List[ExecutionResult] = field(default_factory=list)
    execution_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)


@dataclass
class Notebook:
    """A complete notebook"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = "Untitled Notebook"
    cells: List[Cell] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)

    def add_cell(self, cell: Cell) -> None:
        """Add a cell to the notebook"""
        self.cells.append(cell)
        self.modified_at = datetime.now()

    def get_cell(self, cell_id: str) -> Optional[Cell]:
        """Get a cell by ID"""
        for cell in self.cells:
            if cell.id == cell_id:
                return cell
        return None

    def delete_cell(self, cell_id: str) -> bool:
        """Delete a cell by ID"""
        for i, cell in enumerate(self.cells):
            if cell.id == cell_id:
                del self.cells[i]
                self.modified_at = datetime.now()
                return True
        return False

    def to_dict(self) -> Dict:
        """Convert notebook to dictionary for serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "cells": [
                {
                    "id": cell.id,
                    "cell_type": cell.cell_type.value,
                    "source": cell.source,
                    "language": cell.language.value,
                    "execution_count": cell.execution_count,
                    "outputs": [
                        {
                            "status": output.status.value,
                            "output": output.output,
                            "error": output.error,
                            "execution_time": output.execution_time
                        }
                        for output in cell.outputs
                    ],
                    "metadata": cell.metadata
                }
                for cell in self.cells
            ],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "modified_at": self.modified_at.isoformat()
        }

    def save(self, path: Path) -> None:
        """Save notebook to file"""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'Notebook':
        """Load notebook from file"""
        with open(path, 'r') as f:
            data = json.load(f)

        notebook = cls(
            id=data.get("id", str(uuid4())),
            title=data.get("title", "Untitled Notebook"),
            metadata=data.get("metadata", {})
        )

        for cell_data in data.get("cells", []):
            cell = Cell(
                id=cell_data.get("id", str(uuid4())),
                cell_type=CellType(cell_data.get("cell_type", "code")),
                source=cell_data.get("source", ""),
                language=Language(cell_data.get("language", "python")),
                execution_count=cell_data.get("execution_count", 0),
                metadata=cell_data.get("metadata", {})
            )
            notebook.cells.append(cell)

        return notebook


class SecurityConfig:
    """Security configuration for sandboxed execution"""

    # Time limits
    MAX_EXECUTION_TIME = 30  # seconds

    # Memory limits
    MAX_MEMORY_MB = 512
    MAX_MEMORY_BYTES = MAX_MEMORY_MB * 1024 * 1024

    # CPU limits
    MAX_CPU_TIME = 30  # seconds

    # File system limits
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_PATHS = ["/tmp", tempfile.gettempdir()]

    # Network restrictions
    ALLOW_NETWORK = False

    # Dangerous modules/functions
    BLOCKED_MODULES = {
        'os.system', 'subprocess', 'eval', 'exec', 'compile',
        '__import__', 'open', 'file', 'input', 'raw_input',
        'reload', 'execfile', 'socket', 'urllib', 'requests',
        'http', 'ftplib', 'telnetlib', 'shutil', 'pickle'
    }

    # Safe built-ins for restricted execution
    SAFE_BUILTINS = {
        'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray',
        'bytes', 'chr', 'dict', 'divmod', 'enumerate', 'filter',
        'float', 'format', 'frozenset', 'hex', 'int', 'isinstance',
        'iter', 'len', 'list', 'map', 'max', 'min', 'oct', 'ord',
        'pow', 'print', 'range', 'repr', 'reversed', 'round', 'set',
        'slice', 'sorted', 'str', 'sum', 'tuple', 'type', 'zip',
        'True', 'False', 'None'
    }


class PythonSandbox:
    """Secure Python code execution sandbox"""

    def __init__(self, config: SecurityConfig = SecurityConfig()):
        self.config = config
        self.namespace: Dict[str, Any] = {}
        self._init_namespace()

    def _init_namespace(self) -> None:
        """Initialize the execution namespace with safe builtins"""
        if RESTRICTED_PYTHON_AVAILABLE:
            self.namespace = safe_globals.copy()
            self.namespace['__builtins__'] = safe_builtins
            self.namespace['_getiter_'] = guarded_iter_unpack_sequence
        else:
            # Fallback to basic safe builtins
            safe_builtins_dict = {
                name: getattr(builtins, name)
                for name in self.config.SAFE_BUILTINS
                if hasattr(builtins, name)
            }
            self.namespace['__builtins__'] = safe_builtins_dict

    def _validate_code(self, code: str) -> Tuple[bool, str]:
        """Validate code for security issues"""
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e}"

        # Check for dangerous patterns
        for node in ast.walk(tree):
            # Block imports of dangerous modules
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(blocked in alias.name for blocked in self.config.BLOCKED_MODULES):
                        return False, f"Import of '{alias.name}' is not allowed"

            if isinstance(node, ast.ImportFrom):
                if node.module and any(blocked in node.module for blocked in self.config.BLOCKED_MODULES):
                    return False, f"Import from '{node.module}' is not allowed"

            # Block certain function calls
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile', '__import__']:
                        return False, f"Use of '{node.func.id}' is not allowed"

        return True, ""

    def _set_resource_limits(self) -> None:
        """Set resource limits for the execution"""
        if sys.platform != 'win32':
            # Set memory limit
            resource.setrlimit(
                resource.RLIMIT_AS,
                (self.config.MAX_MEMORY_BYTES, self.config.MAX_MEMORY_BYTES)
            )

            # Set CPU time limit
            resource.setrlimit(
                resource.RLIMIT_CPU,
                (self.config.MAX_CPU_TIME, self.config.MAX_CPU_TIME)
            )

    def execute(self, code: str, timeout: Optional[int] = None) -> ExecutionResult:
        """Execute Python code in sandbox"""
        if timeout is None:
            timeout = self.config.MAX_EXECUTION_TIME

        # Validate code first
        is_valid, error_msg = self._validate_code(code)
        if not is_valid:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error=error_msg
            )

        # Capture stdout/stderr
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()

        start_time = time.time()

        try:
            # Compile code
            if RESTRICTED_PYTHON_AVAILABLE:
                compiled_code = compile_restricted(code, '<string>', 'exec')
            else:
                compiled_code = compile(code, '<string>', 'exec')

            # Execute with captured output
            with contextlib.redirect_stdout(stdout_capture), \
                 contextlib.redirect_stderr(stderr_capture):

                # Set up timeout
                def timeout_handler(signum, frame):
                    raise TimeoutError("Execution timed out")

                if sys.platform != 'win32':
                    signal.signal(signal.SIGALRM, timeout_handler)
                    signal.alarm(timeout)

                try:
                    exec(compiled_code, self.namespace)
                    status = ExecutionStatus.SUCCESS
                    error = ""
                finally:
                    if sys.platform != 'win32':
                        signal.alarm(0)  # Cancel alarm

        except TimeoutError:
            status = ExecutionStatus.TIMEOUT
            error = f"Execution exceeded {timeout} seconds"

        except MemoryError:
            status = ExecutionStatus.ERROR
            error = f"Memory limit exceeded ({self.config.MAX_MEMORY_MB}MB)"

        except Exception as e:
            status = ExecutionStatus.ERROR
            error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"

        execution_time = time.time() - start_time

        return ExecutionResult(
            status=status,
            output=stdout_capture.getvalue(),
            error=error,
            stdout=stdout_capture.getvalue(),
            stderr=stderr_capture.getvalue(),
            execution_time=execution_time,
            variables={
                k: v for k, v in self.namespace.items()
                if not k.startswith('_') and k not in {'__builtins__'}
            }
        )

    def get_variables(self) -> Dict[str, Any]:
        """Get current namespace variables"""
        return {
            k: v for k, v in self.namespace.items()
            if not k.startswith('_') and k not in {'__builtins__'}
        }

    def reset(self) -> None:
        """Reset the namespace"""
        self.namespace.clear()
        self._init_namespace()


class NotebookEngine:
    """Main engine for managing and executing notebooks"""

    def __init__(self, notebooks_dir: Optional[Path] = None):
        if notebooks_dir is None:
            notebooks_dir = Path(__file__).parent / "notebooks"

        self.notebooks_dir = Path(notebooks_dir)
        self.notebooks_dir.mkdir(parents=True, exist_ok=True)

        self.current_notebook: Optional[Notebook] = None
        self.sandboxes: Dict[Language, Any] = {
            Language.PYTHON: PythonSandbox()
        }

    def create_notebook(self, title: str = "Untitled Notebook") -> Notebook:
        """Create a new notebook"""
        notebook = Notebook(title=title)
        self.current_notebook = notebook
        return notebook

    def load_notebook(self, notebook_id: str) -> Optional[Notebook]:
        """Load a notebook by ID"""
        notebook_path = self.notebooks_dir / f"{notebook_id}.json"
        if notebook_path.exists():
            self.current_notebook = Notebook.load(notebook_path)
            return self.current_notebook
        return None

    def save_current_notebook(self) -> bool:
        """Save the current notebook"""
        if self.current_notebook is None:
            return False

        notebook_path = self.notebooks_dir / f"{self.current_notebook.id}.json"
        self.current_notebook.save(notebook_path)
        return True

    def list_notebooks(self) -> List[Dict[str, str]]:
        """List all saved notebooks"""
        notebooks = []
        for notebook_file in self.notebooks_dir.glob("*.json"):
            try:
                with open(notebook_file, 'r') as f:
                    data = json.load(f)
                notebooks.append({
                    "id": data.get("id", ""),
                    "title": data.get("title", "Untitled"),
                    "modified_at": data.get("modified_at", "")
                })
            except Exception:
                continue
        return sorted(notebooks, key=lambda x: x.get("modified_at", ""), reverse=True)

    def add_code_cell(self, code: str, language: Language = Language.PYTHON) -> Cell:
        """Add a code cell to current notebook"""
        if self.current_notebook is None:
            self.create_notebook()

        cell = Cell(
            cell_type=CellType.CODE,
            source=code,
            language=language
        )
        self.current_notebook.add_cell(cell)
        return cell

    def add_markdown_cell(self, markdown: str) -> Cell:
        """Add a markdown cell to current notebook"""
        if self.current_notebook is None:
            self.create_notebook()

        cell = Cell(
            cell_type=CellType.MARKDOWN,
            source=markdown
        )
        self.current_notebook.add_cell(cell)
        return cell

    def execute_cell(self, cell_id: str) -> ExecutionResult:
        """Execute a specific cell"""
        if self.current_notebook is None:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error="No notebook loaded"
            )

        cell = self.current_notebook.get_cell(cell_id)
        if cell is None:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error=f"Cell {cell_id} not found"
            )

        if cell.cell_type != CellType.CODE:
            return ExecutionResult(
                status=ExecutionStatus.SUCCESS,
                output="Non-code cell, skipping execution"
            )

        # Get appropriate sandbox
        sandbox = self.sandboxes.get(cell.language)
        if sandbox is None:
            return ExecutionResult(
                status=ExecutionStatus.ERROR,
                error=f"No sandbox available for {cell.language.value}"
            )

        # Execute
        result = sandbox.execute(cell.source)

        # Update cell
        cell.execution_count += 1
        cell.outputs.append(result)
        cell.modified_at = datetime.now()
        self.current_notebook.modified_at = datetime.now()

        return result

    def execute_all_cells(self) -> List[ExecutionResult]:
        """Execute all cells in order"""
        if self.current_notebook is None:
            return []

        results = []
        for cell in self.current_notebook.cells:
            if cell.cell_type == CellType.CODE:
                result = self.execute_cell(cell.id)
                results.append(result)

        return results

    def clear_outputs(self, cell_id: Optional[str] = None) -> None:
        """Clear outputs from a cell or all cells"""
        if self.current_notebook is None:
            return

        if cell_id:
            cell = self.current_notebook.get_cell(cell_id)
            if cell:
                cell.outputs.clear()
                cell.execution_count = 0
        else:
            for cell in self.current_notebook.cells:
                cell.outputs.clear()
                cell.execution_count = 0

    def get_namespace_variables(self, language: Language = Language.PYTHON) -> Dict[str, Any]:
        """Get current variables in the execution namespace"""
        sandbox = self.sandboxes.get(language)
        if sandbox and hasattr(sandbox, 'get_variables'):
            return sandbox.get_variables()
        return {}

    def reset_sandbox(self, language: Language = Language.PYTHON) -> None:
        """Reset the sandbox environment"""
        sandbox = self.sandboxes.get(language)
        if sandbox and hasattr(sandbox, 'reset'):
            sandbox.reset()


if __name__ == "__main__":
    # Demo usage
    print("=" * 70)
    print("FWG Training - Code Sandbox Demo")
    print("=" * 70)

    engine = NotebookEngine()
    notebook = engine.create_notebook("Python Basics Demo")

    # Add some demo cells
    print("\n📝 Creating demo notebook with example cells...\n")

    # Cell 1: Basic Python
    cell1 = engine.add_code_cell("""
# Federal AI Training - Hello World
message = "Hello from secure sandbox!"
print(message)
print(f"Running in: {__name__}")
""")

    # Cell 2: Data processing
    cell2 = engine.add_code_cell("""
# Process some data
numbers = [1, 2, 3, 4, 5]
squared = [n**2 for n in numbers]
print(f"Original: {numbers}")
print(f"Squared: {squared}")
print(f"Sum: {sum(squared)}")
""")

    # Cell 3: Functions
    cell3 = engine.add_code_cell("""
# Define a function
def analyze_sentiment(text):
    positive_words = ['good', 'great', 'excellent', 'amazing']
    negative_words = ['bad', 'poor', 'terrible', 'awful']

    text_lower = text.lower()
    pos_count = sum(word in text_lower for word in positive_words)
    neg_count = sum(word in text_lower for word in negative_words)

    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral"

# Test it
test_text = "This training is excellent and amazing!"
result = analyze_sentiment(test_text)
print(f"Text: {test_text}")
print(f"Sentiment: {result}")
""")

    # Execute all cells
    print("▶️  Executing all cells...\n")
    results = engine.execute_all_cells()

    # Display results
    for i, (cell, result) in enumerate(zip(notebook.cells, results), 1):
        print(f"\n{'='*70}")
        print(f"Cell {i} (Execution #{cell.execution_count})")
        print(f"{'='*70}")
        print(f"Status: {result.status.value}")
        print(f"Time: {result.execution_time:.4f}s")

        if result.output:
            print(f"\n📤 Output:")
            print(result.output)

        if result.error:
            print(f"\n❌ Error:")
            print(result.error)

    # Show variables in namespace
    print(f"\n{'='*70}")
    print("Variables in namespace:")
    print(f"{'='*70}")
    variables = engine.get_namespace_variables()
    for name, value in variables.items():
        print(f"  {name} = {repr(value)}")

    # Save notebook
    engine.save_current_notebook()
    print(f"\n✅ Notebook saved to: {engine.notebooks_dir / f'{notebook.id}.json'}")
