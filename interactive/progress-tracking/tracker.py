#!/usr/bin/env python3
"""
Progress Tracking System for FWG LLM Training
Gamified learning with XP, levels, badges, and achievement tracking
"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class BadgeLevel(Enum):
    """Badge difficulty levels"""
    BRONZE = "🥉"
    SILVER = "🥈"
    GOLD = "🥇"
    DIAMOND = "💎"
    SPECIAL = "⭐"


class SkillLevel(Enum):
    """User skill progression levels"""
    NOVICE = (0, "🌱", "Just getting started")
    APPRENTICE = (100, "🌿", "Learning the basics")
    PRACTITIONER = (300, "🌳", "Building real skills")
    EXPERT = (600, "🏆", "Advanced proficiency")
    MASTER = (1000, "⭐", "Deep expertise")
    ARCHITECT = (1500, "👑", "System design mastery")
    FEDERAL_AI_LEAD = (2500, "💎", "Federal AI excellence")

    def __init__(self, xp_required: int, emoji: str, description: str):
        self.xp_required = xp_required
        self.emoji = emoji
        self.description = description


@dataclass
class Badge:
    """Achievement badge"""
    name: str
    description: str
    level: BadgeLevel
    icon: str
    module: Optional[str] = None
    earned_date: Optional[str] = None
    xp_value: int = 0

    def to_dict(self):
        return asdict(self)


@dataclass
class ModuleProgress:
    """Progress for a single module"""
    module_number: str
    module_name: str
    reading_complete: bool = False
    quiz_passed: bool = False
    quiz_score: int = 0
    lab_complete: bool = False
    challenges_complete: int = 0
    total_challenges: int = 0
    time_spent: int = 0  # minutes
    last_activity: Optional[str] = None

    @property
    def completion_percentage(self) -> int:
        """Calculate overall completion percentage"""
        components = [
            self.reading_complete,
            self.quiz_passed,
            self.lab_complete,
            (self.challenges_complete / max(self.total_challenges, 1)) >= 1.0
        ]
        return int((sum(components) / len(components)) * 100)

    @property
    def badge_earned(self) -> Optional[BadgeLevel]:
        """Determine badge level earned"""
        if self.completion_percentage >= 100:
            if self.quiz_score >= 90:
                return BadgeLevel.GOLD
            elif self.quiz_score >= 80:
                return BadgeLevel.SILVER
            else:
                return BadgeLevel.BRONZE
        elif self.completion_percentage >= 75:
            return BadgeLevel.SILVER
        elif self.completion_percentage >= 50:
            return BadgeLevel.BRONZE
        return None


class ProgressTracker:
    """Track user progress through the training"""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.db_path = Path(__file__).parent / f"progress_{user_id}.db"
        self.init_database()

    def init_database(self):
        """Initialize SQLite database for persistence"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # User profile table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile (
                user_id TEXT PRIMARY KEY,
                total_xp INTEGER DEFAULT 0,
                current_level TEXT DEFAULT 'NOVICE',
                streak_days INTEGER DEFAULT 0,
                last_activity_date TEXT,
                created_date TEXT
            )
        """)

        # Module progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS module_progress (
                module_number TEXT PRIMARY KEY,
                module_name TEXT,
                reading_complete INTEGER DEFAULT 0,
                quiz_passed INTEGER DEFAULT 0,
                quiz_score INTEGER DEFAULT 0,
                lab_complete INTEGER DEFAULT 0,
                challenges_complete INTEGER DEFAULT 0,
                total_challenges INTEGER DEFAULT 0,
                time_spent INTEGER DEFAULT 0,
                last_activity TEXT
            )
        """)

        # Badges table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS badges (
                badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                level TEXT,
                icon TEXT,
                module TEXT,
                earned_date TEXT,
                xp_value INTEGER
            )
        """)

        # Activity log table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activity_log (
                activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                activity_type TEXT,
                module TEXT,
                description TEXT,
                xp_earned INTEGER
            )
        """)

        # Initialize user if doesn't exist
        cursor.execute("""
            INSERT OR IGNORE INTO user_profile (user_id, created_date)
            VALUES (?, ?)
        """, (self.user_id, datetime.now().isoformat()))

        conn.commit()
        conn.close()

    def add_xp(self, amount: int, reason: str, module: str = None):
        """Add XP and log the activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Update total XP
        cursor.execute("""
            UPDATE user_profile
            SET total_xp = total_xp + ?
            WHERE user_id = ?
        """, (amount, self.user_id))

        # Log activity
        cursor.execute("""
            INSERT INTO activity_log (timestamp, activity_type, module, description, xp_earned)
            VALUES (?, ?, ?, ?, ?)
        """, (datetime.now().isoformat(), "xp_gained", module, reason, amount))

        # Update level if needed
        total_xp = self.get_total_xp()
        new_level = self._calculate_level(total_xp)
        cursor.execute("""
            UPDATE user_profile
            SET current_level = ?
            WHERE user_id = ?
        """, (new_level.name, self.user_id))

        conn.commit()
        conn.close()

        # Check if level up
        return new_level

    def _calculate_level(self, total_xp: int) -> SkillLevel:
        """Calculate skill level based on total XP"""
        for level in reversed(list(SkillLevel)):
            if total_xp >= level.xp_required:
                return level
        return SkillLevel.NOVICE

    def get_total_xp(self) -> int:
        """Get user's total XP"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT total_xp FROM user_profile WHERE user_id = ?", (self.user_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else 0

    def get_current_level(self) -> SkillLevel:
        """Get user's current skill level"""
        total_xp = self.get_total_xp()
        return self._calculate_level(total_xp)

    def update_streak(self):
        """Update daily activity streak"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT last_activity_date, streak_days
            FROM user_profile
            WHERE user_id = ?
        """, (self.user_id,))

        result = cursor.fetchone()
        last_activity = result[0] if result else None
        current_streak = result[1] if result else 0

        today = datetime.now().date()

        if last_activity:
            last_date = datetime.fromisoformat(last_activity).date()
            days_diff = (today - last_date).days

            if days_diff == 1:
                # Consecutive day - increment streak
                current_streak += 1
            elif days_diff > 1:
                # Streak broken - reset
                current_streak = 1
            # If days_diff == 0, same day - keep streak
        else:
            # First activity
            current_streak = 1

        cursor.execute("""
            UPDATE user_profile
            SET last_activity_date = ?,
                streak_days = ?
            WHERE user_id = ?
        """, (today.isoformat(), current_streak, self.user_id))

        conn.commit()
        conn.close()

        return current_streak

    def award_badge(self, badge: Badge):
        """Award a badge to the user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        badge.earned_date = datetime.now().isoformat()

        cursor.execute("""
            INSERT INTO badges (name, description, level, icon, module, earned_date, xp_value)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (badge.name, badge.description, badge.level.name, badge.icon,
              badge.module, badge.earned_date, badge.xp_value))

        conn.commit()
        conn.close()

        # Add XP for badge
        if badge.xp_value > 0:
            self.add_xp(badge.xp_value, f"Badge earned: {badge.name}", badge.module)

    def get_earned_badges(self) -> List[Badge]:
        """Get all earned badges"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM badges ORDER BY earned_date DESC")
        rows = cursor.fetchall()
        conn.close()

        badges = []
        for row in rows:
            badges.append(Badge(
                name=row[1],
                description=row[2],
                level=BadgeLevel[row[3]],
                icon=row[4],
                module=row[5],
                earned_date=row[6],
                xp_value=row[7]
            ))

        return badges

    def update_module_progress(self, module_number: str, **kwargs):
        """Update progress for a specific module"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Build update query dynamically
        fields = []
        values = []
        for key, value in kwargs.items():
            if key in ['reading_complete', 'quiz_passed', 'lab_complete']:
                fields.append(f"{key} = ?")
                values.append(1 if value else 0)
            else:
                fields.append(f"{key} = ?")
                values.append(value)

        fields.append("last_activity = ?")
        values.append(datetime.now().isoformat())
        values.append(module_number)

        query = f"""
            UPDATE module_progress
            SET {', '.join(fields)}
            WHERE module_number = ?
        """

        cursor.execute(query, values)
        conn.commit()
        conn.close()

        # Update streak
        self.update_streak()

    def get_dashboard_summary(self) -> Dict:
        """Get comprehensive dashboard summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get user stats
        cursor.execute("""
            SELECT total_xp, current_level, streak_days
            FROM user_profile
            WHERE user_id = ?
        """, (self.user_id,))
        user_stats = cursor.fetchone()

        # Get module completion stats
        cursor.execute("""
            SELECT
                COUNT(*) as total_modules,
                SUM(CASE WHEN quiz_passed = 1 THEN 1 ELSE 0 END) as modules_completed
            FROM module_progress
        """)
        module_stats = cursor.fetchone()

        # Get badge count
        cursor.execute("SELECT COUNT(*) FROM badges")
        badge_count = cursor.fetchone()[0]

        # Get recent activities
        cursor.execute("""
            SELECT timestamp, activity_type, module, description, xp_earned
            FROM activity_log
            ORDER BY timestamp DESC
            LIMIT 5
        """)
        recent_activities = cursor.fetchall()

        conn.close()

        current_level = SkillLevel[user_stats[1]] if user_stats else SkillLevel.NOVICE
        total_xp = user_stats[0] if user_stats else 0

        # Calculate progress to next level
        current_level_xp = current_level.xp_required
        next_levels = [l for l in SkillLevel if l.xp_required > current_level_xp]
        next_level = next_levels[0] if next_levels else current_level
        xp_to_next = next_level.xp_required - total_xp

        return {
            "level": current_level,
            "total_xp": total_xp,
            "xp_to_next_level": xp_to_next,
            "next_level": next_level,
            "streak_days": user_stats[2] if user_stats else 0,
            "modules_completed": module_stats[1] if module_stats else 0,
            "total_modules": 27,
            "badges_earned": badge_count,
            "recent_activities": recent_activities
        }


# Command-line interface
if __name__ == "__main__":
    import sys

    tracker = ProgressTracker()

    if len(sys.argv) > 1 and sys.argv[1] == "dashboard":
        summary = tracker.get_dashboard_summary()

        print("\n" + "="*70)
        print("YOUR LEARNING PROGRESS")
        print("="*70 + "\n")

        level = summary['level']
        print(f"Level: {level.value[1]} {level.name} - {level.value[2]}")
        print(f"Total XP: {summary['total_xp']} / {summary['next_level'].xp_required}")

        # Progress bar
        if summary['xp_to_next_level'] > 0:
            progress = int((summary['total_xp'] - level.xp_required) /
                         (summary['next_level'].xp_required - level.xp_required) * 100)
            bar = "█" * (progress // 2) + "░" * (50 - progress // 2)
            print(f"{bar} {progress}%")
        print(f"Next level: {summary['xp_to_next_level']} XP needed\n")

        print(f"Modules Completed: {summary['modules_completed']}/{summary['total_modules']}")
        print(f"Badges Earned: {summary['badges_earned']}")
        print(f"Current Streak: {summary['streak_days']} days 🔥\n")

        print("="*70)
    else:
        print("FWG Progress Tracker")
        print("Usage: python tracker.py dashboard")
