from __future__ import annotations

from typing import List, Dict

def _mat_mul(A, B, mod):
    return [
        [(A[0][0] * B[0][j] + A[0][1] * B[1][j] + A[0][2] * B[2][j]) % mod for j in range(3)],
        [(A[1][0] * B[0][j] + A[1][1] * B[1][j] + A[1][2] * B[2][j]) % mod for j in range(3)],
        [(A[2][0] * B[0][j] + A[2][1] * B[1][j] + A[2][2] * B[2][j]) % mod for j in range(3)],
    ]

def _mat_pow(C, e, mod):
    # 3x3 fast pow
    I = [[1 % mod, 0, 0], [0, 1 % mod, 0], [0, 0, 1 % mod]]
    base = [row[:] for row in C]
    out = [row[:] for row in I]
    while e > 0:
        if e & 1:
            out = _mat_mul(out, base, mod)
        base = _mat_mul(base, base, mod)
        e >>= 1
    return out

def companion_matrix_k(k: int, mod: int):
    km1 = (k - 1) % mod
    k2 = (k * k) % mod
    return [
        [km1, 0, k2],
        [1, 0, 0],
        [0, 1, 0],
    ]

def same_matrix(A, B):
    return all(A[i][j] == B[i][j] for i in range(3) for j in range(3))

def verify_with_t1(k: int, m: int, t1: int) -> Dict:
    C = companion_matrix_k(k, m)
    I = [[1 % m, 0, 0], [0, 1 % m, 0], [0, 0, 1 % m]]
    Ct = _mat_pow(C, t1, m)
    ok_global = same_matrix(Ct, I)
    return {"ok_global": ok_global, "Ct_equals_I": ok_global}

def verify_per_prime(k: int, per_prime: List[Dict]) -> List[Dict]:
    """Verifica per ciascun fattore (p^a) con ok=True che C^{t1_p} ≡ I (mod p^a)."""
    out = []
    for row in per_prime:
        p, a, ok = row["p"], row["a"], row["ok"]
        if not ok:
            out.append({"p": p, "a": a, "ok": False, "reason": "per-prime not FSLL or missing c_p"})
            continue
        mod = p ** a
        C = companion_matrix_k(k, mod)
        I = [[1 % mod, 0, 0], [0, 1 % mod, 0], [0, 0, 1 % mod]]
        t1_p = row["t1_p"]
        Ct = _mat_pow(C, t1_p, mod)
        out.append({"p": p, "a": a, "ok": same_matrix(Ct, I)})
    return out
