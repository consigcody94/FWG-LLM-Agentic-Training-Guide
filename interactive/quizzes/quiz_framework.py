#!/usr/bin/env python3
"""
Interactive Quiz Framework for FWG LLM Training
Provides engaging, gamified knowledge assessment with instant feedback
"""

import json
import time
import random
from typing import List, Dict, Optional, Any
from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import sys


# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


@dataclass
class Question:
    """Base class for quiz questions"""
    question: str
    explanation: str
    points: int = 10
    reference: Optional[str] = None
    tags: List[str] = None


@dataclass
class MultipleChoice(Question):
    """Multiple choice question"""
    options: List[str]
    correct: int  # Index of correct answer

    def check_answer(self, answer: int) -> bool:
        return answer == self.correct


@dataclass
class TrueFalse(Question):
    """True/False question"""
    correct: bool

    def check_answer(self, answer: bool) -> bool:
        return answer == self.correct


@dataclass
class FillInBlank(Question):
    """Fill in the blank question"""
    correct_answers: List[str]  # Multiple acceptable answers

    def check_answer(self, answer: str) -> bool:
        return answer.strip().lower() in [a.lower() for a in self.correct_answers]


@dataclass
class CodeChallenge(Question):
    """Code completion challenge"""
    starter_code: str
    test_cases: List[Dict[str, Any]]
    hints: List[str] = None

    def check_answer(self, code: str) -> bool:
        # In a real implementation, this would execute the code safely
        # For now, we'll just check if it's not empty
        return len(code.strip()) > 0


