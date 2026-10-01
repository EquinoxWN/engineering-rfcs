.PHONY: setup lint test check check-repos bench ci audit

setup:
	python -m pip install -r requirements-dev.txt

lint:
	python -m yamllint -d relaxed .
	python -m ruff check .
	python -m ruff format --check .

# Structural check of the templates and this repository's own RFCs and ADRs.
check:
	python tools/check_docs.py

test:
	python -m pytest -q

# Check sibling project repositories cloned next to this one, e.g. make check-repos REPOS="../lsm-kv-store"
check-repos:
	python tools/check_docs.py $(REPOS)

bench: check

# Known vulnerabilities in the installed dependencies.
audit:
	python -m pip_audit -r requirements-dev.txt

ci: setup lint check test
