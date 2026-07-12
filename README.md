# discernio

A Python hypothesis lab. Each top-level folder is a self-contained experiment with its own dependencies and virtual environment.

## Getting Started

Open this repo in VS Code and choose **"Reopen in Container"**. The devcontainer will:
- Set up Python 3.14
- Install `uv` (fast venv/package manager)
- Install `ruff`, `pylint`, and `pyrefly` globally
- Install Claude Code (`claude`)

## Working on a Hypothesis

```bash
cd hypothesis-NNN-short-description

# First time: create venv and install deps
uv sync

# Run the hypothesis
uv run python main.py

# Add a new dependency
uv add requests
```

## Adding a New Hypothesis

1. Create a folder: `hypothesis-NNN-short-description/`
2. Copy the structure from `hypothesis-001-example/`
3. Update `pyproject.toml` with the hypothesis name and any dependencies
4. Update `README.md` with the hypothesis statement

## Linting and Type Checking

Run from the repo root (picks up shared config from root `pyproject.toml`):

```bash
ruff check .
pylint hypothesis-NNN-short-description/
pyrefly check hypothesis-NNN-short-description/
```

Or from inside a hypothesis folder:

```bash
ruff check .
pylint main.py
pyrefly check main.py
```
