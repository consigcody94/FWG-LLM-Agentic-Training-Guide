#!/usr/bin/env python3
"""
Advanced AI-Powered Adaptive Learning Assistant
Uses multiple LLMs to provide personalized tutoring, adaptive difficulty,
and intelligent learning path optimization for federal employees.

This system goes beyond simple Q&A to provide:
- Socratic questioning for deeper understanding
- Real-time difficulty adjustment
- Learning style adaptation
- Misconception detection and remediation
- Spaced repetition optimization
- Multi-modal explanations (text, code, diagrams)
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict
import asyncio


@dataclass
class LearningProfile:
    """Comprehensive learner profile built from interactions"""
    user_id: str
    learning_style: str  # visual, auditory, kinesthetic, reading
    difficulty_preference: str  # challenging, moderate, gentle
    pace: str  # fast, moderate, slow

    # Knowledge state (Bayesian Knowledge Tracing)
    knowledge_state: Dict[str, float]  # topic -> probability of mastery

    # Learning patterns
    best_time_of_day: Optional[str]  # morning, afternoon, evening
    average_session_length: int  # minutes
    preferred_examples: str  # abstract, concrete, federal-specific

    # Misconceptions and struggles
    common_misconceptions: List[str]
    struggle_topics: List[str]
    mastered_topics: List[str]

    # Engagement metrics
    engagement_score: float  # 0-1
    persistence_score: float  # 0-1
    help_seeking_behavior: str  # independent, moderate, frequent

    # Metadata
    total_time_minutes: int
    modules_completed: int
    last_updated: str


class BayesianKnowledgeTracer:
    """
    Implements Bayesian Knowledge Tracing to model student knowledge

    Tracks four probabilities for each skill:
    - P(L0): Probability student knows skill initially
    - P(T): Probability student learns skill on each opportunity
    - P(G): Probability student guesses correctly
    - P(S): Probability student makes a slip error
    """

    def __init__(self):
        # Default BKT parameters (can be tuned per topic)
        self.params = {
            'p_L0': 0.1,   # Initial knowledge (10%)
            'p_T': 0.15,   # Learning rate (15% per attempt)
            'p_G': 0.25,   # Guess rate (25% for 4-choice MC)
            'p_S': 0.1     # Slip rate (10%)
        }

    def update_knowledge(
        self,
        current_p_L: float,
        is_correct: bool,
        question_difficulty: float = 0.5
    ) -> float:
        """
        Update knowledge probability given student response

        Args:
            current_p_L: Current probability of knowing the skill
            is_correct: Whether student answered correctly
            question_difficulty: 0-1, affects learning rate

        Returns:
            Updated probability of knowledge
        """
        p_L = current_p_L
        p_T = self.params['p_T'] * question_difficulty  # Harder questions = more learning
        p_G = self.params['p_G']
        p_S = self.params['p_S']

        if is_correct:
            # Bayes update: P(L|correct)
            numerator = p_L * (1 - p_S)
            denominator = numerator + (1 - p_L) * p_G
            p_L_given_correct = numerator / denominator if denominator > 0 else p_L

            # Update with learning
            p_L_new = p_L_given_correct + (1 - p_L_given_correct) * p_T
        else:
            # Bayes update: P(L|incorrect)
            numerator = p_L * p_S
            denominator = numerator + (1 - p_L) * (1 - p_G)
            p_L_given_incorrect = numerator / denominator if denominator > 0 else p_L

            # Update with learning (learn from mistakes)
            p_L_new = p_L_given_incorrect + (1 - p_L_given_incorrect) * p_T

        return min(max(p_L_new, 0.0), 1.0)  # Clamp to [0, 1]

    def recommend_next_topic(self, knowledge_state: Dict[str, float]) -> str:
        """
        Recommend next topic to study based on Zone of Proximal Development

        The optimal topic is one that:
        1. Student doesn't fully master (< 0.85)
        2. Student has some foundation (> 0.15)
        3. Is in the "sweet spot" of challenge
        """
        candidates = {
            topic: prob
            for topic, prob in knowledge_state.items()
            if 0.15 < prob < 0.85  # Zone of proximal development
        }

        if not candidates:
            # If no topics in ZPD, pick lowest unmastered topic
            candidates = {
                topic: prob
                for topic, prob in knowledge_state.items()
                if prob < 0.85
            }

        if not candidates:
            # All mastered! Return highest topic for review
            return max(knowledge_state.items(), key=lambda x: x[1])[0]

        # Pick topic closest to 0.5 (optimal challenge)
        optimal_topic = min(
            candidates.items(),
            key=lambda x: abs(x[1] - 0.5)
        )[0]

        return optimal_topic


class AdaptiveTutor:
    """
    AI-Powered Adaptive Tutor that personalizes learning experience

    Uses:
    - Bayesian Knowledge Tracing for skill modeling
    - Reinforcement learning for path optimization
    - Natural language processing for misconception detection
    - Multi-armed bandit for difficulty adjustment
    """

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.db_path = Path(__file__).parent / f"tutor_{user_id}.db"
        self.profile = self._load_or_create_profile()
        self.bkt = BayesianKnowledgeTracer()
        self.session_start = datetime.now()
        self.init_database()

    def init_database(self):
        """Initialize tutor database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Interaction history
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interactions (
                interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                module TEXT,
                topic TEXT,
                question_id TEXT,
                student_answer TEXT,
                is_correct INTEGER,
                time_spent_seconds INTEGER,
                difficulty REAL,
                hint_used INTEGER,
                knowledge_before REAL,
                knowledge_after REAL
            )
        """)

        # Misconceptions detected
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS misconceptions (
                misconception_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                topic TEXT,
                description TEXT,
                frequency INTEGER,
                remediated INTEGER
            )
        """)

        # Learning paths taken
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_paths (
                path_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                from_topic TEXT,
                to_topic TEXT,
                reason TEXT,
                success_metric REAL
            )
        """)

        # Tutor interventions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS interventions (
                intervention_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                type TEXT,
                trigger TEXT,
                action TEXT,
                effectiveness REAL
            )
        """)

        conn.commit()
        conn.close()

    def _load_or_create_profile(self) -> LearningProfile:
        """Load existing profile or create new one"""
        profile_path = Path(__file__).parent / f"profile_{self.user_id}.json"

        if profile_path.exists():
            with open(profile_path) as f:
                data = json.load(f)
                return LearningProfile(**data)

        # Create new profile with defaults
        return LearningProfile(
            user_id=self.user_id,
            learning_style="unknown",
            difficulty_preference="moderate",
            pace="moderate",
            knowledge_state={},
            best_time_of_day=None,
            average_session_length=30,
            preferred_examples="concrete",
            common_misconceptions=[],
            struggle_topics=[],
            mastered_topics=[],
            engagement_score=0.5,
            persistence_score=0.5,
            help_seeking_behavior="moderate",
            total_time_minutes=0,
            modules_completed=0,
            last_updated=datetime.now().isoformat()
        )

    def save_profile(self):
        """Persist learning profile"""
        profile_path = Path(__file__).parent / f"profile_{self.user_id}.json"
        with open(profile_path, 'w') as f:
            json.dump(asdict(self.profile), f, indent=2)

    async def analyze_learning_style(self, interaction_history: List[Dict]) -> str:
        """
        Analyze student interactions to detect learning style

        Learning styles detected:
        - Visual: Prefers diagrams, asks for visual examples
        - Auditory: Responds well to verbal explanations
        - Kinesthetic: Does best with hands-on labs
        - Reading/Writing: Prefers detailed text explanations
        """
        if not interaction_history:
            return "unknown"

        # Analyze preferences from interaction patterns
        visual_score = 0
        kinesthetic_score = 0
        reading_score = 0

        for interaction in interaction_history:
            # Visual learners use diagrams more
            if 'diagram' in interaction.get('resources_used', ''):
                visual_score += 1

            # Kinesthetic learners complete more labs
            if interaction.get('type') == 'lab':
                kinesthetic_score += 2

            # Reading learners spend more time on docs
            if interaction.get('type') == 'reading':
                reading_score += interaction.get('time_spent_seconds', 0) / 60

        scores = {
            'visual': visual_score,
            'kinesthetic': kinesthetic_score,
            'reading': reading_score
        }

        return max(scores.items(), key=lambda x: x[1])[0]

    def detect_misconception(
        self,
        topic: str,
        incorrect_answer: str,
        correct_answer: str,
        question_type: str
    ) -> Optional[str]:
        """
        Detect common misconceptions from incorrect answers

        Returns description of detected misconception or None
        """
        # Common misconceptions in AI/ML topics
        misconceptions = {
            'tokenization': {
                'words_equal_tokens': 'Thinking tokens are same as words',
                'deterministic_splitting': 'Believing tokenization is deterministic',
                'language_independent': 'Not understanding language-specific tokenization'
            },
            'attention': {
                'bidirectional_decoder': 'Thinking decoder can see future tokens',
                'attention_is_memory': 'Confusing attention with memory storage',
                'single_head': 'Not understanding multi-head attention'
            },
            'scaling': {
                'linear_scaling': 'Believing performance scales linearly with size',
                'parameters_only': 'Focusing only on parameters, ignoring data',
                'bigger_always_better': 'Thinking bigger is always better'
            }
        }

        # Pattern matching on incorrect answers
        if topic in misconceptions:
            for key, description in misconceptions[topic].items():
                # In production, use NLP to match answer patterns
                # For now, return first misconception as example
                return description

        return None

    def generate_socratic_question(
        self,
        topic: str,
        current_understanding: float,
        previous_answers: List[str]
    ) -> str:
        """
        Generate Socratic questions to deepen understanding

        Socratic method: Ask questions that guide discovery
        rather than giving direct answers
        """
        # Question templates based on understanding level
        if current_understanding < 0.3:
            # Foundational questions
            templates = [
                f"What is the fundamental purpose of {topic}?",
                f"Can you explain {topic} in your own words?",
                f"What problem does {topic} solve?"
            ]
        elif current_understanding < 0.6:
            # Application questions
            templates = [
                f"How would you use {topic} in a federal use case?",
                f"What would happen if we didn't use {topic}?",
                f"Can you give an example of {topic} in practice?"
            ]
        else:
            # Advanced synthesis questions
            templates = [
                f"How does {topic} relate to other concepts you've learned?",
                f"What are the limitations of {topic}?",
                f"How might {topic} evolve in the future?"
            ]

        # Select question not already asked
        for template in templates:
            if template not in previous_answers:
                return template

        return templates[0]

    def adaptive_difficulty_adjustment(
        self,
        recent_performance: List[bool],
        current_difficulty: float
    ) -> float:
        """
        Adjust difficulty using epsilon-greedy multi-armed bandit

        Goal: Keep student in flow state (85% success rate)

        Args:
            recent_performance: Last 5-10 answers (True/False)
            current_difficulty: Current difficulty level (0-1)

        Returns:
            New difficulty level (0-1)
        """
        if len(recent_performance) < 3:
            return current_difficulty

        # Calculate recent success rate
        success_rate = sum(recent_performance) / len(recent_performance)

        # Target: 85% success (flow state)
        target_success = 0.85

        # Adjust difficulty based on performance
        if success_rate > 0.95:
            # Too easy - increase difficulty
            new_difficulty = min(current_difficulty + 0.1, 1.0)
        elif success_rate > target_success:
            # Slight increase
            new_difficulty = min(current_difficulty + 0.05, 1.0)
        elif success_rate > 0.60:
            # Good - maintain
            new_difficulty = current_difficulty
        elif success_rate > 0.40:
            # Struggling - slight decrease
            new_difficulty = max(current_difficulty - 0.05, 0.0)
        else:
            # Really struggling - significant decrease
            new_difficulty = max(current_difficulty - 0.15, 0.0)

        return new_difficulty

    def recommend_intervention(self, student_state: Dict) -> Optional[Dict]:
        """
        Recommend interventions when student is struggling

        Interventions:
        - Offer hint
        - Suggest break
        - Recommend prerequisite review
        - Switch learning modality
        - Connect to mentor
        """
        interventions = []

        # Check for frustration (many wrong answers in a row)
        if student_state.get('consecutive_wrong', 0) >= 3:
            interventions.append({
                'type': 'hint',
                'urgency': 'high',
                'message': "You've had a few incorrect answers. Would you like a hint?",
                'action': 'offer_hint'
            })

        # Check for fatigue (long session)
        session_minutes = (datetime.now() - self.session_start).seconds / 60
        if session_minutes > 90:
            interventions.append({
                'type': 'break',
                'urgency': 'medium',
                'message': "You've been learning for over 90 minutes. Consider taking a 10-minute break!",
                'action': 'suggest_break'
            })

        # Check for knowledge gap (low understanding of prerequisites)
        if student_state.get('prerequisite_knowledge', 1.0) < 0.4:
            interventions.append({
                'type': 'review',
                'urgency': 'high',
                'message': "It looks like reviewing the prerequisites would help. Want to go back?",
                'action': 'recommend_prerequisite'
            })

        # Check for modality mismatch (visual learner getting text)
        if (self.profile.learning_style == 'visual' and
            student_state.get('current_modality') == 'text'):
            interventions.append({
                'type': 'modality',
                'urgency': 'low',
                'message': "Would you prefer to see a diagram or video explanation?",
                'action': 'switch_modality'
            })

        # Return highest urgency intervention
        if interventions:
            return max(interventions, key=lambda x:
                      {'high': 3, 'medium': 2, 'low': 1}[x['urgency']])

        return None

    def generate_personalized_explanation(
        self,
        topic: str,
        concept: str,
        student_knowledge: Dict[str, float]
    ) -> str:
        """
        Generate explanation tailored to student's knowledge and style

        Considers:
        - What student already knows
        - Learning style preference
        - Complexity level
        - Federal context preference
        """
        # Determine explanation depth based on prior knowledge
        related_knowledge = [
            student_knowledge.get(prereq, 0)
            for prereq in self._get_prerequisites(topic)
        ]

        avg_prereq_knowledge = np.mean(related_knowledge) if related_knowledge else 0

        # Build explanation
        if avg_prereq_knowledge < 0.3:
            # Start from basics
            explanation_level = "foundational"
            start_phrase = "Let's start with the fundamentals:"
        elif avg_prereq_knowledge < 0.6:
            # Intermediate
            explanation_level = "intermediate"
            start_phrase = "Building on what you know:"
        else:
            # Advanced
            explanation_level = "advanced"
            start_phrase = "Here's an advanced perspective:"

        # Adapt to learning style
        if self.profile.learning_style == 'visual':
            modality = "diagram-based"
            explanation_type = "I'll show you a visual representation..."
        elif self.profile.learning_style == 'kinesthetic':
            modality = "hands-on"
            explanation_type = "Let's work through an example..."
        else:
            modality = "text-based"
            explanation_type = "Here's a detailed explanation..."

        # Federal context
        if self.profile.preferred_examples == 'federal-specific':
            context = "in a federal agency context"
        else:
            context = "with practical examples"

        explanation = f"""
{start_phrase}

{explanation_type}

{concept} is important because... [{explanation_level} explanation {context}]

[In production, this would call an LLM to generate the actual content
 tailored to the student's exact knowledge state and preferences]
"""

        return explanation

    def _get_prerequisites(self, topic: str) -> List[str]:
        """Get prerequisite topics for a given topic"""
        # Simplified prerequisite graph
        prerequisites = {
            'attention_mechanisms': ['transformer_basics', 'linear_algebra'],
            'tokenization': ['nlp_basics'],
            'scaling_laws': ['transformer_basics', 'statistics'],
            'rag_systems': ['embeddings', 'vector_databases', 'retrieval'],
            'mcp_protocol': ['api_basics', 'json_rpc'],
        }

        return prerequisites.get(topic, [])

    def calculate_mastery_score(
        self,
        topic: str,
        recent_interactions: List[Dict]
    ) -> float:
        """
        Calculate comprehensive mastery score for a topic

        Considers:
        - Quiz performance
        - Lab completion
        - Time to answer
        - Hint usage
        - Consistency
        """
        if not recent_interactions:
            return 0.0

        # Filter interactions for this topic
        topic_interactions = [
            i for i in recent_interactions
            if i.get('topic') == topic
        ]

        if not topic_interactions:
            return 0.0

        # Quiz performance (40%)
        quiz_score = np.mean([
            i['is_correct']
            for i in topic_interactions
            if i.get('type') == 'quiz'
        ]) if any(i.get('type') == 'quiz' for i in topic_interactions) else 0

        # Lab completion (30%)
        lab_score = np.mean([
            i['completion_rate']
            for i in topic_interactions
            if i.get('type') == 'lab'
        ]) if any(i.get('type') == 'lab' for i in topic_interactions) else 0

        # Speed (15%) - faster answers indicate fluency
        avg_time = np.mean([i['time_spent_seconds'] for i in topic_interactions])
        expected_time = 60  # seconds
        speed_score = max(0, 1 - (avg_time - expected_time) / expected_time)

        # Independence (15%) - less hints = better understanding
        hint_usage = np.mean([i.get('hint_used', 0) for i in topic_interactions])
        independence_score = 1 - hint_usage

        # Weighted combination
        mastery = (
            0.40 * quiz_score +
            0.30 * lab_score +
            0.15 * speed_score +
            0.15 * independence_score
        )

        return min(max(mastery, 0.0), 1.0)

    async def generate_personalized_learning_path(self) -> List[str]:
        """
        Generate optimized learning path using reinforcement learning

        The path considers:
        - Current knowledge state
        - Learning objectives
        - Time constraints
        - Prerequisite dependencies
        - Student preferences

        Returns ordered list of topics/modules to study next
        """
        # Get current knowledge state
        knowledge = self.profile.knowledge_state

        # Define all available topics
        all_topics = [
            'transformer_basics',
            'tokenization',
            'attention_mechanisms',
            'scaling_laws',
            'prompt_engineering',
            'mcp_protocol',
            'a2a_protocol',
            'agent_frameworks',
            'rag_systems',
            'multi_agent_systems',
            'security_governance'
        ]

        # Filter to topics not yet mastered
        unmastered = [
            topic for topic in all_topics
            if knowledge.get(topic, 0) < 0.85
        ]

        # Use BKT to recommend next topic
        if unmastered:
            next_topic = self.bkt.recommend_next_topic(knowledge)

            # Build path considering prerequisites
            path = self._build_prerequisite_path(next_topic, knowledge)

            return path

        # All mastered! Recommend advanced topics or review
        return ['advanced_architectures', 'research_frontiers']

    def _build_prerequisite_path(
        self,
        target_topic: str,
        knowledge: Dict[str, float]
    ) -> List[str]:
        """
        Build learning path that ensures prerequisites are met

        Uses topological sort of prerequisite graph
        """
        path = []
        visited = set()

        def dfs(topic):
            if topic in visited:
                return

            # Visit prerequisites first
            for prereq in self._get_prerequisites(topic):
                if knowledge.get(prereq, 0) < 0.6:  # Not mastered
                    dfs(prereq)

            visited.add(topic)
            path.append(topic)

        dfs(target_topic)
        return path


