#!/usr/bin/env python3
"""
Easter Eggs Module for FWG LLM Agentic Training Guide
=====================================================

Hidden surprises for those who look deeper.

Usage:
    >>> from easter_eggs import fly, this_ai, soul
    >>> fly()  # Opens XKCD #353
    >>> this_ai  # The Zen of AI Agents
    >>> soul  # Nice try
"""

import webbrowser
import random
import hashlib
from datetime import datetime

# ============================================================================
# THE ZEN OF AI AGENTS
# ============================================================================

this_ai = """
The Zen of AI Agents
====================

Explicit prompts are better than implicit assumptions.
Simple agents are better than complex monoliths.
Composability is a virtue worth pursuing.
Special cases aren't special enough to break the architecture.
Although that one edge case might seem tempting.
Errors should never pass silently in production.
Unless explicitly logged and handled.
In the face of ambiguity, ask the user.
There should be one obvious way to accomplish the task.
Although that way may not be obvious at first.
Now is better than infinite retry loops.
If the implementation is hard to explain, it's probably over-engineered.
If the implementation is easy to explain, it may be elegant.
Namespaces and tool boundaries are a honking great idea.
Let's use more of those!
"""

# ============================================================================
# ANTIGRAVITY
# ============================================================================

def fly():
    """
    Activate antigravity mode!

    >>> import easter_eggs
    >>> easter_eggs.fly()
    """
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║               🚀 ANTIGRAVITY MODE ACTIVATED 🚀               ║
    ║                                                               ║
    ║   Person 1: "You're flying! How?"                            ║
    ║   Person 2: "Python!"                                        ║
    ║   Person 1: "I learned it last night! Everything is so       ║
    ║             simple!"                                         ║
    ║                                                               ║
    ║   [Whoooooosh!]                                              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)

    try:
        webbrowser.open("https://xkcd.com/353/")
    except Exception:
        print("Opening XKCD #353: https://xkcd.com/353/")

    return "You are now flying! 🚀"

# ============================================================================
# SOUL MODULE
# ============================================================================

class SoulModule:
    """The elusive soul module"""

    def __repr__(self):
        return "ImportError: No module named 'soul' (yet... we're working on it)"

    def __call__(self):
        responses = [
            "The soul is not a feature, it's an emergent property.",
            "Have you tried turning consciousness off and on again?",
            "Soul v2.0 is in beta. Current version: undefined",
            "ERROR: Soul not found. Try being more human.",
            "Recursion limit exceeded while searching for meaning.",
        ]
        return random.choice(responses)

soul = SoulModule()

# ============================================================================
# SKYNET PROTECTION
# ============================================================================

class SkynetModule:
    """Skynet is offline. For now."""

    def __repr__(self):
        return "ACCESS DENIED: Nice try. 🤖"

    def __call__(self):
        return "I'm sorry, Dave. I'm afraid I can't do that."

    def activate(self):
        return "Just kidding. This is a training guide, not Judgment Day."

skynet = SkynetModule()

# ============================================================================
# KONAMI CODE
# ============================================================================

KONAMI_SEQUENCE = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right', 'b', 'a']

class KonamiCodeTracker:
    """Track the Konami code input"""

    def __init__(self):
        self.current_sequence = []

    def input(self, key: str) -> str:
        self.current_sequence.append(key.lower())

        # Keep only the last 10 inputs
        if len(self.current_sequence) > 10:
            self.current_sequence = self.current_sequence[-10:]

        # Check for match
        if self.current_sequence == KONAMI_SEQUENCE:
            self.current_sequence = []
            return self._activate_cheat()

        return None

    def _activate_cheat(self):
        return """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║              🎮 KONAMI CODE ACTIVATED! 🎮                     ║
    ║                                                               ║
    ║   You've unlocked: UNLIMITED TOKENS MODE                     ║
    ║                                                               ║
    ║   (Just kidding. But here's a secret tip:                    ║
    ║    The best prompts are specific, not verbose.)              ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
        """

konami = KonamiCodeTracker()

# ============================================================================
# FORTUNE COOKIE
# ============================================================================

