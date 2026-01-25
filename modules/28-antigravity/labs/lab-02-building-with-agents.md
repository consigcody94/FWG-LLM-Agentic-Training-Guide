# Lab 28.2: Building with Agents

## Overview

In this lab, you will build a complete web application using Google Antigravity's agent orchestration features. You'll work with multiple agents in parallel and learn to effectively review and iterate on artifacts.

**Duration:** 90 minutes
**Difficulty:** Intermediate
**Prerequisites:** Lab 28.1 completed, familiarity with web development concepts

## Learning Objectives

1. Use Planning mode for multi-component applications
2. Work effectively with artifacts (plans, diffs, screenshots)
3. Provide feedback and iterate with agents
4. Orchestrate multiple agents working in parallel

## Project: Task Management Application

You will build a simple task management app with:
- Backend API (Python Flask)
- Frontend UI (HTML/CSS/JavaScript)
- Local storage (SQLite)

## Part 1: Project Setup with Planning Mode (20 minutes)

### Task 1.1: Create Project Directory

```bash
mkdir ~/task-manager-app
cd ~/task-manager-app
antigravity .
```

### Task 1.2: Start Planning Mode Task

1. Switch to Manager View (`Cmd + E`)
2. Configure:
   - **Mode:** Planning
   - **Model:** Gemini 3 Pro (or default)
3. Enter this task:

```
Create a task management web application with:

Backend:
- Python Flask API
- SQLite database
- REST endpoints for CRUD operations on tasks
- Each task has: id, title, description, status (todo/in-progress/done), created_at

Frontend:
- Simple HTML/CSS/JavaScript (no framework needed)
- Display tasks in three columns (Kanban-style)
- Ability to add, edit, delete, and move tasks between columns
- Clean, modern UI

Project structure should be organized with separate backend/ and frontend/ directories.
```

4. Click "Start Agent"

### Task 1.3: Review Implementation Plan