class Quiz:
    """Interactive quiz with gamification"""

    def __init__(
        self,
        title: str,
        module: str,
        difficulty: str = "intermediate",
        time_limit: Optional[int] = None,
        passing_score: int = 70
    ):
        self.title = title
        self.module = module
        self.difficulty = difficulty
        self.time_limit = time_limit  # in minutes
        self.passing_score = passing_score
        self.questions: List[Question] = []
        self.answers = []
        self.start_time = None
        self.score = 0
        self.total_points = 0

    def add_question(self, question: Question):
        """Add a question to the quiz"""
        self.questions.append(question)
        self.total_points += question.points

    def print_header(self):
        """Print quiz header with styling"""
        print("\n" + "="*70)
        print(f"{Colors.BOLD}{Colors.CYAN}{self.title}{Colors.END}")
        print("="*70)
        print(f"{Colors.YELLOW}Module:{Colors.END} {self.module}")
        print(f"{Colors.YELLOW}Difficulty:{Colors.END} {self.difficulty}")
        print(f"{Colors.YELLOW}Questions:{Colors.END} {len(self.questions)}")
        print(f"{Colors.YELLOW}Total Points:{Colors.END} {self.total_points}")
        if self.time_limit:
            print(f"{Colors.YELLOW}Time Limit:{Colors.END} {self.time_limit} minutes")
        print(f"{Colors.YELLOW}Passing Score:{Colors.END} {self.passing_score}%")
        print("="*70 + "\n")

    def print_question(self, idx: int, question: Question):
        """Print a formatted question"""
        print(f"\n{Colors.BOLD}Question {idx + 1} of {len(self.questions)}{Colors.END}")
        print(f"{Colors.CYAN}[{question.points} points]{Colors.END}\n")
        print(f"{question.question}\n")

        if isinstance(question, MultipleChoice):
            for i, option in enumerate(question.options):
                letter = chr(65 + i)  # A, B, C, D...
                print(f"  {letter}) {option}")
        elif isinstance(question, TrueFalse):
            print(f"  A) True")
            print(f"  B) False")
        elif isinstance(question, FillInBlank):
            print(f"  (Type your answer)")
        elif isinstance(question, CodeChallenge):
            print(f"{Colors.MAGENTA}Code Challenge:{Colors.END}")
            print(f"```python")
            print(question.starter_code)
            print(f"```")
            if question.hints:
                print(f"\n{Colors.YELLOW}💡 Hints available (type 'hint' for a clue){Colors.END}")

    def get_answer(self, question: Question) -> Any:
        """Get user's answer with validation"""
        while True:
            if isinstance(question, MultipleChoice):
                answer = input(f"\n{Colors.BOLD}Your answer (A-{chr(65 + len(question.options) - 1)}):{Colors.END} ").strip().upper()
                if answer and answer[0] in [chr(65 + i) for i in range(len(question.options))]:
                    return ord(answer[0]) - 65  # Convert A,B,C to 0,1,2
                print(f"{Colors.RED}Invalid input. Please enter a letter (A-{chr(65 + len(question.options) - 1)}){Colors.END}")

            elif isinstance(question, TrueFalse):
                answer = input(f"\n{Colors.BOLD}Your answer (A=True, B=False):{Colors.END} ").strip().upper()
                if answer in ['A', 'B']:
                    return answer == 'A'
                print(f"{Colors.RED}Invalid input. Please enter A or B{Colors.END}")

            elif isinstance(question, FillInBlank):
                answer = input(f"\n{Colors.BOLD}Your answer:{Colors.END} ").strip()
                if answer:
                    return answer
                print(f"{Colors.RED}Please provide an answer{Colors.END}")

            elif isinstance(question, CodeChallenge):
                print(f"\n{Colors.YELLOW}Enter your code (type 'END' on a new line when done):{Colors.END}")
                lines = []
                while True:
                    line = input()
                    if line.strip() == 'END':
                        break
                    lines.append(line)
                return '\n'.join(lines)

    def show_feedback(self, is_correct: bool, question: Question, answer: Any):
        """Show immediate feedback for the answer"""
        if is_correct:
            print(f"\n{Colors.GREEN}✅ Correct!{Colors.END}")
            self.score += question.points

            # Fun positive reinforcement
            encouragements = [
                "Excellent work!",
                "You're on fire! 🔥",
                "Keep it up!",
                "Federal AI expert in the making!",
                "Outstanding!",
            ]
            print(f"{Colors.GREEN}{random.choice(encouragements)}{Colors.END}")
        else:
            print(f"\n{Colors.RED}❌ Incorrect{Colors.END}")

            # Show correct answer for MC and T/F
            if isinstance(question, MultipleChoice):
                correct_letter = chr(65 + question.correct)
                print(f"{Colors.YELLOW}Correct answer: {correct_letter}) {question.options[question.correct]}{Colors.END}")

        # Always show explanation
        print(f"\n{Colors.CYAN}📚 Explanation:{Colors.END}")
        print(f"{question.explanation}")

        # Show reference if available
        if question.reference:
            print(f"\n{Colors.MAGENTA}📖 Reference:{Colors.END} {question.reference}")

        # Show progress
        percentage = int((self.score / self.total_points) * 100) if self.total_points > 0 else 0
        print(f"\n{Colors.BOLD}Score: {self.score}/{self.total_points} ({percentage}%){Colors.END}")

        # Progress bar
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        print(f"{Colors.GREEN}{bar}{Colors.END} {percentage}%")

        print("\n" + "-"*70)
        time.sleep(1)  # Brief pause before next question

    def show_final_results(self):
        """Display final quiz results"""
        percentage = int((self.score / self.total_points) * 100) if self.total_points > 0 else 0
        passed = percentage >= self.passing_score

        print("\n" + "="*70)
        print(f"{Colors.BOLD}{Colors.CYAN}QUIZ COMPLETE!{Colors.END}")
        print("="*70 + "\n")

        print(f"{Colors.BOLD}Final Score: {self.score}/{self.total_points} ({percentage}%){Colors.END}\n")

        # Visual score representation
        bar_length = 50
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        color = Colors.GREEN if passed else Colors.RED
        print(f"{color}{bar}{Colors.END} {percentage}%\n")

        # Pass/Fail status
        if passed:
            print(f"{Colors.GREEN}✅ PASSED{Colors.END}")
            print(f"\n{Colors.BOLD}🎉 Congratulations!{Colors.END}")
            print(f"You've demonstrated mastery of {self.module} material.")

            # Badge earned
            if percentage >= 90:
                badge = "🥇 GOLD BADGE"
                xp = "100 XP"
            elif percentage >= 80:
                badge = "🥈 SILVER BADGE"
                xp = "75 XP"
            else:
                badge = "🥉 BRONZE BADGE"
                xp = "50 XP"

            print(f"\n{Colors.YELLOW}Badge Earned: {badge}{Colors.END}")
            print(f"{Colors.CYAN}XP Gained: {xp}{Colors.END}")
        else:
            print(f"{Colors.RED}❌ NOT PASSED{Colors.END}")
            print(f"\nYou need {self.passing_score}% to pass (you scored {percentage}%).")
            print(f"\n{Colors.YELLOW}Don't give up! Review the material and try again.{Colors.END}")
            print(f"Focus on the questions you missed.")

        # Performance breakdown
        print(f"\n{Colors.BOLD}Performance Breakdown:{Colors.END}")
        questions_correct = sum(1 for a in self.answers if a)
        questions_total = len(self.questions)
        print(f"  Questions correct: {questions_correct}/{questions_total}")
        print(f"  Points earned: {self.score}/{self.total_points}")

        if self.start_time:
            elapsed = int((time.time() - self.start_time) / 60)
            print(f"  Time taken: {elapsed} minutes")

        # Recommendations
        print(f"\n{Colors.BOLD}Next Steps:{Colors.END}")
        if passed:
            next_module = int(self.module) + 1 if self.module.isdigit() else "next"
            print(f"  ✅ Complete the hands-on lab for this module")
            print(f"  ✅ Move on to Module {next_module:02d}")
        else:
            print(f"  📖 Review the module documentation")
            print(f"  💡 Focus on topics you missed")
            print(f"  🔄 Retake the quiz when ready")

        print("\n" + "="*70 + "\n")

    def run(self):
        """Run the interactive quiz"""
        self.start_time = time.time()
        self.print_header()

        # Shuffle questions for variety
        if input(f"{Colors.YELLOW}Randomize question order? (y/n):{Colors.END} ").lower() == 'y':
            random.shuffle(self.questions)

        print(f"\n{Colors.GREEN}Starting quiz... Good luck! 🍀{Colors.END}")
        print(f"\nPress Enter to begin...")
        input()

        # Ask each question
        for idx, question in enumerate(self.questions):
            self.print_question(idx, question)
            answer = self.get_answer(question)

            # Check answer
            if isinstance(question, MultipleChoice):
                is_correct = question.check_answer(answer)
            elif isinstance(question, TrueFalse):
                is_correct = question.check_answer(answer)
            elif isinstance(question, FillInBlank):
                is_correct = question.check_answer(answer)
            elif isinstance(question, CodeChallenge):
                is_correct = question.check_answer(answer)
            else:
                is_correct = False

            self.answers.append(is_correct)
            self.show_feedback(is_correct, question, answer)

        # Show final results
        self.show_final_results()

        # Save progress
        self.save_progress()

    def save_progress(self):
        """Save quiz results to progress tracker"""
        progress_dir = Path(__file__).parent.parent / "progress-tracking"
        progress_dir.mkdir(exist_ok=True)

        progress_file = progress_dir / "progress.json"

        # Load existing progress
        if progress_file.exists():
            with open(progress_file) as f:
                progress = json.load(f)
        else:
            progress = {"quizzes": [], "total_xp": 0}

        # Add this quiz result
        percentage = int((self.score / self.total_points) * 100) if self.total_points > 0 else 0

        # Calculate XP
        if percentage >= 90:
            xp = 100
        elif percentage >= 80:
            xp = 75
        elif percentage >= 70:
            xp = 50
        else:
            xp = 25

        progress["quizzes"].append({
            "module": self.module,
            "title": self.title,
            "score": self.score,
            "total": self.total_points,
            "percentage": percentage,
            "passed": percentage >= self.passing_score,
            "xp_earned": xp,
            "date": datetime.now().isoformat(),
            "time_spent": int((time.time() - self.start_time) / 60) if self.start_time else 0
        })

        progress["total_xp"] += xp

        # Save updated progress
        with open(progress_file, 'w') as f:
            json.dump(progress, f, indent=2)


# Example usage
if __name__ == "__main__":
    # Demo quiz
    quiz = Quiz(
        title="Demo Quiz - Getting Started",
        module="00",
        difficulty="beginner",
        passing_score=70
    )

    quiz.add_question(MultipleChoice(
        question="What is the primary purpose of this training guide?",
        options=[
            "To teach traditional programming",
            "To provide AI agent training for federal employees",
            "To learn web development",
            "To study cybersecurity"
        ],
        correct=1,
        explanation="This training guide is specifically designed to teach federal employees about LLM agentic systems.",
        points=10
    ))

    quiz.add_question(TrueFalse(
        question="Large Language Models always give deterministic outputs (same input = same output)",
        correct=False,
        explanation="LLMs are probabilistic and can give slightly different outputs for the same input due to temperature and sampling settings.",
        points=10
    ))

    print(f"{Colors.BOLD}{Colors.GREEN}FWG Interactive Quiz System{Colors.END}\n")
    print("This is a demo quiz to showcase the framework.")
    print(f"\nTo start, run: {Colors.CYAN}quiz.run(){Colors.END}\n")
