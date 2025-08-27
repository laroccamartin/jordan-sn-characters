import argparse, json
from .partitions import parse_partition, dim_hook_length
from .roichman import normalized_character_mc, unnormalized_from_normalized

def main():
    ap = argparse.ArgumentParser(description="Jordan (2008) classical estimator for normalized S_n characters (Roichman + GNW).")
    ap.add_argument("--lambda", dest="lam", required=True, help="partition λ, e.g., 4,2,1")
    ap.add_argument("--mu", required=True, help="cycle type μ, e.g., 3,2,2,1")
    ap.add_argument("--epsilon", type=float, default=0.03)
    ap.add_argument("--delta", type=float, default=1e-3)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--T", type=int, default=None)
    ap.add_argument("--raw", action="store_true")
    args = ap.parse_args()

    lam = parse_partition(args.lam)
    mu  = parse_partition(args.mu)

    nhat = normalized_character_mc(lam, mu, epsilon=args.epsilon, delta=args.delta, seed=args.seed, T=args.T)
    if args.raw:
        print(nhat); return
    dlam = dim_hook_length(lam)
    print(json.dumps({
        "lambda": lam, "mu": mu,
        "epsilon": args.epsilon, "delta": args.delta, "seed": args.seed, "T": args.T,
        "d_lambda": int(dlam),
        "chi_hat_est": nhat,
        "chi_est": unnormalized_from_normalized(lam, nhat),
    }, indent=2))

if __name__ == "__main__":
    main()