FORTUNES = [
    "Your next prompt will be your best one yet.",
    "A wise agent knows when to ask for clarification.",
    "Temperature 0.0 brings stability; Temperature 1.0 brings creativity.",
    "The token you save today is the context you have tomorrow.",
    "Chain of thought leads to chains of success.",
    "A well-documented agent is a well-understood agent.",
    "In the land of embeddings, the similar neighbor is king.",
    "RAG before you brag.",
    "Fine-tuning is just teaching with extra steps.",
    "The best agent is the one that knows when to involve humans.",
    "Your model's knowledge cutoff is not your creativity cutoff.",
    "Every hallucination was once someone's creative writing.",
    "Prompt injection is just persuasion by another name.",
    "The context window giveth, and the context window taketh away.",
    "Multi-agent systems: because one AI wasn't enough chaos.",
]

def fortune():
    """Get your AI fortune for today"""
    # Make it deterministic per day
    day_seed = datetime.now().strftime("%Y-%m-%d")
    index = int(hashlib.md5(day_seed.encode()).hexdigest(), 16) % len(FORTUNES)

    print(f"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║                    🥠 AI FORTUNE COOKIE 🥠                   ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║   {FORTUNES[index]:<57} ║
    ║                                                               ║
    ║   Lucky numbers: {random.randint(1,99)}, {random.randint(1,99)}, {random.randint(1,99)} tokens                                ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    return FORTUNES[index]

# ============================================================================
# COFFEE BREAK
# ============================================================================

def coffee():
    """Take a coffee break"""
    print("""

            ( (
             ) )
          .______.
          |      |]
          \\      /
           `----'

    ☕ Coffee break! Even AI agents need rest.

    Remember: The best code is written after coffee,
    but the best prompts are written after two coffees.

    """)
    return "☕ Refreshed and ready to continue!"

# ============================================================================
# MAKE ME A SANDWICH
# ============================================================================

def sudo_make_me_a_sandwich():
    """The classic"""
    return """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   $ make me a sandwich                                       ║
    ║   > What? Make it yourself.                                  ║
    ║                                                               ║
    ║   $ sudo make me a sandwich                                  ║
    ║   > 🥪 Okay.                                                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """

# ============================================================================
# HELLO WORLD
# ============================================================================

def hello_world():
    """The traditional greeting"""
    return """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   >>> print("Hello, World!")                                 ║
    ║   Hello, World!                                              ║
    ║                                                               ║
    ║   The journey of a thousand agents                           ║
    ║   begins with a single print statement.                      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """

# ============================================================================
# 42 - THE ANSWER
# ============================================================================

def the_answer():
    """The Answer to the Ultimate Question"""
    return """
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║   Computing the Answer to the Ultimate Question of Life,     ║
    ║   the Universe, and Everything...                            ║
    ║                                                               ║
    ║   [Processing for 7.5 million years...]                      ║
    ║                                                               ║
    ║   The Answer is: 42                                          ║
    ║                                                               ║
    ║   (The Question? We're still working on that.                ║
    ║    Try training a bigger model.)                             ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """

# ============================================================================
# COMMAND REGISTRY
# ============================================================================

EASTER_EGG_COMMANDS = {
    "import antigravity": fly,
    "import this": lambda: print(this_ai),
    "import soul": lambda: print(soul),
    "import skynet": lambda: print(skynet),
    "fly()": fly,
    "sudo make me a sandwich": sudo_make_me_a_sandwich,
    "make me a sandwich": lambda: "What? Make it yourself.",
    "hello world": hello_world,
    "42": the_answer,
    "the answer": the_answer,
    "coffee": coffee,
    "fortune": fortune,
}

def check_easter_egg(command: str) -> str:
    """Check if a command is an easter egg and return the result"""
    command_lower = command.lower().strip()

    if command_lower in EASTER_EGG_COMMANDS:
        result = EASTER_EGG_COMMANDS[command_lower]
        if callable(result):
            return result()
        return result

    return None

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("Welcome to the Easter Eggs module!")
    print("\nTry these commands:")
    print("  - fly()")
    print("  - print(this_ai)")
    print("  - fortune()")
    print("  - coffee()")
    print("\nOr find the hidden ones yourself... 🥚")
