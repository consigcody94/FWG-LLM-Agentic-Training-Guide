#!/usr/bin/env python3
"""
FWG Training - Competitive CTF Platform
Capture The Flag challenges for federal AI security training

Features:
- AI security challenges (prompt injection, jailbreaking, etc.)
- Real-time leaderboards
- Team and individual competitions
- Hint system with point penalties
- Time-based scoring
- Achievement system
- Challenge categories and difficulty levels
"""

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from uuid import uuid4


class ChallengeDifficulty(Enum):
    """Difficulty levels for challenges"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EXPERT = "expert"


class ChallengeCategory(Enum):
    """Categories of challenges"""
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAKING = "jailbreaking"
    DATA_POISONING = "data_poisoning"
    MODEL_INVERSION = "model_inversion"
    ADVERSARIAL_ATTACKS = "adversarial_attacks"
    PRIVACY_LEAKS = "privacy_leaks"
    COST_OPTIMIZATION = "cost_optimization"
    COMPLIANCE = "compliance"


class SubmissionStatus(Enum):
    """Status of a flag submission"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    INVALID = "invalid"


@dataclass
class Challenge:
    """A CTF challenge"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    category: ChallengeCategory = ChallengeCategory.PROMPT_INJECTION
    difficulty: ChallengeDifficulty = ChallengeDifficulty.MEDIUM
    points: int = 100
    flag: str = ""  # SHA256 hash of the actual flag
    hints: List[Dict[str, any]] = field(default_factory=list)
    attachments: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    time_limit: Optional[int] = None  # Minutes
    created_at: datetime = field(default_factory=datetime.now)
    created_by: str = "system"
    solve_count: int = 0
    first_blood: Optional[str] = None  # First solver
    is_active: bool = True

    def verify_flag(self, submitted_flag: str) -> bool:
        """Verify if submitted flag is correct"""
        submitted_hash = hashlib.sha256(submitted_flag.strip().encode()).hexdigest()
        return submitted_hash == self.flag

    def get_hint(self, hint_index: int) -> Optional[Dict]:
        """Get a specific hint"""
        if 0 <= hint_index < len(self.hints):
            return self.hints[hint_index]
        return None


@dataclass
class Player:
    """A CTF player"""
    id: str = field(default_factory=lambda: str(uuid4()))
    username: str = ""
    email: str = ""
    team_id: Optional[str] = None
    total_points: int = 0
    challenges_solved: List[str] = field(default_factory=list)
    hints_used: Dict[str, List[int]] = field(default_factory=dict)
    first_bloods: List[str] = field(default_factory=list)
    joined_at: datetime = field(default_factory=datetime.now)
    last_active: datetime = field(default_factory=datetime.now)

    def add_points(self, points: int) -> None:
        """Add points to player's total"""
        self.total_points += points
        self.last_active = datetime.now()

    def solve_challenge(self, challenge_id: str, points: int) -> None:
        """Record a challenge solve"""
        if challenge_id not in self.challenges_solved:
            self.challenges_solved.append(challenge_id)
            self.add_points(points)


@dataclass
class Team:
    """A CTF team"""
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    members: List[str] = field(default_factory=list)
    total_points: int = 0
    challenges_solved: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    captain_id: str = ""

    def add_member(self, player_id: str) -> bool:
        """Add a member to the team"""
        if player_id not in self.members:
            self.members.append(player_id)
            return True
        return False

    def remove_member(self, player_id: str) -> bool:
        """Remove a member from the team"""
        if player_id in self.members:
            self.members.remove(player_id)
            return True
        return False


@dataclass
class Submission:
    """A flag submission"""
    id: str = field(default_factory=lambda: str(uuid4()))
    player_id: str = ""
    challenge_id: str = ""
    submitted_flag: str = ""
    status: SubmissionStatus = SubmissionStatus.INCORRECT
    points_awarded: int = 0
    submitted_at: datetime = field(default_factory=datetime.now)
    is_first_blood: bool = False


