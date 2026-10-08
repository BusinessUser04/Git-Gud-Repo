# Power v4

Inputs in order: Presence (P), Capability (C), Spectacle (Sp), Rarity (R).
Each is a nullable integer from 0 to 20. Zero is valid. Missing or invalid source
input produces diagnostics and Pending with no computed score or tier. Future
typed objects reject fractions, booleans, strings and values
outside the range rather than coercing them.

```
score = round_half_up(0.75*P + 1.75*C + 2.00*Sp + 0.50*R)
      = floor((3*P + 7*C + 8*Sp + 2*R + 2) / 4)
```

Round the total once. Runtime default half-even rounding is unsuitable. The
self-check (`scripts/power.py --check`) compares integer arithmetic with independent exact decimal half-up
rounding across all 21^4 = 194,481 combinations.

| Tier | Rounded score |
|---|---|
| S | 70–100 |
| S- | 66–69 |
| A+ | 62–65 |
| A | 58–61 |
| A- | 54–57 |
| B+ | 50–53 |
| B | 46–49 |
| B- | 42–45 |
| C+ | 38–41 |
| C | 34–37 |
| C- | 28–33 |
| D+ | 24–27 |
| D | 16–23 |
| D- | 12–15 |
| E | 0–11 |

S+ is owner-override-only. An override controls the effective tier even while the
computed score/tier remain Pending. No Presence/Rarity gate, species bonus or
collection-relative rescaling applies. A stored provider score is a derived copy,
never an additional authoritative input.

Presence measures representative individual body magnitude; Capability assesses
functional effectiveness; Spectacle assesses extraordinary supported biology;
Rarity assesses global abundance/distribution of the resolved identity. Personal
novelty and significance belong to the encounter. Shared traits can inform C/Sp
only with distinct reasons. A broad-rank rating carries a representative-estimate
flag and uses supported shared traits without combining exceptional relatives.

An assessed rating preserves model version, assessment date and reasoning for
each axis. Label estimates and uncertainty explicitly; consequential uncertain
claims need evidence targeted to those claims. Ordinary encounters reuse this
metadata. Do not manufacture metadata for wholly unassessed inputs; absent rating
versus unassessed record remains open.

Adapter-stored scores remain derived copies. Authorized weight changes recompute
every populated copy; tier-band-only changes do not rewrite scores. Collection-wide
drift detection is read-only. Power v4 itself remains unchanged.

## Reproducible proof

Hash UTF-8 bytes without BOM/header, one `P,C,Sp,R,score` row per lexicographically
nested P/C/Sp/R combination from 0 through 20. Every row, including the last, ends
in LF. Expected SHA-256:

`189280162b94f72e72cc2f1c0d8e3dc07b9509fa61afbfe2339be2d8a4b80188`

`python scripts/power.py --check` generates these bytes in memory, compares the integer
formula with exact-decimal half-up rounding for every combination, and checks the
digest. A mismatch fails; do not update the expected digest to accommodate a failure.
The exhaustive table need not be committed.
