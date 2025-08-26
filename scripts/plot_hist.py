import argparse, numpy as np, matplotlib.pyplot as plt
from src.jordan_chars.partitions import parse_partition
from src.jordan_chars.roichman import normalized_character_mc

ap = argparse.ArgumentParser()
ap.add_argument("--lambda", dest="lam", required=True)
ap.add_argument("--mu", required=True)
ap.add_argument("--T", type=int, default=5000)
ap.add_argument("--trials", type=int, default=20)
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--out", type=str, default="results/hist.png")
args = ap.parse_args()

lam = parse_partition(args.lam); mu = parse_partition(args.mu)
vals = []
for t in range(args.trials):
    v = normalized_character_mc(lam, mu, seed=args.seed+t, T=args.T)
    vals.append(v)
print("mean±std:", float(np.mean(vals)), float(np.std(vals)))
plt.figure()
plt.hist(vals, bins=20)
plt.title(f"chi_hat(λ={lam}, μ={mu}), T={args.T}, trials={args.trials}")
plt.xlabel("estimate"); plt.ylabel("count")
plt.tight_layout(); plt.savefig(args.out, dpi=150)
print("saved", args.out)
