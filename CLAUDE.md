# Ice Cream Shop - Project Guide

## Overview
A Python CLI application for managing an ice cream shop — inventory, orders, and sales reporting.

## Tech Stack
- Python 3.11+
- SQLite for data storage
- Click for CLI interface
- pytest for testing

## Project Structure
```
icecream/
├── CLAUDE.md          # This file — project context for Claude Code
├── .claude/
│   ├── settings.json  # Claude Code settings (permissions, hooks)
│   └── commands/      # Custom slash commands for git workflows
├── src/
│   └── icecream/
│       ├── __init__.py
│       ├── cli.py     # CLI entry points
│       ├── models.py  # Data models and DB schema
│       ├── shop.py    # Core business logic
│       └── reports.py # Sales reporting
├── tests/
│   ├── conftest.py
│   ├── test_models.py
│   ├── test_shop.py
│   └── test_reports.py
├── pyproject.toml
└── README.md
```

## Development Commands
- Install: `pip install -e ".[dev]"`
- Run tests: `pytest`
- Run tests with coverage: `pytest --cov=icecream`
- Lint: `ruff check src/ tests/`
- Format: `ruff format src/ tests/`
- Run CLI: `icecream --help`

## Git Workflow
- Branch from `main` for all feature work: `git checkout -b feature/<name>`
- Run `ruff check` and `pytest` before every commit.
- Write commit messages in imperative mood ("Add feature", not "Added feature").
- Do not force-push or reset --hard without explicit approval.
- Use `gh pr create` for pull requests.

## Custom Slash Commands
- `/git-summary` — Show current git state (status, recent log, branches, diff stats)
- `/git-review` — Review uncommitted changes for bugs, style, and security
- `/git-smart-commit` — Lint + test + commit (refuses to commit if checks fail)
- `/git-pr` — Push branch and create a GitHub pull request
- `/git-branch-cleanup` — Safely delete merged branches

## Conventions
- Use type hints on all function signatures.
- Keep functions small — max ~30 lines.
- Write a test for every public function.
- Use descriptive variable names; avoid single-letter names except in comprehensions.
- SQL queries go in `models.py`, business logic in `shop.py`.
- Use `decimal.Decimal` for all monetary values.
