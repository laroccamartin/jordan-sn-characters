import argparse, time, statistics as st, json, pathlib
from src.jordan_chars.partitions import parse_partition
from src.jordan_chars.roichman import normalized_character_mc

def bench_once(lam, mu, T, seed):
    t0 = time.perf_counter()
    v = normalized_character_mc(lam, mu, seed=seed, T=T)
    dt = time.perf_counter() - t0
    return v, dt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lambda", dest="lam", required=True, help="e.g. 7,1")
    ap.add_argument("--mu", required=True, help="e.g. 8 or 3,2,2,1")
    ap.add_argument("--T_list", default="1000,2000,4000,8000,16000")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--out", default="results/timing.json")
    args = ap.parse_args()

    lam = parse_partition(args.lam)
    mu  = parse_partition(args.mu)
    Ts = [int(x) for x in args.T_list.split(",")]

    rows = []
    for T in Ts:
        durs = []
        vals = []
        for r in range(args.repeats):
            v, dt = bench_once(lam, mu, T, seed=1234 + r)
            vals.append(v); durs.append(dt)
        rows.append({
            "T": T,
            "repeats": args.repeats,
            "mean_s": st.mean(durs),
            "std_s": st.pstdev(durs),
            "mean_per_sample_ms": (st.mean(durs) / T) * 1000.0,
            "value_mean": st.mean(vals),
            "value_std": st.pstdev(vals),
        })

    outp = pathlib.Path(args.out)
    outp.parent.mkdir(parents=True, exist_ok=True)
    meta = {"lambda": lam, "mu": mu}
    outp.write_text(json.dumps({"meta": meta, "rows": rows}, indent=2))
    print(f"[ok] wrote {outp}")

if __name__ == "__main__":
    main()
