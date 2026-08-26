.PHONY: help install dev lint fmt test clean run

help:
	@echo "Quantum Lens - Radical multi-perspective analysis engine"
	@echo ""
	@echo "Available targets:"
	@echo "  install       Install dependencies with uv"
	@echo "  dev           Install dev dependencies (includes test, lint tools)"
	@echo "  lint          Smoke check: scripts compile and expose a CLI"
	@echo "  fmt           Placeholder, no formatter configured yet"
	@echo "  test          Run test suite"
	@echo "  clean         Remove build artifacts (not your workspace)"
	@echo "  run           Run quantum-lens (requires Claude setup)"

install:
	uv pip install --system -e .

dev:
	uv pip install --system -e ".[dev]"

lint:
	@echo "Smoke check: scripts import, parse and expose a CLI. No pylint/pycodestyle configured."
	python scripts/ql_persist.py --help > /dev/null && echo "  ✓ ql_persist.py"
	python scripts/ql_workspace.py --help > /dev/null && echo "  ✓ ql_workspace.py"
	python -m py_compile scripts/*.py && echo "  ✓ All scripts compile"

fmt:
	@echo "No formatter configured yet. Add black or ruff-format here when one is chosen."

test:
	python scripts/test_ql_persist.py

clean:
	@echo "Removing build artifacts only. Your .quantum-lens/ workspace is left untouched."
	rm -rf __pycache__ .pytest_cache *.egg-info dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	@echo "Quantum Lens runs as a Claude Code scenario."
	@echo "Usage: claude"
	@echo "Then: /quantum-lens <input>"
	@echo "      /quantum-solve <input>"
	@echo "      /quantum-full <input>"
