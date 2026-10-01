"""Check that RFCs and ADRs are complete: required sections present, no template placeholders.

Usage:
    python tools/check_docs.py                 # this repo's templates and docs
    python tools/check_docs.py ../lsm-kv-store ../cdc-lakehouse   # other repos' docs/rfc and docs/adr
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

RFC_SECTIONS = (
    "Problem",
    "Goals",
    "Non-goals",
    "Proposed design",
    "Alternatives considered",
    "Measurement plan",
    "Milestones",
    "Risks and open questions",
)
ADR_SECTIONS = ("Context", "Decision", "Consequences")
STATUSES = ("Draft", "In review", "Accepted", "Rejected", "Superseded")
# Text left over from the scaffold or the templates.
PLACEHOLDERS = (
    r"_alternative \d_",
    r"_trade-off_",
    r"_What could make this design wrong\?_",
    r"_TBD_",
    r"<[a-z][a-z -]*>",
)


@dataclass
class Finding:
    """One problem in one document."""

    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def _headings(text: str) -> list[str]:
    """Return every level-2 heading."""
    return [m.group(1).strip() for m in re.finditer(r"^## (.+)$", text, re.MULTILINE)]


def _status(text: str) -> str | None:
    """Return the value of the Status line, if any."""
    m = re.search(r"^- \*\*Status:\*\*\s*(.+)$", text, re.MULTILINE)
    return m.group(1).strip() if m else None


def check(path: Path, kind: str, template: bool = False) -> list[Finding]:
    """Check one RFC or ADR file."""
    text = path.read_text(encoding="utf-8")
    required = RFC_SECTIONS if kind == "rfc" else ADR_SECTIONS
    heads = _headings(text)
    found = [Finding(path, f"missing section '## {s}'") for s in required if s not in heads]
    if not text.startswith("# "):
        found.append(Finding(path, "first line must be a '# ' title"))
    status = _status(text)
    if status is None:
        found.append(Finding(path, "missing '- **Status:**' line"))
    elif not template and not status.startswith(STATUSES):
        found.append(Finding(path, f"status {status!r} must start with one of {STATUSES}"))
    if not template:
        prose = _strip_code(text)
        found.extend(
            Finding(path, f"unfilled placeholder matching {pattern!r}")
            for pattern in PLACEHOLDERS
            if re.search(pattern, prose)
        )
        if kind == "rfc":
            rows = _alternative_rows(text)
            if rows < 2:
                found.append(
                    Finding(path, f"'Alternatives considered' lists {rows} option(s); need at least 2")
                )
    return found


def _strip_code(text: str) -> str:
    """Drop fenced blocks and inline code, where placeholder-like text is legitimate."""
    text = re.sub(r"^```.*?^```", "", text, flags=re.MULTILINE | re.DOTALL)
    return re.sub(r"`[^`\n]*`", "", text)


def _alternative_rows(text: str) -> int:
    """Count table rows in the Alternatives section, excluding header and divider."""
    m = re.search(r"^## Alternatives considered$(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    if not m:
        return 0
    rows = [ln for ln in m.group(1).splitlines() if ln.startswith("|")]
    return max(0, len(rows) - 2)


def check_repo(root: Path) -> tuple[int, list[Finding]]:
    """Check every RFC and ADR under root/docs; return (documents checked, findings)."""
    docs = [(p, "rfc") for p in sorted((root / "docs" / "rfc").glob("*.md"))]
    docs += [(p, "adr") for p in sorted((root / "docs" / "adr").glob("*.md"))]
    findings = [f for p, kind in docs for f in check(p, kind)]
    return len(docs), findings


def main(argv: list[str]) -> int:
    """Check templates here, or the repos given on the command line."""
    here = Path(__file__).resolve().parents[1]
    findings: list[Finding] = []
    if argv:
        for arg in argv:
            n, f = check_repo(Path(arg))
            print(f"{Path(arg).resolve().name}: {n} documents, {len(f)} problems")
            findings += f
    else:
        findings += check(here / "templates" / "rfc.md", "rfc", template=True)
        findings += check(here / "templates" / "adr.md", "adr", template=True)
        n, f = check_repo(here)
        findings += f
        print(f"templates: 2, own documents: {n}, problems: {len(findings)}")
    for f in findings:
        print(f"  {f}")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
