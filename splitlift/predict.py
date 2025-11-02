from __future__ import annotations

import json, math, os
from typing import Dict, List, Tuple

# --- utilities ---------------------------------------------------------------
def lcm(a: int, b: int) -> int:
    return abs(a*b) // math.gcd(a, b) if a and b else 0

def lcm_many(vals: List[int]) -> int:
    out = 1
    for v in vals:
        out = lcm(out, v)
    return out

def factorize(n: int) -> List[Tuple[int,int]]:
    """Trial division sufficiente per i nostri esempi didattici."""
    if n <= 1:
        return []
    fac = []
    # fattori di 2
    c = 0
    while n % 2 == 0:
        n //= 2; c += 1
    if c: fac.append((2,c))
    # dispari
    f = 3
    while f*f <= n:
        c = 0
        while n % f == 0:
            n //= f; c += 1
        if c:
            fac.append((f,c))
        f += 2
    if n > 1:
        fac.append((n,1))
    return fac

def load_cp_map(k: int, repo_root: str) -> Dict[int,int]:
    """Carica cp_maps/k{K}.json → dict {p: c_p}."""
    path = os.path.join(repo_root, "cp_maps", f"k{k}.json")
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    cp = {int(p): int(c) for p, c in data.get("cp", {}).items()}
    return cp

# --- core predict ------------------------------------------------------------
def predict_fsll(k: int, m: int, repo_root: str = ".") -> Dict:
    """
    Ritorna un dizionario JSON-friendly con:
      - k, m, factors
      - per_prime: [{p,a,c_p,t1_p,ok}]
      - t1_est (se possibile), mode ("fsll" | "fallback"), reason (se fallback)
    """
    factors = factorize(m)  # [(p,a)]
    cp_map = load_cp_map(k, repo_root)

    per_prime = []
    ok_all = True
    reasons = []

    for (p, a) in factors:
        # invertibilità (det = k^2): p | k  ⇒ non invertibile
        if k % p == 0:
            ok_all = False
            per_prime.append({
                "p": p, "a": a, "c_p": None, "t1_p": None, "ok": False,
                "note": "non-invertibile: p | k"
            })
            reasons.append(f"p|k @ p={p}")
            continue

        c_p = cp_map.get(p)
        if c_p is None:
            ok_all = False
            per_prime.append({
                "p": p, "a": a, "c_p": None, "t1_p": None, "ok": False,
                "note": "p non presente in cp_map per questo k"
            })
            reasons.append(f"missing c_p @ p={p}")
            continue

        t1_p = c_p * (p ** a)

        per_prime.append({
            "p": p, "a": a, "c_p": c_p, "t1_p": t1_p, "ok": True
        })

    out = {
        "k": k,
        "m": m,
        "factors": [{"p": p, "a": a} for (p,a) in factors],
        "per_prime": per_prime,
    }

    if ok_all:
        t1_est = lcm_many([row["t1_p"] for row in per_prime])
        out.update({
            "mode": "fsll",
            "t1_est": t1_est,
            "c_m": t1_est / m if m else None,
            "tn_rule": "t_n = t1 * m^{n-1}"
        })
    else:
        out.update({
            "mode": "fallback",
            "reason": "; ".join(reasons) if reasons else "unknown"
        })
    return out