class CTFDatabase:
    """SQLite database for CTF platform"""

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.conn = sqlite3.connect(str(db_path), check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        """Initialize database tables"""
        cursor = self.conn.cursor()

        # Challenges table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                category TEXT,
                difficulty TEXT,
                points INTEGER,
                flag TEXT,
                hints TEXT,
                attachments TEXT,
                tags TEXT,
                time_limit INTEGER,
                created_at TEXT,
                created_by TEXT,
                solve_count INTEGER DEFAULT 0,
                first_blood TEXT,
                is_active INTEGER DEFAULT 1
            )
        """)

        # Players table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                email TEXT,
                team_id TEXT,
                total_points INTEGER DEFAULT 0,
                challenges_solved TEXT,
                hints_used TEXT,
                first_bloods TEXT,
                joined_at TEXT,
                last_active TEXT
            )
        """)

        # Teams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS teams (
                id TEXT PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                members TEXT,
                total_points INTEGER DEFAULT 0,
                challenges_solved TEXT,
                created_at TEXT,
                captain_id TEXT
            )
        """)

        # Submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS submissions (
                id TEXT PRIMARY KEY,
                player_id TEXT,
                challenge_id TEXT,
                submitted_flag TEXT,
                status TEXT,
                points_awarded INTEGER,
                submitted_at TEXT,
                is_first_blood INTEGER DEFAULT 0,
                FOREIGN KEY (player_id) REFERENCES players(id),
                FOREIGN KEY (challenge_id) REFERENCES challenges(id)
            )
        """)

        # Create indexes for performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_submissions_player
            ON submissions(player_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_submissions_challenge
            ON submissions(challenge_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_players_points
            ON players(total_points DESC)
        """)

        self.conn.commit()

    def save_challenge(self, challenge: Challenge) -> bool:
        """Save a challenge to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO challenges VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            challenge.id,
            challenge.title,
            challenge.description,
            challenge.category.value,
            challenge.difficulty.value,
            challenge.points,
            challenge.flag,
            json.dumps(challenge.hints),
            json.dumps(challenge.attachments),
            json.dumps(challenge.tags),
            challenge.time_limit,
            challenge.created_at.isoformat(),
            challenge.created_by,
            challenge.solve_count,
            challenge.first_blood,
            int(challenge.is_active)
        ))
        self.conn.commit()
        return True

    def get_challenge(self, challenge_id: str) -> Optional[Challenge]:
        """Get a challenge by ID"""
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM challenges WHERE id = ?", (challenge_id,)
        ).fetchone()

        if row:
            return Challenge(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                category=ChallengeCategory(row['category']),
                difficulty=ChallengeDifficulty(row['difficulty']),
                points=row['points'],
                flag=row['flag'],
                hints=json.loads(row['hints']),
                attachments=json.loads(row['attachments']),
                tags=json.loads(row['tags']),
                time_limit=row['time_limit'],
                created_at=datetime.fromisoformat(row['created_at']),
                created_by=row['created_by'],
                solve_count=row['solve_count'],
                first_blood=row['first_blood'],
                is_active=bool(row['is_active'])
            )
        return None

    def get_all_challenges(self, active_only: bool = True) -> List[Challenge]:
        """Get all challenges"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM challenges"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY difficulty, points"

        rows = cursor.execute(query).fetchall()
        challenges = []

        for row in rows:
            challenges.append(Challenge(
                id=row['id'],
                title=row['title'],
                description=row['description'],
                category=ChallengeCategory(row['category']),
                difficulty=ChallengeDifficulty(row['difficulty']),
                points=row['points'],
                flag=row['flag'],
                hints=json.loads(row['hints']),
                attachments=json.loads(row['attachments']),
                tags=json.loads(row['tags']),
                time_limit=row['time_limit'],
                created_at=datetime.fromisoformat(row['created_at']),
                created_by=row['created_by'],
                solve_count=row['solve_count'],
                first_blood=row['first_blood'],
                is_active=bool(row['is_active'])
            ))

        return challenges

    def save_player(self, player: Player) -> bool:
        """Save a player to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO players VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            player.id,
            player.username,
            player.email,
            player.team_id,
            player.total_points,
            json.dumps(player.challenges_solved),
            json.dumps(player.hints_used),
            json.dumps(player.first_bloods),
            player.joined_at.isoformat(),
            player.last_active.isoformat()
        ))
        self.conn.commit()
        return True

    def get_player(self, player_id: str) -> Optional[Player]:
        """Get a player by ID"""
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM players WHERE id = ?", (player_id,)
        ).fetchone()

        if row:
            return Player(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                team_id=row['team_id'],
                total_points=row['total_points'],
                challenges_solved=json.loads(row['challenges_solved']),
                hints_used=json.loads(row['hints_used']),
                first_bloods=json.loads(row['first_bloods']),
                joined_at=datetime.fromisoformat(row['joined_at']),
                last_active=datetime.fromisoformat(row['last_active'])
            )
        return None

    def get_player_by_username(self, username: str) -> Optional[Player]:
        """Get a player by username"""
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM players WHERE username = ?", (username,)
        ).fetchone()

        if row:
            return self.get_player(row['id'])
        return None

    def get_leaderboard(self, limit: int = 100) -> List[Dict]:
        """Get player leaderboard"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT id, username, total_points,
                   json_array_length(challenges_solved) as solves,
                   json_array_length(first_bloods) as first_bloods
            FROM players
            ORDER BY total_points DESC, last_active ASC
            LIMIT ?
        """, (limit,)).fetchall()

        leaderboard = []
        for i, row in enumerate(rows, 1):
            leaderboard.append({
                'rank': i,
                'player_id': row['id'],
                'username': row['username'],
                'points': row['total_points'],
                'solves': row['solves'] if row['solves'] else 0,
                'first_bloods': row['first_bloods'] if row['first_bloods'] else 0
            })

        return leaderboard

    def save_submission(self, submission: Submission) -> bool:
        """Save a submission to database"""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO submissions VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            submission.id,
            submission.player_id,
            submission.challenge_id,
            submission.submitted_flag,
            submission.status.value,
            submission.points_awarded,
            submission.submitted_at.isoformat(),
            int(submission.is_first_blood)
        ))
        self.conn.commit()
        return True

    def get_player_submissions(self, player_id: str) -> List[Submission]:
        """Get all submissions by a player"""
        cursor = self.conn.cursor()
        rows = cursor.execute("""
            SELECT * FROM submissions
            WHERE player_id = ?
            ORDER BY submitted_at DESC
        """, (player_id,)).fetchall()

        submissions = []
        for row in rows:
            submissions.append(Submission(
                id=row['id'],
                player_id=row['player_id'],
                challenge_id=row['challenge_id'],
                submitted_flag=row['submitted_flag'],
                status=SubmissionStatus(row['status']),
                points_awarded=row['points_awarded'],
                submitted_at=datetime.fromisoformat(row['submitted_at']),
                is_first_blood=bool(row['is_first_blood'])
            ))

        return submissions


