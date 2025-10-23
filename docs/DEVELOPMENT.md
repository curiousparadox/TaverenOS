# TaverenOS Development Guide

This guide captures the essential steps to get a local TaverenOS development environment running.

## 1. Requirements
- Python 3.11+
- Optional: Redis (for future state persistence experiments)

## 2. Setup
1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Run the test suite to ensure everything is wired correctly:
   ```bash
   pytest
   ```

## 3. Code Quality
- `black` and `ruff` are configured in `pyproject.toml`. Run them locally prior to commits.
- GitHub Actions will execute linting and tests on every push (see `.github/workflows/ci.yml`).

## 4. Project Structure
- `src/taverenos/core`: Symbolic reasoning primitives.
- `src/taverenos/diagnostics`: Diagnostics aggregators and reporting helpers.
- `src/taverenos/compression`: EEV compression scaffolding.
- `src/taverenos/automation`: Ritual automation payloads.
- `tests`: Pytest-based unit tests.
- `docs`: Project documentation.

## 5. Next Steps
- Expand the diagnostics module with concrete rule evaluation logic.
- Introduce adapters for ingesting telemetry data.
- Prototype FastAPI endpoints for interacting with the reasoning loop.