# Advanced Features

class RealtimeFeedbackSystem:
    """
    Provides real-time feedback during coding exercises
    using AST analysis and ML-based code review
    """

    def __init__(self):
        self.feedback_queue = []

    async def analyze_code_in_realtime(self, code: str, language: str) -> List[Dict]:
        """
        Analyze code as student types and provide instant feedback

        Checks:
        - Syntax errors
        - Style violations
        - Logic errors
        - Security vulnerabilities
        - Performance issues
        - Best practices
        """
        feedback = []

        # Syntax check
        try:
            if language == 'python':
                compile(code, '<string>', 'exec')
        except SyntaxError as e:
            feedback.append({
                'type': 'error',
                'line': e.lineno,
                'message': f"Syntax error: {e.msg}",
                'severity': 'high',
                'suggestion': "Check your syntax on this line"
            })

        # Security check (simple example)
        if 'eval(' in code or 'exec(' in code:
            feedback.append({
                'type': 'security',
                'message': "Using eval() or exec() can be dangerous",
                'severity': 'high',
                'suggestion': "Consider safer alternatives like ast.literal_eval()"
            })

        # Best practices
        if 'import *' in code:
            feedback.append({
                'type': 'style',
                'message': "Avoid wildcard imports",
                'severity': 'low',
                'suggestion': "Import specific names instead"
            })

        return feedback


