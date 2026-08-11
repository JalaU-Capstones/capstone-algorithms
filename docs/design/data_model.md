# Data Model Design

**Date:** August 2026

## Entity: StudentRecord
**Purpose:** Represents a student's performance evaluation in a specific subject.

### Fields
| Field | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Auto-increment | Unique identifier for the record. |
| `name` | `VARCHAR(100)` | Not Null | Student's full name. |
| `category` | `VARCHAR(50)` | Not Null | Skill level: Junior, Mid, Senior, Expert. |
| `score` | `NUMERIC(5,2)` | Not Null | Evaluation score from 0.00 to 100.00. |
| `subject` | `VARCHAR(100)` | Not Null | Evaluated subject or course name. |
| `created_at` | `TIMESTAMP` | Not Null, Default `now()` | Timestamp when the record was created. |

### ER Diagram

```text
+-----------------------+
|    student_records    |
+-----------------------+
| PK | id         : INT |
|    | name       : STR |
|    | category   : STR |
|    | score      : NUM |
|    | subject    : STR |
|    | created_at : TS  |
+-----------------------+
```

### Constraints and Validation Rules
- **Name:** Maximum 100 characters.
- **Category:** Maximum 50 characters. Limited conceptually to Junior, Mid, Senior, Expert.
- **Score:** Numeric field with 5 precision and 2 scale, allowing values from 0.00 to 100.00.
- **Subject:** Maximum 100 characters.

### Schema Notes
This schema was chosen to keep the data model simple and flat, ideal for learning sorting and searching algorithms in the capstone project. A single table avoids complex joins while still providing enough realistic data fields (strings, decimals, timestamps) to implement diverse sorting and filtering logic.
