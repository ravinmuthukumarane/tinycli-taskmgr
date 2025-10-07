"""Main CLI application for Tiny Task Manager."""

import typer
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from datetime import datetime
import csv
import json

from .storage import TaskStorage

app = typer.Typer(
    name="tinytask",
    help="🎯 A tiny CLI task manager for personal productivity",
    add_completion=False,
)

console = Console()
storage = TaskStorage()

# Priority colors
PRIORITY_COLORS = {
    "low": "blue",
    "medium": "yellow",
    "high": "red"
}

PRIORITY_SYMBOLS = {
    "low": "○",
    "medium": "◐",
    "high": "●"
}


@app.command()
def add(
    title: str = typer.Argument(..., help="Task description"),
    tags: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Add tags (can be used multiple times)"),
    priority: str = typer.Option("medium", "--priority", "-p", help="Priority: low, medium, or high"),
):
    """
    ➕ Add a new task.
    
    Example:
        task add "Buy groceries" --tag shopping --tag personal --priority high
    """
    if priority not in ["low", "medium", "high"]:
        console.print("[red]❌ Priority must be: low, medium, or high[/red]")
        raise typer.Exit(1)
    
    task = storage.add_task(title, tags, priority)
    
    console.print(f"\n[green]✓[/green] Task added with ID [bold]{task['id']}[/bold]")
    _display_task(task)


@app.command()
def list(
    all: bool = typer.Option(False, "--all", "-a", help="Show completed tasks too"),
    tag: Optional[str] = typer.Option(None, "--tag", "-t", help="Filter by tag"),
    priority: Optional[str] = typer.Option(None, "--priority", "-p", help="Filter by priority"),
):
    """
    📋 List tasks with optional filtering.
    
    Example:
        task list
        task list --all
        task list --tag work --priority high
    """
    tasks = storage.get_tasks(show_done=all, tag_filter=tag, priority_filter=priority)
    
    if not tasks:
        console.print("\n[yellow]📭 No tasks found![/yellow]")
        if not all:
            console.print("[dim]Tip: Use --all to see completed tasks[/dim]\n")
        return
    
    # Create table
    table = Table(
        show_header=True,
        header_style="bold cyan",
        box=box.ROUNDED,
        title="📋 Tasks" if not tag and not priority else f"📋 Filtered Tasks",
        title_style="bold magenta"
    )
    
    table.add_column("ID", style="dim", width=4)
    table.add_column("Status", width=6)
    table.add_column("Priority", width=8)
    table.add_column("Title", style="white")
    table.add_column("Tags", style="cyan")
    
    for task in tasks:
        status = "✓" if task['done'] else "○"
        status_color = "green" if task['done'] else "white"
        
        priority_text = task.get('priority', 'medium')
        priority_symbol = PRIORITY_SYMBOLS.get(priority_text, "○")
        priority_color = PRIORITY_COLORS.get(priority_text, "white")
        
        tags_str = ", ".join(f"#{t}" for t in task.get('tags', []))
        
        title = task['title']
        if task['done']:
            title = f"[dim strikethrough]{title}[/dim strikethrough]"
        
        table.add_row(
            str(task['id']),
            f"[{status_color}]{status}[/{status_color}]",
            f"[{priority_color}]{priority_symbol} {priority_text}[/{priority_color}]",
            title,
            tags_str or "[dim]—[/dim]"
        )
    
    console.print()
    console.print(table)
    console.print()
    
    # Summary
    total = len(tasks)
    done_count = sum(1 for t in tasks if t['done'])
    pending = total - done_count
    
    if all:
        console.print(f"[dim]Total: {total} | Done: {done_count} | Pending: {pending}[/dim]\n")


@app.command()
def done(
    task_id: int = typer.Argument(..., help="ID of the task to mark as done"),
):
    """
    ✓ Mark a task as completed.
    
    Example:
        task done 1
    """
    task = storage.mark_done(task_id)
    
    if task:
        console.print(f"\n[green]✓[/green] Task [bold]{task_id}[/bold] marked as done!")
        _display_task(task)
    else:
        console.print(f"\n[red]❌ Task with ID {task_id} not found[/red]\n")
        raise typer.Exit(1)


@app.command()
def undone(
    task_id: int = typer.Argument(..., help="ID of the task to mark as not done"),
):
    """
    ○ Mark a task as not done (reopen it).
    
    Example:
        task undone 1
    """
    task = storage.mark_undone(task_id)
    
    if task:
        console.print(f"\n[yellow]○[/yellow] Task [bold]{task_id}[/bold] marked as not done!")
        _display_task(task)
    else:
        console.print(f"\n[red]❌ Task with ID {task_id} not found[/red]\n")
        raise typer.Exit(1)


