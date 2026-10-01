# ADR 0002: Lint design documents in CI

- **Status:** Accepted

## Context

A template only helps if people fill it in. The portfolio kit generated RFCs with placeholder
alternatives (`_alternative 1_`), and nothing stopped a repository from shipping them that way.
Reviewers should spend their time on the design, not on noticing missing sections.

## Decision

`tools/check_docs.py` checks every RFC and ADR for the required sections, a valid status line,
leftover template or scaffold text, and at least two real alternatives in each RFC. CI runs it
on this repository's own documents; each project can run it against its `docs/` folder.

## Consequences

- An incomplete RFC fails CI before a human reviews it.
- The check is structural only. Whether the design is good is still the reviewer's job; the
  checklist in `process.md` covers that part.
- Changing the required sections means changing the checker and its tests together.
