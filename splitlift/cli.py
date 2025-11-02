import argparse, json, os, sys

from . import __version__
from .predict import predict_fsll
from .verify import verify_with_t1, verify_per_prime

def _save_to(path: str, text: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

def _factorize_int(n: int) -> str:
    """Fattorizza n (>=1) e restituisce una stringa tipo '2^3·3·5'."""
    if n <= 1:
        return str(n)
    x = n
    fac = []
    # 2
    c = 0
    while x % 2 == 0:
        x //= 2
        c += 1
    if c:
        fac.append((2, c))
    # dispari
    f = 3
    while f * f <= x:
        c = 0
        while x % f == 0:
            x //= f
            c += 1
        if c:
            fac.append((f, c))
        f += 2
    if x > 1:
        fac.append((x, 1))
    # format
    parts = []
    for p, a in fac:
        parts.append(f"{p}^{a}" if a > 1 else f"{p}")
    return "·".join(parts)

def cmd_predict(args):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    result = predict_fsll(args.k, args.m, repo_root=repo_root)

    # --- JSON first ---
    if args.json:
        out = json.dumps(result, indent=2, ensure_ascii=False)
        if args.out:
            _save_to(args.out, out + "\n")
        else:
            print(out)
        return

    # --- CSV second ---
    if args.csv:
        cols = ["k", "m", "mode", "t1_est", "c_m"]
        lines = []
        lines.append(",".join(cols))
        lines.append(",".join(str(result.get(c, "")) for c in cols))
        # per-prime
        lines.append("\nper_prime")
        pcols = ["p", "a", "c_p", "t1_p", "ok"]
        lines.append(",".join(pcols))
        for row in result.get("per_prime", []):
            lines.append(",".join(str(row.get(c, "")) for c in pcols))
        out = "\n".join(lines) + "\n"
        if args.out:
            _save_to(args.out, out)
        else:
            sys.stdout.write(out)
        return

    # --- Human banner (no --json/--csv) ---
    mode = result.get("mode")
    if mode == "fsll":
        t1 = result.get("t1_est")
        t1_fact = _factorize_int(int(t1)) if isinstance(t1, int) else "?"
        parts = []
        for row in result["per_prime"]:
            p = row["p"]; a = row["a"]; cp = row["c_p"]; t1p = row["t1_p"]
            parts.append(f"{p}^{a}→{cp}·{p}^{a}={t1p}")
        print(f"FSLL[OK] t1={t1}  (factor: {t1_fact})  c_m={result.get('c_m')}")
        print("  contrib:", ", ".join(parts))
        print("  rule:", result.get("tn_rule"))
    else:
        print(f"FSLL[FAIL] reason: {result.get('reason')}")

def cmd_verify(args):
    # 1) usa predict per derivare t1_est e per_prime
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    pred = predict_fsll(args.k, args.m, repo_root=repo_root)

    if pred.get("mode") != "fsll":
        print("FSLL[FAIL] Non in fast-path FSLL per questo (k,m); verifica globale non significativa.")
        print("Reason:", pred.get("reason"))
        # exit code non-zero per CI (2 = improper state per verify FSLL)
        sys.exit(2)

    t1 = pred["t1_est"]
    # 2) verifica globale su m
    glob = verify_with_t1(args.k, args.m, t1)
    # 3) verifica per-prime su ciascun p^a con ok=True
    per_p = verify_per_prime(args.k, pred["per_prime"])

    ok_all = glob["ok_global"] and all(r["ok"] for r in per_p)

    banner = "VERIFY[OK]" if ok_all else "VERIFY[FAIL]"
    print(f"{banner}  C^t1 ≡ I (mod m): {glob['ok_global']}  (t1={t1})")
    print("per-prime:")
    for r in per_p:
        print(f" - p={r['p']}^(a={r['a']}): {'OK' if r['ok'] else 'FAIL'}")

    # exit code per CI
    sys.exit(0 if ok_all else 1)

def cmd_measure(args):
    print(f"[splitlift] measure (coverage/uniformity)")
    print(f"- k={args.k}, m={args.m}, N={args.N}, use_fsll={args.use_fsll}, seed={args.seed}")

def cmd_run(args):
    print(f"[splitlift] run (predict → verify → measure)")
    print(f"- k={args.k}, m={args.m}, mode={args.mode}, use_fsll={args.use_fsll}")

def main():
    p = argparse.ArgumentParser(prog="splitlift", description="split-lift — ricorrenze mod m (FSLL)")
    p.add_argument("--version", action="version", version=f"splitlift {__version__}")
    sub = p.add_subparsers(dest="cmd", required=True)

    # predict
    sp = sub.add_parser("predict", help="stima t1 con FSLL/LCM/CRT quando possibile")
    sp.add_argument("--k", type=int, required=True)
    sp.add_argument("--m", type=int, required=True)
    sp.add_argument("--explain", action="store_true")
    sp.add_argument("--json", action="store_true")
    sp.add_argument("--csv", action="store_true")
    sp.add_argument("--out", type=str, help="salva output su file (csv/json)")
    sp.set_defaults(func=cmd_predict)

    # verify
    sv = sub.add_parser("verify", help="verifica ordine/lifting (per-prime e globale)")
    sv.add_argument("--k", type=int, required=True)
    sv.add_argument("--m", type=int, required=True)
    sv.add_argument("--deep", action="store_true")
    sv.add_argument("--per-prime", dest="per_prime", action="store_true")
    sv.set_defaults(func=cmd_verify)

    # measure
    sm = sub.add_parser("measure", help="misura coverage/uniformità dei residui")
    sm.add_argument("--k", type=int, required=True)
    sm.add_argument("--m", type=int, required=True)
    sm.add_argument("--N", type=int, default=0, help="se 0, auto")
    sm.add_argument("--use-fsll", dest="use_fsll", action="store_true")
    sm.add_argument("--seed", default="auto")
    sm.set_defaults(func=cmd_measure)

    # run
    sr = sub.add_parser("run", help="pipeline completa: predict → verify → measure")
    sr.add_argument("--k", type=int, required=True)
    sr.add_argument("--m", type=int, required=True)
    sr.add_argument("--mode", choices=["auto", "fsll", "naive"], default="auto")
    sr.add_argument("--use-fsll", dest="use_fsll", action="store_true")
    sr.set_defaults(func=cmd_run)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
