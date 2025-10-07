# 🎃 Contributing to Tiny Task Manager

Welcome to Tiny Task Manager! We're excited that you want to contribute. This project is participating in **Hacktoberfest 2025**! 🎉

## 🌟 Hacktoberfest 2025

This repository is part of Hacktoberfest 2025! We welcome contributions from developers of all skill levels.

### What is Hacktoberfest?

Hacktoberfest is a month-long celebration of open-source software run by DigitalOcean. During October, contributors can make pull requests to participating repositories and earn rewards!

### How to Participate

1. Register at [hacktoberfest.com](https://hacktoberfest.com)
2. Make 4 quality pull requests during October
3. Contribute to this or other participating projects
4. Get your PR reviewed and merged!

**Important**: Make sure your PRs are meaningful and not spam. Quality over quantity!

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Python and CLI applications

### Setting Up Your Development Environment

1. **Fork the repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone your fork**
   
   ```bash
   git clone https://github.com/YOUR-USERNAME/tinycli-taskmgr.git
   cd tinycli-taskmgr
   ```

3. **Set up the upstream remote**
   
   ```bash
   git remote add upstream https://github.com/ravinmuthukumarane/tinycli-taskmgr.git
   ```

4. **Create a virtual environment** (recommended)
   
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

5. **Install dependencies**
   
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

6. **Test the installation**
   
   ```bash
   task --help
   ```

## 🎯 How to Contribute

### Types of Contributions We Love

#### 🐛 Bug Fixes
- Fix existing issues
- Improve error handling
- Fix typos or formatting issues

#### ✨ New Features
- Implement features from our roadmap (see below)
- Suggest and implement your own ideas
- Improve existing features

#### 📚 Documentation
- Improve README
- Add code comments
- Create tutorials or guides
- Add examples

#### 🧪 Testing
- Write unit tests
- Improve test coverage
- Add integration tests

#### 🎨 UI/UX Improvements
- Improve CLI output formatting
- Better color schemes
- Enhanced error messages

## 📋 Feature Ideas & Good First Issues

### 🟢 Good First Issues (Great for Beginners!)

1. **Add color themes** - Allow users to customize color schemes
2. **Add task completion sound** - Optional sound notification when marking tasks done
3. **Improve help text** - Make command descriptions more detailed
4. **Add configuration file** - Support for `.tinytaskrc` config file
5. **Add task IDs in search results** - Make search output more consistent
6. **Validate tag names** - Prevent special characters in tags
7. **Add --version flag** - Show version information
8. **Improve error messages** - Make them more user-friendly

### 🟡 Intermediate Issues

1. **Recurring tasks** - Auto-create tasks on schedule (daily, weekly, monthly)
2. **Task dependencies** - Mark tasks that block others
3. **Subtasks/Checklists** - Break tasks into smaller steps
4. **Time tracking** - Log time spent on tasks with start/stop
5. **Task templates** - Reusable task patterns
6. **Undo command** - Revert last action
7. **Bulk operations** - Edit multiple tasks at once
8. **Natural language dates** - Accept "tomorrow", "next week", etc.

### 🔴 Advanced Issues

1. **Terminal UI (TUI)** - Interactive interface using `textual` or `rich`
2. **Sync functionality** - Cloud sync via Git or cloud storage
3. **Calendar integration** - Export to iCal format
4. **GitHub integration** - Import issues as tasks
5. **Plugin system** - Allow custom extensions
6. **Smart suggestions** - AI-powered task prioritization
7. **Multi-user support** - Shared task lists
8. **Mobile companion app** - PWA or native app

## 🔄 Contribution Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

**Branch naming conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `test/` - Test additions or changes
- `refactor/` - Code refactoring

### 2. Make Your Changes

- Write clean, readable code
- Follow Python PEP 8 style guide
- Add comments for complex logic
- Keep commits small and focused

### 3. Test Your Changes

```bash
# Test the CLI manually
task add "Test task" --tag test
task list
task done 1

# Run the app with different scenarios
task add "Test due date" --due 2025-10-15
task list --overdue
task search "test"
```

### 4. Commit Your Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

**Commit message format:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Formatting, missing semicolons, etc.
- `refactor:` - Code refactoring
- `test:` - Adding tests
- `chore:` - Maintenance tasks

### 5. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 6. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the PR template (see below)
5. Submit!

## 📝 Pull Request Guidelines

### PR Title Format

```
[Category] Brief description
```

Examples:
- `[Feature] Add recurring tasks functionality`
- `[Fix] Resolve issue with date parsing`
- `[Docs] Update installation instructions`

### PR Description Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement

## Related Issue
Closes #[issue number] (if applicable)

## Testing
How did you test this change?
- [ ] Manual testing
- [ ] Added unit tests
- [ ] Tested on multiple platforms

## Screenshots (if applicable)
Add screenshots for UI changes

## Checklist
- [ ] Code follows the project's style guidelines
- [ ] Self-review of code completed
- [ ] Comments added for complex code
- [ ] Documentation updated (if needed)
- [ ] No new warnings generated
- [ ] Tested on Windows/macOS/Linux (mention which)

## Additional Notes
Any other information reviewers should know.
```

## 🎨 Code Style Guidelines

### Python Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings for functions and classes

### Example Function

```python
def add_task(title: str, tags: Optional[List[str]] = None, 
             priority: str = "medium") -> Dict:
    """Add a new task to the storage.
    
    Args:
        title: The task description
        tags: Optional list of tags
        priority: Priority level (low, medium, high)
    
    Returns:
        The created task dictionary
    
    Raises:
        ValueError: If priority is invalid
    """
    # Implementation here
    pass
```

### CLI Output Style

- Use Rich library for formatting
- Consistent emoji usage (see existing commands)
- Color coding:
  - 🔴 Red: Errors, high priority, overdue
  - 🟡 Yellow: Warnings, medium priority, today
  - 🔵 Blue/Cyan: Info, low priority, future
  - 🟢 Green: Success, completed

## 🧪 Testing

### Manual Testing Checklist

Before submitting a PR, test these scenarios:

- [ ] Add tasks with various options
- [ ] List tasks with different filters
- [ ] Edit existing tasks
- [ ] Search functionality
- [ ] Archive completed tasks
- [ ] Export to JSON and CSV
- [ ] Error handling (invalid dates, missing tasks, etc.)

### Future: Automated Tests

We're working on adding a test suite. Contributions to testing are highly valued!

## 📚 Resources

### Project Resources
- [README.md](README.md) - Project overview
- [LICENSE](LICENSE) - MIT License
- [Issues](https://github.com/ravinmuthukumarane/tinycli-taskmgr/issues) - Bug reports and feature requests

### Learning Resources
- [Typer Documentation](https://typer.tiangolo.com/) - CLI framework
- [Rich Documentation](https://rich.readthedocs.io/) - Terminal formatting
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Git Workflow Guide](https://www.atlassian.com/git/tutorials/comparing-workflows)

## 💬 Communication

### Getting Help

- **Issues**: Use GitHub Issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact maintainers for sensitive issues

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Help others learn and grow
- Follow GitHub's Community Guidelines

## 🏆 Recognition

All contributors will be:
- Added to the README contributors section
- Credited in release notes
- Thanked in commit messages

Top contributors may be invited to become maintainers!

## 🎃 Hacktoberfest Specific Guidelines

### What Counts as a Valid Contribution?

✅ **Valid:**
- Bug fixes with proper testing
- New features from the roadmap
- Documentation improvements
- Code refactoring with clear benefits
- Test additions
- Meaningful UI/UX improvements

❌ **Invalid:**
- Minor formatting changes without substance
- Adding/removing whitespace
- Changing quotes or minor styling
- Duplicate PRs
- PRs created just to increase count

### Labels

We use these labels for Hacktoberfest:
- `hacktoberfest` - General Hacktoberfest issues
- `good first issue` - Perfect for beginners
- `help wanted` - We need help on this
- `enhancement` - New features
- `bug` - Bug fixes needed
- `documentation` - Docs improvements

## 📅 Hacktoberfest 2025 Timeline

- **October 1-31**: Submit your PRs!
- **Early October**: Best time to start
- **Mid-October**: Review period
- **Late October**: Final PRs and reviews

## 🙏 Thank You!

Thank you for contributing to Tiny Task Manager! Your contributions help make this tool better for everyone. Whether this is your first open-source contribution or your hundredth, we appreciate your time and effort.

Happy Hacking! 🎃👨‍💻👩‍💻

---

**Questions?** Open an issue or start a discussion. We're here to help!

**Ready to contribute?** Check out our [Issues page](https://github.com/ravinmuthukumarane/tinycli-taskmgr/issues) to get started!
