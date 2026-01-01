#!/usr/bin/env python3
"""
FWG Training - CTF Web Interface
Real-time web interface for CTF competitions

Features:
- Live leaderboard updates via WebSocket
- Challenge browser and submission
- Team management
- Hint system
- Real-time notifications
- Progress tracking
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Set

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request
    from fastapi.responses import HTMLResponse, JSONResponse
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  FastAPI not installed. Run: pip install fastapi uvicorn websockets")

from ctf_engine import (
    CTFEngine, ChallengeCategory, ChallengeDifficulty,
    SubmissionStatus
)


# Pydantic models
class PlayerCreate(BaseModel):
    username: str
    email: str = ""


class FlagSubmission(BaseModel):
    player_id: str
    challenge_id: str
    flag: str


class HintRequest(BaseModel):
    player_id: str
    challenge_id: str
    hint_index: int


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="FWG CTF Platform",
        description="Competitive Capture The Flag for Federal AI Training",
        version="1.0.0"
    )

    # Global CTF engine
    engine = CTFEngine()

    # WebSocket connection manager
    class ConnectionManager:
        def __init__(self):
            self.active_connections: List[WebSocket] = []

        async def connect(self, websocket: WebSocket):
            await websocket.accept()
            self.active_connections.append(websocket)

        def disconnect(self, websocket: WebSocket):
            self.active_connections.remove(websocket)

        async def broadcast(self, message: dict):
            """Broadcast message to all connected clients"""
            for connection in self.active_connections:
                try:
                    await connection.send_json(message)
                except:
                    pass

    manager = ConnectionManager()


    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main CTF interface"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FWG CTF Platform</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Courier New', monospace;
            background: #0a0e27;
            color: #00ff41;
            min-height: 100vh;
            overflow-x: hidden;
        }

        .matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 0;
            opacity: 0.1;
            pointer-events: none;
        }

        .container {
            position: relative;
            z-index: 1;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        .header {
            background: linear-gradient(135deg, #1a1f3a 0%, #0f1419 100%);
            border: 2px solid #00ff41;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }

        .header h1 {
            font-size: 36px;
            text-shadow: 0 0 10px #00ff41;
            margin-bottom: 10px;
        }

        .header .tagline {
            color: #00cc33;
            font-size: 14px;
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 300px;
            gap: 20px;
        }

        .section {
            background: rgba(10, 14, 39, 0.9);
            border: 2px solid #00ff41;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 0 15px rgba(0, 255, 65, 0.2);
        }

        .section h2 {
            color: #00ff41;
            margin-bottom: 15px;
            text-transform: uppercase;
            font-size: 20px;
            border-bottom: 1px solid #00ff41;
            padding-bottom: 10px;
        }

        .challenge {
            background: rgba(0, 20, 40, 0.8);
            border: 1px solid #00cc33;
            padding: 15px;
            margin-bottom: 15px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .challenge:hover {
            border-color: #00ff41;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.4);
            transform: translateX(5px);
        }

        .challenge.solved {
            border-color: #00ff88;
            opacity: 0.7;
        }

        .challenge-title {
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 5px;
            color: #00ff41;
        }

        .challenge-meta {
            font-size: 12px;
            color: #00cc33;
            display: flex;
            justify-content: space-between;
            margin-top: 8px;
        }

        .difficulty-easy { color: #00ff41; }
        .difficulty-medium { color: #ffaa00; }
        .difficulty-hard { color: #ff4444; }
        .difficulty-expert { color: #ff00ff; }

        .category-badge {
            background: #00ff41;
            color: #0a0e27;
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 10px;
            font-weight: bold;
        }

        .leaderboard {
            background: rgba(10, 14, 39, 0.95);
            border: 2px solid #00ff41;
            padding: 20px;
            box-shadow: 0 0 20px rgba(0, 255, 65, 0.3);
        }

        .leaderboard h2 {
            color: #00ff41;
            margin-bottom: 15px;
            text-transform: uppercase;
            text-align: center;
        }

        .leaderboard-item {
            background: rgba(0, 20, 40, 0.6);
            border-left: 3px solid #00ff41;
            padding: 10px;
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .leaderboard-item.rank-1 {
            border-left-color: #ffd700;
            background: rgba(255, 215, 0, 0.1);
        }

        .leaderboard-item.rank-2 {
            border-left-color: #c0c0c0;
            background: rgba(192, 192, 192, 0.1);
        }

        .leaderboard-item.rank-3 {
            border-left-color: #cd7f32;
            background: rgba(205, 127, 50, 0.1);
        }

        .rank {
            font-weight: bold;
            width: 30px;
        }

        .username {
            flex: 1;
            padding: 0 10px;
        }

        .points {
            font-weight: bold;
            color: #00ff41;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: #0a0e27;
            border: 2px solid #00ff41;
            padding: 30px;
            max-width: 600px;
            width: 90%;
            box-shadow: 0 0 30px rgba(0, 255, 65, 0.5);
        }

        .modal-content h2 {
            color: #00ff41;
            margin-bottom: 20px;
        }

        .modal-content input {
            width: 100%;
            padding: 10px;
            background: rgba(0, 20, 40, 0.8);
            border: 1px solid #00ff41;
            color: #00ff41;
            font-family: 'Courier New', monospace;
            margin-bottom: 15px;
        }

        .modal-content button {
            padding: 10px 20px;
            background: #00ff41;
            color: #0a0e27;
            border: none;
            cursor: pointer;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            margin-right: 10px;
        }

        .modal-content button:hover {
            background: #00cc33;
        }

        .modal-content button.secondary {
            background: transparent;
            border: 1px solid #00ff41;
            color: #00ff41;
        }

        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: #00ff41;
            color: #0a0e27;
            padding: 15px 25px;
            border-radius: 5px;
            font-weight: bold;
            z-index: 2000;
            animation: slideIn 0.3s ease-out;
        }

        .notification.success { background: #00ff41; }
        .notification.error { background: #ff4444; color: white; }
        .notification.firstblood { background: #ff0000; color: white; animation: pulse 0.5s infinite; }

        @keyframes slideIn {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-box {
            background: rgba(0, 20, 40, 0.6);
            border: 1px solid #00ff41;
            padding: 15px;
            text-align: center;
        }

        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #00ff41;
        }

        .stat-label {
            font-size: 12px;
            color: #00cc33;
            margin-top: 5px;
        }

        .connection-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            padding: 8px 15px;
            background: rgba(0, 20, 40, 0.9);
            border: 1px solid #00ff41;
            border-radius: 20px;
            font-size: 12px;
            z-index: 999;
        }

        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #00ff41;
            margin-right: 5px;
            animation: pulse 2s infinite;
        }

        .status-dot.disconnected {
            background: #ff4444;
            animation: none;
        }

        .hint-button {
            padding: 5px 10px;
            background: #ffaa00;
            color: #0a0e27;
            border: none;
            cursor: pointer;
            font-size: 12px;
            margin-top: 10px;
        }

        .hints-list {
            margin-top: 10px;
            padding: 10px;
            background: rgba(255, 170, 0, 0.1);
            border-left: 2px solid #ffaa00;
        }
    </style>
</head>
<body>
    <canvas class="matrix-bg" id="matrix"></canvas>

    <div class="container">
        <div class="header">
            <h1>🏛️ FWG CTF PLATFORM</h1>
            <div class="tagline">Federal AI Security Training - Capture The Flag</div>
        </div>

        <div class="stats">
            <div class="stat-box">
                <div class="stat-value" id="totalSolves">0</div>
                <div class="stat-label">CHALLENGES SOLVED</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="totalPoints">0</div>
                <div class="stat-label">TOTAL POINTS</div>
            </div>
            <div class="stat-box">
                <div class="stat-value" id="currentRank">-</div>
                <div class="stat-label">CURRENT RANK</div>
            </div>
        </div>

        <div class="main-grid">
            <div>
                <div class="section">
                    <h2>🎯 Challenges</h2>
                    <div id="challengesList">
                        Loading challenges...
                    </div>
                </div>
            </div>

            <div>
                <div class="leaderboard">
                    <h2>🏆 LEADERBOARD</h2>
                    <div id="leaderboardList">
                        Loading...
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="modal" id="challengeModal">
        <div class="modal-content">
            <h2 id="modalTitle">Challenge</h2>
            <div id="modalDescription"></div>
            <div id="modalHints"></div>
            <input type="text" id="flagInput" placeholder="FLAG{...}" />
            <div>
                <button onclick="submitFlag()">SUBMIT</button>
                <button onclick="requestHint()" class="hint-button">💡 GET HINT</button>
                <button class="secondary" onclick="closeModal()">CANCEL</button>
            </div>
        </div>
    </div>

    <div class="modal" id="loginModal">
        <div class="modal-content">
            <h2>ENTER THE ARENA</h2>
            <input type="text" id="usernameInput" placeholder="Username" />
            <input type="email" id="emailInput" placeholder="Email (optional)" />
            <div>
                <button onclick="login()">JOIN CTF</button>
            </div>
        </div>
    </div>

    <div class="connection-status">
        <span class="status-dot" id="statusDot"></span>
        <span id="statusText">CONNECTED</span>
    </div>

    <script>
        // Matrix rain effect
        const canvas = document.getElementById('matrix');
        const ctx = canvas.getContext('2d');
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*()';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array(Math.floor(columns)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = 'rgba(10, 14, 39, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00ff41';
            ctx.font = fontSize + 'px monospace';

            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);

                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }

        setInterval(drawMatrix, 50);

        // Global state
        let currentPlayer = null;
        let selectedChallenge = null;
        let ws = null;

        // WebSocket connection
        function connectWebSocket() {
            ws = new WebSocket(`ws://${window.location.host}/ws`);

            ws.onopen = () => {
                console.log('WebSocket connected');
                updateConnectionStatus(true);
            };

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            };

            ws.onclose = () => {
                console.log('WebSocket disconnected');
                updateConnectionStatus(false);
                setTimeout(connectWebSocket, 3000);
            };

            ws.onerror = (error) => {
                console.error('WebSocket error:', error);
            };
        }

        function handleWebSocketMessage(data) {
            if (data.type === 'leaderboard_update') {
                updateLeaderboard(data.leaderboard);
            } else if (data.type === 'new_solve') {
                showNotification(`${data.username} solved ${data.challenge}!`, 'success');
            } else if (data.type === 'first_blood') {
                showNotification(`🩸 FIRST BLOOD: ${data.username} on ${data.challenge}!`, 'firstblood');
            }
        }

        function updateConnectionStatus(connected) {
            const dot = document.getElementById('statusDot');
            const text = document.getElementById('statusText');
            if (connected) {
                dot.classList.remove('disconnected');
                text.textContent = 'CONNECTED';
            } else {
                dot.classList.add('disconnected');
                text.textContent = 'DISCONNECTED';
            }
        }

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            document.getElementById('loginModal').classList.add('active');
            connectWebSocket();
        });

        async function login() {
            const username = document.getElementById('usernameInput').value;
            const email = document.getElementById('emailInput').value;

            if (!username) {
                alert('Please enter a username');
                return;
            }

            const response = await fetch('/api/players', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({username, email})
            });

            currentPlayer = await response.json();
            document.getElementById('loginModal').classList.remove('active');

            loadChallenges();
            loadLeaderboard();
            loadPlayerStats();
        }

        async function loadChallenges() {
            const response = await fetch('/api/challenges');
            const challenges = await response.json();

            const container = document.getElementById('challengesList');
            container.innerHTML = challenges.map(c => `
                <div class="challenge ${c.solved ? 'solved' : ''}" onclick="openChallenge('${c.id}')">
                    <div class="challenge-title">${c.title}</div>
                    <div>${c.description.substring(0, 100)}...</div>
                    <div class="challenge-meta">
                        <span class="category-badge">${c.category}</span>
                        <span class="difficulty-${c.difficulty}">${c.difficulty.toUpperCase()}</span>
                        <span>${c.points} PTS</span>
                        <span>${c.solve_count} solves</span>
                    </div>
                </div>
            `).join('');
        }

        async function loadLeaderboard() {
            const response = await fetch('/api/leaderboard');
            const leaderboard = await response.json();
            updateLeaderboard(leaderboard);
        }

        function updateLeaderboard(leaderboard) {
            const container = document.getElementById('leaderboardList');
            container.innerHTML = leaderboard.slice(0, 10).map(entry => `
                <div class="leaderboard-item rank-${entry.rank}">
                    <span class="rank">#${entry.rank}</span>
                    <span class="username">${entry.username}</span>
                    <span class="points">${entry.points}</span>
                </div>
            `).join('');

            // Update current rank
            if (currentPlayer) {
                const myRank = leaderboard.find(e => e.player_id === currentPlayer.id);
                document.getElementById('currentRank').textContent = myRank ? `#${myRank.rank}` : '-';
            }
        }

        async function loadPlayerStats() {
            if (!currentPlayer) return;

            const response = await fetch(`/api/players/${currentPlayer.id}/stats`);
            const stats = await response.json();

            document.getElementById('totalSolves').textContent = stats.challenges_solved;
            document.getElementById('totalPoints').textContent = stats.total_points;
        }

        async function openChallenge(challengeId) {
            const response = await fetch(`/api/challenges/${challengeId}`);
            selectedChallenge = await response.json();

            document.getElementById('modalTitle').textContent = selectedChallenge.title;
            document.getElementById('modalDescription').innerHTML = `
                <p>${selectedChallenge.description}</p>
                <p style="margin-top: 10px; color: #00cc33;">
                    <strong>${selectedChallenge.difficulty}</strong> | ${selectedChallenge.points} points | ${selectedChallenge.solve_count} solves
                </p>
            `;
            document.getElementById('modalHints').innerHTML = '';
            document.getElementById('flagInput').value = '';

            document.getElementById('challengeModal').classList.add('active');
        }

        function closeModal() {
            document.getElementById('challengeModal').classList.remove('active');
        }

        async function submitFlag() {
            const flag = document.getElementById('flagInput').value;

            if (!flag || !currentPlayer || !selectedChallenge) return;

            const response = await fetch('/api/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    player_id: currentPlayer.id,
                    challenge_id: selectedChallenge.id,
                    flag
                })
            });

            const result = await response.json();

            if (result.status === 'correct') {
                showNotification(result.message, 'success');
                closeModal();
                loadChallenges();
                loadPlayerStats();

                // Broadcast solve event
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        type: 'solve',
                        player: currentPlayer.username,
                        challenge: selectedChallenge.title,
                        first_blood: result.message.includes('FIRST BLOOD')
                    }));
                }
            } else {
                showNotification('Incorrect flag!', 'error');
            }
        }

        async function requestHint() {
            // Implementation for hint request
            showNotification('Hint system coming soon!', 'success');
        }

        function showNotification(message, type = 'success') {
            const notif = document.createElement('div');
            notif.className = `notification ${type}`;
            notif.textContent = message;
            document.body.appendChild(notif);

            setTimeout(() => notif.remove(), 3000);
        }
    </script>
</body>
</html>
        """
        return HTMLResponse(content=html_content)


    @app.post("/api/players")
    async def create_player(player: PlayerCreate):
        """Create or get existing player"""
        existing = engine.db.get_player_by_username(player.username)
        if existing:
            return {
                "id": existing.id,
                "username": existing.username,
                "email": existing.email
            }

        new_player = engine.create_player(player.username, player.email)
        return {
            "id": new_player.id,
            "username": new_player.username,
            "email": new_player.email
        }


    @app.get("/api/challenges")
    async def list_challenges():
        """List all active challenges"""
        challenges = engine.db.get_all_challenges(active_only=True)
        return [
            {
                "id": c.id,
                "title": c.title,
                "description": c.description,
                "category": c.category.value,
                "difficulty": c.difficulty.value,
                "points": c.points,
                "solve_count": c.solve_count,
                "solved": False  # TODO: Check if current player solved
            }
            for c in challenges
        ]


    @app.get("/api/challenges/{challenge_id}")
    async def get_challenge(challenge_id: str):
        """Get challenge details"""
        challenge = engine.db.get_challenge(challenge_id)
        if not challenge:
            raise HTTPException(status_code=404, detail="Challenge not found")

        return {
            "id": challenge.id,
            "title": challenge.title,
            "description": challenge.description,
            "category": challenge.category.value,
            "difficulty": challenge.difficulty.value,
            "points": challenge.points,
            "solve_count": challenge.solve_count,
            "hints_count": len(challenge.hints)
        }


    @app.post("/api/submit")
    async def submit_flag(submission: FlagSubmission):
        """Submit a flag"""
        status, points, message = engine.submit_flag(
            submission.player_id,
            submission.challenge_id,
            submission.flag
        )

        # Broadcast to all clients if solved
        if status == SubmissionStatus.CORRECT:
            player = engine.db.get_player(submission.player_id)
            challenge = engine.db.get_challenge(submission.challenge_id)

            await manager.broadcast({
                "type": "leaderboard_update",
                "leaderboard": engine.get_leaderboard()
            })

            if "FIRST BLOOD" in message:
                await manager.broadcast({
                    "type": "first_blood",
                    "username": player.username,
                    "challenge": challenge.title
                })
            else:
                await manager.broadcast({
                    "type": "new_solve",
                    "username": player.username,
                    "challenge": challenge.title
                })

        return {
            "status": status.value,
            "points": points,
            "message": message
        }


    @app.get("/api/leaderboard")
    async def get_leaderboard():
        """Get current leaderboard"""
        return engine.get_leaderboard(limit=100)


    @app.get("/api/players/{player_id}/stats")
    async def get_player_stats(player_id: str):
        """Get player statistics"""
        stats = engine.get_player_stats(player_id)
        if not stats:
            raise HTTPException(status_code=404, detail="Player not found")
        return stats


    @app.websocket("/ws")
    async def websocket_endpoint(websocket: WebSocket):
        """WebSocket endpoint for real-time updates"""
        await manager.connect(websocket)
        try:
            while True:
                data = await websocket.receive_text()
                # Echo back for now
                await websocket.send_text(data)
        except WebSocketDisconnect:
            manager.disconnect(websocket)


def start_server(host: str = "127.0.0.1", port: int = 8001):
    """Start the CTF web server"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI not installed. Cannot start web server.")
        return

    print("=" * 70)
    print("🏛️ FWG Training - CTF Platform Starting...")
    print("=" * 70)
    print(f"\n🌐 Server: http://{host}:{port}")
    print(f"📊 Leaderboard updates: Real-time via WebSocket")
    print("\n💡 Features:")
    print("  • AI Security Challenges")
    print("  • Live Leaderboard")
    print("  • Hint System")
    print("  • First Blood Bonus")
    print("\n" + "=" * 70 + "\n")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
