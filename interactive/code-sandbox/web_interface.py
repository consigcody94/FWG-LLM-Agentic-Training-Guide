#!/usr/bin/env python3
"""
FWG Training - Web Interface for Code Sandbox
FastAPI-based Jupyter-style notebook interface

Features:
- Browser-based notebook interface
- Real-time code execution
- Cell management (add, delete, reorder)
- Output rendering (text, HTML, markdown)
- Variable inspection
- Notebook persistence
- Keyboard shortcuts
- Auto-save
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
    from fastapi.responses import HTMLResponse, JSONResponse
    from fastapi.staticfiles import StaticFiles
    from pydantic import BaseModel
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("⚠️  FastAPI not installed. Run: pip install fastapi uvicorn websockets")
    print("    Web interface will not be available.")

from sandbox_engine import (
    Cell, CellType, ExecutionResult, ExecutionStatus,
    Language, Notebook, NotebookEngine
)


# Pydantic models for API
class CellCreate(BaseModel):
    source: str
    cell_type: str = "code"
    language: str = "python"


class CellUpdate(BaseModel):
    source: Optional[str] = None
    cell_type: Optional[str] = None


class NotebookCreate(BaseModel):
    title: str = "Untitled Notebook"


class ExecuteRequest(BaseModel):
    cell_id: str


if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="FWG Training - Code Sandbox",
        description="Jupyter-style notebook interface for interactive learning",
        version="1.0.0"
    )

    # Global notebook engine
    engine = NotebookEngine()


    @app.get("/", response_class=HTMLResponse)
    async def root():
        """Serve the main notebook interface"""
        html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FWG Training - Code Sandbox</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        .header {
            background: white;
            padding: 20px 30px;
            border-radius: 10px 10px 0 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .header h1 {
            color: #667eea;
            font-size: 24px;
        }

        .header-buttons button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            margin-left: 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            transition: background 0.3s;
        }

        .header-buttons button:hover {
            background: #5568d3;
        }

        .header-buttons button.danger {
            background: #e74c3c;
        }

        .header-buttons button.danger:hover {
            background: #c0392b;
        }

        .notebook-title {
            font-size: 16px;
            color: #666;
        }

        .notebook {
            background: white;
            padding: 20px;
            border-radius: 0 0 10px 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }

        .cell {
            background: #f8f9fa;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            margin-bottom: 15px;
            overflow: hidden;
            transition: all 0.3s;
        }

        .cell:hover {
            border-color: #667eea;
        }

        .cell.executing {
            border-color: #f39c12;
            animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .cell-toolbar {
            background: #e9ecef;
            padding: 8px 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #dee2e6;
        }

        .cell-toolbar-left {
            display: flex;
            gap: 10px;
            align-items: center;
        }

        .cell-type-badge {
            background: #667eea;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
        }

        .execution-count {
            color: #666;
            font-size: 12px;
        }

        .cell-actions button {
            background: transparent;
            border: none;
            padding: 5px 10px;
            cursor: pointer;
            color: #666;
            font-size: 14px;
            transition: color 0.3s;
        }

        .cell-actions button:hover {
            color: #667eea;
        }

        .cell-actions button.delete:hover {
            color: #e74c3c;
        }

        .cell-input {
            padding: 15px;
        }

        .cell-input textarea {
            width: 100%;
            min-height: 100px;
            border: none;
            background: white;
            padding: 15px;
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 14px;
            border-radius: 5px;
            resize: vertical;
            outline: none;
        }

        .cell-output {
            padding: 15px;
            background: white;
            border-top: 1px solid #dee2e6;
        }

        .output-content {
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 13px;
            white-space: pre-wrap;
            color: #2c3e50;
        }

        .output-error {
            color: #e74c3c;
            background: #fadbd8;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        .output-success {
            color: #27ae60;
            background: #d5f4e6;
            padding: 10px;
            border-radius: 5px;
            margin-top: 10px;
        }

        .execution-stats {
            font-size: 12px;
            color: #7f8c8d;
            margin-top: 10px;
            padding-top: 10px;
            border-top: 1px solid #ecf0f1;
        }

        .add-cell-button {
            width: 100%;
            padding: 15px;
            background: #ecf0f1;
            border: 2px dashed #bdc3c7;
            border-radius: 8px;
            color: #7f8c8d;
            font-size: 14px;
            cursor: pointer;
            transition: all 0.3s;
        }

        .add-cell-button:hover {
            background: #667eea;
            border-color: #667eea;
            color: white;
        }

        .variables-panel {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .variables-panel h3 {
            color: #667eea;
            margin-bottom: 15px;
        }

        .variable-item {
            background: #f8f9fa;
            padding: 10px;
            margin-bottom: 8px;
            border-radius: 5px;
            font-family: 'Monaco', 'Menlo', 'Courier New', monospace;
            font-size: 13px;
        }

        .variable-name {
            color: #667eea;
            font-weight: 600;
        }

        .variable-value {
            color: #2c3e50;
        }

        .status-bar {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #2c3e50;
            color: white;
            padding: 10px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
        }

        .status-indicator {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #27ae60;
        }

        .status-dot.error {
            background: #e74c3c;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }

        .modal.active {
            display: flex;
        }

        .modal-content {
            background: white;
            padding: 30px;
            border-radius: 10px;
            max-width: 500px;
            width: 90%;
        }

        .modal-content h2 {
            color: #667eea;
            margin-bottom: 20px;
        }

        .modal-content input {
            width: 100%;
            padding: 10px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            margin-bottom: 20px;
            font-size: 14px;
        }

        .modal-buttons {
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }

        .modal-buttons button {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }

        .modal-buttons button.primary {
            background: #667eea;
            color: white;
        }

        .modal-buttons button.secondary {
            background: #e9ecef;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div>
                <h1>🏛️ FWG Training - Code Sandbox</h1>
                <div class="notebook-title" id="notebookTitle">Untitled Notebook</div>
            </div>
            <div class="header-buttons">
                <button onclick="newNotebook()">📝 New</button>
                <button onclick="saveNotebook()">💾 Save</button>
                <button onclick="loadNotebook()">📂 Load</button>
                <button onclick="executeAll()">▶️ Run All</button>
                <button onclick="clearAll()" class="danger">🗑️ Clear All</button>
            </div>
        </div>

        <div class="notebook" id="notebook">
            <!-- Cells will be dynamically added here -->
        </div>

        <button class="add-cell-button" onclick="addCell('code')">
            ➕ Add Code Cell (Shift+Enter to execute)
        </button>

        <div class="variables-panel" style="margin-top: 20px;">
            <h3>📊 Variables in Memory</h3>
            <div id="variables">
                <p style="color: #999;">No variables yet. Execute some code!</p>
            </div>
        </div>
    </div>

    <div class="status-bar">
        <div class="status-indicator">
            <div class="status-dot" id="statusDot"></div>
            <span id="statusText">Ready</span>
        </div>
        <div>
            <span id="cellCount">0 cells</span> •
            <span id="lastSaved">Not saved</span>
        </div>
    </div>

    <div class="modal" id="loadModal">
        <div class="modal-content">
            <h2>Load Notebook</h2>
            <div id="notebookList"></div>
            <div class="modal-buttons">
                <button class="secondary" onclick="closeModal()">Cancel</button>
            </div>
        </div>
    </div>

    <script>
        let currentNotebookId = null;
        let cells = [];

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {
            createNewNotebook();
        });

        async function createNewNotebook() {
            const response = await fetch('/api/notebooks', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({title: 'Untitled Notebook'})
            });

            const notebook = await response.json();
            currentNotebookId = notebook.id;
            document.getElementById('notebookTitle').textContent = notebook.title;

            // Add initial cell
            addCell('code');
            updateStatus('New notebook created', false);
        }

        async function addCell(type = 'code') {
            if (!currentNotebookId) await createNewNotebook();

            const response = await fetch(`/api/notebooks/${currentNotebookId}/cells`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    source: '',
                    cell_type: type,
                    language: 'python'
                })
            });

            const cell = await response.json();
            renderCell(cell);
            updateCellCount();
        }

        function renderCell(cell) {
            const notebook = document.getElementById('notebook');
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            cellDiv.id = `cell-${cell.id}`;

            const output = cell.outputs && cell.outputs.length > 0 ? cell.outputs[cell.outputs.length - 1] : null;

            cellDiv.innerHTML = `
                <div class="cell-toolbar">
                    <div class="cell-toolbar-left">
                        <span class="cell-type-badge">${cell.cell_type}</span>
                        <span class="execution-count">In [${cell.execution_count || ' '}]</span>
                    </div>
                    <div class="cell-actions">
                        <button onclick="executeCell('${cell.id}')" title="Run (Shift+Enter)">▶️</button>
                        <button onclick="clearCellOutput('${cell.id}')" title="Clear Output">🗑️</button>
                        <button onclick="deleteCell('${cell.id}')" class="delete" title="Delete Cell">❌</button>
                    </div>
                </div>
                <div class="cell-input">
                    <textarea id="input-${cell.id}" onkeydown="handleKeydown(event, '${cell.id}')">${cell.source}</textarea>
                </div>
                <div class="cell-output" id="output-${cell.id}" style="display: ${output ? 'block' : 'none'}">
                    ${output ? renderOutput(output) : ''}
                </div>
            `;

            notebook.appendChild(cellDiv);
        }

        function renderOutput(output) {
            let html = '';

            if (output.output) {
                html += `<div class="output-content">${escapeHtml(output.output)}</div>`;
            }

            if (output.error) {
                html += `<div class="output-error">${escapeHtml(output.error)}</div>`;
            } else if (output.status === 'success') {
                html += `<div class="output-success">✅ Executed successfully</div>`;
            }

            if (output.execution_time) {
                html += `<div class="execution-stats">⏱️ ${output.execution_time.toFixed(4)}s</div>`;
            }

            return html;
        }

        async function executeCell(cellId) {
            const cellDiv = document.getElementById(`cell-${cellId}`);
            const textarea = document.getElementById(`input-${cellId}`);
            const source = textarea.value;

            // Update cell source
            await fetch(`/api/notebooks/${currentNotebookId}/cells/${cellId}`, {
                method: 'PATCH',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({source})
            });

            // Mark as executing
            cellDiv.classList.add('executing');
            updateStatus('Executing...', false);

            try {
                const response = await fetch(`/api/notebooks/${currentNotebookId}/cells/${cellId}/execute`, {
                    method: 'POST'
                });

                const result = await response.json();

                // Display output
                const outputDiv = document.getElementById(`output-${cellId}`);
                outputDiv.style.display = 'block';
                outputDiv.innerHTML = renderOutput(result);

                // Update execution count
                const countSpan = cellDiv.querySelector('.execution-count');
                const execCount = parseInt(countSpan.textContent.match(/\\d+/)?.[0] || 0) + 1;
                countSpan.textContent = `In [${execCount}]`;

                updateStatus(result.status === 'success' ? 'Execution complete' : 'Execution failed', result.status !== 'success');

                // Update variables
                await refreshVariables();

            } catch (error) {
                updateStatus('Execution error', true);
            } finally {
                cellDiv.classList.remove('executing');
            }
        }

        async function executeAll() {
            updateStatus('Executing all cells...', false);
            const response = await fetch(`/api/notebooks/${currentNotebookId}/execute`, {
                method: 'POST'
            });
            const results = await response.json();
            updateStatus(`Executed ${results.length} cells`, false);

            // Reload notebook to show results
            await loadCurrentNotebook();
        }

        async function refreshVariables() {
            const response = await fetch(`/api/notebooks/${currentNotebookId}/variables`);
            const variables = await response.json();

            const varsDiv = document.getElementById('variables');
            if (Object.keys(variables).length === 0) {
                varsDiv.innerHTML = '<p style="color: #999;">No variables yet. Execute some code!</p>';
            } else {
                varsDiv.innerHTML = Object.entries(variables).map(([name, value]) => `
                    <div class="variable-item">
                        <span class="variable-name">${name}</span> = <span class="variable-value">${JSON.stringify(value)}</span>
                    </div>
                `).join('');
            }
        }

        async function clearCellOutput(cellId) {
            const outputDiv = document.getElementById(`output-${cellId}`);
            outputDiv.style.display = 'none';
            outputDiv.innerHTML = '';
        }

        async function deleteCell(cellId) {
            if (!confirm('Delete this cell?')) return;

            await fetch(`/api/notebooks/${currentNotebookId}/cells/${cellId}`, {
                method: 'DELETE'
            });

            document.getElementById(`cell-${cellId}`).remove();
            updateCellCount();
        }

        async function clearAll() {
            if (!confirm('Clear all outputs?')) return;

            await fetch(`/api/notebooks/${currentNotebookId}/clear`, {
                method: 'POST'
            });

            document.querySelectorAll('.cell-output').forEach(div => {
                div.style.display = 'none';
                div.innerHTML = '';
            });

            updateStatus('All outputs cleared', false);
        }

        async function saveNotebook() {
            const response = await fetch(`/api/notebooks/${currentNotebookId}/save`, {
                method: 'POST'
            });

            if (response.ok) {
                updateStatus('Notebook saved', false);
                document.getElementById('lastSaved').textContent = `Saved at ${new Date().toLocaleTimeString()}`;
            }
        }

        async function loadCurrentNotebook() {
            const response = await fetch(`/api/notebooks/${currentNotebookId}`);
            const notebook = await response.json();

            document.getElementById('notebook').innerHTML = '';
            notebook.cells.forEach(renderCell);
            document.getElementById('notebookTitle').textContent = notebook.title;
            updateCellCount();
        }

        function handleKeydown(event, cellId) {
            if (event.shiftKey && event.key === 'Enter') {
                event.preventDefault();
                executeCell(cellId);
            }
        }

        function updateStatus(text, isError = false) {
            document.getElementById('statusText').textContent = text;
            const dot = document.getElementById('statusDot');
            dot.className = isError ? 'status-dot error' : 'status-dot';
        }

        function updateCellCount() {
            const count = document.querySelectorAll('.cell').length;
            document.getElementById('cellCount').textContent = `${count} cell${count !== 1 ? 's' : ''}`;
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function newNotebook() {
            if (confirm('Create a new notebook? Unsaved changes will be lost.')) {
                createNewNotebook();
            }
        }

        function closeModal() {
            document.getElementById('loadModal').classList.remove('active');
        }
    </script>
</body>
</html>
        """
        return HTMLResponse(content=html_content)


    @app.post("/api/notebooks")
    async def create_notebook(notebook: NotebookCreate):
        """Create a new notebook"""
        nb = engine.create_notebook(notebook.title)
        return {"id": nb.id, "title": nb.title, "created_at": nb.created_at.isoformat()}


    @app.get("/api/notebooks")
    async def list_notebooks():
        """List all notebooks"""
        return engine.list_notebooks()


    @app.get("/api/notebooks/{notebook_id}")
    async def get_notebook(notebook_id: str):
        """Get a specific notebook"""
        notebook = engine.load_notebook(notebook_id)
        if notebook is None:
            raise HTTPException(status_code=404, detail="Notebook not found")
        return notebook.to_dict()


    @app.post("/api/notebooks/{notebook_id}/cells")
    async def add_cell(notebook_id: str, cell: CellCreate):
        """Add a cell to notebook"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        if cell.cell_type == "code":
            new_cell = engine.add_code_cell(
                cell.source,
                Language(cell.language)
            )
        else:
            new_cell = engine.add_markdown_cell(cell.source)

        return {
            "id": new_cell.id,
            "cell_type": new_cell.cell_type.value,
            "source": new_cell.source,
            "language": new_cell.language.value,
            "execution_count": new_cell.execution_count,
            "outputs": []
        }


    @app.patch("/api/notebooks/{notebook_id}/cells/{cell_id}")
    async def update_cell(notebook_id: str, cell_id: str, update: CellUpdate):
        """Update a cell"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        cell = engine.current_notebook.get_cell(cell_id)
        if cell is None:
            raise HTTPException(status_code=404, detail="Cell not found")

        if update.source is not None:
            cell.source = update.source
        if update.cell_type is not None:
            cell.cell_type = CellType(update.cell_type)

        cell.modified_at = datetime.now()
        engine.current_notebook.modified_at = datetime.now()

        return {"status": "updated"}


    @app.delete("/api/notebooks/{notebook_id}/cells/{cell_id}")
    async def delete_cell(notebook_id: str, cell_id: str):
        """Delete a cell"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        success = engine.current_notebook.delete_cell(cell_id)
        if not success:
            raise HTTPException(status_code=404, detail="Cell not found")

        return {"status": "deleted"}


    @app.post("/api/notebooks/{notebook_id}/cells/{cell_id}/execute")
    async def execute_cell(notebook_id: str, cell_id: str):
        """Execute a specific cell"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        result = engine.execute_cell(cell_id)

        return {
            "status": result.status.value,
            "output": result.output,
            "error": result.error,
            "execution_time": result.execution_time,
            "stdout": result.stdout,
            "stderr": result.stderr
        }


    @app.post("/api/notebooks/{notebook_id}/execute")
    async def execute_all(notebook_id: str):
        """Execute all cells in notebook"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        results = engine.execute_all_cells()

        return [
            {
                "status": result.status.value,
                "output": result.output,
                "error": result.error,
                "execution_time": result.execution_time
            }
            for result in results
        ]


    @app.post("/api/notebooks/{notebook_id}/clear")
    async def clear_outputs(notebook_id: str):
        """Clear all cell outputs"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        engine.clear_outputs()
        return {"status": "cleared"}


    @app.post("/api/notebooks/{notebook_id}/save")
    async def save_notebook(notebook_id: str):
        """Save notebook to disk"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        success = engine.save_current_notebook()
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save notebook")

        return {"status": "saved"}


    @app.get("/api/notebooks/{notebook_id}/variables")
    async def get_variables(notebook_id: str):
        """Get current variables in namespace"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        variables = engine.get_namespace_variables()

        # Convert to JSON-serializable format
        serializable_vars = {}
        for name, value in variables.items():
            try:
                json.dumps(value)
                serializable_vars[name] = value
            except (TypeError, ValueError):
                serializable_vars[name] = str(value)

        return serializable_vars


    @app.post("/api/notebooks/{notebook_id}/reset")
    async def reset_sandbox(notebook_id: str):
        """Reset the sandbox environment"""
        if engine.current_notebook is None or engine.current_notebook.id != notebook_id:
            notebook = engine.load_notebook(notebook_id)
            if notebook is None:
                raise HTTPException(status_code=404, detail="Notebook not found")

        engine.reset_sandbox()
        return {"status": "reset"}


def start_server(host: str = "127.0.0.1", port: int = 8000):
    """Start the web server"""
    if not FASTAPI_AVAILABLE:
        print("❌ FastAPI not installed. Cannot start web server.")
        print("   Install with: pip install fastapi uvicorn websockets")
        return

    print("=" * 70)
    print("🚀 Starting FWG Training Code Sandbox Web Interface")
    print("=" * 70)
    print(f"\n📍 Server running at: http://{host}:{port}")
    print(f"📂 Notebooks saved to: {engine.notebooks_dir}")
    print("\n💡 Tips:")
    print("  • Press Shift+Enter to execute a cell")
    print("  • Use 'Run All' to execute all cells in order")
    print("  • Variables persist between cell executions")
    print("  • Auto-save your work regularly!")
    print("\n" + "=" * 70 + "\n")

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    start_server()