@app.command()
def delete(
    task_id: int = typer.Argument(..., help="ID of the task to delete"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """
    🗑️  Delete a task permanently.
    
    Example:
        task delete 1
        task delete 1 --force
    """
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete task {task_id}?")
        if not confirm:
            console.print("\n[yellow]Cancelled[/yellow]\n")
            raise typer.Abort()
    
    if storage.delete_task(task_id):
        console.print(f"\n[green]✓[/green] Task [bold]{task_id}[/bold] deleted\n")
    else:
        console.print(f"\n[red]❌ Task with ID {task_id} not found[/red]\n")
        raise typer.Exit(1)


@app.command()
def tag(
    task_id: int = typer.Argument(..., help="ID of the task"),
    tags: List[str] = typer.Argument(..., help="Tags to set (replaces existing tags)"),
):
    """
    🏷️  Update tags for a task.
    
    Example:
        task tag 1 work urgent
    """
    task = storage.update_task_tags(task_id, tags)
    
    if task:
        console.print(f"\n[green]✓[/green] Tags updated for task [bold]{task_id}[/bold]")
        _display_task(task)
    else:
        console.print(f"\n[red]❌ Task with ID {task_id} not found[/red]\n")
        raise typer.Exit(1)


@app.command()
def export(
    format: str = typer.Option("json", "--format", "-f", help="Export format: json or csv"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    all: bool = typer.Option(False, "--all", "-a", help="Include completed tasks"),
):
    """
    💾 Export tasks to a file.
    
    Example:
        task export --format json --output tasks_backup.json
        task export --format csv --output tasks.csv --all
    """
    tasks = storage.get_tasks(show_done=all)
    
    if not tasks:
        console.print("\n[yellow]No tasks to export[/yellow]\n")
        return
    
    # Generate default filename if not provided
    if output is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"tasks_{timestamp}.{format}"
    
    try:
        if format == "json":
            with open(output, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, indent=2, ensure_ascii=False)
        elif format == "csv":
            with open(output, 'w', newline='', encoding='utf-8') as f:
                if tasks:
                    writer = csv.DictWriter(f, fieldnames=tasks[0].keys())
                    writer.writeheader()
                    for task in tasks:
                        # Convert lists to strings for CSV
                        row = task.copy()
                        row['tags'] = ','.join(row.get('tags', []))
                        writer.writerow(row)
        else:
            console.print(f"\n[red]❌ Unsupported format: {format}[/red]")
            console.print("[dim]Supported formats: json, csv[/dim]\n")
            raise typer.Exit(1)
        
        console.print(f"\n[green]✓[/green] Exported {len(tasks)} tasks to [bold]{output}[/bold]\n")
    
    except Exception as e:
        console.print(f"\n[red]❌ Export failed: {e}[/red]\n")
        raise typer.Exit(1)


@app.command()
def clear(
    done: bool = typer.Option(False, "--done", "-d", help="Clear only completed tasks"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
):
    """
    🧹 Clear tasks (completed only by default, or all with --all).
    
    Example:
        task clear --done
        task clear --force
    """
    tasks = storage.get_all_tasks()
    
    if done:
        to_delete = [t for t in tasks if t['done']]
        action = "completed tasks"
    else:
        to_delete = tasks
        action = "ALL tasks"
    
    if not to_delete:
        console.print(f"\n[yellow]No {action} to clear[/yellow]\n")
        return
    
    if not force:
        confirm = typer.confirm(f"Are you sure you want to delete {len(to_delete)} {action}?")
        if not confirm:
            console.print("\n[yellow]Cancelled[/yellow]\n")
            raise typer.Abort()
    
    for task in to_delete:
        storage.delete_task(task['id'])
    
    console.print(f"\n[green]✓[/green] Cleared {len(to_delete)} {action}\n")


@app.command()
def stats():
    """
    📊 Show task statistics.
    """
    tasks = storage.get_all_tasks()
    
    if not tasks:
        console.print("\n[yellow]No tasks yet![/yellow]\n")
        return
    
    total = len(tasks)
    done = sum(1 for t in tasks if t['done'])
    pending = total - done
    
    # Count by priority
    priority_counts = {"low": 0, "medium": 0, "high": 0}
    for task in tasks:
        if not task['done']:
            priority_counts[task.get('priority', 'medium')] += 1
    
    # All tags
    all_tags = set()
    for task in tasks:
        all_tags.update(task.get('tags', []))
    
    # Create stats panel
    stats_text = f"""
[bold cyan]Total Tasks:[/bold cyan] {total}
[green]✓ Completed:[/green] {done} ({done*100//total if total > 0 else 0}%)
[yellow]○ Pending:[/yellow] {pending}

[bold cyan]Pending by Priority:[/bold cyan]
  [red]● High:[/red] {priority_counts['high']}
  [yellow]◐ Medium:[/yellow] {priority_counts['medium']}
  [blue]○ Low:[/blue] {priority_counts['low']}

[bold cyan]Tags:[/bold cyan] {len(all_tags)}
  {', '.join(f'#{t}' for t in sorted(all_tags)) if all_tags else '[dim]none[/dim]'}
    """
    
    panel = Panel(
        stats_text.strip(),
        title="📊 Task Statistics",
        border_style="cyan",
        box=box.ROUNDED
    )
    
    console.print()
    console.print(panel)
    console.print()


def _display_task(task: dict):
    """Display a single task in a nice format."""
    priority_color = PRIORITY_COLORS.get(task.get('priority', 'medium'), 'white')
    priority_symbol = PRIORITY_SYMBOLS.get(task.get('priority', 'medium'), '○')
    
    status = "[green]✓ Done[/green]" if task['done'] else "[yellow]○ Pending[/yellow]"
    tags = ", ".join(f"[cyan]#{t}[/cyan]" for t in task.get('tags', []))
    
    info = f"""
[bold]ID:[/bold] {task['id']}
[bold]Title:[/bold] {task['title']}
[bold]Status:[/bold] {status}
[bold]Priority:[/bold] [{priority_color}]{priority_symbol} {task.get('priority', 'medium')}[/{priority_color}]
[bold]Tags:[/bold] {tags if tags else '[dim]none[/dim]'}
[bold]Created:[/bold] {task['created_at'][:10]}
    """
    
    console.print(Panel(info.strip(), border_style="dim", box=box.ROUNDED))
    console.print()


if __name__ == "__main__":
    app()