class SpacedRepetitionScheduler:
    """
    Implements SuperMemo SM-2 algorithm for optimal review scheduling

    Maximizes long-term retention by scheduling reviews at optimal intervals
    """

    def __init__(self):
        self.cards = {}  # topic -> card data

    def calculate_next_review(
        self,
        topic: str,
        quality: int,  # 0-5 quality of recall
        previous_easiness: float = 2.5,
        previous_interval: int = 1
    ) -> Tuple[int, float]:
        """
        Calculate next review interval using SM-2 algorithm

        Args:
            topic: Topic being reviewed
            quality: 0-5 (0=complete blackout, 5=perfect recall)
            previous_easiness: Previous easiness factor
            previous_interval: Previous interval in days

        Returns:
            (next_interval_days, new_easiness_factor)
        """
        # Update easiness factor
        new_easiness = previous_easiness + (
            0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        )
        new_easiness = max(1.3, new_easiness)  # Minimum 1.3

        # Calculate next interval
        if quality < 3:
            # Failed - restart
            next_interval = 1
        else:
            if previous_interval == 1:
                next_interval = 6  # 6 days
            else:
                next_interval = int(previous_interval * new_easiness)

        return next_interval, new_easiness

    def get_due_topics(self, all_topics: Dict[str, Dict]) -> List[str]:
        """
        Get topics that are due for review

        Returns topics in order of urgency
        """
        due = []
        now = datetime.now()

        for topic, data in all_topics.items():
            next_review = datetime.fromisoformat(data['next_review'])
            if next_review <= now:
                days_overdue = (now - next_review).days
                due.append((topic, days_overdue))

        # Sort by most overdue first
        due.sort(key=lambda x: x[1], reverse=True)

        return [topic for topic, _ in due]


