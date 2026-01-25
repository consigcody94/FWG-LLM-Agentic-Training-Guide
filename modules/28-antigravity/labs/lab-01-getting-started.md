# Lab 28.1: Getting Started with Google Antigravity

## Overview

In this lab, you will install Google Antigravity, configure security policies, and complete your first agent-assisted task.

**Duration:** 45 minutes
**Difficulty:** Beginner
**Prerequisites:** Gmail account, Chrome browser

## Learning Objectives

1. Install Google Antigravity on your system
2. Configure appropriate security policies
3. Navigate Editor and Manager views
4. Complete a simple task with agent assistance

## Part 1: Installation (10 minutes)

### Task 1.1: Download and Install

1. Visit https://antigravity.google/download
2. Select your operating system (macOS, Windows, or Linux)
3. Run the installer

### Task 1.2: Initial Setup

During the setup flow, you'll be asked to:

1. **Import settings or start fresh**
   - If you use VS Code or Cursor, choose "Import settings"
   - Otherwise, choose "Start fresh"

2. **Select theme**
   - Choose dark or light mode based on preference

3. **Configure autonomy levels** (Important!)

For this lab, select the **Review-driven development** preset:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONFIGURATION PRESET                                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ○ Secure Mode          - Enhanced restrictions                             │
│  ● Review-driven        - Balanced with checkpoints  ← SELECT THIS          │
│  ○ Agent-driven         - Minimal interruptions                             │
│  ○ Custom               - Full control                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Task 1.3: Verify Installation

Open a terminal and run:

```bash
antigravity --version
```

Expected output:
```
Google Antigravity v1.x.x
```

## Part 2: Interface Navigation (15 minutes)

### Task 2.1: Open a Project

Create a new directory for this lab:

```bash
mkdir ~/antigravity-lab
cd ~/antigravity-lab
antigravity .
```

### Task 2.2: Explore Editor View

The Editor View should look familiar if you've used VS Code:

1. **File Explorer** (left sidebar) - Browse project files
2. **Code Editor** (center) - Edit code
3. **Agent Panel** (right sidebar) - Chat with agent
4. **Terminal** (bottom) - Run commands

**Practice keyboard shortcuts:**

| Try This | Shortcut |
|----------|----------|
| Open agent panel | `Cmd + L` (Mac) or `Ctrl + L` (Windows) |
| Inline command | `Cmd + I` or `Ctrl + I` |
| Toggle terminal | `Cmd + `` ` or `Ctrl + `` ` |
| Command palette | `Cmd + Shift + P` or `Ctrl + Shift + P` |

### Task 2.3: Explore Manager View

Switch to Manager View:

1. Press `Cmd + E` (Mac) or `Ctrl + E` (Windows)
2. Or click "Manager" in the top navigation

In Manager View, observe:

- **Inbox** - List of all conversations
- **Active Agents** - Currently running agents
- **New Task** area - Start new agent tasks
- **Model selector** - Choose AI model
- **Mode selector** - Planning vs Fast mode

### Task 2.4: Return to Editor View

Press `Cmd + E` / `Ctrl + E` again to switch back to Editor View.

## Part 3: First Agent Task (15 minutes)

### Task 3.1: Create a Simple Python Script

In the Editor View agent panel, type:

```
Create a Python script that:
1. Asks the user for their name
2. Greets them with a personalized message
3. Tells them the current date and time
```

Observe how the agent:
1. Creates an implementation plan
2. Shows you a code diff
3. Waits for your approval

### Task 3.2: Review and Accept the Code

1. Read the proposed code diff
2. If satisfied, click "Accept" or type "accept"
3. The agent will create the file

### Task 3.3: Run the Script

The agent may offer to run the script for you. If using Review-driven mode, you'll see:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TERMINAL COMMAND APPROVAL                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Agent wants to run: python greeting.py                                     │
│                                                                             │
│  [Approve]  [Deny]  [Approve & Remember]                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Click "Approve" to run the script.

### Task 3.4: Iterate with Feedback

Now modify the script by commenting:

```
Add a feature that asks for the user's favorite color
and includes it in the greeting
```

Watch how the agent updates the code and shows you the diff.

## Part 4: Manager View Task (5 minutes)

### Task 4.1: Start an Agent in Planning Mode

1. Switch to Manager View (`Cmd + E`)
2. Set Mode to "Planning"
3. Set Model to "Gemini 3 Pro" (or default)
4. Enter this task:

```
Create a README.md file for this project that explains
what the greeting script does and how to run it
```

5. Click "Start Agent"

### Task 4.2: Review Artifacts

Watch as the agent produces:

1. **Task List** - Steps it will take
2. **Implementation Plan** - What the README will contain
3. **Code Diff** - The actual README content

Add a comment to the Implementation Plan:

```
Also include a section about requirements (Python version needed)
```

The agent will incorporate your feedback.

## Deliverables

By the end of this lab, you should have:

1. ✅ Google Antigravity installed and configured
2. ✅ Familiarity with Editor View and Manager View
3. ✅ A `greeting.py` script created with agent assistance
4. ✅ A `README.md` created using Planning mode

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Successfully installed Antigravity | 20 |
| Configured Review-driven mode | 15 |
| Created Python script with agent | 25 |
| Used inline commands (Cmd+I) | 15 |
| Created README using Planning mode | 25 |
| **Total** | **100** |

## Troubleshooting

### Issue: Agent panel not responding

1. Check your internet connection
2. Try reloading the window: `Cmd + Shift + P` → "Reload Window"
3. Check if you're signed in to your Gmail account

### Issue: Terminal commands not executing

1. Verify your security policy allows terminal execution
2. Go to Settings → Security → Terminal Execution
3. Ensure it's set to "Auto" or "Request approval"

### Issue: Model selection unavailable

During public preview, some models may have limited availability based on your region and quota.

## Next Steps

Continue to [Lab 28.2: Building with Agents](lab-02-building-with-agents.md) to learn how to build a complete application using Antigravity's agent orchestration features.
