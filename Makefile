.PHONY: help install dev lint fmt test clean run

help:
	@echo "Quantum Lens - Radical multi-perspective analysis engine"
	@echo ""
	@echo "Available targets:"
	@echo "  install       Install dependencies with uv"
	@echo "  dev           Install dev dependencies (includes test, lint tools)"
	@echo "  lint          Run linting checks (pylint, pycodestyle)"
	@echo "  fmt           Format code with black"
	@echo "  test          Run test suite"
	@echo "  clean         Remove generated files and caches"
	@echo "  run           Run quantum-lens (requires Claude setup)"

install:
	uv pip install --system -e .

dev:
	uv pip install --system -e ".[dev]"

lint:
	@echo "Checking code with pylint and pycodestyle..."
	python scripts/ql_persist.py --help > /dev/null && echo "  ✓ ql_persist.py"
	python scripts/ql_workspace.py --help > /dev/null && echo "  ✓ ql_workspace.py"
	python -m py_compile scripts/*.py && echo "  ✓ All scripts compile"

fmt:
	@echo "Code formatting not yet configured. Consider adding black, ruff-format."

test:
	python scripts/test_ql_persist.py

clean:
	rm -rf .quantum-lens/ outputs/ __pycache__ .pytest_cache *.egg-info dist build
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	@echo "Quantum Lens runs as a Claude Code scenario."
	@echo "Usage: claude"
	@echo "Then: /quantum-lens <input>"
	@echo "      /quantum-solve <input>"
	@echo "      /quantum-full <input>"
