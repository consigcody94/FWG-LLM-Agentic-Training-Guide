#!/usr/bin/env python3
"""
Example 01: Simple Chatbot
A multi-provider conversational AI application.
"""

import os
import sys
import argparse
import logging
from typing import Optional
from dataclasses import dataclass
from datetime import datetime

from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


# =============================================================================
# Configuration
# =============================================================================

@dataclass
class Config:
    """Application configuration."""
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    system_prompt: str = """You are a helpful AI assistant for Federal Working Group.
You provide accurate, concise information while following federal guidelines.
You are professional, respectful, and security-conscious."""


# =============================================================================
# Provider Implementations
# =============================================================================

class LLMProvider:
    """Base class for LLM providers."""

    def chat(self, messages: list, stream: bool = False) -> str:
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    """OpenAI provider implementation."""

    def __init__(self, config: Config):
        from openai import OpenAI
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.config = config
        self.model = config.model if config.model else "gpt-4o-mini"

    def chat(self, messages: list, stream: bool = False) -> str:
        if stream:
            return self._stream_chat(messages)
        else:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content

    def _stream_chat(self, messages: list) -> str:
        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            stream=True
        )
        full_response = ""
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                print(content, end="", flush=True)
                full_response += content
        print()  # Newline at end
        return full_response


class AnthropicProvider(LLMProvider):
    """Anthropic provider implementation."""

    def __init__(self, config: Config):
        import anthropic
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.config = config
        self.model = config.model if config.model else "claude-3-5-sonnet-20241022"

    def chat(self, messages: list, stream: bool = False) -> str:
        # Extract system prompt and messages
        system = ""
        user_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                user_messages.append(msg)

        if stream:
            return self._stream_chat(system, user_messages)
        else:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.config.max_tokens,
                system=system,
                messages=user_messages
            )
            return response.content[0].text

    def _stream_chat(self, system: str, messages: list) -> str:
        with self.client.messages.stream(
            model=self.model,
            max_tokens=self.config.max_tokens,
            system=system,
            messages=messages
        ) as stream:
            full_response = ""
            for text in stream.text_stream:
                print(text, end="", flush=True)
                full_response += text
            print()
            return full_response


class OllamaProvider(LLMProvider):
    """Ollama provider implementation."""

    def __init__(self, config: Config):
        import ollama
        self.client = ollama
        self.config = config
        self.model = config.model if config.model else "llama3.2"

    def chat(self, messages: list, stream: bool = False) -> str:
        if stream:
            return self._stream_chat(messages)
        else:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response["message"]["content"]

    def _stream_chat(self, messages: list) -> str:
        stream = self.client.chat(
            model=self.model,
            messages=messages,
            stream=True
        )
        full_response = ""
        for chunk in stream:
            content = chunk["message"]["content"]
            print(content, end="", flush=True)
            full_response += content
        print()
        return full_response


def get_provider(name: str, config: Config) -> LLMProvider:
    """Factory function to get the appropriate provider."""
    providers = {
        "openai": OpenAIProvider,
        "anthropic": AnthropicProvider,
        "ollama": OllamaProvider
    }

    if name not in providers:
        raise ValueError(f"Unknown provider: {name}. Available: {list(providers.keys())}")

    return providers[name](config)


# =============================================================================
# Chat Application
# =============================================================================

class ChatApp:
    """Main chat application."""

    def __init__(self, provider: LLMProvider, config: Config):
        self.provider = provider
        self.config = config
        self.messages = [
            {"role": "system", "content": config.system_prompt}
        ]
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def chat(self, user_input: str, stream: bool = True) -> str:
        """Process a user message and return the response."""
        # Log the interaction (sanitized)
        logger.info(f"User input received, length: {len(user_input)}")

        # Add user message to history
        self.messages.append({"role": "user", "content": user_input})

        try:
            # Get response from LLM
            response = self.provider.chat(self.messages, stream=stream)

            # Add assistant response to history
            self.messages.append({"role": "assistant", "content": response})

            # Log success
            logger.info(f"Response generated, length: {len(response)}")

            return response

        except Exception as e:
            logger.error(f"Chat error: {type(e).__name__}: {e}")
            raise

    def clear_history(self):
        """Clear conversation history."""
        self.messages = [
            {"role": "system", "content": self.config.system_prompt}
        ]
        logger.info("Conversation history cleared")


# =============================================================================
# Main Application
# =============================================================================

def print_banner():
    """Print application banner."""
    print("""
╔══════════════════════════════════════════════════════════════╗
║               FWG Simple Chatbot Example                     ║
║                                                              ║
║  Commands:                                                   ║
║    /clear  - Clear conversation history                      ║
║    /exit   - Exit the application                            ║
║    /help   - Show this help                                  ║
╚══════════════════════════════════════════════════════════════╝
    """)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Simple Chatbot Example")
    parser.add_argument(
        "--provider",
        choices=["openai", "anthropic", "ollama"],
        default="openai",
        help="LLM provider to use"
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Model to use (provider-specific)"
    )
    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Disable streaming responses"
    )
    args = parser.parse_args()

    # Initialize configuration
    config = Config(
        provider=args.provider,
        model=args.model
    )

    # Initialize provider
    try:
        provider = get_provider(args.provider, config)
        logger.info(f"Initialized {args.provider} provider")
    except Exception as e:
        print(f"Error initializing provider: {e}")
        sys.exit(1)

    # Initialize chat application
    app = ChatApp(provider, config)

    # Print banner
    print_banner()
    print(f"Using provider: {args.provider}")
    print("-" * 60)

    # Main loop
    while True:
        try:
            # Get user input
            user_input = input("\n👤 You: ").strip()

            if not user_input:
                continue

            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                if command == "/exit":
                    print("Goodbye!")
                    break
                elif command == "/clear":
                    app.clear_history()
                    print("Conversation history cleared.")
                    continue
                elif command == "/help":
                    print_banner()
                    continue
                else:
                    print(f"Unknown command: {command}")
                    continue

            # Get and display response
            print("\n🤖 Assistant: ", end="")
            app.chat(user_input, stream=not args.no_stream)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            logger.exception("Error during chat")


if __name__ == "__main__":
    main()
