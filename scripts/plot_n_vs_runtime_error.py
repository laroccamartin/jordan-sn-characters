import argparse, random, time, csv, math, pathlib
import numpy as np
import matplotlib.pyplot as plt

from src.jordan_chars.partitions import parse_partition
from src.jordan_chars.roichman import normalized_character_mc
from src.jordan_chars.murnaghan_nakayama import normalized_character_exact

def all_partitions(n):
    def gen(rem, maxp, pref):
        if rem == 0:
            yield tuple(pref)
            return
        for k in range(min(rem, maxp), 0, -1):
            pref.append(k)
            yield from gen(rem-k, k, pref)
            pref.pop()
    yield from gen(n, n, [])

def choose_partitions(n, k, seed=0):
    plist = list(all_partitions(n))
    rng = random.Random(seed)
    rng.shuffle(plist)
    # Avoid trivial extremes for variety if possible
    filtered = [p for p in plist if p not in [(n,), tuple([1]*n)]]
    base = filtered if len(filtered) >= k else plist
    return base[:k]

def cycle_type(n):
    return (n,)

def identity_type(n):
    return tuple([1]*n)

def random_cycle_type(n, rng):
    # sample a random partition of n (uniform over integer partitions)
    plist = list(all_partitions(n))
    return rng.choice(plist)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n_min", type=int, default=6)
    ap.add_argument("--n_max", type=int, default=12)
    ap.add_argument("--per_n", type=int, default=10, help="random partitions λ per n")
    ap.add_argument("--T", type=int, default=8000)
    ap.add_argument("--mu_kind", choices=["ncycle","identity","random"], default="ncycle")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out_csv", default="results/runtime_error_n6to12.csv")
    ap.add_argument("--out_plot_runtime", default="results/plot_runtime_vs_n.png")
    ap.add_argument("--out_plot_error", default="results/plot_error_vs_n.png")
    args = ap.parse_args()

    rng = random.Random(args.seed)
    rows = []
    for n in range(args.n_min, args.n_max+1):
        lam_list = choose_partitions(n, args.per_n, seed=args.seed + n)
        if args.mu_kind == "ncycle":
            mu = cycle_type(n)
        elif args.mu_kind == "identity":
            mu = identity_type(n)
        else:
            mu = random_cycle_type(n, rng)

        for lam in lam_list:
            t0 = time.perf_counter()
            est = normalized_character_mc(lam, mu, seed=rng.randrange(1<<30), T=args.T)
            dur = time.perf_counter() - t0
            truth = normalized_character_exact(lam, mu)
            err = abs(est - truth)
            rows.append({
                "n": n, "lambda": lam, "mu": mu, "T": args.T,
                "runtime_s": dur, "per_sample_ms": (1000.0*dur/args.T),
                "chi_hat_est": est, "chi_hat_true": truth, "abs_err": err
            })

    # write CSV
    outp = pathlib.Path(args.out_csv)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    print(f"[ok] wrote {outp}")

    # plots
    xs_r, ys_r = [], []
    xs_e, ys_e = [], []
    jitter = lambda: rng.uniform(-0.15, 0.15)
    for r in rows:
        xs_r.append(r["n"] + jitter()); ys_r.append(r["runtime_s"])
        xs_e.append(r["n"] + jitter()); ys_e.append(r["abs_err"])

    # runtime plot
    plt.figure()
    plt.scatter(xs_r, ys_r, s=18)
    plt.xlabel("n"); plt.ylabel("runtime (s)")
    plt.xticks(list(range(args.n_min, args.n_max+1)))
    plt.title(f"Runtime vs n (T={args.T}, μ={args.mu_kind})")
    plt.tight_layout(); plt.savefig(args.out_plot_runtime, dpi=160)
    print(f"[ok] wrote {args.out_plot_runtime}")

    # error plot
    plt.figure()
    plt.scatter(xs_e, ys_e, s=18)
    plt.xlabel("n"); plt.ylabel("absolute error in normalized character")
    plt.xticks(list(range(args.n_min, args.n_max+1)))
    plt.title(f"Absolute error vs n (T={args.T}, μ={args.mu_kind})")
    plt.tight_layout(); plt.savefig(args.out_plot_error, dpi=160)
    print(f"[ok] wrote {args.out_plot_error}")
