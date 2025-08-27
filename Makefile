.PHONY: setup test example
setup:
\tpython -m venv .venv && . .venv/bin/activate && pip install -U pip && pip install -r requirements.txt
test:
\tpytest -q
example:
\tpython -m src.jordan_chars.estimate --lambda 5,3 --mu 3,2,2,1 --T 5000 --raw
