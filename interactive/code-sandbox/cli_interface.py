#!/usr/bin/env python3
"""
FWG Training - CLI Interface for Code Sandbox
Terminal-based notebook interface for quick experimentation

Usage:
    python cli_interface.py                    # Start interactive mode
    python cli_interface.py --file notebook.json   # Load specific notebook
    python cli_interface.py --demo             # Run demo
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.syntax import Syntax
    from rich.table import Table
    from rich.layout import Layout
    from rich.live import Live
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️  Rich not installed. Run: pip install rich")
    print("    CLI will use basic output.")

from sandbox_engine import NotebookEngine, Language, CellType


class NotebookCLI:
    """CLI interface for notebook management"""

    def __init__(self):
        self.engine = NotebookEngine()
        if RICH_AVAILABLE:
            self.console = Console()
        self.running = True

    def display_header(self):
        """Display the application header"""
        if RICH_AVAILABLE:
            header = Panel(
                "[bold blue]🏛️ FWG Training - Code Sandbox CLI[/bold blue]\n"
                "[dim]Jupyter-style notebooks for federal AI training[/dim]",
                border_style="blue",
                box=box.DOUBLE
            )
            self.console.print(header)
        else:
            print("=" * 70)
            print("🏛️ FWG Training - Code Sandbox CLI")
            print("Jupyter-style notebooks for federal AI training")
            print("=" * 70)

    def display_menu(self):
        """Display the main menu"""
        if RICH_AVAILABLE:
            menu = Table(title="📋 Main Menu", box=box.ROUNDED)
            menu.add_column("Command", style="cyan", no_wrap=True)
            menu.add_column("Description", style="white")

            commands = [
                ("new", "Create a new notebook"),
                ("load", "Load an existing notebook"),
                ("list", "List all notebooks"),
                ("add", "Add a new cell"),
                ("edit", "Edit a cell"),
                ("run", "Execute a cell"),
                ("runall", "Execute all cells"),
                ("show", "Show notebook contents"),
                ("vars", "Display variables in memory"),
                ("clear", "Clear all outputs"),
                ("reset", "Reset sandbox environment"),
                ("save", "Save current notebook"),
                ("export", "Export notebook to file"),
                ("help", "Show this menu"),
                ("exit", "Exit the application"),
            ]

            for cmd, desc in commands:
                menu.add_row(cmd, desc)

            self.console.print(menu)
        else:
            print("\n📋 Main Menu:")
            print("  new      - Create a new notebook")
            print("  load     - Load an existing notebook")
            print("  list     - List all notebooks")
            print("  add      - Add a new cell")
            print("  edit     - Edit a cell")
            print("  run      - Execute a cell")
            print("  runall   - Execute all cells")
            print("  show     - Show notebook contents")
            print("  vars     - Display variables in memory")
            print("  clear    - Clear all outputs")
            print("  reset    - Reset sandbox environment")
            print("  save     - Save current notebook")
            print("  export   - Export notebook to file")
            print("  help     - Show this menu")
            print("  exit     - Exit the application")

    def create_notebook(self):
        """Create a new notebook"""
        if RICH_AVAILABLE:
            title = Prompt.ask("[cyan]Notebook title[/cyan]", default="Untitled Notebook")
        else:
            title = input("Notebook title [Untitled Notebook]: ") or "Untitled Notebook"

        notebook = self.engine.create_notebook(title)

        if RICH_AVAILABLE:
            self.console.print(f"\n✅ Created notebook: [green]{notebook.title}[/green] (ID: {notebook.id})")
        else:
            print(f"\n✅ Created notebook: {notebook.title} (ID: {notebook.id})")

    def list_notebooks(self):
        """List all saved notebooks"""
        notebooks = self.engine.list_notebooks()

        if not notebooks:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No saved notebooks found.[/yellow]")
            else:
                print("No saved notebooks found.")
            return

        if RICH_AVAILABLE:
            table = Table(title=f"📚 Saved Notebooks ({len(notebooks)})", box=box.ROUNDED)
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Last Modified", style="dim")

            for nb in notebooks:
                table.add_row(
                    nb['id'][:8] + "...",
                    nb['title'],
                    nb.get('modified_at', 'Unknown')[:19]
                )

            self.console.print(table)
        else:
            print(f"\n📚 Saved Notebooks ({len(notebooks)}):")
            for nb in notebooks:
                print(f"  {nb['id'][:8]}... - {nb['title']} (Modified: {nb.get('modified_at', 'Unknown')[:19]})")

    def load_notebook(self):
        """Load an existing notebook"""
        if RICH_AVAILABLE:
            notebook_id = Prompt.ask("[cyan]Enter notebook ID[/cyan]")
        else:
            notebook_id = input("Enter notebook ID: ")

        notebook = self.engine.load_notebook(notebook_id)

        if notebook:
            if RICH_AVAILABLE:
                self.console.print(f"\n✅ Loaded: [green]{notebook.title}[/green] ({len(notebook.cells)} cells)")
            else:
                print(f"\n✅ Loaded: {notebook.title} ({len(notebook.cells)} cells)")
        else:
            if RICH_AVAILABLE:
                self.console.print(f"[red]❌ Notebook {notebook_id} not found[/red]")
            else:
                print(f"❌ Notebook {notebook_id} not found")

    def add_cell(self):
        """Add a new cell to the notebook"""
        if self.engine.current_notebook is None:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No notebook loaded. Creating new notebook...[/yellow]")
            else:
                print("No notebook loaded. Creating new notebook...")
            self.create_notebook()

        if RICH_AVAILABLE:
            cell_type = Prompt.ask(
                "[cyan]Cell type[/cyan]",
                choices=["code", "markdown"],
                default="code"
            )
        else:
            cell_type = input("Cell type (code/markdown) [code]: ") or "code"

        if RICH_AVAILABLE:
            self.console.print("[dim]Enter cell content (press Enter twice to finish):[/dim]")
        else:
            print("Enter cell content (press Enter twice to finish):")

        lines = []
        empty_lines = 0

        while True:
            try:
                line = input()
                if line == "":
                    empty_lines += 1
                    if empty_lines >= 2:
                        break
                    lines.append(line)
                else:
                    empty_lines = 0
                    lines.append(line)
            except EOFError:
                break

        # Remove trailing empty lines
        while lines and lines[-1] == "":
            lines.pop()

        content = "\n".join(lines)

        if cell_type == "code":
            cell = self.engine.add_code_cell(content, Language.PYTHON)
        else:
            cell = self.engine.add_markdown_cell(content)

        if RICH_AVAILABLE:
            self.console.print(f"\n✅ Added {cell_type} cell (ID: {cell.id[:8]}...)")
        else:
            print(f"\n✅ Added {cell_type} cell (ID: {cell.id[:8]}...)")

    def show_notebook(self):
        """Show notebook contents"""
        if self.engine.current_notebook is None:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No notebook loaded.[/yellow]")
            else:
                print("No notebook loaded.")
            return

        notebook = self.engine.current_notebook

        if RICH_AVAILABLE:
            self.console.print(f"\n[bold blue]📓 {notebook.title}[/bold blue]")
            self.console.print(f"[dim]ID: {notebook.id}[/dim]")
            self.console.print(f"[dim]Cells: {len(notebook.cells)}[/dim]\n")

            for i, cell in enumerate(notebook.cells, 1):
                panel_title = f"Cell {i} [{cell.cell_type.value}] - In[{cell.execution_count}]"

                if cell.cell_type == CellType.CODE:
                    syntax = Syntax(
                        cell.source,
                        cell.language.value,
                        theme="monokai",
                        line_numbers=True
                    )
                    self.console.print(Panel(syntax, title=panel_title, border_style="cyan"))

                    # Show latest output
                    if cell.outputs:
                        latest = cell.outputs[-1]
                        output_text = ""

                        if latest.output:
                            output_text += latest.output

                        if latest.error:
                            output_text += f"\n[red]{latest.error}[/red]"

                        if output_text:
                            self.console.print(Panel(
                                output_text,
                                title=f"Output - {latest.status.value}",
                                border_style="green" if latest.status.value == "success" else "red"
                            ))

                else:
                    self.console.print(Panel(cell.source, title=panel_title, border_style="blue"))

                self.console.print()

        else:
            print(f"\n📓 {notebook.title}")
            print(f"ID: {notebook.id}")
            print(f"Cells: {len(notebook.cells)}\n")

            for i, cell in enumerate(notebook.cells, 1):
                print(f"{'='*70}")
                print(f"Cell {i} [{cell.cell_type.value}] - In[{cell.execution_count}]")
                print(f"{'='*70}")
                print(cell.source)

                if cell.outputs:
                    latest = cell.outputs[-1]
                    print(f"\nOutput [{latest.status.value}]:")
                    if latest.output:
                        print(latest.output)
                    if latest.error:
                        print(f"Error: {latest.error}")

                print()

    def execute_cell(self):
        """Execute a specific cell"""
        if self.engine.current_notebook is None:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No notebook loaded.[/yellow]")
            else:
                print("No notebook loaded.")
            return

        # Show cells
        cells = self.engine.current_notebook.cells
        if not cells:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No cells in notebook.[/yellow]")
            else:
                print("No cells in notebook.")
            return

        if RICH_AVAILABLE:
            print("\nAvailable cells:")
            for i, cell in enumerate(cells, 1):
                preview = cell.source[:50].replace('\n', ' ')
                if len(cell.source) > 50:
                    preview += "..."
                self.console.print(f"  {i}. [{cell.cell_type.value}] {preview}")

            choice = Prompt.ask("\n[cyan]Cell number to execute[/cyan]", default="1")
        else:
            print("\nAvailable cells:")
            for i, cell in enumerate(cells, 1):
                preview = cell.source[:50].replace('\n', ' ')
                if len(cell.source) > 50:
                    preview += "..."
                print(f"  {i}. [{cell.cell_type.value}] {preview}")

            choice = input("\nCell number to execute [1]: ") or "1"

        try:
            cell_index = int(choice) - 1
            if cell_index < 0 or cell_index >= len(cells):
                raise ValueError()

            cell = cells[cell_index]

            if RICH_AVAILABLE:
                self.console.print(f"\n▶️  Executing cell {choice}...")
            else:
                print(f"\n▶️  Executing cell {choice}...")

            result = self.engine.execute_cell(cell.id)

            if RICH_AVAILABLE:
                status_color = "green" if result.status.value == "success" else "red"
                self.console.print(f"\n[{status_color}]{result.status.value.upper()}[/{status_color}]")
                self.console.print(f"[dim]Time: {result.execution_time:.4f}s[/dim]\n")

                if result.output:
                    self.console.print(Panel(result.output, title="Output", border_style="green"))

                if result.error:
                    self.console.print(Panel(result.error, title="Error", border_style="red"))
            else:
                print(f"\n{result.status.value.upper()}")
                print(f"Time: {result.execution_time:.4f}s\n")

                if result.output:
                    print("Output:")
                    print(result.output)

                if result.error:
                    print("Error:")
                    print(result.error)

        except (ValueError, IndexError):
            if RICH_AVAILABLE:
                self.console.print("[red]Invalid cell number[/red]")
            else:
                print("Invalid cell number")

    def execute_all(self):
        """Execute all cells"""
        if self.engine.current_notebook is None:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No notebook loaded.[/yellow]")
            else:
                print("No notebook loaded.")
            return

        if RICH_AVAILABLE:
            self.console.print("\n▶️  Executing all cells...\n")
        else:
            print("\n▶️  Executing all cells...\n")

        results = self.engine.execute_all_cells()

        for i, result in enumerate(results, 1):
            if RICH_AVAILABLE:
                status_color = "green" if result.status.value == "success" else "red"
                self.console.print(f"Cell {i}: [{status_color}]{result.status.value}[/{status_color}] ({result.execution_time:.4f}s)")
            else:
                print(f"Cell {i}: {result.status.value} ({result.execution_time:.4f}s)")

        if RICH_AVAILABLE:
            self.console.print(f"\n✅ Executed {len(results)} cells")
        else:
            print(f"\n✅ Executed {len(results)} cells")

    def show_variables(self):
        """Display current variables"""
        variables = self.engine.get_namespace_variables()

        if not variables:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No variables in memory. Execute some code first![/yellow]")
            else:
                print("No variables in memory. Execute some code first!")
            return

        if RICH_AVAILABLE:
            table = Table(title="📊 Variables in Memory", box=box.ROUNDED)
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Type", style="yellow")
            table.add_column("Value", style="white")

            for name, value in variables.items():
                value_str = repr(value)
                if len(value_str) > 50:
                    value_str = value_str[:50] + "..."

                table.add_row(name, type(value).__name__, value_str)

            self.console.print(table)
        else:
            print("\n📊 Variables in Memory:")
            for name, value in variables.items():
                value_str = repr(value)
                if len(value_str) > 50:
                    value_str = value_str[:50] + "..."
                print(f"  {name} ({type(value).__name__}) = {value_str}")

    def save_notebook(self):
        """Save current notebook"""
        if self.engine.current_notebook is None:
            if RICH_AVAILABLE:
                self.console.print("[yellow]No notebook to save.[/yellow]")
            else:
                print("No notebook to save.")
            return

        success = self.engine.save_current_notebook()

        if success:
            if RICH_AVAILABLE:
                self.console.print(f"✅ Notebook saved: [green]{self.engine.current_notebook.title}[/green]")
            else:
                print(f"✅ Notebook saved: {self.engine.current_notebook.title}")
        else:
            if RICH_AVAILABLE:
                self.console.print("[red]❌ Failed to save notebook[/red]")
            else:
                print("❌ Failed to save notebook")

    def run(self):
        """Main CLI loop"""
        self.display_header()
        self.display_menu()

        while self.running:
            try:
                if RICH_AVAILABLE:
                    command = Prompt.ask("\n[bold cyan]sandbox>[/bold cyan]", default="help").strip().lower()
                else:
                    command = input("\nsandbox> ").strip().lower() or "help"

                if command == "exit":
                    if RICH_AVAILABLE:
                        if Confirm.ask("Save notebook before exiting?", default=True):
                            self.save_notebook()
                        self.console.print("\n[blue]👋 Goodbye![/blue]")
                    else:
                        save = input("Save notebook before exiting? (y/n) [y]: ") or "y"
                        if save.lower() == "y":
                            self.save_notebook()
                        print("\n👋 Goodbye!")
                    self.running = False

                elif command == "new":
                    self.create_notebook()
                elif command == "load":
                    self.load_notebook()
                elif command == "list":
                    self.list_notebooks()
                elif command == "add":
                    self.add_cell()
                elif command == "show":
                    self.show_notebook()
                elif command == "run":
                    self.execute_cell()
                elif command == "runall":
                    self.execute_all()
                elif command == "vars":
                    self.show_variables()
                elif command == "clear":
                    self.engine.clear_outputs()
                    if RICH_AVAILABLE:
                        self.console.print("✅ All outputs cleared")
                    else:
                        print("✅ All outputs cleared")
                elif command == "reset":
                    self.engine.reset_sandbox()
                    if RICH_AVAILABLE:
                        self.console.print("✅ Sandbox environment reset")
                    else:
                        print("✅ Sandbox environment reset")
                elif command == "save":
                    self.save_notebook()
                elif command == "help":
                    self.display_menu()
                else:
                    if RICH_AVAILABLE:
                        self.console.print(f"[red]Unknown command: {command}[/red]")
                        self.console.print("[dim]Type 'help' for available commands[/dim]")
                    else:
                        print(f"Unknown command: {command}")
                        print("Type 'help' for available commands")

            except KeyboardInterrupt:
                print()
                if RICH_AVAILABLE:
                    if Confirm.ask("\nReally exit?", default=False):
                        self.running = False
                else:
                    confirm = input("\nReally exit? (y/n) [n]: ") or "n"
                    if confirm.lower() == "y":
                        self.running = False

            except Exception as e:
                if RICH_AVAILABLE:
                    self.console.print(f"[red]Error: {e}[/red]")
                else:
                    print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description="FWG Training Code Sandbox CLI")
    parser.add_argument("--file", help="Load specific notebook file")
    parser.add_argument("--demo", action="store_true", help="Run demo")

    args = parser.parse_args()

    cli = NotebookCLI()

    if args.demo:
        # Run demo mode
        print("Running demo...")
        cli.create_notebook()
        # Add demo cells
        cli.engine.add_code_cell("print('Hello from FWG Training Sandbox!')")
        cli.engine.add_code_cell("numbers = [1, 2, 3, 4, 5]\nprint(f'Sum: {sum(numbers)}')")
        cli.execute_all()
        cli.show_notebook()
        return

    if args.file:
        # Load specific file
        notebook_id = Path(args.file).stem
        cli.engine.load_notebook(notebook_id)

    cli.run()


if __name__ == "__main__":
    main()
