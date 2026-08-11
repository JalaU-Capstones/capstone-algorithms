# Capstone Algorithms — Student Performance Analysis System

> **Algorithms 1 · Capstone Project · Jala University — Software Engineering**
> **Author:** Diego Alejandro Botina Herrera
> **Academic period:** August 2026

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

---

## Overview

A console-based data analysis, search, and classification system focused on **student academic performance records**. The project demonstrates the practical implementation of fundamental algorithms studied throughout the Algorithms 1 course, including search and sorting algorithms with full complexity analysis.

The system manages student performance records and provides interactive functionality to register, list, search, sort, and compute statistics on the data.

---

## System Requirements

| Tool | Version |
|---|---|
| Python | 3.14+ |
| Docker | 29.7+ |
| Docker Compose | 5.4+ |
| uv (package manager) | latest |

---

## Project Structure

```
capstone-algorithms/
├── docs/
│   ├── complexity/
│   │   ├── search_analysis.md        # Big-O analysis for search algorithms
│   │   ├── sort_analysis.md          # Big-O analysis for sort algorithms
│   │   └── stats_analysis.md         # Complexity for statistics operations
│   └── design/
│       ├── data_model.md             # Entity design and schema
│       └── architecture.md           # Layered architecture overview
├── migrations/
│   ├── env.py
│   └── versions/                     # Alembic versioned migrations
├── src/
│   └── capstone/
│       ├── main.py                   # Application entry point
│       ├── config.py                 # Environment configuration
│       ├── models/                   # SQLAlchemy models + DTOs
│       ├── repository/               # Data access layer (Repository pattern)
│       ├── algorithms/               # Search and sort algorithm implementations
│       ├── services/                 # Business logic layer
│       ├── stats/                    # Statistics processing module
│       └── cli/                      # Interactive console menu
├── tests/
│   ├── unit/                         # Unit tests per module
│   ├── integration/                  # Integration tests (DB layer)
│   └── conftest.py
├── docker-compose.yml                # PostgreSQL service
├── pyproject.toml                    # Project config: ruff, mypy, pytest
├── alembic.ini
├── .env.example
└── README.md
```

---

## Algorithms Implemented

### Search
| Algorithm | Best Case | Average Case | Worst Case |
|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) |
| Binary Search | O(1) | O(log n) | O(log n) |

### Sorting
| Algorithm | Best Case | Average Case | Worst Case | Space |
|---|---|---|---|---|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) |

> Full complexity analysis with elementary operation counting, T(n) formulation, and LaTeX notation available in [`docs/complexity/`](docs/complexity/).

---

## Data Model

```
StudentRecord
├── id          : INTEGER       (Primary Key, auto-increment)
├── name        : VARCHAR(100)  (Student full name)
├── category    : VARCHAR(50)   (Level: Junior | Mid | Senior | Expert)
├── score       : DECIMAL(5,2)  (Evaluation score: 0.00 – 100.00)
├── subject     : VARCHAR(100)  (Evaluated subject/course)
└── created_at  : TIMESTAMP     (Record creation timestamp)
```

---

## Interactive Menu

```
========================================
  Student Performance Analysis System
========================================
  1 — Register new record
  2 — List all records
  3 — Search record
  4 — Sort records
  5 — Show statistics
  6 — Exit
========================================
```

---

## Development Notes

### Module resolution (src layout)

This project uses the `src/` layout. The `capstone` package is installed
in editable mode via:

    uv pip install -e .

This must be run once after cloning. After installation, all commands
work without any `PYTHONPATH` prefix:

    uv run python -m capstone.main
    uv run pytest
    uv run alembic upgrade head

If you ever see `ModuleNotFoundError: No module named 'capstone'`, it means
the package is not installed in editable mode. Re-run `uv pip install -e .`
to fix it.

### Test database

Tests use a separate database to prevent corrupting Alembic migration state.
Create it once with:

    docker exec -it capstone_db psql -U capstone_user \
      -c "CREATE DATABASE capstone_test_db;"

Tests use transaction rollback for isolation — no manual cleanup needed.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/JalaU-Capstones/capstone-algorithms.git
cd capstone-algorithms
```

### 2. Start the database

```bash
docker compose up -d
```

### 3. Install dependencies

```bash
pip install uv
uv sync
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Edit .env with your local database credentials if needed
```

### 5. Run database migrations

```bash
uv run alembic upgrade head
```

### 6. Seed initial data

```bash
uv run python -m capstone.scripts.seed
```

### 7. Run the application

```bash
uv run python -m capstone.main
```

---

## Development

### Run tests with coverage

```bash
uv run pytest --cov=src/capstone --cov-report=term-missing
```

> Minimum required coverage: **70%**

### Run linter

```bash
uv run ruff check .
uv run ruff format --check .
```

### Run type checker

```bash
uv run mypy src/
```

---

## Branching Strategy — GitHub Flow

```
main                          ← always stable and deployable
└── feature/phase-1-foundation
└── feature/phase-2-algorithms
└── feature/phase-3-services
└── feature/phase-4-cli
└── feature/phase-5-docs
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
| 1 — Foundation | Project setup, Docker, DB schema, migrations, repository layer | 🔲 Pending |
| 2 — Algorithms | Search + sort implementations, unit tests, complexity docs | 🔲 Pending |
| 3 — Services | Business logic layer, statistics module | 🔲 Pending |
| 4 — CLI | Interactive menu, full integration | 🔲 Pending |
| 5 — Docs | Complexity reports, README, PDF base | 🔲 Pending |

---

## Academic Context

This project was developed as the **partial capstone submission** for the **Algorithms 1** course at **Jala University**, Software Engineering program. The evaluation focuses on:

- Logical organization and code readability
- Correct implementation of search and sorting algorithms
- Complete complexity analysis (elementary operations, T(n), Big-O, Big-Omega)
- Proper use of data structures (lists, matrices, vectors)
- Unit test coverage ≥ 70%

---

## License

This project is licensed under the [MIT License](LICENSE).

© 2026 Diego Alejandro Botina Herrera
