import json, csv, pathlib, datetime as dt

RES = pathlib.Path("results")
lines = [f"\n## Auto Report — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

# Timing report
timing = RES/"timing.json"
if timing.exists():
    data = json.loads(timing.read_text())
    lam, mu = data["meta"]["lambda"], data["meta"]["mu"]
    lines += [f"### Timing (λ={tuple(lam)}, μ={tuple(mu)})"]
    lines += ["| T | mean_s | std_s | per_sample_ms | value_mean | value_std |",
              "|---:|---:|---:|---:|---:|---:|"]
    for r in data["rows"]:
        lines += [f"| {r['T']} | {r['mean_s']:.4f} | {r['std_s']:.4f} | {r['mean_per_sample_ms']:.3f} | {r['value_mean']:.6f} | {r['value_std']:.6f} |"]
    lines += [""]

# Sweep report (top rows by std, etc.)
sweep = RES/"sweep.csv"
if sweep.exists():
    lines += ["### Parameter sweep (selected rows)"]
    with sweep.open() as f:
        reader = list(csv.DictReader(f))
    # Show first 10 rows; user can open CSV for all
    lines += ["| λ | μ | T | seeds | χ̂ mean | χ̂ std |",
              "|---|---|---:|---:|---:|---:|"]
    for row in reader[:10]:
        lines += [f"| {row['lambda']} | {row['mu']} | {row['T']} | {row['n_seeds']} | {row['chi_hat_mean']} | {row['chi_hat_std']} |"]
    lines += [f"\nFull CSV: `{sweep}`\n"]

path = pathlib.Path("RESULTS.md")
path.write_text(path.read_text() + "\n".join(lines) if path.exists() else "\n".join(lines))
print("[ok] RESULTS.md appended.")
