# RFC 0001: engineering-rfcs design

- **Status:** Accepted (M1 implemented)
- **Author:** AUTHOR_NAME
- **Created:** 2026

## Problem

At Staff level, the writing matters as much as the code: why a design was chosen, what was
rejected, and what was learned when it broke. In personal projects that writing usually does not
exist, or it lives in scattered notes nobody can find. Reviewers and interviewers then only see
code, not judgement.

## Goals

- Every flagship project gets an RFC before it is built (M1).
- Decisions made during a build are captured as short ADRs with their consequences (M1).
- Shared templates and a written process, so every document has the same shape (M1).
- A checker that fails CI on incomplete documents (M1).
- Later: public design reviews in PR threads (M2), blameless postmortems from chaos drills and
  fuzzing finds (M2), a review checklist and a full index from RFC to code to postmortem (M3).

## Non-goals

- A documentation website. Markdown rendered by GitHub is enough.
- Storing each project's documents here. They live next to their code; this repository holds the
  process, templates, tooling and the index.
- Running as a hosted production service.

## Proposed design

![architecture](../architecture.png)

| Piece | Location | Purpose |
|---|---|---|
| Process | `process.md` | When to write an RFC, ADR or postmortem; lifecycle; what reviewers check |
| Templates | `templates/rfc.md`, `templates/adr.md` | Starting point with every required section |
| Checker | `tools/check_docs.py` | Required sections, valid status, no leftover placeholders, at least two alternatives |
| Index | `index.md` | One row per project: RFC, ADRs, the code they shaped, results |

The checker runs in CI on this repository and can be pointed at any project:
`python tools/check_docs.py ../lsm-kv-store`.

## Alternatives considered

| Option | Why not (yet) |
|---|---|
| A wiki or Notion space | Separated from the code and its history; review comments are not tied to the text. |
| Keep every RFC in this repository | One place to browse, but the RFC then drifts from the code it describes. Linking from an index keeps both benefits. |
| No checker, rely on review | Worked badly in practice: the kit shipped placeholder alternatives that a quick review missed. See ADR 0002. |
| A heavyweight process (sign-off roles, numbered states) | Too much ceremony for a one-person portfolio; the lifecycle in `process.md` stays small on purpose. |

## Measurement plan

- M1: number of wave-1 RFCs and ADRs, and how many pass `check_docs.py` (target: all).
- M2: review threads with at least one outside comment; postmortems written.
- M3: a reader can trace one flagship from RFC to code to postmortem through `index.md`.

## Milestones

- **M1 (done):** process, RFC and ADR templates, checker with tests, wave-1 index.
- **M2:** public design reviews, postmortem template and first postmortems.
- **M3:** review checklist, full index, traceability demo.

## Risks and open questions

- Documents can pass the checker and still be shallow. The review checklist (M3) and outside
  reviewers are the countermeasure.
- Index links break if a project renames files; a link check could join CI in M3.
