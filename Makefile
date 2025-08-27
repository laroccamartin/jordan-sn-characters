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

.PHONY: timing sweep report

timing:
	python scripts/timing_study.py --lambda 7,1 --mu 8 --T_list 1000,2000,4000,8000,16000 --repeats 3 --out results/timing.json

sweep:
	python scripts/param_sweep.py --lambdas "8;7,1;5,3" --mus "8;3,2,2,1;1,1,1,1,1,1,1,1" --T_list 2000,4000,8000 --seeds 0,1,2,3,4 --out_csv results/sweep.csv

report:
	python scripts/append_report.py