The agent will produce an Implementation Plan artifact:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  IMPLEMENTATION PLAN                                               [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Project Structure:                                                         │
│  ├── backend/                                                               │
│  │   ├── app.py          # Flask application                               │
│  │   ├── models.py       # SQLAlchemy models                               │
│  │   ├── routes.py       # API routes                                       │
│  │   └── requirements.txt                                                   │
│  └── frontend/                                                              │
│      ├── index.html      # Main page                                        │
│      ├── styles.css      # Styling                                          │
│      └── app.js          # Frontend logic                                   │
│                                                                             │
│  Backend Implementation:                                                    │
│  1. Create Flask app with CORS support                                      │
│  2. Define Task model with SQLAlchemy                                       │
│  3. Implement REST endpoints...                                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Add a comment** to the plan:
```
Add error handling middleware and input validation for all endpoints
```

### Task 1.4: Review Task List

After you comment, the agent updates and produces a Task List:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  TASK LIST                                                         [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ☐ Create project directory structure                                       │
│  ☐ Set up Flask backend with SQLAlchemy                                     │
│  ☐ Define Task model                                                        │
│  ☐ Implement CRUD API endpoints                                             │
│  ☐ Add error handling middleware                                            │
│  ☐ Create HTML structure                                                    │
│  ☐ Style with CSS (Kanban layout)                                           │
│  ☐ Implement JavaScript frontend logic                                      │
│  ☐ Connect frontend to backend API                                          │
│  ☐ Test complete application                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

Review the task list. If it looks complete, let the agent proceed.

## Part 2: Review Code Artifacts (25 minutes)

### Task 2.1: Backend Code Review

As the agent works, it will produce code diff artifacts. Review each one carefully:

**Example: models.py diff**
```diff
+ # backend/models.py
+ from flask_sqlalchemy import SQLAlchemy
+ from datetime import datetime
+
+ db = SQLAlchemy()
+
+ class Task(db.Model):
+     id = db.Column(db.Integer, primary_key=True)
+     title = db.Column(db.String(100), nullable=False)
+     description = db.Column(db.Text)
+     status = db.Column(db.String(20), default='todo')
+     created_at = db.Column(db.DateTime, default=datetime.utcnow)
+
+     def to_dict(self):
+         return {
+             'id': self.id,
+             'title': self.title,
+             'description': self.description,
+             'status': self.status,
+             'created_at': self.created_at.isoformat()
+         }
```

**For each diff, you can:**
- **Accept** - Apply the changes
- **Reject** - Discard and ask for revision
- **Comment** - Request specific modifications

### Task 2.2: Add Feedback via Comments

On the routes.py diff, add a comment:

```
Add rate limiting to prevent abuse - max 100 requests per minute per IP
```

The agent will update the code to include rate limiting.

### Task 2.3: Frontend Code Review

Review the HTML, CSS, and JavaScript diffs:

**Example: Check the CSS for responsive design**

If you notice the CSS doesn't handle mobile screens well, comment:

```
Add responsive styles for mobile devices (< 768px width)
```

### Task 2.4: Track Progress

Watch the Task List artifact update as items are completed:

```
  ☑ Create project directory structure
  ☑ Set up Flask backend with SQLAlchemy
  ☑ Define Task model
  ☑ Implement CRUD API endpoints
  ☑ Add error handling middleware
  ☐ Create HTML structure                    [In Progress]
  ☐ Style with CSS (Kanban layout)
  ☐ Implement JavaScript frontend logic
  ☐ Connect frontend to backend API
  ☐ Test complete application
```

## Part 3: Testing with Browser Agent (20 minutes)

### Task 3.1: Run the Application

Once all code is created, ask the agent:

```
Start the backend server and serve the frontend. Then test the application.
```

The agent will:
1. Install dependencies (`pip install -r requirements.txt`)
2. Start the Flask server
3. Open the frontend in the browser agent

### Task 3.2: Review Screenshots

The agent will produce screenshot artifacts showing the running application:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  SCREENSHOT: Initial Application State                             [Artifact]│
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Screenshot showing Kanban board with three empty columns:                 │
│   Todo | In Progress | Done]                                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Task 3.3: Request Functional Test

Ask the agent to test functionality:

```
Test adding a new task, moving it between columns, and deleting it.
Take screenshots of each step.
```

Review the screenshots to verify:
- ✅ Task creation works
- ✅ Drag-and-drop or status change works
- ✅ Delete functionality works

### Task 3.4: Request Browser Recording

For complex interactions:

```
Record a video showing the complete workflow: adding 3 tasks,
moving them through the columns, and deleting one.
```

The agent will produce a browser recording artifact you can watch.

## Part 4: Parallel Agent Orchestration (15 minutes)

### Task 4.1: Start Multiple Agents

Now let's improve the application using multiple agents in parallel.

In Manager View, start **three separate agents**:

**Agent 1: Documentation**
```
Create comprehensive documentation including:
- README.md with setup instructions
- API documentation for all endpoints
- Screenshots of the application
```

**Agent 2: Testing**
```
Create unit tests for the backend:
- Test all CRUD operations
- Test error handling
- Test input validation
Use pytest framework
```

**Agent 3: Enhancement**
```
Add a search/filter feature:
- Search tasks by title
- Filter by status
- Update both backend and frontend
```

### Task 4.2: Monitor Multiple Agents

In Manager View, you can see all three agents working simultaneously:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  ACTIVE AGENTS                                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  [Agent 1] Documentation                                                    │
│   └─ Status: Writing README.md...                                          │
│                                                                             │
│  [Agent 2] Testing                                                          │
│   └─ Status: Creating test_routes.py...                                    │
│                                                                             │
│  [Agent 3] Enhancement                                                      │
│   └─ Status: Updating routes.py with search endpoint...                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Task 4.3: Review and Merge

As each agent completes, review their artifacts and accept changes.

Watch for potential conflicts - if Agent 2 and Agent 3 both modify the same file, you may need to resolve merge conflicts.

## Part 5: Final Review (10 minutes)

### Task 5.1: Request Walkthrough

Ask any agent:

```
Generate a walkthrough artifact summarizing all changes made
to the project and verification steps.
```

### Task 5.2: Final Testing

Run the complete test suite:

```
Run all tests and show me the results
```

### Task 5.3: Verify Project Structure

Your final project should look like:

```
task-manager-app/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── routes.py
│   ├── requirements.txt
│   └── tests/
│       └── test_routes.py
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── app.js
├── README.md
└── API.md
```

## Deliverables

By the end of this lab, you should have:

1. ✅ Complete task management application
2. ✅ Backend with Flask API and SQLite
3. ✅ Frontend with Kanban-style UI
4. ✅ Search/filter functionality
5. ✅ Unit tests
6. ✅ Documentation (README.md, API.md)

## Evaluation Criteria

| Criteria | Points |
|----------|--------|
| Used Planning mode effectively | 15 |
| Reviewed and iterated on artifacts | 20 |
| Application runs correctly | 20 |
| Browser testing completed | 15 |
| Orchestrated multiple agents | 15 |
| All deliverables complete | 15 |
| **Total** | **100** |

## Troubleshooting

### Issue: Agents producing conflicting changes

1. Have one agent finish before starting another on the same files
2. Or use the "Undo" feature to revert to a checkpoint
3. Manually resolve conflicts if needed

### Issue: Browser agent not loading page

1. Ensure the server is actually running
2. Check the terminal for any errors
3. Try manually opening the URL to verify

### Issue: Tests failing

1. Review the test code diff carefully
2. Ensure the test expectations match your implementation
3. Comment on the test diff to request corrections

## Next Steps

Continue to [Lab 28.3: Custom Rules and Workflows](lab-03-customization.md) to learn how to create reusable configurations for team environments.
