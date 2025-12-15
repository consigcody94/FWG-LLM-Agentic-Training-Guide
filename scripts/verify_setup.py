#!/usr/bin/env python3
"""
FWG LLM Agentic Training Guide - Setup Verification Script

This script verifies that all required dependencies and tools are
properly installed for the training exercises.

Usage:
    python scripts/verify_setup.py
"""

import subprocess
import sys
import shutil
from typing import Tuple, List

# ANSI color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_header():
    """Print verification header."""
    print(f"""
{BOLD}╔══════════════════════════════════════════════════════════════╗
║     FWG LLM Agentic Training Guide - Setup Verification       ║
╚══════════════════════════════════════════════════════════════╝{RESET}
""")

def check_python_version() -> Tuple[bool, str]:
    """Check Python version is 3.11+."""
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    return False, f"Python {version.major}.{version.minor}.{version.micro} (3.11+ required)"

def check_command(command: str, version_flag: str = "--version") -> Tuple[bool, str]:
    """Check if a command is available."""
    path = shutil.which(command)
    if path:
        try:
            result = subprocess.run(
                [command, version_flag],
                capture_output=True,
                text=True,
                timeout=10
            )
            version = result.stdout.strip() or result.stderr.strip()
            # Get first line only
            version = version.split('\n')[0][:50]
            return True, version
        except Exception as e:
            return True, f"Found at {path}"
    return False, "Not installed"

def check_python_package(package: str) -> Tuple[bool, str]:
    """Check if a Python package is installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-c", f"import {package}; print({package}.__version__ if hasattr({package}, '__version__') else 'installed')"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "Not installed"
    except Exception:
        return False, "Not installed"

def check_ollama_models() -> List[str]:
    """Check installed Ollama models."""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = [line.split()[0] for line in lines if line.strip()]
            return models
    except Exception:
        pass
    return []

def print_result(name: str, passed: bool, detail: str = ""):
    """Print a check result."""
    status = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
    detail_str = f" ({detail})" if detail else ""
    print(f"  {status} {name}{detail_str}")

def main():
    """Run all verification checks."""
    print_header()

    all_passed = True

    # System Requirements
    print(f"{BOLD}System Requirements:{RESET}")

    passed, detail = check_python_version()
    print_result("Python 3.11+", passed, detail)
    all_passed = all_passed and passed

    passed, detail = check_command("node", "--version")
    print_result("Node.js", passed, detail)

    passed, detail = check_command("git", "--version")
    print_result("Git", passed, detail)
    all_passed = all_passed and passed

    print()

    # LLM Tools
    print(f"{BOLD}LLM Tools:{RESET}")

    passed, detail = check_command("ollama", "--version")
    print_result("Ollama", passed, detail)

    if passed:
        models = check_ollama_models()
        if models:
            print(f"    Models: {', '.join(models[:5])}")
            if len(models) > 5:
                print(f"    ... and {len(models) - 5} more")
        else:
            print(f"    {YELLOW}No models installed. Run: ollama pull llama3.2{RESET}")

    passed, detail = check_command("claude", "--version")
    print_result("Claude Code CLI", passed, detail)

    print()

    # Python Packages
    print(f"{BOLD}Python Packages:{RESET}")

    packages = [
        ("openai", "openai"),
        ("anthropic", "anthropic"),
        ("langchain", "langchain"),
        ("fastapi", "fastapi"),
        ("pydantic", "pydantic"),
        ("httpx", "httpx"),
        ("tiktoken", "tiktoken"),
    ]

    for name, import_name in packages:
        passed, detail = check_python_package(import_name)
        print_result(name, passed, detail)
        if not passed:
            all_passed = False

    print()

    # API Keys (check if environment variables are set)
    print(f"{BOLD}Environment Variables (API Keys):{RESET}")

    import os
    api_keys = [
        ("OPENAI_API_KEY", "OpenAI"),
        ("ANTHROPIC_API_KEY", "Anthropic"),
        ("GOOGLE_API_KEY", "Google AI"),
    ]

    for env_var, name in api_keys:
        value = os.environ.get(env_var)
        if value:
            masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "***"
            print_result(f"{name} ({env_var})", True, masked)
        else:
            print_result(f"{name} ({env_var})", False, "Not set")

    print()

    # Summary
    print(f"{BOLD}{'─' * 60}{RESET}")
    if all_passed:
        print(f"{GREEN}{BOLD}✓ All required checks passed!{RESET}")
        print(f"\nYou're ready to start the training exercises.")
    else:
        print(f"{YELLOW}{BOLD}⚠ Some checks failed.{RESET}")
        print(f"\nPlease install missing dependencies before proceeding.")
        print(f"Run: pip install -r requirements.txt")

    print()
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
