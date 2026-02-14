# Python3 Systematic Learning Guide — For Java Architects

> [中文版 (Chinese Version)](README_CN.md)

## Overview

A hands-on Python3 tutorial designed for experienced Java backend engineers. Learn Python quickly by mapping concepts to their Java equivalents.

## Project Structure

```
python_tutorial/
├── 01_syntax/          # Chapter 1: Syntax Basics
├── 02_concurrency/     # Chapter 2: Concurrency
├── 03_stdlib/          # Chapter 3: Standard Library
├── 04_frameworks/      # Chapter 4: Web Frameworks
├── 05_packaging/       # Chapter 5: Packaging & Build
└── requirements.txt    # Dependencies
```

## Learning Plan

### Phase 1: Syntax Basics (`01_syntax/`)

| # | Topic | File | Java Comparison |
|---|-------|------|-----------------|
| 1 | Types & Variables | `01_types_and_variables.py` | Dynamic typing vs Static typing |
| 2 | Control Flow | `02_control_flow.py` | match-case vs switch |
| 3 | Functions | `03_functions.py` | First-class citizens vs Methods |
| 4 | OOP | `04_oop.py` | Multiple inheritance & MRO vs Single inheritance + Interfaces |
| 5 | Decorators | `05_decorators.py` | Python's approach to AOP / Annotations |
| 6 | Generators & Iterators | `06_generators_iterators.py` | Python's approach to Stream API |
| 7 | Type Hints | `07_type_hints.py` | Static typing in Python |
| 8 | Error Handling | `08_error_handling.py` | try-except vs try-catch |
| 9 | Comprehensions | `09_comprehensions.py` | Python's unique elegant syntax |

### Phase 2: Concurrency (`02_concurrency/`)

| # | Topic | File | Java Comparison |
|---|-------|------|-----------------|
| 1 | Threading | `01_threading_basics.py` | GIL limitations vs Java true parallelism |
| 2 | Multiprocessing | `02_multiprocessing.py` | Bypassing the GIL |
| 3 | asyncio | `03_asyncio_basics.py` | Coroutines vs CompletableFuture |
| 4 | concurrent.futures | `04_concurrent_futures.py` | Similar to ExecutorService |
| 5 | Sync Primitives | `05_sync_primitives.py` | Lock / Event / Semaphore |

### Phase 3: Standard Library (`03_stdlib/`)

| # | Topic | File | Java Comparison |
|---|-------|------|-----------------|
| 1 | collections | `01_collections_module.py` | Enhanced containers |
| 2 | itertools | `02_itertools_module.py` | Stream utilities |
| 3 | pathlib & os | `03_pathlib_and_os.py` | java.nio.file.Path |
| 4 | logging | `04_logging_module.py` | SLF4J / Logback |
| 5 | JSON & Serialization | `05_json_and_serialization.py` | Jackson / Gson |
| 6 | Regular Expressions | `06_re_module.py` | java.util.regex |
| 7 | dataclasses | `07_dataclasses_module.py` | Lombok @Data / Record |
| 8 | Context Managers | `08_contextmanager.py` | try-with-resources |
| 9 | Numbers & Math | `09_numbers_and_math.py` | BigDecimal / Math |
| 10 | Date & Time | `10_datetime_module.py` | java.time (LocalDateTime/ZonedDateTime) |

### Phase 4: Web Frameworks (`04_frameworks/`)

| # | Topic | Directory | Java Comparison |
|---|-------|-----------|-----------------|
| 1 | Flask | `flask_demo/` | Lightweight web, like minimal Spring Boot |
| 2 | FastAPI | `fastapi_demo/` | Modern async web with built-in OpenAPI |
| 3 | SQLAlchemy | `sqlalchemy_demo/` | ORM, like MyBatis / JPA |

### Phase 5: Packaging & Build (`05_packaging/`)

| # | Topic | Description | Java Comparison |
|---|-------|-------------|-----------------|
| 1 | venv | Virtual environment isolation | Similar to classloader isolation |
| 2 | pip | Package management | Maven / Gradle dependency management |
| 3 | pyproject.toml | Project configuration | pom.xml / build.gradle |
| 4 | Poetry | Modern package manager | Similar to Gradle |
| 5 | uv | Next-gen package manager (Rust) | Speed leap like Gradle vs Maven |
| 6 | Testing | pytest | JUnit |

## Quick Start

```bash
# 1. Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run any demo
python3 01_syntax/01_types_and_variables.py
```

## Key Differences Cheat Sheet (Java vs Python)

| Aspect | Java | Python |
|--------|------|--------|
| Type System | Static, strongly typed | Dynamic, strongly typed |
| Execution | Compiled to bytecode (JVM) | Interpreted (CPython) |
| Concurrency | True multi-threading | GIL limitation; multiprocessing / coroutines |
| Package Manager | Maven / Gradle | pip / Poetry / uv |
| Build Config | pom.xml / build.gradle | pyproject.toml |
| Web Framework | Spring Boot | Flask / FastAPI / Django |
| ORM | JPA / MyBatis | SQLAlchemy / Django ORM |
| Interface / Abstract | interface / abstract | ABC (Abstract Base Class) / Protocol |
| Lambda | `(x) -> x + 1` | `lambda x: x + 1` |
| Null | `null` | `None` |
| Entry Point | `public static void main` | `if __name__ == "__main__"` |
