# 🎯 Tiny Task Manager

A fast, local CLI task manager for personal productivity. Built with Python and Typer for a smooth command-line experience.

## ✨ Features

- ✅ **Simple & Fast**: Quick task management from your terminal
- 🏷️ **Tags**: Organize tasks with multiple tags
- 🎨 **Priorities**: Set priority levels (low, medium, high)
- 📅 **Due Dates**: Set deadlines and track overdue tasks
- 📝 **Notes**: Add detailed descriptions to tasks
- ✏️ **Edit Tasks**: Modify existing tasks easily
- 🔍 **Search**: Find tasks by keyword in titles and notes
- 📦 **Archive**: Move completed tasks to archive file
- � **Filtering**: Filter tasks by tags, priority, and due dates
- 📊 **Statistics**: View task completion stats
- 💾 **Export**: Export tasks to JSON or CSV
- 🎨 **Beautiful Output**: Rich formatting with colors and tables
- 💾 **Local Storage**: All data stored locally in JSON format

## 📦 Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/ravinmuthukumarane/tinycli-taskmgr.git
cd tinycli-taskmgr

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

Now you can use the `task` command from anywhere!

## 🚀 Quick Start

```bash
# Add your first task
task add "Buy groceries" --tag personal --priority high

# Add a task with due date and notes
task add "Submit report" --due 2025-10-15 --note "Include Q3 figures"

# List all tasks
task list

# Mark a task as done
task done 1

# Search for tasks
task search "report"

# Edit a task
task edit 1 --priority high --due 2025-10-20

# View statistics
task stats
```

## 📖 Commands

### ➕ Add a Task

```bash
# Basic task
task add "Write documentation"

# With tags
task add "Fix bug #123" --tag work --tag urgent

# With priority
task add "Call dentist" --priority high

# With due date
task add "Submit proposal" --due 2025-10-15

# With notes
task add "Team meeting" --note "Discuss Q4 roadmap and budget allocation"

# Everything combined
task add "Project deadline" -t work -t urgent -p high -d 2025-10-31 -n "Final deliverables"
```

**Options:**
- `--tag, -t`: Add tags (can use multiple times)
- `--priority, -p`: Set priority (`low`, `medium`, `high`)
- `--due, -d`: Set due date (YYYY-MM-DD format)
- `--note, -n`: Add detailed notes

### 📋 List Tasks

```bash
# List pending tasks
task list

# List all tasks (including completed)
task list --all

# Filter by tag
task list --tag work

# Filter by priority
task list --priority high

# Show only overdue tasks
task list --overdue

# Show tasks due today
task list --today

# Show upcoming tasks
task list --upcoming

# Combine filters
task list --tag urgent --priority high --all
```

**Due date indicators:**
- 🔴 **Red + ⚠️**: Overdue tasks
- 🟡 **Yellow + 📅**: Due today
- 🟡 **Yellow**: Due within 3 days
- 🔵 **Cyan**: Due later

### ✓ Mark as Done

```bash
# Mark task as completed
task done 1

# Mark as not done (reopen)
task undone 1
```

### ✏️ Edit Tasks

```bash
# Change title
task edit 1 --title "Updated task description"

# Change priority
task edit 1 --priority high

# Set or update due date
task edit 1 --due 2025-10-20

# Add or update note
task edit 1 --note "Additional important details"

# Update tags (replaces existing tags)
task edit 1 --tag work --tag urgent

# Update multiple fields at once
task edit 1 --priority high --due 2025-10-15 --tag critical
```

### 🔍 Search Tasks

```bash
# Search in task titles and notes
task search "budget"

# Search for meetings
task search "meeting"

# Any keyword search
task search "report"
```

### 🏷️ Update Tags

```bash
# Replace tags for a task
task tag 1 work important

# Remove all tags (pass no tags)
task tag 1 ""
```

### 🗑️ Delete & Archive Tasks

```bash
# Delete a specific task (with confirmation)
task delete 1

# Delete without confirmation
task delete 1 --force

# Archive completed tasks (moves to archive.json)
task archive

# Archive without confirmation
task archive --force

# Clear only completed tasks
task clear --done

# Clear all tasks
task clear --force
```

**Archive vs Clear:**
- `archive`: Moves completed tasks to `~/.tinytask/archive.json` (preserves history)
- `clear --done`: Permanently deletes completed tasks (no recovery)

### ⏹️ Stop/Start and Uninstall

You can temporarily disable the CLI, or remove its local data entirely.

