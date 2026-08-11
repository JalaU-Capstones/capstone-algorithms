# System Architecture

**Date:** August 2026

## Layered Architecture Diagram

```text
+-----------------------+
|      CLI (View)       |  <-- menu.py
+-----------+-----------+
            |
            v
+-----------+-----------+
|      Services         |  <-- record_service.py
|    (Business Logic)   |
+-----------+-----------+
            |
            v
+-----------+-----------+
|     Algorithms        |  <-- search.py, sort.py, statistics.py
+-----------+-----------+
            |
            v
+-----------+-----------+
|     Repository        |  <-- record_repository.py
|    (Data Access)      |
+-----------+-----------+
            |
            v
+-----------+-----------+
|       Database        |  <-- PostgreSQL
+-----------------------+
```

## Layer Responsibilities
- **CLI (Command Line Interface):** Handles user input and formats output. Depends only on the Service layer.
- **Services:** Contains business logic and orchestrates calls to algorithms and repositories.
- **Algorithms:** Pure functions or isolated modules for searching, sorting, and statistical calculations.
- **Repository:** Abstracts database access. Translates domain objects (DTOs) to and from SQLAlchemy models.
- **Database:** Stores data persistently (PostgreSQL).

## SOLID Principles
- **Single Responsibility Principle (SRP):** Each layer and class has one responsibility. For example, `RecordRepository` only handles DB interactions.
- **Dependency Inversion Principle (DIP):** The Service layer depends on repository abstractions (and DTOs) rather than direct database models or engines.

## Design Patterns
- **Repository Pattern:** Isolates the data access code from the rest of the application. It provides a collection-like interface for accessing `StudentRecord` data, shielding business logic from SQLAlchemy complexities.

## Data Flow
1. **User Action:** The user selects an option in the CLI menu.
2. **CLI:** The CLI layer parses input and calls a method on the `RecordService`.
3. **Service:** The service validates the request, optionally calls the algorithm layer, and uses the `RecordRepository` to read/write data.
4. **Repository:** The repository translates the request into an SQL query via SQLAlchemy.
5. **Database:** PostgreSQL executes the query and returns the results.
6. **Return:** The data flows back up as DTOs, which the CLI formats and displays to the user.
