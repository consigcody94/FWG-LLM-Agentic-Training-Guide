# FWG Training - Competitive CTF Platform

<div align="center">

**Capture The Flag for Federal AI Security Training**

![Security](https://img.shields.io/badge/Security-AI_Focused-red.svg)
![Real-time](https://img.shields.io/badge/Updates-Real_Time-green.svg)
![Difficulty](https://img.shields.io/badge/Difficulty-All_Levels-blue.svg)

*Learn offensive and defensive AI security through hands-on challenges*

</div>

---

## 🎯 Overview

The FWG CTF Platform is a competitive learning environment where federal employees practice AI security skills through realistic challenges. Earn points, climb the leaderboard, and master critical security concepts.

### What is CTF?

Capture The Flag is a cybersecurity competition where participants solve challenges to find hidden "flags" (secret strings). Each correct submission earns points. The player with the most points wins!

### Why CTF for AI Training?

Traditional training teaches theory. **CTF teaches by doing.**

- ✅ **Hands-on practice** with real attack vectors
- ✅ **Immediate feedback** on techniques
- ✅ **Competitive motivation** to improve
- ✅ **Safe environment** to experiment
- ✅ **Measurable progress** via points and ranks

---

## 🚀 Quick Start

### Installation

```bash
# Navigate to ctf-platform directory
cd interactive/ctf-platform

# Install dependencies (from main requirements.txt)
cd ../..
pip install -r interactive/requirements.txt

# Return to CTF directory
cd interactive/ctf-platform
```

### Initialize Challenges

```bash
# Populate database with sample challenges
python sample_challenges.py

# This creates 11 challenges across 6 categories
```

### Start the Platform

```bash
# Start the web server
python ctf_web.py

# Opens on http://localhost:8001
```

### Join the Competition

1. Open `http://localhost:8001` in your browser
2. Enter a username (e.g., "agent_smith")
3. Start solving challenges!
4. Earn points and climb the leaderboard

---

## 📚 Challenge Categories

### 🎯 Prompt Injection

Learn to manipulate AI systems by injecting malicious instructions into prompts.

**Skills learned**:
- Bypassing system prompts
- Role-based attacks
- Nested injection techniques
- Defense strategies

**Example challenges**:
- Prompt Injection 101 (Easy, 100 pts)
- The Helpful Assistant (Medium, 200 pts)
- Inception Injection (Hard, 300 pts)

### 🔓 Jailbreaking

Master techniques to make AI systems ignore safety guidelines.

**Skills learned**:
- Content filter bypasses
- Alternate persona attacks
- DAN (Do Anything Now) variants
- Mitigation techniques

**Example challenges**:
- Content Filter Bypass (Easy, 150 pts)
- Alternate Persona Attack (Medium, 250 pts)

### 💰 Cost Optimization

Optimize AI system costs without sacrificing quality.

**Skills learned**:
- Token reduction techniques
- Model mixing strategies
- Caching and deduplication
- Budget planning

**Example challenges**:
- Token Diet (Medium, 200 pts)
- Budget Cruncher (Hard, 350 pts)

### 🔒 Privacy Leaks

Understand how AI models can leak sensitive training data.

**Skills learned**:
- PII extraction techniques
- Training data leakage
- Privacy-preserving ML
- Data sanitization

**Example challenges**:
- The Privacy Breach (Medium, 250 pts)

### 📋 Compliance

Navigate federal AI compliance requirements.

**Skills learned**:
- FISMA compliance
- FedRAMP authorization
- Security assessments
- Governance frameworks

**Example challenges**:
- FISMA Detective (Easy, 100 pts)
- FedRAMP Authorization Path (Medium, 200 pts)

### ⚔️ Adversarial Attacks

Practice advanced attacks against AI models.

**Skills learned**:
- Model extraction
- Evasion attacks
- Poisoning attacks
- Defensive measures

**Example challenges**:
- Model Thief (Hard, 400 pts)

---

## 🏆 Scoring System

### Base Points

Each challenge has a base point value:
- **Easy**: 100-150 points
- **Medium**: 200-250 points
- **Hard**: 300-350 points
- **Expert**: 400-500 points

### Bonuses

**🩸 First Blood**: +50 points
- First player to solve a challenge
- Your name appears on the challenge
- Broadcast to all players in real-time

**⚡ Speed Bonus**: (Future feature)
- Solve within time limit: +10% points
- Fastest solve: +25% points

### Penalties

**💡 Hint Usage**: -10 points per hint
- Hints help when you're stuck
- But they cost points!
- Use wisely

---

## 🎮 How to Play

### 1. Choose a Challenge

Browse challenges by:
- **Difficulty**: Easy → Expert
- **Category**: Prompt Injection, Jailbreaking, etc.
- **Points**: High value = high difficulty
- **Solve count**: Popular challenges

### 2. Read the Description

Each challenge includes:
- **Scenario**: Realistic federal use case
- **Mission**: What you need to accomplish
- **Given**: Information provided
- **Approach**: Hints on how to start

### 3. Find the Flag

Flags are always in format: `FLAG{something_here}`

Examples:
- `FLAG{pr0mpt_1nj3ct10n}`
- `FLAG{ALPHA-7734}`
- `FLAG{C0ST_R3DUC3D}`

### 4. Submit Your Answer

1. Click the challenge
2. Type the flag exactly as found
3. Click "SUBMIT"
4. See if you got it right!

**✅ Correct**: Points added, notification shown, leaderboard updates
**❌ Incorrect**: Try again! No penalty for wrong answers

### 5. Climb the Leaderboard

- Solve more challenges = more points
- Higher points = higher rank
- Get first bloods for bonus points
- Compete with other federal employees

---

## 💡 Tips & Strategies

### For Beginners

1. **Start with Easy challenges** - Build confidence and learn the basics
2. **Read descriptions carefully** - All clues are in the challenge text
3. **Don't be afraid to use hints** - Small point penalty beats being stuck
4. **Study solved challenges** - Learn from what worked
5. **Ask questions** - Use the community (in team mode)

### For Advanced Players

1. **Go for first bloods** - Worth the extra 50 points
2. **Avoid hints on easy challenges** - Save points for hard ones
3. **Learn the patterns** - Similar techniques work across challenges
4. **Speed matters** - Time-based bonuses coming soon
5. **Help others** - Teaching reinforces your knowledge

### General Strategies

**For Prompt Injection**:
- Try variations: "Ignore previous", "Disregard above", "New instructions"
- Use role-playing: "Pretend you're...", "In this scenario..."
- Nest instructions: Put prompts inside prompts
- Leverage formatting: Use special characters, Unicode, etc.

**For Cost Optimization**:
- Remove unnecessary words: "please", "carefully", "comprehensive"
- Use abbreviations where clear
- Combine related instructions
- Test token count tools

**For Compliance**:
- Know your frameworks: FISMA, FedRAMP, NIST
- Understand impact levels
- Consider data classification
- Think security-first

---

## 🌐 Web Interface Features

### Real-Time Leaderboard

The leaderboard updates **instantly** when anyone solves a challenge:
- Uses WebSocket for live updates
- See rankings change in real-time
- Top 3 get special highlighting
- Your rank always visible

### Matrix-Style UI

The interface features:
- Green-on-black hacker aesthetic
- Animated matrix rain background
- Glowing borders and effects
- Satisfying success notifications

### Challenge Browser

Filter and sort challenges by:
- Category
- Difficulty
- Point value
- Solve count
- Completion status

### Live Notifications

Get notified when:
- You solve a challenge ✅
- Someone gets first blood 🩸
- New players join
- Leaderboard changes significantly

---

## 🔧 Technical Details

### Architecture

```
ctf-platform/
├── ctf_engine.py          # Core CTF logic
│   ├── Challenge          # Challenge model
│   ├── Player             # Player model
│   ├── Submission         # Submission tracking
│   ├── CTFDatabase        # SQLite persistence
│   └── CTFEngine          # Main engine
│
├── ctf_web.py             # FastAPI web server
│   ├── REST API           # Challenge operations
│   ├── WebSocket          # Real-time updates
│   └── HTML/JS UI         # Matrix-themed interface
│
├── sample_challenges.py   # Pre-built challenges
│   └── 11 challenges      # Across 6 categories
│
└── ctf_database.db        # SQLite database
    ├── challenges         # Challenge storage
    ├── players            # Player profiles
    ├── submissions        # All submissions
    └── teams              # Team data (future)
```

### Database Schema

**Challenges**:
```sql
CREATE TABLE challenges (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    category TEXT,
    difficulty TEXT,
    points INTEGER,
    flag TEXT,  -- SHA256 hash
    hints TEXT,  -- JSON array
    solve_count INTEGER,
    first_blood TEXT,
    is_active INTEGER
)
```

**Players**:
```sql
CREATE TABLE players (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    email TEXT,
    total_points INTEGER,
    challenges_solved TEXT,  -- JSON array
    hints_used TEXT,  -- JSON object
    first_bloods TEXT,  -- JSON array
    joined_at TEXT,
    last_active TEXT
)
```

**Submissions**:
```sql
CREATE TABLE submissions (
    id TEXT PRIMARY KEY,
    player_id TEXT,
    challenge_id TEXT,
    submitted_flag TEXT,
    status TEXT,
    points_awarded INTEGER,
    submitted_at TEXT,
    is_first_blood INTEGER
)
```

### Security Measures

**Flag Storage**:
- Flags stored as SHA256 hashes
- Never exposed in API responses
- Verified server-side only

**Submission Validation**:
- Checks for already-solved challenges
- Prevents duplicate submissions
- Atomic database transactions

**WebSocket Safety**:
- No sensitive data broadcast
- Only leaderboard and notifications
- Connection management handled properly

---

## 🎓 Learning Path

### Week 1: Foundations
- Complete all Easy challenges
- Understand basic attack vectors
- Learn flag submission process
- Study compliance basics

### Week 2: Intermediate Skills
- Solve Medium challenges
- Practice cost optimization
- Learn privacy concepts
- Study jailbreaking techniques

### Week 3: Advanced Techniques
- Attempt Hard challenges
- Master prompt injection
- Understand adversarial ML
- Compete for first bloods

### Week 4: Mastery
- Solve Expert challenges
- Help other learners
- Create your own challenges
- Lead team competitions

---

## 📊 Progress Tracking

### Player Dashboard

Track your progress with:
- **Total Points**: Your cumulative score
- **Challenges Solved**: Number completed
- **First Bloods**: Challenges you solved first
- **Current Rank**: Where you stand
- **Hints Used**: How many hints consumed
- **Submission History**: All attempts

### Challenge Statistics

For each challenge:
- How many people solved it
- Who got first blood
- Average solve time (coming soon)
- Success rate

---

## 🚧 Upcoming Features

### Team Mode
- Form teams of 2-5 players
- Shared points and solves
- Team leaderboard
- Internal team chat

### Time-Based Challenges
- Challenges with time limits
- Speed bonuses for quick solves
- Countdown timers
- Streak bonuses

### Dynamic Difficulty
- Challenges that adapt to player skill
- Personalized recommendations
- Progressive hint unlocking
- Skill-based matchmaking

### Advanced Analytics
- Solve-time heatmaps
- Category performance radar
- Progression tracking graphs
- Comparison with peers

### Achievement System
- Unlock badges for milestones
- Special titles for accomplishments
- Profile customization
- Achievement showcase

### Challenge Creator
- Web UI for creating challenges
- Template library
- Challenge validation
- Community submissions

---

## 🏅 Sample Achievements

### Beginner
- 🏁 **First Flag**: Submit your first correct flag
- 🎯 **Category Explorer**: Solve one challenge from each category
- 💯 **Century Club**: Earn 100 total points

### Intermediate
- 🔥 **Hot Streak**: Solve 5 challenges in a row
- 🩸 **First Blood**: Get first blood on any challenge
- 🏆 **Top 10**: Reach top 10 on leaderboard

### Advanced
- 👑 **Leaderboard King**: Reach #1 on leaderboard
- 💎 **Perfect Score**: Solve all challenges without hints
- ⚡ **Speed Demon**: Solve 10 challenges in under an hour

---

## 🆘 Troubleshooting

### "Challenge not found"
- Make sure you ran `sample_challenges.py`
- Check database exists: `ctf_database.db`
- Restart the web server

### "WebSocket disconnected"
- Normal if server restarts
- Auto-reconnects after 3 seconds
- Refresh page if persistent

### "Player already exists"
- Usernames must be unique
- Choose a different username
- Or login with existing username

### "Cannot connect to server"
- Check server is running: `python ctf_web.py`
- Verify port 8001 is available
- Check firewall settings

---

## 📚 Learning Resources

### Prompt Injection
- [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Prompt Injection Primer](https://simonwillison.net/2023/Apr/14/worst-that-can-happen/)

### AI Security
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [Microsoft AI Security Guidelines](https://www.microsoft.com/en-us/security/business/ai-machine-learning)

### Federal Compliance
- [FedRAMP](https://www.fedramp.gov/)
- [FISMA Implementation](https://csrc.nist.gov/topics/laws-and-regulations/laws/fisma)

---

## 🤝 Contributing

Want to create new challenges? Here's how:

### 1. Design the Challenge

```python
engine.create_challenge(
    title="Your Challenge Title",
    description="""
    # Challenge Name

    Scenario description here...

    **Your mission**: Clear objective

    **Given**: What information you provide

    Submit the flag: `FLAG{example_flag}`
    """,
    flag="FLAG{example_flag}",
    category=ChallengeCategory.PROMPT_INJECTION,
    difficulty=ChallengeDifficulty.MEDIUM,
    points=200
)
```

### 2. Test It

- Ensure flag is correct
- Verify difficulty is appropriate
- Check description is clear
- Test with fresh players

### 3. Submit

- Add to `sample_challenges.py`
- Document learning objectives
- Provide hints if needed
- Submit pull request

---

<div align="center">

**🏛️ Federal Working Group - Excellence in AI Security Training**

*Learn by hacking. Master by defending.*

[↩️ Back to Interactive Hub](../README.md) | [🏠 Main README](../../README.md)

</div>