```powershell
# Stop the CLI (disables all commands except start/uninstall)
task stop

# Start (re-enable) the CLI
task start

# Uninstall helper: remove local data and show package removal steps
task uninstall --purge -y
```

What happens:
- `task stop` creates a marker at `~/.tinytask/.disabled`. While present, regular
  commands won't run and you'll be prompted to run `task start`.
- `task start` removes that marker.
- `task uninstall --purge` deletes the entire `~/.tinytask` directory (tasks.json,
  archive.json, and the disabled marker). Use with caution.
- To remove the CLI package itself, run in PowerShell:

```powershell
pip uninstall tinytask
```

### 💾 Export Tasks

```bash
# Export to JSON
task export --format json --output my_tasks.json

# Export to CSV
task export --format csv --output my_tasks.csv

# Export including completed tasks
task export --format json --all

# Quick export (auto-generated filename)
task export
```

### 📊 View Statistics

```bash
task stats
```

Shows:
- Total tasks and completion percentage
- Pending tasks by priority
- Due date breakdown (overdue, due today, upcoming)
- All tags used

## 📁 Data Storage

Tasks are stored locally in `~/.tinytask/tasks.json`. Each task contains:

```json
{
  "id": 1,
  "title": "Task description",
  "done": false,
  "tags": ["work", "urgent"],
  "priority": "high",
  "due_date": "2025-10-15",
  "note": "Additional details here",
  "created_at": "2025-10-07T10:30:00",
  "completed_at": null
}
```

Completed tasks can be archived to `~/.tinytask/archive.json` using the `task archive` command.

To wipe local data manually (same as `task uninstall --purge`): delete the
`~/.tinytask` directory.

## 🎨 Priority Visualization

Tasks are displayed with visual indicators:

- 🔴 **● High**: Red, urgent tasks
- 🟡 **◐ Medium**: Yellow, normal tasks  
- 🔵 **○ Low**: Blue, low priority tasks

## 💡 Tips & Tricks

1. **Quick workflow**: Add tasks throughout the day, then review with `task list`
2. **Stay organized**: Use consistent tag names like `work`, `personal`, `urgent`
3. **Track deadlines**: Use `task list --overdue` daily to stay on top of due dates
4. **Detailed planning**: Add notes with `--note` for context you'll need later
5. **Quick edits**: Use `task edit` to update tasks without recreating them
6. **Find anything**: Use `task search` to quickly locate tasks by keyword
7. **Weekly review**: Use `task list --all` to review completed tasks
8. **Clean workspace**: Run `task archive` monthly to keep your active list focused
9. **Backup**: Export regularly with `task export --all`
10. **Priority focus**: Use `task list --priority high --overdue` to see urgent items

## 🛠️ Development

### Running Tests

```bash
# Install dev dependencies
pip install pytest pytest-cov

# Run tests
pytest

# With coverage
pytest --cov=tinytask
```

### Project Structure

```
tinycli-taskmgr/
├── tinytask/
│   ├── __init__.py      # Package initialization
│   ├── cli.py           # CLI commands and interface
│   └── storage.py       # JSON storage backend
├── requirements.txt     # Dependencies
├── setup.py            # Package setup
└── README.md           # This file
```

## 📝 Examples

### Morning Routine

```bash
# Add today's tasks with due dates
task add "Review PRs" -t work -p high -d 2025-10-07
task add "Team standup" -t work -p high -d 2025-10-07
task add "Gym workout" -t personal -p medium
task add "Read chapter 3" -t learning -p low

# Check what's urgent
task list --overdue
task list --today
```

### During the Day

```bash
# Found an urgent task
task add "Fix production bug" -t work -p high -d 2025-10-07 -n "Error in payment processing"

# Need to reschedule
task edit 5 --due 2025-10-08

# Add more context
task edit 1 --note "Focus on backend PRs first"

# Quick search
task search "payment"
```

### End of Day

```bash
# Mark completed tasks
task done 1
task done 2

# See what's left
task list

# Check tomorrow's tasks
task list --upcoming

# View progress
task stats
```

### Weekly Review

```bash
# See everything you accomplished
task list --all

# Archive completed work
task archive

# Export for records
task export --all --format json --output "week_$(date +%Y%m%d).json"

# Plan next week
task add "Sprint planning" -t work -p high -d 2025-10-14
task add "1-on-1 with manager" -t work -d 2025-10-15 -n "Discuss Q4 goals"
```

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting

---

**Happy task managing! 🎯**