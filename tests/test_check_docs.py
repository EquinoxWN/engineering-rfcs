"""The document checker accepts complete documents and rejects incomplete ones."""

from pathlib import Path

import pytest
from check_docs import check, check_repo, main

ROOT = Path(__file__).resolve().parents[1]

GOOD_RFC = """# RFC 0001: example

- **Status:** Accepted

## Problem
Real problem.
## Goals
- one
## Non-goals
- one
## Proposed design
Design.
## Alternatives considered
| Option | Why not (yet) |
|---|---|
| A | slower |
| B | costlier |
## Measurement plan
Numbers.
## Milestones
- M1
## Risks and open questions
- one
"""

GOOD_ADR = """# ADR 0002: example

- **Status:** Accepted

## Context
Why.
## Decision
What.
## Consequences
- trade-off
"""


def write(tmp_path, name, text):
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_complete_documents_pass(tmp_path):
    assert check(write(tmp_path, "rfc.md", GOOD_RFC), "rfc") == []
    assert check(write(tmp_path, "adr.md", GOOD_ADR), "adr") == []


@pytest.mark.parametrize(
    ("mutation", "expected"),
    [
        (lambda t: t.replace("## Non-goals\n- one\n", ""), "Non-goals"),
        (lambda t: t.replace("- **Status:** Accepted\n", ""), "Status"),
        (lambda t: t.replace("Accepted", "Maybe"), "status"),
        (lambda t: t.replace("| B | costlier |\n", ""), "need at least 2"),
        (lambda t: t.replace("| A | slower |", "| _alternative 1_ | _trade-off_ |"), "placeholder"),
        (lambda t: t.replace("Numbers.", "_TBD_"), "placeholder"),
        (
            lambda t: t.replace(
                "- **Status:** Accepted\n", "- **Status:** Accepted\n- **Author:** AUTHOR_NAME\n"
            ),
            "placeholder",
        ),
        (lambda t: t.replace("# RFC", "RFC"), "title"),
    ],
)
def test_incomplete_rfc_is_rejected(tmp_path, mutation, expected):
    findings = check(write(tmp_path, "rfc.md", mutation(GOOD_RFC)), "rfc")
    assert any(expected in f.message for f in findings), findings


def test_placeholders_inside_code_are_allowed(tmp_path):
    text = GOOD_RFC.replace(
        "Design.",
        "Files live in `tests/<rule>/` and the kit shipped `_alternative 1_`.\n```\npath/<name>.yml\n```",
    )
    assert check(write(tmp_path, "rfc.md", text), "rfc") == []


def test_adr_missing_consequences_is_rejected(tmp_path):
    text = GOOD_ADR.replace("## Consequences\n- trade-off\n", "")
    assert check(write(tmp_path, "adr.md", text), "adr")


def test_templates_are_valid_templates():
    assert check(ROOT / "templates" / "rfc.md", "rfc", template=True) == []
    assert check(ROOT / "templates" / "adr.md", "adr", template=True) == []


def test_templates_would_fail_as_real_documents():
    """Copying a template without filling it in must not pass review."""
    assert check(ROOT / "templates" / "rfc.md", "rfc")


def test_this_repository_passes(capsys):
    assert main([]) == 0
    n, findings = check_repo(ROOT)
    assert n >= 2
    assert findings == []


def test_scaffold_rfc_is_flagged(tmp_path):
    """The untouched scaffold RFC from the portfolio kit must be caught."""
    scaffold = GOOD_RFC.replace(
        "| A | slower |\n| B | costlier |",
        "| _alternative 1_ | _trade-off_ |\n| _alternative 2_ | _trade-off_ |",
    )
    (tmp_path / "docs" / "rfc").mkdir(parents=True)
    write(tmp_path / "docs" / "rfc", "0001-design.md", scaffold)
    n, findings = check_repo(tmp_path)
    assert n == 1
    assert findings
