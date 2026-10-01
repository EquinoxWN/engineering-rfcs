# How design documents work here

## When to write what

| Document | Write it when | Size |
|---|---|---|
| **RFC** | Before building anything that takes more than a few days or that others will depend on | 1 to 3 pages |
| **ADR** | During the build, whenever you make a decision a future reader would question | Half a page |
| **Postmortem** (M2) | After an outage, a chaos drill or a serious fuzzing find | 1 to 2 pages |

Rule of thumb: an RFC decides *what and why* before the code; ADRs record *each non-obvious
choice* as the code is written.

## RFC lifecycle

```
Draft ──► In review ──► Accepted ──► Accepted (Mn implemented)
                    └─► Rejected
Accepted ──► Superseded (by RFC NNNN)
```

1. **Draft.** Copy `templates/rfc.md` into the project as `docs/rfc/NNNN-<topic>.md`. Write the
   problem and goals first; if they do not convince you, stop.
2. **In review.** Open a pull request containing only the RFC. Reviewers comment on the PR
   thread, so every critique and answer stays public and linked to the text it changed.
3. **Accepted.** Merge once the open questions are answered or recorded as risks. Code starts.
4. **Implemented.** Update the status line as milestones land (for example
   "Accepted (M1 implemented)"), so the document never claims more than the code does.
5. **Superseded or rejected.** Never delete an RFC. Mark it and link to the replacement.

## What reviewers check

- The problem is real and stated before the solution.
- Non-goals are explicit.
- At least two real alternatives appear, each with the trade-off that ruled it out.
- The measurement plan names concrete numbers and the command that produces them.
- Risks are honest. "None" is almost never true.

`tools/check_docs.py` enforces the mechanical part of this list: required sections, a valid
status, no leftover template text, and at least two alternatives. CI runs it.

## ADR rules

- Number ADRs in order per project (`docs/adr/0002-...`). ADR 0001 records the decision to keep
  ADRs at all.
- One decision per ADR, with its consequences, including the bad ones.
- An ADR is immutable once accepted. To change your mind, write a new ADR that supersedes it.
