"""Storage module for managing tasks in JSON format.

Also provides simple lifecycle helpers:
- disable/enable: Put the CLI into a disabled state by creating/removing a
    marker file. While disabled, most commands will refuse to run.
- uninstall: Remove the data directory (e.g., ~/.tinytask).
"""

import json
import os
import shutil
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional


class TaskStorage:
    """Handles reading and writing tasks to a JSON file."""
    
    def __init__(self, file_path: Optional[str] = None):
        """Initialize the task storage.
        
        Args:
            file_path: Path to the tasks file. Defaults to ~/.tinytask/tasks.json
        """
        if file_path is None:
            home = Path.home()
            self.storage_dir = home / ".tinytask"
            self.storage_dir.mkdir(exist_ok=True)
            self.file_path = self.storage_dir / "tasks.json"
        else:
            self.file_path = Path(file_path)
            self.storage_dir = self.file_path.parent
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize file if it doesn't exist
        if not self.file_path.exists():
            self._write_tasks([])

        self._disabled_flag = self.storage_dir / ".disabled"
    
    def _read_tasks(self) -> List[Dict]:
        """Read all tasks from the JSON file."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _write_tasks(self, tasks: List[Dict]) -> None:
        """Write tasks to the JSON file."""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, indent=2, ensure_ascii=False)
    
    def _get_next_id(self, tasks: List[Dict]) -> int:
        """Get the next available task ID."""
        if not tasks:
            return 1
        return max(task['id'] for task in tasks) + 1
    
    def add_task(self, title: str, tags: Optional[List[str]] = None, 
                 priority: str = "medium", due_date: Optional[str] = None,
                 note: Optional[str] = None) -> Dict:
        """Add a new task.
        
        Args:
            title: The task description
            tags: Optional list of tags
            priority: Priority level (low, medium, high)
            due_date: Optional due date in YYYY-MM-DD format
            note: Optional detailed notes
        
        Returns:
            The created task dictionary
        """
        tasks = self._read_tasks()
        task = {
            'id': self._get_next_id(tasks),
            'title': title,
            'done': False,
            'tags': tags or [],
            'priority': priority,
            'due_date': due_date,
            'note': note,
            'created_at': datetime.now().isoformat(),
            'completed_at': None
        }
        tasks.append(task)
        self._write_tasks(tasks)
        return task
    
    def get_tasks(self, show_done: bool = False, 
                  tag_filter: Optional[str] = None,
                  priority_filter: Optional[str] = None,
                  due_filter: Optional[str] = None) -> List[Dict]:
        """Get tasks with optional filtering.
        
        Args:
            show_done: Include completed tasks
            tag_filter: Filter by tag
            priority_filter: Filter by priority
            due_filter: Filter by due date (overdue, today, upcoming)
        
        Returns:
            List of filtered tasks
        """
        tasks = self._read_tasks()
        
        # Filter by completion status
        if not show_done:
            tasks = [t for t in tasks if not t['done']]
        
        # Filter by tag
        if tag_filter:
            tasks = [t for t in tasks if tag_filter in t.get('tags', [])]
        
        # Filter by priority
        if priority_filter:
            tasks = [t for t in tasks if t.get('priority') == priority_filter]
        
        # Filter by due date
        if due_filter:
            today = date.today()
            filtered = []
            for task in tasks:
                due_date = task.get('due_date')
                if not due_date:
                    continue
                
                try:
                    task_date = date.fromisoformat(due_date)
                    if due_filter == 'overdue' and task_date < today and not task['done']:
                        filtered.append(task)
                    elif due_filter == 'today' and task_date == today:
                        filtered.append(task)
                    elif due_filter == 'upcoming' and task_date > today:
                        filtered.append(task)
                except ValueError:
                    continue
            tasks = filtered
        
        return tasks
    
    def mark_done(self, task_id: int) -> Optional[Dict]:
        """Mark a task as done.
        
        Args:
            task_id: The ID of the task to mark as done
        
        Returns:
            The updated task, or None if not found
        """
        tasks = self._read_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['done'] = True
                task['completed_at'] = datetime.now().isoformat()
                self._write_tasks(tasks)
                return task
        return None
    
    def mark_undone(self, task_id: int) -> Optional[Dict]:
        """Mark a task as not done.
        
        Args:
            task_id: The ID of the task to mark as not done
        
        Returns:
            The updated task, or None if not found
        """
        tasks = self._read_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['done'] = False
                task['completed_at'] = None
                self._write_tasks(tasks)
                return task
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task.
        
        Args:
            task_id: The ID of the task to delete
        
        Returns:
            True if deleted, False if not found
        """
        tasks = self._read_tasks()
        original_length = len(tasks)
        tasks = [t for t in tasks if t['id'] != task_id]
        
        if len(tasks) < original_length:
            self._write_tasks(tasks)
            return True
        return False
    
    def update_task_tags(self, task_id: int, tags: List[str]) -> Optional[Dict]:
        """Update tags for a task.
        
        Args:
            task_id: The ID of the task
            tags: New list of tags
        
        Returns:
            The updated task, or None if not found
        """
        tasks = self._read_tasks()
        for task in tasks:
            if task['id'] == task_id:
                task['tags'] = tags
                self._write_tasks(tasks)
                return task
        return None
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks including completed ones."""
        return self._read_tasks()
    
    def edit_task(self, task_id: int, title: Optional[str] = None,
                  priority: Optional[str] = None, tags: Optional[List[str]] = None,
                  due_date: Optional[str] = None, note: Optional[str] = None) -> Optional[Dict]:
        """Edit a task's properties.
        
        Args:
            task_id: The ID of the task to edit
            title: New title (if provided)
            priority: New priority (if provided)
            tags: New tags list (if provided)
            due_date: New due date (if provided)
            note: New note (if provided)
        
        Returns:
            The updated task, or None if not found
        """
        tasks = self._read_tasks()
        for task in tasks:
            if task['id'] == task_id:
                if title is not None:
                    task['title'] = title
                if priority is not None:
                    task['priority'] = priority
                if tags is not None:
                    task['tags'] = tags
                if due_date is not None:
                    task['due_date'] = due_date
                if note is not None:
                    task['note'] = note
                self._write_tasks(tasks)
                return task
        return None
    
    def search_tasks(self, query: str) -> List[Dict]:
        """Search tasks by keyword in title and notes.
        
        Args:
            query: Search query string
        
        Returns:
            List of matching tasks
        """
        tasks = self._read_tasks()
        query_lower = query.lower()
        results = []
        
        for task in tasks:
            # Search in title
            if query_lower in task['title'].lower():
                results.append(task)
                continue
            
            # Search in notes
            note = task.get('note', '')
            if note and query_lower in note.lower():
                results.append(task)
        
        return results
    
    def archive_completed(self) -> int:
        """Archive completed tasks to a separate file.
        
        Returns:
            Number of tasks archived
        """
        tasks = self._read_tasks()
        archive_path = self.storage_dir / "archive.json"
        
        # Read existing archive
        if archive_path.exists():
            try:
                with open(archive_path, 'r', encoding='utf-8') as f:
                    archived = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                archived = []
        else:
            archived = []
        
        # Separate completed and pending tasks
        completed = [t for t in tasks if t['done']]
        pending = [t for t in tasks if not t['done']]
        
        # Add completed tasks to archive with archive timestamp
        for task in completed:
            task['archived_at'] = datetime.now().isoformat()
            archived.append(task)
        
        # Write updated files
        with open(archive_path, 'w', encoding='utf-8') as f:
            json.dump(archived, f, indent=2, ensure_ascii=False)
        
        self._write_tasks(pending)
        
        return len(completed)

    # --- Lifecycle helpers ---
    def is_disabled(self) -> bool:
        """Return True if the CLI is in a disabled state."""
        return self._disabled_flag.exists()

    def disable(self, reason: Optional[str] = None) -> None:
        """Disable the CLI by creating a marker file.

        Args:
            reason: Optional reason text stored in the flag file for reference.
        """
        content = {
            "disabled_at": datetime.now().isoformat(),
            "reason": reason or "manually disabled",
        }
        with open(self._disabled_flag, "w", encoding="utf-8") as f:
            json.dump(content, f, indent=2)

    def enable(self) -> None:
        """Enable the CLI by removing the disabled marker file (if present)."""
        try:
            if self._disabled_flag.exists():
                self._disabled_flag.unlink()
        except OSError:
            # Non-fatal; leave as-is
            pass

    def uninstall(self) -> bool:
        """Delete the entire storage directory (~/.tinytask).

        Returns:
            True if directory removed or didn't exist; False on failure.
        """
        try:
            if self.storage_dir.exists() and self.storage_dir.is_dir():
                shutil.rmtree(self.storage_dir)
            return True
        except Exception:
            return False
