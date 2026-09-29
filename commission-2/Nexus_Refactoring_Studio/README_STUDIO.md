# Nexus refactoring studio — Week 6 Tuesday

**Working exercise only. Nothing is submitted or graded today.**
This is a disposable, offline-compatible subset of **basic Nexus**, not Nexus 2,
not a customer feature implementation, and not a replacement team repository.

## Start
1. Extract the ZIP. Open the `Nexus_Refactoring_Studio` folder in your editor.
2. Open a terminal in that folder. Python 3.10 or newer is required.
3. Run `python3 check_refactoring.py` (or `python check_refactoring.py` if that
   selects Python 3.10+ on your machine). No package installation is needed.
4. The untouched sample should report **14 tests, OK**. Record the actual result.
   Do not begin a refactoring with a failing baseline.

Two students can share one working environment. Spend no more than three minutes
troubleshooting setup before using the projected code / paper-diff route. In the
paper route, predict checks and write **not executed**, never “tests passed.”

## Only when instructed: make one change
Edit only `src/northstar/reporting.py`.
Extract the expression that formats one customer into a helper named
`_format_customer_row(customer: Customer) -> str` in the same module.
Call it where the existing row-formatting expression is used.

Keep the existing header, field order, input order, validation calls/check order,
exception types/messages, and newline behavior. Leave the service's permission
check and active-customer selection where they are. Do not change input data,
email rules, tag rules, sorting, CSV escaping, or the tests to match new output.
Use `reporting_before.py.txt` as a comparison baseline. A diff with one helper and
one changed use site is the target; there is no need for a new framework.

Run `python3 check_refactoring.py` again. These instructor-authored checks cover
selected current behavior, not every possible input, caller, side effect, or
performance property. Green tests are evidence, not a proof or a design verdict.
In your normal development environment, run the existing full suite as well.

## Peer review and working notes
Use `WORKING_NOTES.md`, a notebook, or your existing notes. Explain the diff, the
behavior it preserves, what you actually checked, and whether the extraction is
worth keeping. Reverting a low-value extraction is a valid engineering judgment.
No pull request, repository push, report revision, or new submission is required.

## Working in your own basic nexus/ instead
Use the `src/northstar/reporting.py` inside **basic nexus/**, not nexus2/.
Compare it to this snapshot first. If it differs, do not overwrite it: use this
lab copy. Place `check_refactoring.py` beside that basic project's `src/` only
when it matches, and preserve your normal baseline/work. Do not reset or replace
team work. The standalone copy above is the recommended low-setup route.

## Source provenance
Seven source modules are verbatim from CS5320/northstar-platform, commit:
`d2de51b4f2d5f718dd45e5ce553665b610a38dcf`.
Their Git blob hashes were checked against the connected GitHub response.
The repository is CC0 1.0 Universal; see SOURCE_MANIFEST.json for canonical links.
The package marker, regression checks, instructions, and notes are new teaching
materials. The full upstream repository and its existing tests are not bundled.

## Next class
Keep both your submitted assessment and today's working notes. The next class
introduces additional evidence and a guided Nexus 2 comparison. Do not switch
versions for today's exercise.
