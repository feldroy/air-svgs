# Load .env automatically (for colors, etc.)
set dotenv-load := true
set dotenv-filename := ".env"

# Centralize the default Python version used in CI / tasks. Update here to
# change all places that target Python 3.13.
PY_VERSION := "3.13"

# Show available commands
list:
    @just --list

# Run the blog in development mode with reload
run: 
    @lsof -ti tcp:8000 | xargs kill -9 || true
    uv run air run

# Run all the formatting, linting, and type checking commands
qa:
    uv run --python={{PY_VERSION}} --isolated --group lint -- ruff format .
    uv run --python={{PY_VERSION}} --isolated --group lint -- ruff check --fix .
    uv run --python={{PY_VERSION}} --isolated --group lint --group test -- ty check .

# Run all the tests for all the supported Python versions
test-all:
    uv run --python=3.10 --isolated --group test -- pytest
    uv run --python=3.11 --isolated --group test -- pytest
    uv run --python=3.12 --isolated --group test -- pytest
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest

# Run Test Coverage
test-coverage:
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest --cov=src -q

# Show the 10 slowest tests (timings)
test-durations:
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest --durations=10 -vvv --no-header

# Build and open only the HTML coverage report
coverage-html:
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest -vvv --cov=src --cov-fail-under=0 --cov-report=html:./.cov_html
    open ./.cov_html/index.html

# Run all the tests, but allow for arguments to be passed
test *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest {{ARGS}}

# Run all the tests, but on failure, drop into the debugger
pdb *ARGS:
    @echo "Running with arg: {{ARGS}}"
    uv run --python={{PY_VERSION}} --isolated --group test -- pytest --pdb --maxfail=10 {{ARGS}}

# Deploy to FastAPI Cloud
deploy:
    uv run fastapi deploy
