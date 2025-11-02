import argparse
from . import __version__

def cmd_predict(args):
    print(f"[splitlift] predict (FSLL fast-path if possible)")
    print(f"- k={args.k}, m={args.m}, explain={args.explain}, json={args.json}, csv={args.csv}")

def cmd_verify(args):
    print(f"[splitlift] verify (order checks per-prime/global)")
    print(f"- k={args.k}, m={args.m}, deep={args.deep}, per_prime={args.per_prime}")

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
    sr.add_argument("--mode", choices=["auto","fsll","naive"], default="auto")
    sr.add_argument("--use-fsll", dest="use_fsll", action="store_true")
    sr.set_defaults(func=cmd_run)

    args = p.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
