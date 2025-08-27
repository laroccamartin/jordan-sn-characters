import json, os, glob, datetime as dt, pathlib

RES = pathlib.Path("results")
md = [f"\n## Auto Report — {dt.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]

# Example artifacts
j = RES/"example_lambda8_mu3221.json"
if j.exists():
    data = json.loads(j.read_text())
    md += [
        "### Example: λ=(8), μ=(3,2,2,1)",
        f"- d_λ = {data['d_lambda']}",
        f"- χ̂ estimate = {data['chi_hat_est']:.6f}",
        f"- χ estimate  = {data['chi_est']:.1f}",
        ""
    ]

# Pull any sign/standard quick checks
for name in ["example_sign_lambda1n_mu8.txt", "example_standard_lambda71_mu8.txt"]:
    p = RES/name
    if p.exists():
        md += [f"### {name.replace('_',' ').replace('.txt','')}", f"- value: `{p.read_text().strip()}`", ""]

# Attach histogram if present
h = RES/"hist_lambda53_mu3221.png"
if h.exists():
    md += ["### Histogram", f"![hist]({h.as_posix()})", ""]

# Write/append RESULTS.md
path = pathlib.Path("RESULTS.md")
path.write_text(path.read_text() + "\n".join(md) if path.exists() else "\n".join(md))
print("[ok] RESULTS.md updated.")
