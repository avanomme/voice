#!/usr/bin/env bash
# refresh_problems.sh — lint Python + JS/TS/HTML and dump JSON problems for Gemini/Claude

set -e

mkdir -p .vscode

# --- Python lint (Ruff preferred, fallback to Flake8) ---
if command -v ruff &>/dev/null; then
  echo "Running Ruff on Python files…"
  # Ruff uses --output-format json
  ruff check --output-format json . > .vscode/python_problems.json || true
elif command -v flake8 &>/dev/null; then
  echo "Running Flake8 on Python files…"
  flake8 --format=json --output-file .vscode/python_problems.json . || true
else
  echo "No Python linter found (install ruff or flake8)" >&2
  echo "[]" > .vscode/python_problems.json
fi

# --- JS/TS/HTML lint (ESLint) ---
if command -v eslint &>/dev/null; then
  echo "Running ESLint on JS/TS/HTML files…"
  # Use --fix-dry-run to also include potential fixes in output
  eslint --fix-dry-run -f json . > .vscode/js_problems.json || true
else
  echo "No ESLint found (npm install eslint @eslint/js …)" >&2
  echo "[]" > .vscode/js_problems.json
fi

# --- Merge into one problems.json ---
if command -v jq &>/dev/null; then
  # Merge the two JSON arrays into one array
  jq -s 'add' .vscode/python_problems.json .vscode/js_problems.json > .vscode/problems.json
else
  # Fallback: just concatenate
  cat .vscode/python_problems.json .vscode/js_problems.json > .vscode/problems.json
fi

echo "Problems refreshed into .vscode/problems.json"