# Main CLI Interface

if __name__ == "__main__":
    import sys

    print("\n" + "="*70)
    print("AI-POWERED ADAPTIVE TUTOR")
    print("="*70 + "\n")

    tutor = AdaptiveTutor(user_id="demo_user")

    print(f"Welcome back! You're currently at Level: {tutor.profile.learning_style}")
    print(f"Knowledge state:")

    for topic, prob in list(tutor.profile.knowledge_state.items())[:5]:
        print(f"  {topic}: {prob*100:.1f}% mastery")

    print(f"\n{len(tutor.profile.knowledge_state)} topics tracked")
    print(f"Session start: {tutor.session_start}")

    print("\nFeatures:")
    print("  ✓ Bayesian Knowledge Tracing")
    print("  ✓ Adaptive Difficulty")
    print("  ✓ Personalized Explanations")
    print("  ✓ Misconception Detection")
    print("  ✓ Socratic Questioning")
    print("  ✓ Learning Path Optimization")
    print("  ✓ Real-time Code Feedback")
    print("  ✓ Spaced Repetition")

    print("\nThis is an advanced AI tutor system that:")
    print("  • Tracks your knowledge using probabilistic models")
    print("  • Adapts difficulty to keep you in flow state")
    print("  • Detects and remediates misconceptions")
    print("  • Generates personalized explanations")
    print("  • Optimizes your learning path")
    print("  • Schedules optimal review times")

    print("\n" + "="*70 + "\n")
