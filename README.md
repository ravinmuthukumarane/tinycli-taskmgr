# 🎯 Tiny Task Manager

A fast, local CLI task manager for personal productivity. Built with Python and Typer for a smooth command-line experience.

## ✨ Features

- ✅ **Simple & Fast**: Quick task management from your terminal
- 🏷️ **Tags**: Organize tasks with multiple tags
- 🎨 **Priorities**: Set priority levels (low, medium, high)
- 🔍 **Filtering**: Filter tasks by tags and priority
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

# List all tasks
task list

# Mark a task as done
task done 1

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

# Multiple tags and priority
task add "Plan vacation" -t personal -t travel -p medium
```

**Priority levels**: `low`, `medium` (default), `high`

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

# Combine filters
task list --tag urgent --priority high --all
```

### ✓ Mark as Done

```bash
# Mark task as completed
task done 1

# Mark as not done (reopen)
task undone 1
```

### 🏷️ Update Tags

```bash
# Replace tags for a task
task tag 1 work important

# Remove all tags (pass no tags)
task tag 1 ""
```

### 🗑️ Delete Tasks

```bash
# Delete a specific task (with confirmation)
task delete 1

# Delete without confirmation
task delete 1 --force

# Clear only completed tasks
task clear --done

# Clear all tasks
task clear --force
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
- Total tasks
- Completion percentage
- Pending tasks by priority
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
  "created_at": "2025-10-07T10:30:00",
  "completed_at": null
}
```

## 🎨 Priority Visualization

Tasks are displayed with visual indicators:

- 🔴 **● High**: Red, urgent tasks
- 🟡 **◐ Medium**: Yellow, normal tasks  
- 🔵 **○ Low**: Blue, low priority tasks

## 💡 Tips & Tricks

1. **Quick workflow**: Add tasks throughout the day, then review with `task list`
2. **Stay organized**: Use consistent tag names like `work`, `personal`, `urgent`
3. **Weekly review**: Use `task list --all` to review completed tasks
4. **Backup**: Export regularly with `task export --all`
5. **Clean up**: Run `task clear --done` monthly to archive completed tasks

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
# Add today's tasks
task add "Review PRs" -t work -p high
task add "Team standup" -t work -p high  
task add "Gym workout" -t personal -p medium
task add "Read chapter 3" -t learning -p low

# Check the list
task list
```

### End of Day

```bash
# Mark completed tasks
task done 1
task done 2

# See what's left
task list

# View progress
task stats
```

### Weekly Review

```bash
# See everything you accomplished
task list --all

# Export for records
task export --all --format json --output "week_$(date +%Y%m%d).json"

# Clean up
task clear --done
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