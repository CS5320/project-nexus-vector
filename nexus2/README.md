# Northstar Platform v2

This repository contains a representative slice of the Atlas platform used for software design analysis.

The codebase is intentionally mixed:

- some parts are reasonably well designed,
- some are merely adequate,
- some contain clear design problems,
- and some preserve awkward behavior because existing tests depend on it.

Students should not assume that every unusual design choice is accidental—or that every class should be rewritten.

## Design Concepts Represented

- abstraction and information hiding
- cohesion and coupling
- responsibility assignment
- dependency inversion
- interface segregation
- Law of Demeter
- duplicated validation
- inconsistent error handling
- observer-style notifications
- strategy-based reporting
- technical debt
- characterization testing
- architecture drift

## Running the Project

```bash
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip setuptools
python -m pip install -e ".[dev]"
python -m pytest
```

## Repository Structure

```text
src/northstar/
    api.py
    auth.py
    customer_service.py
    errors.py
    events.py
    models.py
    notifications.py
    policies.py
    reporting.py
    repository.py
    services.py
tests/
docs/
```

## Current Engineering Concerns

- `CustomerService` performs too many unrelated responsibilities.
- Authorization checks are duplicated and inconsistent.
- Validation logic appears in multiple places.
- The API layer exposes inconsistent error shapes.
- Reporting behavior has grown without a clear abstraction boundary.
- Notifications are tightly coupled to customer operations.
- Some classes expose internal state more broadly than necessary.
- Existing tests preserve behavior that may not be desirable.

## Important

Do not begin by “fixing everything.”

First determine:

1. What the current design is trying to accomplish.
2. Which parts are stable and useful.
3. Which problems are local versus architectural.
4. Which changes could alter externally visible behavior.
