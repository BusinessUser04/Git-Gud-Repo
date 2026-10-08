"""Power v4: deterministic score and tier from four 0-20 integer inputs.

Usage:  python scripts/power.py PRESENCE CAPABILITY SPECTACLE RARITY
        python scripts/power.py --check      (verify all 194,481 combinations)

score = round_half_up(0.75*P + 1.75*C + 2.00*Sp + 0.50*R), rounded once after the sum.
Standard library only. Missing or invalid inputs give Pending (no score, no tier);
they are never clamped, coerced or replaced with zero.
"""

from __future__ import annotations

import hashlib
import itertools
import sys
from decimal import ROUND_HALF_UP, Decimal

# (label, min score, max score). S+ is owner-override-only and has no band.
TIER_BANDS = (
    ("S", 70, 100), ("S-", 66, 69), ("A+", 62, 65), ("A", 58, 61), ("A-", 54, 57),
    ("B+", 50, 53), ("B", 46, 49), ("B-", 42, 45), ("C+", 38, 41), ("C", 34, 37),
    ("C-", 28, 33), ("D+", 24, 27), ("D", 16, 23), ("D-", 12, 15), ("E", 0, 11),
)  # fmt: skip

# SHA-256 of the "P,C,Sp,R,score" table (LF line endings, nested loops 0..20).
EXPECTED_DIGEST = "189280162b94f72e72cc2f1c0d8e3dc07b9509fa61afbfe2339be2d8a4b80188"


def score(p: int, c: int, sp: int, r: int) -> int:
    """Integer form of the formula: floor((3P + 7C + 8Sp + 2R + 2) / 4)."""
    return (3 * p + 7 * c + 8 * sp + 2 * r + 2) // 4


def exact_score(p: int, c: int, sp: int, r: int) -> int:
    """Independent check using exact decimals and one half-up rounding."""
    total = Decimal("0.75") * p + Decimal("1.75") * c + Decimal(2) * sp + Decimal("0.5") * r
    return int(total.quantize(Decimal(1), rounding=ROUND_HALF_UP))


def tier(value: int) -> str:
    for label, low, high in TIER_BANDS:
        if low <= value <= high:
            return label
    raise ValueError(f"Score {value} is outside 0..100.")


def evaluate(inputs: list) -> tuple[int, str] | None:
    """Return (score, tier), or None (Pending) if any input is missing or invalid."""
    for v in inputs:
        if isinstance(v, bool) or not isinstance(v, int) or not 0 <= v <= 20:
            return None
    s = score(*inputs)
    return s, tier(s)


def check_all() -> bool:
    rows = []
    for p, c, sp, r in itertools.product(range(21), repeat=4):
        s = score(p, c, sp, r)
        if s != exact_score(p, c, sp, r):
            print(f"MISMATCH at {(p, c, sp, r)}")
            return False
        rows.append(f"{p},{c},{sp},{r},{s}\n")
    digest = hashlib.sha256("".join(rows).encode("utf-8")).hexdigest()
    print(f"{len(rows)} combinations, digest {digest}")
    return digest == EXPECTED_DIGEST


def main(argv: list[str]) -> int:
    if argv == ["--check"]:
        ok = check_all()
        print("OK" if ok else "FAILED")
        return 0 if ok else 1
    try:
        values = [int(a) for a in argv]
    except ValueError:
        values = []
    if len(values) != 4:
        print(__doc__)
        return 2
    result = evaluate(values)
    print("Pending (inputs must be integers 0-20)" if result is None else f"{result[0]} {result[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
