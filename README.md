# split-lift
Predict → Verify → Measure per ricorrenze mod "m" (in modalità FSLL: Full-Split Linear-Lift).

**Ricerca → Verifica → Misura.**  
Ordina \(t_1\), LCM/CRT quando *full-split*, lifting lineare su torri \(p^a\), e misura di coverage/uniformità dei residui. 
Modalità **FSLL (Full-Split Linear-Lift)** come "fast-path" con fallback automatico.

> Fa parte di **Turbo-LAB**. 
**split-lift** (ricorrenze/FSLL) e **Turbo-Bucketizer** (hashing IPv4) sono **progetti distinti** di Turbo-LAB, con domini e codice diversi.

## FSLL in 3 righe
- **Full-Split:** per ogni \(p\mid m\), il polinomio caratteristico si spezza in 3 radici distinte in \(\mathbb{F}_p^\*\).
- **Linear-Lift:** su \(p^a\): \(t_1(p^a)=c_p\cdot p^{a-1}\).
- **Composto (CRT/LCM):** \(t_1(m)=\mathrm{lcm}(c_p\,p^{a-1})\) se tutti i fattori sono FSLL.

## Come si usa (anteprima CLI)
splitlift --version
splitlift predict --k 13 --m 255 --explain
splitlift verify  --k 13 --m 255 --deep --per-prime
splitlift measure --k 13 --m 255 --use-fsll --N 2040
splitlift run     --k 13 --m 255 --mode auto --use-fsll

## Esempi lampo
- **FSLL OK (composto):** `k=13, m=255` → \(t_1=\mathrm{lcm}(3,20,136)=2040\).
- **FSLL OK (primo):** `k=10, m=11` → \(t_1=10\).
- **FSLL FAIL (confronto):** `k=8, m=7` → rotazione (λ=1), niente mixing.

---

## FSLL (come “usarlo” davvero)
Quando **FSLL [OK]** (Full-Split + Linear-Lift), hai questi "superpoteri":

1) **Periodo gratis** — niente "run" pesanti:
   - Per ogni primo buono \(p\mid m\) vale: \(t_1(p^a)=c_p\cdot p^{a-1}\) con \(c_p\mid(p-1)\).
   - Per composti \(m=\prod p^{a}\): \(t_1(m)=\mathrm{lcm}\big(c_p\,p^{a-1}\big)\).

2) **Misura giusta** — scegli **N = t₁** (o un multiplo):
   - Misurare uniformità con \(N\) non multiplo di \(t_1\) sballa i contatori.
   - Regola pratica: se non sai che fare, usa **N = t₁**.

3) **Semi senza magie** — contano solo per evitare "sottospazi sfigati":
   - Evita tutto-zero / tutti multipli di un primo di \(m\).
   - Per \(p=3\): usa componenti in classi diverse (0,1,2).
   - Se un seme dà coverage < m su \(N=t_1\), cambialo (o usa `--seed_find`).

4) **Torre p-adica** — scala facile:
   - Passi da \(p\) a \(p^a\)? Moltiplica \(t_1\) per \(p\) a ogni livello: nessuna sorpresa.

5) **QA rapido** — come capisci che “non è FSLL”:
   - Presenza di \(\lambda=1\) mod \(p\), radici multiple (Jordan) o \(p\mid k\).
   - Sintomi: periodo osservato troppo corto, coverage < m, deviazione alta anche con \(N=t_1\).

**Ad esempio**: `k=13, m=255=3·5·17`  
\(c_3=1,\ c_5=4,\ c_{17}=8 \Rightarrow t_1=\mathrm{lcm}(3,20,136)=\mathbf{2040}\).  
Misura con \(N=2040\): coverage \(=255\), conteggi piatti (semi normali).

---

# cp_maps — mappa iniziale dei c_p

Formato JSON per ciascun k:
{
  "k": <int>,
  "cp": { "<p>": <c_p>, ... },
  "notes": "opzionale"
}

Significato:
- c_p = LCM degli ordini delle radici del polinomio caratteristico di C_k in F_p*.
- In modalità FSLL: t1(p^a) = c_p * p^(a-1); per m composti: t1(m) = lcm(c_p * p^(a-1)).

---

## Roadmap breve
- [X] CLI `splitlift` con `predict | verify | measure | run`
- [X] Seed-policy automatica (`--seed_find`)
- [X] Export JSON/CSV
- [ ] Test lifting per-prime e residui

## Licenza
MIT — vedi `LICENSE`.