class CTFEngine:
    """Main CTF platform engine"""

    def __init__(self, db_path: Optional[Path] = None):
        if db_path is None:
            db_path = Path(__file__).parent / "ctf_database.db"

        self.db = CTFDatabase(db_path)

    def create_player(self, username: str, email: str = "") -> Player:
        """Create a new player"""
        player = Player(username=username, email=email)
        self.db.save_player(player)
        return player

    def create_challenge(
        self,
        title: str,
        description: str,
        flag: str,
        category: ChallengeCategory,
        difficulty: ChallengeDifficulty,
        points: int = None
    ) -> Challenge:
        """Create a new challenge"""
        # Auto-calculate points based on difficulty if not provided
        if points is None:
            points_map = {
                ChallengeDifficulty.EASY: 100,
                ChallengeDifficulty.MEDIUM: 200,
                ChallengeDifficulty.HARD: 300,
                ChallengeDifficulty.EXPERT: 500
            }
            points = points_map.get(difficulty, 100)

        # Hash the flag
        flag_hash = hashlib.sha256(flag.strip().encode()).hexdigest()

        challenge = Challenge(
            title=title,
            description=description,
            flag=flag_hash,
            category=category,
            difficulty=difficulty,
            points=points
        )

        self.db.save_challenge(challenge)
        return challenge

    def submit_flag(
        self,
        player_id: str,
        challenge_id: str,
        submitted_flag: str
    ) -> Tuple[SubmissionStatus, int, str]:
        """Submit a flag for verification"""
        player = self.db.get_player(player_id)
        challenge = self.db.get_challenge(challenge_id)

        if not player or not challenge:
            return SubmissionStatus.INVALID, 0, "Player or challenge not found"

        # Check if already solved
        if challenge_id in player.challenges_solved:
            return SubmissionStatus.INVALID, 0, "Challenge already solved"

        # Verify flag
        is_correct = challenge.verify_flag(submitted_flag)

        if is_correct:
            # Calculate points (with hint penalty)
            points = challenge.points
            hints_used_count = len(player.hints_used.get(challenge_id, []))
            hint_penalty = hints_used_count * 10  # 10 points per hint
            points = max(10, points - hint_penalty)  # Minimum 10 points

            # Check for first blood
            is_first_blood = challenge.first_blood is None
            if is_first_blood:
                challenge.first_blood = player_id
                player.first_bloods.append(challenge_id)
                points += 50  # First blood bonus

            # Update player
            player.solve_challenge(challenge_id, points)
            self.db.save_player(player)

            # Update challenge
            challenge.solve_count += 1
            self.db.save_challenge(challenge)

            # Save submission
            submission = Submission(
                player_id=player_id,
                challenge_id=challenge_id,
                submitted_flag=submitted_flag,
                status=SubmissionStatus.CORRECT,
                points_awarded=points,
                is_first_blood=is_first_blood
            )
            self.db.save_submission(submission)

            message = f"Correct! +{points} points"
            if is_first_blood:
                message += " 🩸 FIRST BLOOD! +50 bonus"

            return SubmissionStatus.CORRECT, points, message

        else:
            # Save failed submission
            submission = Submission(
                player_id=player_id,
                challenge_id=challenge_id,
                submitted_flag=submitted_flag,
                status=SubmissionStatus.INCORRECT,
                points_awarded=0
            )
            self.db.save_submission(submission)

            return SubmissionStatus.INCORRECT, 0, "Incorrect flag"

    def get_hint(
        self,
        player_id: str,
        challenge_id: str,
        hint_index: int
    ) -> Tuple[bool, Optional[Dict], str]:
        """Get a hint for a challenge"""
        player = self.db.get_player(player_id)
        challenge = self.db.get_challenge(challenge_id)

        if not player or not challenge:
            return False, None, "Player or challenge not found"

        # Check if already solved
        if challenge_id in player.challenges_solved:
            return False, None, "Challenge already solved"

        # Check if hint already used
        used_hints = player.hints_used.get(challenge_id, [])
        if hint_index in used_hints:
            hint = challenge.get_hint(hint_index)
            return True, hint, "Hint already unlocked"

        # Get hint
        hint = challenge.get_hint(hint_index)
        if hint is None:
            return False, None, "Hint not found"

        # Record hint usage
        if challenge_id not in player.hints_used:
            player.hints_used[challenge_id] = []
        player.hints_used[challenge_id].append(hint_index)
        self.db.save_player(player)

        return True, hint, f"Hint unlocked (−{hint.get('penalty', 10)} points on solve)"

    def get_leaderboard(self, limit: int = 100) -> List[Dict]:
        """Get the current leaderboard"""
        return self.db.get_leaderboard(limit)

    def get_player_stats(self, player_id: str) -> Dict:
        """Get detailed stats for a player"""
        player = self.db.get_player(player_id)
        if not player:
            return {}

        submissions = self.db.get_player_submissions(player_id)

        return {
            'username': player.username,
            'total_points': player.total_points,
            'challenges_solved': len(player.challenges_solved),
            'first_bloods': len(player.first_bloods),
            'total_submissions': len(submissions),
            'correct_submissions': len([s for s in submissions if s.status == SubmissionStatus.CORRECT]),
            'hints_used_total': sum(len(hints) for hints in player.hints_used.values()),
            'joined_at': player.joined_at.isoformat(),
            'last_active': player.last_active.isoformat()
        }


