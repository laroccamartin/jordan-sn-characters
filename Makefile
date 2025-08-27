.PHONY: setup test run-examples report ci

setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt

test:
\tpytest -q

run-examples:
\tbash scripts/run_examples.sh

report:
\tpython scripts/auto_report.py

ci:
\t@echo "Open Actions tab on GitHub; CI runs pytest on push."
