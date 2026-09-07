# Design Notes

These notes were collected during prior maintenance work.

- Customer management and reporting may not belong in the same service.
- Validation behavior differs depending on which operation is used.
- The API layer does not expose a consistent error model.
- Notifications are triggered directly from domain operations.
- Authorization checks appear both in `AuthClient` and directly in service methods.
- Existing tests should be treated as characterization tests before redesigning behavior.

These notes are observations, not approved architecture decisions.
