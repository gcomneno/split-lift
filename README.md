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

## Esempi lampo
- **FSLL OK (composto):** `k=13, m=255` → \(t_1=\mathrm{lcm}(3,20,136)=2040\).
- **FSLL OK (primo):** `k=10, m=11` → \(t_1=10\).
- **FSLL FAIL (confronto):** `k=8, m=7` → rotazione (λ=1), niente mixing.

## Roadmap breve
- [X] CLI `splitlift` con `predict | verify | measure | run`
- [X] Seed-policy automatica (`--seed_find`)
- [X] Export JSON/CSV
- [ ] Test lifting per-prime e residui

## Licenza
MIT — vedi `LICENSE`.
