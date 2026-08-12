# System Architecture

> Student Performance Analysis System | August 2026

---

## 1. Overview

The Student Performance Analysis System is a console-based application that manages and
analyzes academic performance records for university students. Built with Python 3.14 and
PostgreSQL 17, it provides interactive CRUD operations, search and sorting algorithms, and
statistical analysis through a rich terminal interface. The system is structured around a
strict four-layer architecture — CLI, Service, Repository, and Database — enforcing a clean
separation of concerns at every level. Each layer communicates only with its immediate
neighbor, making the codebase easy to test, extend, and reason about independently of
external infrastructure.

---

## 2. Layered Architecture

```text
┌─────────────────────────────────────┐
│            CLI Layer                │
│         (cli/menu.py)               │
│    MenuController + rich output     │
└──────────────┬──────────────────────┘
               │ uses
┌──────────────▼──────────────────────┐
│          Service Layer              │
│      (services/record_service.py)   │
│    RecordService — orchestration    │
└───────┬──────────────┬─────────────┘
        │              │
┌───────▼──────┐  ┌────▼────────────────────┐
│  Repository  │  │    Algorithm Layer       │
│    Layer     │  │  (algorithms/search.py   │
│ (repository/ │  │   algorithms/sort.py)    │
│  record_     │  │  + stats/statistics.py   │
│  repository) │  └─────────────────────────┘
└───────┬──────┘
        │
┌───────▼──────────────────────────────┐
│          Database Layer              │
│   PostgreSQL 17 (via Docker)         │
│   SQLAlchemy 2.x ORM + Alembic       │
└──────────────────────────────────────┘
```

---

## 3. Layer Responsibilities

**CLI Layer (`cli/menu.py` — `MenuController`):**
The CLI layer is the sole point of contact with the user. It reads user input, formats output
using `rich` styled tables and panels, and delegates every business decision to the Service
layer. This layer knows nothing about databases, algorithms, or data access — it only knows
how to present data and capture intent.

**Service Layer (`services/record_service.py` — `RecordService`):**
The Service layer orchestrates all business logic. It receives requests from the CLI,
validates inputs, calls the appropriate algorithm functions (search, sort, statistics), and
delegates data persistence to the Repository layer. It never formats output for the terminal
and never interacts with SQLAlchemy sessions directly.

**Algorithm Layer (`algorithms/search.py`, `algorithms/sort.py`, `stats/statistics.py`):**
The Algorithm layer contains pure, stateless functions that implement the core computational
logic of the project: linear search, binary search, bubble sort, selection sort, insertion
sort, and statistical aggregations. These functions accept plain Python lists or DTOs and
return results without any side effects, making them trivially testable in isolation.

**Repository Layer (`repository/record_repository.py` — `RecordRepository`):**
The Repository layer is the only layer allowed to communicate with the database. It
translates domain-level `StudentRecordDTO` objects to and from SQLAlchemy ORM models and
executes all SQL queries. The rest of the application never imports SQLAlchemy session or
model objects directly.

**Database Layer (PostgreSQL 17 via Docker + SQLAlchemy 2.x + Alembic):**
The database layer stores all student records persistently. Schema changes are managed
exclusively through Alembic versioned migrations, ensuring that the database state is always
reproducible and version-controlled. The database is never accessed by any layer above the
Repository.

---

## 4. SOLID Principles Applied

| Principle | Application |
|---|---|
| Single Responsibility | Each module has one reason to change: `menu.py` handles I/O, `record_service.py` handles orchestration, `record_repository.py` handles persistence. |
| Open/Closed | Algorithm functions (`search.py`, `sort.py`) are open for extension (new algorithms can be added) without modifying the `RecordService` that calls them. |
| Liskov Substitution | `RecordRepository` can be replaced with any compatible repository implementation (e.g., an in-memory stub for testing) without breaking the `RecordService`. |
| Interface Segregation | The CLI depends only on `RecordService` and its public methods; it has no knowledge of the repository interface or SQLAlchemy internals. |
| Dependency Inversion | `RecordService` receives its `RecordRepository` dependency via constructor injection, depending on the abstraction rather than a concrete database connection. |

---

## 5. Design Patterns Used

### Repository Pattern
**Implementation:** `RecordRepository` in `repository/record_repository.py` provides a
collection-like interface (`add`, `get_all`, `get_by_id`, `update`, `delete`) over the
`student_records` PostgreSQL table.
**Benefit:** Business logic and algorithm code are completely decoupled from SQLAlchemy
sessions and SQL syntax. Swapping the underlying database engine (e.g., for SQLite in
tests) requires changes only in this one class.

### Dependency Injection
**Implementation:** `RecordService.__init__` accepts a `RecordRepository` instance as a
constructor parameter. `MenuController.__init__` accepts a `RecordService` instance.
**Benefit:** Every layer can be tested in isolation by injecting a mock or stub dependency.
The application's wiring is centralized in `main.py`, making the dependency graph explicit
and easy to audit.

### DTO Pattern (Data Transfer Object)
**Implementation:** `StudentRecordDTO` in `models/__init__.py` is a Pydantic model that
carries data between layers. The repository converts ORM objects to DTOs before returning
them; no SQLAlchemy model leaks above the repository boundary.
**Benefit:** The rest of the application works with plain, validated Python objects. Changes
to the database schema or ORM mapping are isolated to the repository and model layers.

---

## 6. Data Flow

1. **User Action:** The user selects an option (e.g., "Search record") from the interactive
   CLI menu rendered by `MenuController`.
2. **CLI → Service:** `MenuController` captures the user's input (name query, sort field,
   etc.) and calls the corresponding method on `RecordService` (e.g.,
   `service.search_by_name("Alice")`).
3. **Service → Algorithm:** `RecordService` retrieves the full record list from the
   repository and passes it to the appropriate algorithm function
   (e.g., `linear_search(records, query)`).
4. **Service → Repository:** For CRUD operations, `RecordService` calls the repository
   directly (e.g., `repository.add(dto)`) without involving the algorithm layer.
5. **Repository → Database:** `RecordRepository` translates the DTO into a SQLAlchemy ORM
   object, opens a session, executes the query against PostgreSQL 17, and commits.
6. **Return Path:** PostgreSQL returns rows → the repository maps them to `StudentRecordDTO`
   instances → the service returns them to the CLI → `MenuController` formats and renders
   the result as a `rich` table in the terminal.

---

## 7. Local Development Databases

- `capstone_db` — the application database used during normal operation.
- `capstone_test_db` — the isolated test database used exclusively by the pytest suite.
- Both databases are created automatically on first `docker compose up` by the init script
  at `docker/postgres/init.sh`.
- Developers never need to create databases manually.
- To reset both databases from scratch:
  ```bash
  docker compose down -v   # destroys the pgdata volume
  docker compose up -d     # recreates the container and both databases
  ```

---

## 8. Project Directory Structure

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
│       ├── architecture.md           # This document — layered architecture overview
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
│       │   ├── __init__.py           # StudentRecordDTO (Pydantic) + StudentRecord ORM
│       │   └── record.py             # SQLAlchemy ORM model for student_records table
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
├── README.md                         # Project overview and setup guide
└── uv.lock                           # Locked dependency graph (uv)
```
