import argparse, csv, itertools, pathlib, statistics as st
from src.jordan_chars.partitions import parse_partition
from src.jordan_chars.roichman import normalized_character_mc

def run(lam, mu, T, seeds):
    vals = [normalized_character_mc(lam, mu, seed=s, T=T) for s in seeds]
    return st.mean(vals), st.pstdev(vals)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lambdas", default="8;7,1;5,3", help="semicolon-separated")
    ap.add_argument("--mus", default="8;3,2,2,1;1,1,1,1,1,1,1,1", help="semicolon-separated")
    ap.add_argument("--T_list", default="2000,4000,8000")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--out_csv", default="results/sweep.csv")
    args = ap.parse_args()

    lam_list = [parse_partition(s) for s in args.lambdas.split(";") if s.strip()]
    mu_list  = [parse_partition(s) for s in args.mus.split(";") if s.strip()]
    T_list   = [int(x) for x in args.T_list.split(",")]
    seeds    = [int(x) for x in args.seeds.split(",")]

    outp = pathlib.Path(args.out_csv)
    outp.parent.mkdir(parents=True, exist_ok=True)
    with outp.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["lambda","mu","T","n_seeds","chi_hat_mean","chi_hat_std"])
        for lam, mu, T in itertools.product(lam_list, mu_list, T_list):
            # skip incompatible sizes quickly
            if sum(lam) != sum(mu):
                continue
            mean, std = run(lam, mu, T, seeds)
            w.writerow([lam, mu, T, len(seeds), f"{mean:.6f}", f"{std:.6f}"])
    print(f"[ok] wrote {outp}")

if __name__ == "__main__":
    main()
