#!/usr/bin/env bash
set -euo pipefail

# Examples: prints JSON and writes quick artifacts into results/
python -m src.jordan_chars.estimate --lambda 8 --mu 3,2,2,1 --T 6000 > results/example_lambda8_mu3221.json
python -m src.jordan_chars.estimate --lambda 1,1,1,1,1,1,1,1 --mu 8 --T 8000 --raw > results/example_sign_lambda1n_mu8.txt
python -m src.jordan_chars.estimate --lambda 7,1 --mu 8 --T 12000 --raw > results/example_standard_lambda71_mu8.txt

# Histogram across trials (normalized character)
python scripts/plot_hist.py \
  --lambda 5,3 --mu 3,2,2,1 --T 4000 --trials 32 \
  --out results/hist_lambda53_mu3221.png
