# Design Notes

These notes were collected during prior maintenance and architecture reviews.

## Observations

- `CustomerService` remains a compatibility layer and a source of architecture drift.
- Newer registration and lifecycle services use centralized authorization and domain events.
- Legacy operations continue to call notification clients directly.
- Validation behavior differs between creation, update, reporting, and tagging.
- The v2 API uses a consistent envelope; legacy endpoints do not.
- Both modern and legacy report implementations remain active.
- Existing tests should be treated as characterization tests before redesigning behavior.

## Questions for Review

- Should `CustomerService` remain a façade, be decomposed, or be retired?
- Is the event-based design worth the additional indirection?
- Should all validation be centralized?
- How should backward compatibility influence the redesign?
- Which inconsistencies are defects, and which are contractual behavior?