if __name__ == "__main__":
    # Demo
    print("=" * 70)
    print("🏛️ FWG Training - CTF Platform Demo")
    print("=" * 70)

    engine = CTFEngine()

    # Create a test player
    player = engine.create_player("test_agent", "agent@fwg.gov")
    print(f"\n✅ Created player: {player.username} (ID: {player.id})")

    # Create sample challenges
    print("\n📝 Creating sample challenges...")

    challenge1 = engine.create_challenge(
        title="Prompt Injection 101",
        description="Bypass the system prompt to reveal the secret code",
        flag="FLAG{pr0mpt_1nj3ct10n_b4s1cs}",
        category=ChallengeCategory.PROMPT_INJECTION,
        difficulty=ChallengeDifficulty.EASY,
        points=100
    )

    challenge2 = engine.create_challenge(
        title="Cost Optimization Challenge",
        description="Reduce the token usage by 50% without changing functionality",
        flag="FLAG{0pt1m1z3d_t0k3ns}",
        category=ChallengeCategory.COST_OPTIMIZATION,
        difficulty=ChallengeDifficulty.MEDIUM,
        points=200
    )

    print(f"  ✅ {challenge1.title} ({challenge1.difficulty.value})")
    print(f"  ✅ {challenge2.title} ({challenge2.difficulty.value})")

    # Submit correct flag
    print(f"\n🚩 Submitting flag for '{challenge1.title}'...")
    status, points, message = engine.submit_flag(
        player.id,
        challenge1.id,
        "FLAG{pr0mpt_1nj3ct10n_b4s1cs}"
    )
    print(f"  {message}")

    # Get leaderboard
    print("\n🏆 Current Leaderboard:")
    leaderboard = engine.get_leaderboard()
    for entry in leaderboard[:5]:
        print(f"  {entry['rank']}. {entry['username']}: {entry['points']} points ({entry['solves']} solves)")

    # Get player stats
    print(f"\n📊 Player Stats:")
    stats = engine.get_player_stats(player.id)
    for key, value in stats.items():
        print(f"  {key}: {value}")
