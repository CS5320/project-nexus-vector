# Northstar Platform

This repository contains a representative implementation of several Atlas platform services used for software design analysis.

The implementation is intentionally incomplete and contains design problems that have accumulated over time. External systems such as authentication, notifications, and reporting have been replaced with simplified local implementations.

## Purpose

Students should use this repository to examine how design principles appear in code, including:

- abstraction and information hiding
- cohesion and coupling
- responsibility assignment
- duplicated validation
- inconsistent error handling
- maintainability and design for change

## Current Engineering Priorities

The Platform Team is preparing for the Atlas 4.0 modernization effort.

### Current Priorities

- Improve service modularity by reducing oversized service classes.
- Continue standardizing API behavior and error responses.
- Reduce duplicated validation logic across services.
- Minimize synchronous dependencies between platform components.
- Clarify domain boundaries within Customer Management.
- Preserve backward compatibility while modernizing legacy functionality.
 
## Running the Tests

```bash
python -m pip install -e ".[dev]"
pytest
```

## Important

Do not assume every design choice in this repository is good. The code is intended to be analyzed, critiqued, and redesigned.
