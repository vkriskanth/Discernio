#!/usr/bin/env bash
set -e

echo "==> Installing uv (fast Python package/venv manager)"
curl -LsSf https://astral.sh/uv/install.sh | sh

echo "==> Installing Python linting and type-checking tools"
pip install pylint pyrefly ruff

echo "==> Installing Claude Code"
npm install -g @anthropic-ai/claude-code

echo "==> Done. Run 'claude --version' and 'uv --version' to verify."
