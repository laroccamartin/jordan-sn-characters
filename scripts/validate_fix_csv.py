import csv, pathlib, sys

# Make repo importable
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.jordan_chars.partitions import parse_partition
from src.jordan_chars.murnaghan_nakayama import normalized_character_exact

def fix_csv(path_in:str, path_out:str=None, tol=1e-12):
    pin = pathlib.Path(path_in)
    if not pin.exists():
        print(f"[error] not found: {pin}", file=sys.stderr)
        sys.exit(2)
    pout = pathlib.Path(path_out) if path_out else pin

    rows = list(csv.DictReader(pin.open()))
    if not rows:
        print("[error] empty CSV", file=sys.stderr)
        sys.exit(2)

    diffs = 0
    for r in rows:
        lam = eval(r["lambda"])  # stored as "(…)" strings
        mu  = eval(r["mu"])
        true_exact = normalized_character_exact(lam, mu)
        # original file has key 'chi_hat_true'
        old = float(r["chi_hat_true"])
        if abs(old - true_exact) > tol:
            diffs += 1
            r["chi_hat_true"] = f"{true_exact:.12f}"
    # write output
    with pout.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

    print(f"[ok] wrote {pout} ({diffs} corrected rows)")
    return diffs

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="outp", default=None, help="default: overwrite input")
    args = ap.parse_args()
    fix_csv(args.inp, args.outp)
