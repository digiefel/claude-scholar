---
name: architecture-design
description: |
  Use when designing the structure of a new software project or adding significant new components that require architectural decisions.

  ✅ USE when:
  - Starting a new project and deciding how to organize code
  - Adding a new module or subsystem with its own internal structure
  - Choosing between architectural patterns (layered, plugin-based, event-driven, etc.)
  - Designing configuration management for a multi-component system
  - Establishing conventions for a codebase that a team will maintain

  ❌ DO NOT USE when:
  - Modifying existing functions or fixing bugs
  - Adding helper functions or small utilities
  - Simple single-file changes
  - Refactoring without structural reorganization

  Key indicator: Does the task require deciding how components relate to each other? If no, skip this skill.
version: 2.0.0
---

# Software Architecture Design

Guidance for designing clean, maintainable software project structures. Focuses on separation of concerns, clear module boundaries, and patterns that scale as a codebase grows.

## Core Principles

### Separation of Concerns

Each module should have a single, clear responsibility:
- Keep data handling, business logic, and I/O in separate layers
- Modules should be independently testable
- Changes to one concern should not ripple through unrelated code

### Layered Architecture

Organize code in layers with clear dependency direction (inner layers don't depend on outer):

```
Entry Points (CLI, API, UI)
    ↓
Application Logic (orchestration, use cases)
    ↓
Domain Logic (core algorithms, business rules)
    ↓
Infrastructure (databases, files, external APIs)
```

### Configuration Management

- Separate configuration from code — use config files, environment variables, or dataclasses
- Make configuration explicit: no magic constants buried in source files
- Use typed configuration objects (e.g., `@dataclass(frozen=True)`) to catch errors early
- Support environment-specific overrides (dev/staging/prod) without code changes

## Directory Structure

A clean project structure reflects its architecture:

```
project/
├── src/                    # Application source code
│   ├── domain/             # Core logic, no external dependencies
│   ├── application/        # Orchestration, use cases
│   ├── infrastructure/     # External systems (DB, files, APIs)
│   └── utils/              # Shared utilities
│
├── tests/                  # Mirror src/ structure
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── config/                 # Configuration files
├── scripts/                # One-off scripts and tooling
├── data/                   # Data files (if applicable)
│   ├── raw/                # Original, immutable inputs
│   └── processed/          # Derived data
│
├── pyproject.toml          # Project metadata and dependencies
└── README.md
```

## Design Patterns

### Plugin / Registry Pattern

Use when you need to add implementations without modifying core code:

```python
REGISTRY: dict[str, type] = {}

def register(name: str):
    def decorator(cls):
        REGISTRY[name] = cls
        return cls
    return decorator

def create(name: str, **kwargs):
    cls = REGISTRY.get(name)
    if cls is None:
        raise ValueError(f"Unknown component: {name}")
    return cls(**kwargs)
```

Good for: parsers, formatters, backends, strategies — any place where you want extensibility.

### Configuration-Driven Components

Components receive a config object rather than individual parameters:

```python
@dataclass(frozen=True)
class ComponentConfig:
    param_a: int
    param_b: str = "default"

class MyComponent:
    def __init__(self, cfg: ComponentConfig):
        self.cfg = cfg
```

Benefits: configs are serializable, testable, and self-documenting.

### Interface / Protocol Boundaries

Define explicit interfaces between layers:

```python
from typing import Protocol

class DataStore(Protocol):
    def get(self, key: str) -> dict: ...
    def put(self, key: str, value: dict) -> None: ...
```

Concrete implementations can be swapped without changing calling code.

## Code Organization Guidelines

### File Size
- Keep files focused: 150–400 lines is a healthy range
- If a file grows beyond 400 lines, consider splitting by responsibility
- Avoid mega-files that mix unrelated concerns

### Import Structure
```python
# Standard library
import os
from pathlib import Path

# Third-party
import numpy as np

# Local
from src.domain import MyClass
```

### Module `__init__.py`
- Expose the public API of each module explicitly
- Don't use `__init__.py` to run logic at import time
- Use `__all__` to document what's meant to be public

## When Starting a New Project

### Step 1: Identify the main layers
What are the distinct concerns? (data ingestion, processing, storage, output)

### Step 2: Define module boundaries
Which parts need to change independently? Group things that change together.

### Step 3: Choose config strategy
How will settings be provided and overridden? Decide early — it affects every module.

### Step 4: Establish conventions
Pick naming, import style, and directory structure before writing much code. Consistency matters more than any particular choice.

### Step 5: Start with tests
Define what "working" looks like before writing implementations.

## Architecture Review Checklist

- [ ] Is each module's responsibility clear and singular?
- [ ] Can each layer be tested independently?
- [ ] Is configuration explicit and typed?
- [ ] Do dependencies point inward (domain ← application ← infrastructure)?
- [ ] Are interfaces between layers defined (not just implicit)?
- [ ] Is the directory structure self-documenting?
- [ ] Are there no circular imports?
