# Capstone Algorithms — Student Performance Analysis System

> **Algorithms 1 · Capstone Project · Jala University — Software Engineering**
> **Author:** Diego Alejandro Botina Herrera | August 2026

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
[![CI](https://img.shields.io/badge/CI-passing-brightgreen?logo=github-actions)](https://github.com/JalaU-Capstones/capstone-algorithms/actions)

---

## Overview

A console-based data analysis, search, and classification system focused on **student academic
performance records**. The system manages student performance records stored in a PostgreSQL 17
database and provides an interactive terminal interface to register, list, search, sort, and
compute statistics on those records. Output is rendered using `rich` styled tables and panels
for a polished user experience directly in the terminal.

This project demonstrates the practical implementation of fundamental algorithms studied
throughout the Algorithms 1 course: linear search O(n), binary search O(log n), and three
comparison-based sorting algorithms (bubble, selection, insertion sort) — all with full
elementary-operation counting, T(n) formulation, and formal Big-O / Big-Omega proofs. Beyond
algorithms, the project applies a strict four-layer architecture (CLI → Service → Repository →
Database), the Repository design pattern, Dependency Injection, DTO Pattern, and all five SOLID
principles — making it both academically rigorous and industrially representative.

---

## Features

- Interactive console menu with `rich` styled output (panels, tables, coloured prompts)
- Full CRUD operations on student performance records (create, list, search, update, delete)
- Linear search **O(n)** and binary search **O(log n)** with operation counters
- Bubble sort, selection sort, and insertion sort with ascending/descending order support
- Statistics: maximum score, minimum score, average score, and record count by category
- Layered architecture (CLI → Service → Repository → Database) with SOLID principles
- Repository design pattern for clean separation of persistence concerns
- Unit and integration tests with pytest — coverage ≥ 70%
- Full complexity analysis with T(n) formulation and Big-O in LaTeX notation (`docs/complexity/`)
- Automated CI/CD pipeline via GitHub Actions (lint, type check, migrations, tests)

---

## Algorithms Implemented

### Search

| Algorithm | Best Case | Average Case | Worst Case | Notes |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | Unsorted list; returns first match |
| Binary Search | O(1) | O(log n) | O(log n) | Requires sorted input |

### Sort

| Algorithm | Best Case | Average Case | Worst Case | Space | Stable |
|---|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | No |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Yes |

> Full complexity analysis with elementary operation counting, T(n) formulation, and
> Big-O / Big-Omega proofs in LaTeX notation available in [`docs/complexity/`](docs/complexity/).

---

## Data Model

```text
StudentRecord (table: student_records)
├── id          : INTEGER       — Primary Key, auto-increment
├── name        : VARCHAR(100)  — Student full name (non-empty)
├── category    : VARCHAR(50)   — Level: Junior | Mid | Senior | Expert
├── score       : NUMERIC(5,2)  — Evaluation score: 0.00 – 100.00
├── subject     : VARCHAR(100)  — Evaluated subject/course (non-empty)
└── created_at  : TIMESTAMP     — Set automatically on insert (UTC)
```

See [`docs/design/data_model.md`](docs/design/data_model.md) for the full field reference,
ER diagram, validation rules, migration strategy, DTO pattern, and sample data.

---

## Project Structure

```text
capstone-algorithms/
├── .github/
│   └── workflows/
│       └── ci.yml                    # GitHub Actions CI pipeline (quality + tests)
├── docs/
│   ├── complexity/
│   │   ├── search_analysis.md        # Big-O analysis: linear + binary search
│   │   ├── sort_analysis.md          # Big-O analysis: bubble, selection, insertion
│   │   └── stats_analysis.md         # Complexity for statistics operations
│   └── design/
│       ├── architecture.md           # Layered architecture, SOLID, patterns, data flow
│       └── data_model.md             # Entity design, ER diagram, validation rules
├── docker/
│   └── postgres/
│       └── init.sh                   # Init script: creates capstone_db + capstone_test_db
├── migrations/
│   ├── env.py                        # Alembic environment configuration
│   ├── script.py.mako                # Migration script template
│   └── versions/
│       └── c189d604bd7f_create_student_records_table.py  # Initial schema migration
├── src/
│   └── capstone/
│       ├── __init__.py               # Package marker
│       ├── main.py                   # Application entry point — wires all layers
│       ├── config.py                 # Environment configuration (DATABASE_URL etc.)
│       ├── algorithms/
│       │   ├── __init__.py
│       │   ├── search.py             # linear_search, binary_search with op counters
│       │   └── sort.py               # bubble_sort, selection_sort, insertion_sort
│       ├── cli/
│       │   ├── __init__.py
│       │   └── menu.py               # MenuController — rich terminal UI
│       ├── models/
│       │   ├── __init__.py           # StudentRecordDTO (Pydantic) + exports
│       │   └── record.py             # SQLAlchemy ORM model for student_records
│       ├── repository/
│       │   ├── __init__.py
│       │   └── record_repository.py  # RecordRepository — CRUD via SQLAlchemy
│       ├── scripts/
│       │   ├── __init__.py
│       │   └── seed.py               # Database seeding script (initial sample data)
│       ├── services/
│       │   ├── __init__.py
│       │   └── record_service.py     # RecordService — business logic orchestration
│       └── stats/
│           ├── __init__.py
│           └── statistics.py         # Statistical functions: max, min, avg, by_category
├── tests/
│   ├── __init__.py
│   ├── conftest.py                   # pytest fixtures: test DB session, sample data
│   ├── integration/                  # Integration tests against capstone_test_db
│   └── unit/                         # Unit tests: algorithms, stats, service logic
├── .env                              # Local environment variables (git-ignored)
├── .env.example                      # Template for environment variables
├── .gitignore                        # Excludes .venv, __pycache__, .env, coverage, etc.
├── alembic.ini                       # Alembic configuration
├── docker-compose.yml                # PostgreSQL 17 service definition
├── LICENSE                           # MIT License
├── pyproject.toml                    # Project metadata, ruff, mypy, pytest config
├── README.md                         # This file
└── uv.lock                           # Locked dependency graph (uv)
```

---

## Development Notes

### Module resolution (src layout)

This project uses the `src/` layout. The `capstone` package is installed
in editable mode via:

```bash
uv pip install -e .
```

This must be run once after cloning. After installation, all commands work without any
`PYTHONPATH` prefix:

```bash
uv run python -m capstone.main
uv run pytest
uv run alembic upgrade head
```

If you ever see `ModuleNotFoundError: No module named 'capstone'`, it means the package is
not installed in editable mode. Re-run `uv pip install -e .` to fix it.

### Test database

Both the application database (`capstone_db`) and the test database (`capstone_test_db`) are
created automatically on the first `docker compose up`. No manual setup is required.

The initialization script at `docker/postgres/init.sh` is mounted into the PostgreSQL
container and executed automatically on first startup.

If you need to reset and recreate both databases from scratch:

```bash
docker compose down -v       # removes the volume (destroys all data)
docker compose up -d         # recreates the container and both databases
```

---

## Getting Started

### System Requirements

| Tool | Version |
|---|---|
| Python | 3.14+ |
| Docker | 29.7+ |
| Docker Compose | 5.4+ |
| uv (package manager) | latest |

### Step-by-step setup

#### 1. Clone the repository

```bash
git clone https://github.com/JalaU-Capstones/capstone-algorithms.git
cd capstone-algorithms
```

#### 2. Start the database

```bash
docker compose up -d
```

> Both `capstone_db` (application) and `capstone_test_db` (tests) are created automatically
> by `docker/postgres/init.sh` on first startup. No manual database creation is needed.

#### 3. Install dependencies

```bash
uv sync --all-extras
```

#### 4. Install the project in editable mode

```bash
uv pip install -e .
```

#### 5. Copy the environment file

```bash
cp .env.example .env
# Edit .env if your local credentials differ from the defaults
```

#### 6. Run database migrations

```bash
uv run alembic upgrade head
```

#### 7. Seed initial data

```bash
uv run python -m capstone.scripts.seed
```

#### 8. Run the application

```bash
uv run python -m capstone.main
```

The interactive menu launches immediately. Use options 1–6 to navigate.

---

## Development Commands

### Running Tests

```bash
uv run pytest --cov=src/capstone --cov-report=term-missing
```

> Minimum required coverage: **70%**. The `pyproject.toml` enforces this with
> `--cov-fail-under=70`.

### Code Quality

```bash
# Linter
uv run ruff check .

# Formatter (check only — no changes)
uv run ruff format --check .

# Formatter (apply changes)
uv run ruff format .

# Type checker
uv run mypy src/
```

---

## CI/CD Pipeline

The project uses a **GitHub Actions** pipeline defined in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

### Triggers

- **Push** to any branch
- **Pull request** targeting `main`

A concurrency group cancels redundant runs on the same branch, so only the most recent push
is tested.

### Job 1 — Code Quality

Runs first on every trigger:

| Step | Command |
|---|---|
| Lint with ruff | `uv run ruff check .` |
| Check formatting | `uv run ruff format --check .` |
| Type check | `uv run mypy src/` |

### Job 2 — Tests

Runs **only if Job 1 passes** (`needs: quality`):

| Step | Details |
|---|---|
| Spin up PostgreSQL 17 | Service container with health-check |
| Create test database | `psql -c "CREATE DATABASE capstone_test_db;"` |
| Run Alembic migrations | `uv run alembic upgrade head` |
| Run test suite | `uv run pytest --cov=src/capstone --cov-report=xml` |
| Upload coverage artifact | `coverage.xml` retained for 7 days |

Both databases use the same credentials as `docker-compose.yml`:
- User: `capstone_user` · Password: `capstone_pass` · DB: `capstone_db`

---

## Complexity Analysis

Full complexity analysis with elementary operation counting, T(n) formulation, and
Big-O / Big-Omega proofs in LaTeX notation is available in the `docs/complexity/` directory:

- **Search algorithms:** [`docs/complexity/search_analysis.md`](docs/complexity/search_analysis.md)
- **Sort algorithms:** [`docs/complexity/sort_analysis.md`](docs/complexity/sort_analysis.md)
- **Statistics operations:** [`docs/complexity/stats_analysis.md`](docs/complexity/stats_analysis.md)

---

## Architecture

The system follows a strict four-layer architecture. See [`docs/design/architecture.md`](docs/design/architecture.md)
for the full design document including SOLID principles table, design patterns, and data flow.

```text
┌──────────────────────────┐
│       CLI Layer          │  MenuController — rich terminal UI
└────────────┬─────────────┘
             │ uses
┌────────────▼─────────────┐
│     Service Layer        │  RecordService — orchestration + validation
└──────┬─────────┬──────────┘
       │         │
┌──────▼───┐  ┌──▼──────────────┐
│ Repo     │  │ Algorithm Layer  │  search.py · sort.py · statistics.py
│ Layer    │  └─────────────────┘
└──────┬───┘
       │
┌──────▼────────────────────┐
│    Database Layer         │  PostgreSQL 17 · SQLAlchemy 2.x · Alembic
└───────────────────────────┘
```

---

## Branching Strategy — GitHub Flow

```text
main                            ← always stable and deployable
└── feature/phase-1-foundation  ← merged via PR
└── feature/phase-2-algorithms  ← merged via PR
└── feature/phase-3-services    ← merged via PR
└── feature/phase-4-cli         ← merged via PR
└── feature/phase-5-docs        ← merged via PR
```

### Commit convention

```
<type>(<scope>): <short description>

Types: feat | fix | test | docs | chore | refactor | style
```

**Examples:**

```
feat(algorithms): implement linear search with operation counter
test(sort): add unit tests for bubble sort worst case
docs(complexity): add T(n) formulation for binary search in LaTeX
chore(config): configure ruff and mypy in pyproject.toml
```

---

## Project Phases

| Phase | Description | Status |
|---|---|---|
| 1 — Foundation | Project setup, Docker, DB schema, migrations, repository layer | ✅ Completed |
| 2 — Algorithms | Search + sort implementations, unit tests, complexity docs | ✅ Completed |
| 3 — Services | Business logic layer, statistics module | ✅ Completed |
| 4 — CLI | Interactive menu, full integration | ✅ Completed |
| 5 — Docs | CI pipeline, final documentation, presentation polish | ✅ Completed |

---

## Academic Context

This project was developed as the **partial capstone submission** for the **Algorithms 1**
course at **Jala University**, Software Engineering program, Semester 4. The evaluation focuses
on:

- Logical organization and code readability
- Correct implementation of search and sorting algorithms
- Complete complexity analysis (elementary operations, T(n), Big-O, Big-Omega)
- Proper use of data structures (lists, DTOs)
- Unit test coverage ≥ 70%
- Layered architecture and application of software engineering principles (SOLID, Repository Pattern)

---

## License

Licensed under the [MIT License](LICENSE).

© 2026 Diego Alejandro Botina Herrera
